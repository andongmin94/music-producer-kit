"""Find existing local audio files by filename/path; never download or decode audio."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

EXTENSIONS = frozenset({'.wav', '.wave', '.flac', '.aif', '.aiff', '.ogg'})
MAX_FILES = 10_000
MAX_HASH_BYTES = 256 * 1024 * 1024


def _identity(stat) -> tuple:
    return stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns


def find_samples(root: Path, query: str = '', limit: int = 20) -> dict:
    """Return bounded, deterministic matches inside an explicitly chosen directory."""
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError('limit must be an integer from 1 to 100')
    if not isinstance(query, str) or len(query) > 256 or any(c in query for c in '\r\n\0'):
        raise ValueError('query must be one line of at most 256 characters')
    root = Path(root)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Choose an existing directory, not a symlink')
    root = root.resolve(strict=True)
    words = query.casefold().split()
    matches, warnings = [], []
    scanned = matched = 0
    scan_complete = True

    def walk_error(error: OSError) -> None:
        warnings.append({'operation': 'directory-read', 'error': type(error).__name__})

    for folder, directories, filenames in os.walk(root, followlinks=False, onerror=walk_error):
        directories[:] = sorted(d for d in directories
                                if not (Path(folder) / d).is_symlink()
                                and not (Path(folder) / d).is_junction())
        for name in sorted(filenames):
            scanned += 1
            if scanned > MAX_FILES:
                scan_complete = False
                break
            path = Path(folder) / name
            if path.suffix.lower() not in EXTENSIONS or path.is_symlink():
                continue
            relative = path.relative_to(root).as_posix()
            if not all(word in relative.casefold() for word in words):
                continue
            try:
                if not path.resolve(strict=True).is_relative_to(root):
                    continue
                before = path.stat()
                if not path.is_file():
                    continue
                matched += 1
                if len(matches) == limit:
                    continue
                record = {'path': relative, 'bytes': before.st_size,
                          'format_hint': path.suffix.lower().lstrip('.'), 'sha256': None}
                if before.st_size > MAX_HASH_BYTES:
                    record['hash_status'] = 'skipped-size-limit'
                else:
                    with path.open('rb') as stream:
                        if _identity(os.fstat(stream.fileno())) != _identity(before):
                            raise ValueError('File changed before hashing')
                        checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
                        if _identity(os.fstat(stream.fileno())) != _identity(before):
                            raise ValueError('File changed while hashing')
                    if path.is_symlink() or _identity(path.stat()) != _identity(before):
                        raise ValueError('File changed after hashing')
                    record.update(sha256=checksum, hash_status='verified-file-bytes')
                matches.append(record)
            except (OSError, ValueError) as error:
                warnings.append({'path': relative, 'operation': 'file-read',
                                 'error': type(error).__name__})
        if not scan_complete:
            break
    return {'matches': matches, 'query': query, 'files_visited': min(scanned, MAX_FILES),
            'matched_in_visited_files': matched, 'truncated': matched > len(matches) or not scan_complete,
            'scan_complete': scan_complete and not warnings, 'warnings': warnings[:20],
            'warning_count': len(warnings), 'audio_analyzed': False,
            'license_verified': False, 'network_used': False,
            'note': 'Filename/path matches only. BPM, key, sound quality and sample rights are not inferred.'}


def main() -> None:
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--query', default='')
    parser.add_argument('--limit', type=int, default=20)
    args = parser.parse_args()
    try:
        result = find_samples(args.directory, args.query, args.limit)
    except (OSError, ValueError) as error:
        parser.exit(2, f'error: {error}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
