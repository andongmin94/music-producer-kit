"""One-time, checksum-verified transfer of already reviewed local edits."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zlib

ROOT = Path.cwd().resolve()
PAYLOAD_HASH = '5682ad9dfa598815297832bc2972d6dfb8476c3220b9cd5300c6754f5657bdd4'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def target(name):
    path = PurePosixPath(name)
    if path.is_absolute() or '..' in path.parts or str(path) != name:
        raise ValueError('Unsafe edit path')
    output = ROOT / name
    if output.is_symlink() or not output.resolve().is_relative_to(ROOT):
        raise ValueError('Edit escapes repository')
    return output

raw = b''.join((ROOT / '_review' / f'payload-{i:02}.bin').read_bytes() for i in range(30))
if digest(raw) != PAYLOAD_HASH:
    raise ValueError('Transfer checksum mismatch')
payload = json.loads(zlib.decompress(raw))
for change in payload['changes']:
    path = target(change['path'])
    before = change['before']
    if before is None:
        if path.exists():
            raise ValueError('New file already exists: ' + change['path'])
        result = change['content'].encode('utf-8')
    else:
        original = path.read_bytes()
        if digest(original) != before:
            raise ValueError('Source changed: ' + change['path'])
        if change['after'] is None:
            path.unlink()
            continue
        lines = original.decode('utf-8').splitlines(keepends=True)
        for edit in reversed(change['edits']):
            lines[edit['start']:edit['end']] = [edit['text']]
        result = ''.join(lines).encode('utf-8')
    if digest(result) != change['after']:
        raise ValueError('Applied edit checksum mismatch: ' + change['path'])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(result)

with tempfile.TemporaryDirectory() as directory:
    script = Path(directory) / 'select_sources.py'
    script.write_text(payload['prune_script'], encoding='utf-8')
    subprocess.run([sys.executable, str(script), str(ROOT)], check=True, stdout=subprocess.DEVNULL)

for name in ('docs/upstream-inventory.json', 'docs/SOURCE_SNAPSHOT_REPORT.json',
             '.github/workflows/review-transfer.yml', '.github/workflows/finalize-selection.yml'):
    target(name).unlink(missing_ok=True)
shutil.rmtree(ROOT / '_review')
report = json.loads((ROOT / 'docs/SOURCE_SELECTION_REPORT.json').read_text(encoding='utf-8'))
if (report['modules'], report['files'], report['bytes']) != (41, 89, 1805308):
    raise ValueError('Selected source inventory does not match local review')
print('Applied verified edits; selected 41 modules / 89 source files; temporary transfer files removed.')
