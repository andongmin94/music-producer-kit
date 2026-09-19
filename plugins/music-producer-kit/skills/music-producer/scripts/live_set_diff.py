"""Read-only bounded .als XML comparison. No format rewriting or automatic exemptions.

Differences include IDs, transport, notes, routing and automation as stored.
A reviewer must map differences to the authorized edit. Equal XML alone does
not prove a UI reopen, playable sources, third-party plugins or musical quality.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

PLUGIN = Path(__file__).resolve().parents[3]

MAX_BYTES = 64 * 1024 * 1024
MAX_NODES = 500_000
MAX_DEPTH = 128


def save_report(value: dict, path: Path) -> None:
    """Create a private report without any backend-specific import or overwrite."""
    path = Path(path).expanduser()
    resolved = path.resolve()
    checkout = PLUGIN.parent.parent
    if resolved.is_relative_to(PLUGIN) or ((checkout / 'AGENTS.md').is_file() and resolved.is_relative_to(checkout)):
        raise ValueError('Keep reports outside the plugin and public checkout')
    if path.suffix.lower() != '.json' or not path.parent.is_dir() or path.is_symlink():
        raise ValueError('Use a new .json file in an existing private directory')
    payload = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    with path.open('x', encoding='utf-8') as stream:
        stream.write(payload)


def read_set(path: Path) -> tuple[ET.Element, dict]:
    if path.suffix.lower() != '.als' or path.is_symlink() or not path.is_file():
        raise ValueError('Select an existing regular .als file')
    before = path.stat()
    if before.st_size > MAX_BYTES:
        raise ValueError('Set file exceeds inspection budget')
    data = path.read_bytes()
    file_hash = hashlib.sha256(data).hexdigest()
    import io
    # Live's saved Set is gzip/XML. Do not silently accept a different container.
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
        xml = stream.read(MAX_BYTES + 1)
    if len(xml) > MAX_BYTES:
        raise ValueError('Uncompressed Set exceeds inspection budget')
    text = xml.decode('utf-8-sig')
    if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
        raise ValueError('DTD/entity declarations are not supported')
    root = ET.fromstring(text)
    if root.tag != 'Ableton' or len(root.findall('LiveSet')) != 1:
        raise ValueError('Expected one Ableton/LiveSet document')
    pending = [(root, 0)]; nodes = 0
    while pending:
        element, depth = pending.pop(); nodes += 1
        if nodes > MAX_NODES or depth > MAX_DEPTH:
            raise ValueError('Set XML exceeds node/depth budget')
        pending.extend((child, depth + 1) for child in element)
    after = path.stat()
    if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
        raise ValueError('Set changed during inspection; save and inspect again')
    return root, {'sha256': file_hash, 'bytes': len(data), 'xml_sha256': hashlib.sha256(xml).hexdigest()}


def compare(before: Path, after: Path, limit: int = 100) -> dict:
    if type(limit) is not int or not 1 <= limit <= 1000:
        raise ValueError('Use a difference limit of 1..1000')
    left, left_id = read_set(before)
    right, right_id = read_set(after)
    differences, total = [], 0

    def changed(path, kind, old, new):
        nonlocal total
        total += 1
        if len(differences) < limit:
            differences.append({'path': path, 'kind': kind, 'before': old, 'after': new})

    stack = [(left, right, '/Ableton')]
    while stack:
        a, b, path = stack.pop()
        if a.tag != b.tag:
            changed(path, 'tag', a.tag, b.tag)
        for attr in sorted(a.attrib.keys() | b.attrib.keys()):
            if a.attrib.get(attr) != b.attrib.get(attr):
                changed(path + '/@' + attr, 'attribute', a.attrib.get(attr), b.attrib.get(attr))
        if (a.text or '').strip() != (b.text or '').strip():
            changed(path + '/text()', 'text', (a.text or '').strip(), (b.text or '').strip())
        if (a.tail or '').strip() != (b.tail or '').strip():
            changed(path + '/tail()', 'text', (a.tail or '').strip(), (b.tail or '').strip())
        ca, cb = list(a), list(b)
        if len(ca) != len(cb):
            changed(path, 'child-count', len(ca), len(cb))
        # Positional traversal retains every attribute. A regenerated ID is a
        # reported change, not an excuse to mask the entire clip/device subtree.
        for i in reversed(range(max(len(ca), len(cb)))):
            pa, pb = ca[i] if i < len(ca) else None, cb[i] if i < len(cb) else None
            child = f'{path}/{(pa if pa is not None else pb).tag}[{i}]'
            if pa is None or pb is None:
                present = pa if pa is not None else pb
                summary = {'tag': present.tag, 'subtree_sha256': hashlib.sha256(ET.tostring(present)).hexdigest(),
                           'nodes': sum(1 for _ in present.iter())}
                changed(child, 'subtree', summary if pa is not None else None, summary if pb is not None else None)
            else:
                stack.append((pa, pb, child))
    return {'kind': 'saved-live-set-xml-diff', 'before_file': left_id, 'after_file': right_id,
            'xml_equivalent': total == 0, 'difference_count': total,
            'differences': differences, 'truncated': total > limit,
            'scope_approval': 'not-automated', 'ui_reopen_proven': False,
            'note': 'Review all changed regions against the requested target, including ID churn. '
                    'No XML path is automatically ignored. Missing external files or plugin state outside this XML are not checked.'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path); parser.add_argument('after', type=Path)
    parser.add_argument('--limit', type=int, default=100)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = compare(args.before, args.after, args.limit)
        save_report(result, args.output)
    except (ValueError, OSError, EOFError, ET.ParseError) as exc:
        parser.exit(2, f'error: {exc}\n')
    print(f"Saved XML comparison: {result['difference_count']} differences; scope review required={not result['xml_equivalent']}")


if __name__ == '__main__':
    main()
