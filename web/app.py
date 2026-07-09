import os
from collections import OrderedDict

from core.parser import FullParser
from editor.formatter import walk_tree, resolve_path
from editor.setter import Setter
from flask import Flask

app = Flask(__name__)

SAVE_PATH = None
PARSER = None
TREE_DATA = None
TREE_JSON = None

def build_tree(leaves):
    root = OrderedDict()
    for path_parts, val in leaves:
        node = root
        for i, part in enumerate(path_parts):
            if i == len(path_parts) - 1:
                node[part] = val
            else:
                if part not in node:
                    node[part] = OrderedDict()
                if not isinstance(node[part], (dict, OrderedDict)):
                    node[part] = OrderedDict({'_val': node[part]})
                node = node[part]
    return root


def tree_to_nested(obj):
    if isinstance(obj, (dict, OrderedDict)):
        children = []
        for k, v in obj.items():
            if k == '_val':
                children.append({'name': '', 'value': v, 'leaf': True})
            elif isinstance(v, (dict, OrderedDict)):
                child = tree_to_nested(v)
                child['name'] = str(k)
                children.append(child)
            elif isinstance(v, list):
                arr_children = []
                for i, item in enumerate(v):
                    if isinstance(item, (dict, OrderedDict)):
                        c = tree_to_nested(item)
                        c['name'] = str(i)
                        arr_children.append(c)
                    else:
                        arr_children.append({'name': str(i), 'value': item, 'leaf': True})
                children.append({'name': str(k), 'children': arr_children})
            else:
                children.append({'name': str(k), 'value': v, 'leaf': True})
        return {'name': '', 'children': children}
    return {'name': '', 'value': obj, 'leaf': True}

def reload_data():
    global PARSER, TREE_DATA, TREE_JSON
    raw = open(SAVE_PATH, 'rb').read()
    PARSER = FullParser(raw)
    PARSER.parse()
    resolved = PARSER._resolve_refs(PARSER.root)
    PARSER.root = resolved
    TREE_DATA = walk_tree(resolved)
    tree = build_tree(TREE_DATA)
    TREE_JSON = tree_to_nested(tree)

