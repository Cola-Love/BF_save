from flask import request, jsonify, send_from_directory
from .app import app
from . import app as _wapp
from .data import *
from editor.setter import Setter
from editor.formatter import walk_tree, resolve_path

from .template import HTML_PAGE


@app.route('/')
def index():
    return HTML_PAGE


@app.route('/api/tree')
def api_tree():
    return jsonify(_wapp.TREE_JSON)


@app.route('/api/leaves')
def api_leaves():
    q = request.args.get('q', '').lower()
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 100))
    all_leaves = []
    for path_parts, val in _wapp.TREE_DATA:
        path_str = ' > '.join(path_parts)
        if q:
            val_str = str(val).lower()
            if q not in path_str.lower() and q not in val_str:
                continue
        all_leaves.append({'path': path_str, 'value': val, 'parts': path_parts})
    total = len(all_leaves)
    start = (page - 1) * per_page
    end = start + per_page
    return jsonify({
        'leaves': all_leaves[start:end],
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page
    })


@app.route('/api/show')
def api_show():
    path = request.args.get('path', '')
    if not path:
        return jsonify({'error': '缺少 path 参数'})
    try:
        obj = resolve_path(_wapp.PARSER.root, path)
        if obj is None:
            return jsonify({'error': f'路径不存在: {path}'})
        leaves = walk_tree(obj)
        result = []
        for parts, val in leaves:
            result.append({'path': ' > '.join(parts), 'value': val})
        return jsonify({'leaves': result, 'path': path})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/set', methods=['POST'])
def api_set():
    data = request.get_json()
    path = data.get('path', '')
    value = data.get('value')
    if not path:
        return jsonify({'error': '缺少 path 参数'})
    setter = Setter(_wapp.SAVE_PATH)
    setter.scan()
    if setter.set_path(path, value):
        setter.save()
        _wapp.reload_data()
        return jsonify({'ok': True, 'path': path, 'value': value})
    return jsonify({'error': f'修改失败: {path}'})


@app.route('/api/reload', methods=['POST'])
def api_reload():
    _wapp.reload_data()
    return jsonify({'ok': True})


@app.route('/api/set_batch', methods=['POST'])
def api_set_batch():
    data = request.get_json()
    items = data.get('items', [])
    if not items:
        return jsonify({'error': '缺少 items'})
    setter = Setter(_wapp.SAVE_PATH)
    setter.scan()
    results = []
    for item in items:
        path = item.get('path', '')
        value = item.get('value')
        if setter.set_path(path, value):
            results.append({'path': path, 'ok': True, 'value': value})
        else:
            results.append({'path': path, 'ok': False, 'error': '修改失败'})
    setter.save()
    _wapp.reload_data()
    return jsonify({'results': results})


@app.route('/api/magic_sword_state')
def api_magic_sword_state():
    try:
        ms = resolve_path(_wapp.PARSER.root, 'magicSword')
        if ms is None:
            return jsonify({'weaponNameId': 0, 'weaponLevel': 0, 'slots': []})
        name_enum = ms.get('magicSwordName', {})
        weapon_name_id = name_enum.get('value__', 0) if isinstance(name_enum, dict) else name_enum
        weapon_level = ms.get('Level', 0)
        obj = resolve_path(_wapp.PARSER.root, 'magicSword > magicSwordEntrys')
        items = obj.get('_items', []) if obj else []
        slots = []
        for i in range(5):
            if i < len(items) and isinstance(items[i], dict):
                name_enum = items[i].get('magicSwordEntryName', {})
                name_val = name_enum.get('value__', 0) if isinstance(name_enum, dict) else name_enum
                slots.append({
                    'index': i,
                    'entryId': int(name_val) if name_val is not None else 0,
                    'level': items[i].get('level', 0),
                    'values': items[i].get('values', 0),
                    'isNightmare': items[i].get('isNightmare', False),
                })
            else:
                slots.append({'index': i, 'entryId': 0, 'level': 0, 'values': 0, 'isNightmare': False})
        return jsonify({
            'weaponNameId': int(weapon_name_id) if weapon_name_id is not None else 0,
            'weaponLevel': weapon_level,
            'slots': slots
        })
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/potion_state')
def api_potion_state():
    try:
        obj = resolve_path(_wapp.PARSER.root, 'potions')
        if isinstance(obj, list):
            items = obj
        elif isinstance(obj, dict):
            items = obj.get('_items', [])
        else:
            items = []
        slots = []
        for i in range(4):
            if i < len(items) and isinstance(items[i], dict):
                name_enum = items[i].get('PotionName', {})
                name_val = name_enum.get('value__', 0) if isinstance(name_enum, dict) else name_enum
                elem_enum = items[i].get('elementType', {})
                elem_val = elem_enum.get('value__', 0) if isinstance(elem_enum, dict) else elem_enum
                slots.append({
                    'index': i,
                    'potionId': int(name_val) if name_val is not None else 0,
                    'level': items[i].get('Level', 0),
                    'elementType': int(elem_val) if elem_val is not None else 0,
                })
            else:
                slots.append({'index': i, 'potionId': 0, 'level': 0, 'elementType': 0})
        return jsonify({'slots': slots})
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/rune_state')
def api_rune_state():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        obj = resolve_path(_wapp.PARSER.root, 'runeInventory')
        if isinstance(obj, list):
            raw_items = obj
        elif isinstance(obj, dict):
            raw_items = obj.get('_items', [])
        else:
            raw_items = []
        valid_items = [(i, r) for i, r in enumerate(raw_items) if r is not None]
        total = len(valid_items)
        pages = max(1, (total + per_page - 1) // per_page)
        if page > pages:
            page = pages
        start = (page - 1) * per_page
        end = start + per_page
        runes = []
        for i, r in valid_items[start:end]:
            mods = r.get('modifiers')
            mod_items = mods.get('_items', []) if mods else []
            real_size = mods.get('_size', 0) if mods else 0
            modifiers = []
            for j in range(5):
                if j < real_size and j < len(mod_items):
                    modifiers.append({
                        'idx': j,
                        'key': mod_items[j].get('key', 0) if isinstance(mod_items[j], dict) else 0,
                        'value': mod_items[j].get('value', 0.0) if isinstance(mod_items[j], dict) else 0.0,
                    })
                else:
                    modifiers.append({'idx': j, 'key': 0, 'value': 0.0})
            runes.append({
                'index': i,
                'id': r.get('id', 0),
                'locked': r.get('locked', False),
                'modifiers': modifiers,
            })
        return jsonify({
            'runes': runes,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': pages,
        })
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/api/general_state')
def api_general_state():
    try:
        root = _wapp.PARSER.root
        return jsonify({
            'souls': root.get('souls', 0),
            'redsouls': root.get('redsouls', 0),
            'dreamAsh': root.get('dreamAsh', 0),
            'timeGlow': root.get('timeGlow', 0),
            'TotalPlayCount': root.get('TotalPlayCount', 0),
        })
    except Exception as e:
        return jsonify({'error': str(e)})