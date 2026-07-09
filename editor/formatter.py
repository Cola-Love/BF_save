from collections import OrderedDict


def format_guid(obj):
    a = obj.get('_a', 0)
    b = obj.get('_b', 0) & 0xFFFF
    c = obj.get('_c', 0) & 0xFFFF
    d = obj.get('_d', 0) & 0xFF
    e = obj.get('_e', 0) & 0xFF
    f = obj.get('_f', 0) & 0xFF
    g = obj.get('_g', 0) & 0xFF
    h = obj.get('_h', 0) & 0xFF
    i = obj.get('_i', 0) & 0xFF
    j = obj.get('_j', 0) & 0xFF
    k = obj.get('_k', 0) & 0xFF
    return f'{a:08x}-{b:04x}-{c:04x}-{d:02x}{e:02x}-{f:02x}{g:02x}{h:02x}{i:02x}{j:02x}{k:02x}'


def walk_tree(obj, prefix_parts=None, max_depth=20):
    if prefix_parts is None:
        prefix_parts = []
    if max_depth <= 0:
        return []
    results = []
    if isinstance(obj, (dict, OrderedDict)):
        tn = obj.get('_type', '')
        keys = [k for k in obj.keys() if k != '_type']
        if keys == ['value__']:
            results.append((prefix_parts, obj['value__']))
            return results
        if tn == 'System.Guid':
            results.append((prefix_parts, format_guid(obj)))
            return results
        if tn.startswith('System.Collections.Generic.List'):
            items = obj.get('_items', [])
            if isinstance(items, list):
                for i, v in enumerate(items):
                    path = prefix_parts + [str(i)]
                    if isinstance(v, (dict, OrderedDict, list)):
                        results.extend(walk_tree(v, path, max_depth - 1))
                    else:
                        results.append((path, v))
            return results
        for k, v in obj.items():
            if k == '_type' or k.startswith('_'):
                continue
            path = prefix_parts + [k]
            if isinstance(v, (dict, OrderedDict, list)):
                results.extend(walk_tree(v, path, max_depth - 1))
            else:
                results.append((path, v))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            path = prefix_parts + [str(i)]
            if isinstance(v, (dict, OrderedDict, list)):
                results.extend(walk_tree(v, path, max_depth - 1))
            else:
                results.append((path, v))
    return results


def resolve_path(obj, path_str):
    parts = [s.strip() for s in path_str.split('>')]
    cur = obj
    for p in parts:
        if not p:
            continue
        if isinstance(cur, list):
            try:
                cur = cur[int(p)]
            except (ValueError, IndexError):
                return None
        elif isinstance(cur, dict):
            if '_items' in cur and p.isdigit():
                items = cur['_items']
                if isinstance(items, list):
                    try:
                        cur = items[int(p)]
                    except (ValueError, IndexError):
                        return None
                    continue
            if p in cur:
                cur = cur[p]
            else:
                return None
        else:
            return None
    return cur


def print_leaf(path_parts, val):
    if isinstance(val, float):
        print(f"{' > '.join(path_parts)}  {val}")
    else:
        print(f"{' > '.join(path_parts)}  {val}")


def print_obj(obj, indent=0, max_depth=3, max_items=20):
    prefix = '  ' * indent
    if isinstance(obj, (dict, OrderedDict)):
        tn = obj.get('_type', 'Object')
        items = [(k, v) for k, v in obj.items() if k != '_type']
        print(f"{prefix}{tn} ({len(items)} fields)")
        if indent >= max_depth: return
        for k, v in items[:max_items]:
            if isinstance(v, (dict, OrderedDict)):
                print(f"{prefix}  {k}: ", end='')
                print_obj(v, indent + 1, max_depth, max_items)
            elif isinstance(v, list):
                if len(v) <= 10: print(f"{prefix}  {k}: [{len(v)}] {v}")
                else: print(f"{prefix}  {k}: [{len(v)}] {v[:5]}...")
            elif isinstance(v, float): print(f"{prefix}  {k}: {v:.4f}")
            else: print(f"{prefix}  {k}: {v}")
        if len(items) > max_items:
            print(f"{prefix}  ... ({len(items) - max_items} more fields)")
    elif isinstance(obj, list):
        if len(obj) <= 10: print(f"{prefix}[{len(obj)}] {obj}")
        else: print(f"{prefix}[{len(obj)}] {obj[:5]}...")
