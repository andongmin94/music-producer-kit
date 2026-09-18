"""Read-only local audio inventory. No playback, upload, account access or purchases."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys

import soundfile as sf

PLUGIN = Path(__file__).resolve().parents[3]
EXTENSIONS = frozenset({'.wav', '.wave', '.aif', '.aiff', '.flac', '.ogg', '.mp3'})


def _limit(value: int) -> None:
    if type(value) is not int or not 1 <= value <= 10000:
        raise ValueError('Use an integer limit between 1 and 10000')


def _root(value: Path) -> Path:
    value = Path(value)
    if value.is_symlink() or value.is_junction():
        raise ValueError('Sample root must not be a symbolic link or junction')
    root = value.resolve(strict=True)
    if not root.is_dir():
        raise ValueError('Sample root must be a directory')
    return root


def _file(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative or '\\' in relative or ':' in relative:
        raise ValueError('Invalid relative sample path')
    name = PurePosixPath(relative)
    if name.is_absolute() or '..' in name.parts or str(name) != relative or relative == '.':
        raise ValueError('Invalid relative sample path')
    path = root
    for part in name.parts:
        path = path / part
        if path.is_symlink() or path.is_junction():
            raise ValueError('Sample links and junctions are not followed')
    if not path.resolve(strict=True).is_relative_to(root) or not stat.S_ISREG(path.stat().st_mode):
        raise ValueError('Sample must be a regular file inside the requested root')
    return path


def _metadata(root: Path, relative: str, *, fingerprint: bool = False) -> dict:
    path = _file(root, relative)
    before = path.stat()
    if path.suffix.casefold() not in EXTENSIONS:
        raise ValueError('Unsupported sample extension')
    info = sf.info(str(path))
    result = {'path': relative, 'bytes': before.st_size, 'mtime_ns': before.st_mtime_ns,
              'sample_rate': info.samplerate, 'channels': info.channels, 'frames': info.frames,
              'duration_seconds': info.duration, 'format': info.format, 'subtype': info.subtype,
              'license': 'not-verified', 'bpm': None, 'key': None,
              'audio_reviewed': False, 'validation': 'header-only'}
    if fingerprint:
        h = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                h.update(chunk)
        result['sha256'] = h.hexdigest()
    after = path.stat()
    if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
        raise ValueError('Sample changed during inspection; inspect again')
    return result


def scan(directory: Path, limit: int = 1000) -> dict:
    """Enumerate explicit root only, without following links or decoding waveforms."""
    _limit(limit)
    root = _root(directory)
    entries, issues = [], []
    examined = 0
    truncated = False

    def walk_error(error: OSError) -> None:
        issues.append({'reason': 'directory-unreadable', 'errno': error.errno})

    for folder, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        current = Path(folder)
        allowed = []
        for name in sorted(dirs):
            path = current / name
            if path.is_symlink() or path.is_junction():
                issues.append({'path': path.relative_to(root).as_posix(), 'reason': 'link-skipped'})
            elif not name.startswith('.'):
                allowed.append(name)
        dirs[:] = allowed
        for name in sorted(files):
            path = current / name
            if path.suffix.casefold() not in EXTENSIONS:
                continue
            if examined >= limit:
                truncated = True
                break
            examined += 1
            relative = path.relative_to(root).as_posix()
            try:
                entries.append(_metadata(root, relative))
            except (OSError, ValueError, sf.SoundFileError):
                issues.append({'path': relative, 'reason': 'unreadable-or-unsupported-audio'})
        if truncated:
            break
    return {'version': 1, 'root': str(root), 'entries': entries, 'issues': issues,
            'examined_files': examined, 'truncated': truncated, 'read_only': True,
            'network_used': False, 'audio_reviewed': False,
            'note': 'Private local inventory. Filename search is not sound similarity or license verification.'}


def find(catalog: dict, query: str, limit: int = 20) -> dict:
    _limit(limit)
    if not isinstance(query, str) or not query.strip() or len(query) > 256:
        raise ValueError('Use a nonempty filename query of at most 256 characters')
    if not isinstance(catalog, dict) or catalog.get('version') != 1 or not isinstance(catalog.get('entries'), list):
        raise ValueError('Invalid local sample inventory')
    tokens = query.casefold().split()
    matches = []
    for entry in catalog['entries']:
        if not isinstance(entry, dict) or not isinstance(entry.get('path'), str):
            raise ValueError('Invalid sample entry')
        if all(token in entry['path'].casefold() for token in tokens):
            matches.append(entry)
    return {'matches': matches[:limit], 'total_matches': len(matches), 'truncated': len(matches) > limit,
            'current_files_rechecked': False, 'audio_reviewed': False,
            'note': 'These are filename matches from a scan; inspect the selected current file before use.'}


def inspect(directory: Path, relative: str) -> dict:
    root = _root(directory)
    return {'root': str(root), 'entry': _metadata(root, relative, fingerprint=True),
            'network_used': False, 'read_only': True}


def save(catalog: dict, output: Path) -> None:
    """Create one private JSON report; never overwrite input or an existing report."""
    output = Path(output)
    if output.resolve().is_relative_to(PLUGIN) or output.resolve().is_relative_to(Path(catalog['root'])):
        raise ValueError('Save the report outside the installed plugin and sample root')
    checkout = PLUGIN.parent.parent
    if (checkout / 'AGENTS.md').is_file() and output.resolve().is_relative_to(checkout):
        raise ValueError('Save private inventory outside the project repository')
    payload = json.dumps(catalog, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    with output.open('x', encoding='utf-8') as stream:
        stream.write(payload)


def main() -> None:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    scanning = commands.add_parser('scan')
    scanning.add_argument('directory', type=Path)
    scanning.add_argument('--output', type=Path, required=True)
    scanning.add_argument('--limit', type=int, default=1000)
    search = commands.add_parser('find')
    search.add_argument('inventory', type=Path)
    search.add_argument('query')
    search.add_argument('--limit', type=int, default=20)
    inspecting = commands.add_parser('inspect')
    inspecting.add_argument('directory', type=Path)
    inspecting.add_argument('relative_file')
    args = parser.parse_args()
    try:
        if args.command == 'scan':
            result = scan(args.directory, args.limit)
            save(result, args.output)
            result = {'saved': str(args.output), 'files': len(result['entries']),
                      'issues': len(result['issues']), 'truncated': result['truncated'],
                      'audio_reviewed': False, 'network_used': False}
        elif args.command == 'find':
            result = find(json.loads(args.inventory.read_text(encoding='utf-8-sig')), args.query, args.limit)
        else:
            result = inspect(args.directory, args.relative_file)
    except (OSError, ValueError, KeyError, TypeError, sf.SoundFileError) as exc:
        parser.exit(2, f'error: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
