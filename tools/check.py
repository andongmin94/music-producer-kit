"""Offline project checks and allowlisted package build; not host certification."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = Path('plugins/music-producer-kit')
MARKETPLACE = Path('.agents/plugins/marketplace.json')
SCHEMA = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
TEXT_SUFFIXES = {'.md', '.json', '.py', '.txt'}
ARCHIVES = ('music-composition-skills.zip', 'lyric-writing-skills.zip')
sys.path.insert(0, str(ROOT / PLUGIN / 'skills/music-producer/scripts'))
from source_library import SourceLibrary


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def within(root: Path, path: Path) -> Path:
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes root: {path.name}')
    return path


def package_files(root: Path) -> list[Path]:
    files = [root / 'README.md', root / MARKETPLACE]
    for folder in (root / PLUGIN, root / 'docs'):
        for path in sorted(folder.rglob('*')):
            if '__pycache__' in path.parts:
                continue
            if path.is_symlink():
                raise ValueError(f'Symlinks are not packaged: {path.name}')
            if path.is_file() and path.suffix in TEXT_SUFFIXES and not path.name.startswith('.'):
                within(root, path)
                files.append(path)
    files.extend(root / PLUGIN / 'library/archives' / name for name in ARCHIVES)
    for path in files:
        if path.is_symlink():
            raise ValueError(f'Symlinks are not packaged: {path.name}')
        within(root, path)
    return sorted(files)


def check(root: Path = ROOT) -> dict:
    root = root.resolve()
    manifest = read_json(root / PLUGIN / 'plugin.json')
    if manifest.get('$schema') != SCHEMA or manifest.get('name') != PLUGIN.name:
        raise ValueError('Use the portable root manifest and matching plugin name')
    if not re.fullmatch(r'\d+\.\d+\.\d+', manifest.get('version', '')):
        raise ValueError('Plugin version must be numeric semver')
    if not manifest.get('description'):
        raise ValueError('Plugin description is missing')
    interface = manifest['extensions']['com.openai']['interface']
    if interface.get('displayName') != 'Music Producer Kit':
        raise ValueError('Incorrect plugin presentation metadata')
    catalog = read_json(root / MARKETPLACE)
    if catalog.get('name') != PLUGIN.name or len(catalog.get('plugins', [])) != 1:
        raise ValueError('Expected one Music Producer Kit marketplace entry')
    entry = catalog['plugins'][0]
    source = entry.get('source', {})
    if source != {'source': 'local', 'path': './plugins/music-producer-kit'}:
        raise ValueError('Marketplace path must identify the packaged plugin')
    if entry.get('name') != manifest['name']:
        raise ValueError('Marketplace and manifest names disagree')
    if entry.get('policy') != {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}:
        raise ValueError('Review marketplace installation/authentication policy')
    if entry.get('category') != 'Productivity':
        raise ValueError('Marketplace category is missing or unexpected')
    for obsolete in ['.claude-plugin', '.codex-plugin', '.agents/skills']:
        if (root / obsolete).exists() or (root / PLUGIN / obsolete).exists():
            raise ValueError(f'Duplicate/obsolete discovery path: {obsolete}')
    skills = sorted((root / PLUGIN / 'skills').rglob('SKILL.md'))
    if len(skills) != 1:
        raise ValueError('Only the curated entry skill may be discoverable')
    seen = set()
    for skill in skills:
        content = skill.read_text(encoding='utf-8')
        pieces = content.split('---', 2)
        if len(pieces) != 3 or pieces[0].strip():
            raise ValueError('Skill must start with frontmatter')
        headers = dict(line.split(':', 1) for line in pieces[1].strip().splitlines())
        name, desc = headers.get('name', '').strip(), headers.get('description', '').strip()
        if name != skill.parent.name or not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', name) or name in seen:
            raise ValueError('Invalid, duplicate or mismatched skill name')
        if not desc or len(desc) > 1024:
            raise ValueError('Skill description is missing or too long')
        seen.add(name)
    files = package_files(root)
    for path in files:
        if path.suffix == '.json':
            read_json(path)
        if path.suffix != '.md':
            continue
        for target in re.findall(r'\[[^\]\n]*\]\(([^)\s]+)\)', path.read_text(encoding='utf-8')):
            if target.startswith(('https://', 'http://', '#', 'mailto:')):
                continue
            destination = within(root, path.parent / target.split('#', 1)[0])
            if not destination.exists():
                raise ValueError(f'Broken link in {path.relative_to(root)}: {target}')
            if path.is_relative_to(root / PLUGIN):
                within(root / PLUGIN, destination)
    inventory = read_json(root / 'docs/upstream-inventory.json')
    counts = {source['repo']: len(source['skills']) for source in inventory['sources']}
    if sorted(counts.values()) != [18, 29]:
        raise ValueError('The audited upstream module inventory is incomplete')
    for source in inventory['sources']:
        if not re.fullmatch('[a-f0-9]{40}', source['commit']):
            raise ValueError('Upstream references must be pinned to a commit')
        names = [s['name'] for s in source['skills']]
        if len(names) != len(set(names)):
            raise ValueError('Duplicate upstream inventory entry')
    library = SourceLibrary(root / PLUGIN / 'library')
    preservation = library.verify()
    expected = {s['repo']: (s['commit'], {m['name'] for m in s['skills']}) for s in inventory['sources']}
    actual = {s['repo']: (s['commit'], set(s['modules'])) for s in library.sources}
    if expected != actual:
        raise ValueError('Bundled source library and adaptation inventory disagree')
    if {Path(s['archive']).name for s in library.sources} != set(ARCHIVES):
        raise ValueError('Source archive allowlist mismatch')
    for source in inventory['sources']:
        path = within(root, root / source['local_archive'])
        if path not in files or not path.is_file():
            raise ValueError('Inventory must point to a packaged local archive')
    scenarios = read_json(root / 'evals/scenarios.json')['scenarios']
    if len(scenarios) < 8 or len({s['id'] for s in scenarios}) != len(scenarios):
        raise ValueError('Behavior scenarios missing or duplicated')
    for scenario in scenarios:
        if not scenario['prompt'] or not scenario['must'] or not scenario['must_not']:
            raise ValueError('Incomplete behavior scenario')
    return {'status': 'pass', 'version': manifest['version'], 'skills': len(skills),
            'upstream_modules_catalogued': sum(counts.values()), 'local_source_library': preservation,
            'behavior_scenarios_defined': len(scenarios), 'behavior_scenarios_executed': False,
            'host_installation_verified': False, 'live_verified': False, 'audio_reviewed': False}


def build_package(root: Path, output: Path) -> None:
    check(root)
    files = package_files(root)
    if output.resolve() in {p.resolve() for p in files}:
        raise ValueError('Output would replace a source file')
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(root).as_posix(), date_time=(2026, 9, 18, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package', type=Path)
    args = parser.parse_args()
    try:
        result = check()
        if args.package:
            build_package(ROOT, args.package)
            result['package'] = str(args.package)
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        parser.exit(2, f'error: {exc}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
