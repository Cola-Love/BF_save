#!/usr/bin/env python3
"""
Unity BinaryFormatter 存档编辑器

用法:
    python3 BF_save.py <save_file>                            查看存档概览
    python3 BF_save.py <save_file> --json                     完整 JSON 输出
    python3 BF_save.py <save_file> --list [page] [n]          分页列出叶子值
    python3 BF_save.py <save_file> --list --save <file>       保存全部叶子值到文件
    python3 BF_save.py <save_file> --find <keyword>           搜索字段
    python3 BF_save.py <save_file> --show <path>              展开指定路径
    python3 BF_save.py <save_file> --set <field> <value>      修改顶层字段
    python3 BF_save.py <save_file> --set --path <p> --value <v> 修改嵌套路径字段
    python3 BF_save.py <save_file> --web [--port 5000]        启动 Web 编辑器
"""

import sys
import json
import os


def _cli_mode(fp, args):
    from core.parser import FullParser
    from editor.setter import Setter
    from editor.formatter import walk_tree, resolve_path, print_leaf, print_obj

    cmd = args[0] if args else ''

    if cmd == '--set' and len(args) >= 2:
        setter = Setter(fp)
        if args[1] == '--path':
            val_idx = None
            for i, a in enumerate(args):
                if a == '--value' and i + 1 < len(args):
                    val_idx = i + 1
                    break
            if val_idx:
                path_str = ' '.join(args[2:val_idx - 1])
                if setter.set_path(path_str, args[val_idx]):
                    setter.save(fp)
            else:
                print("用法: --set --path <path> --value <value>")
        else:
            setter.scan()
            field = args[1]
            val_str = args[2] if len(args) > 2 else ''
            if setter.modify(field, val_str):
                setter.save(fp)
        return

    parser = FullParser(open(fp, 'rb').read())
    data = parser.parse()

    if cmd == '' or cmd == '--web':
        print(f"Libraries: {parser.libs}")
        print(f"Objects: {len(parser.objects)}, Strings: {len(parser.strings)}")
        print()
        print_obj(data, max_depth=3)

    elif cmd == '--json':
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))

    elif cmd == '--list':
        leaves = walk_tree(data)
        total = len(leaves)
        save_idx = None
        for i, a in enumerate(args):
            if a == '--save' and i + 1 < len(args):
                save_idx = i + 1
                break
        if save_idx:
            out_path = args[save_idx]
            if not out_path.endswith('.txt'):
                out_path += '.txt'
            with open(out_path, 'w', encoding='utf-8') as f:
                for path_parts, val in leaves:
                    f.write(' > '.join(path_parts) + '  ' + str(val) + '\n')
            print(f"已保存 {total} 条到: {out_path}")
        else:
            page = int(args[1]) if len(args) >= 2 and args[1] != '--save' else 1
            per_page = int(args[2]) if len(args) >= 3 else 50
            total_pages = (total + per_page - 1) // per_page
            start = (page - 1) * per_page
            end = min(start + per_page, total)
            print(f"共 {total} 条，第 {page}/{total_pages} 页 (第 {start+1}-{end} 条):\n")
            for path_parts, val in leaves[start:end]:
                print_leaf(path_parts, val)
            if page < total_pages:
                print(f"\n--- 下一页: --list {page+1} {per_page} ---")

    elif cmd == '--find' and len(args) >= 2:
        keyword = args[1].lower()
        leaves = walk_tree(data)
        results = [(p, v) for p, v in leaves if any(keyword in seg.lower() for seg in p)]
        print(f"搜索 '{keyword}' — 找到 {len(results)} 条结果:\n")
        for path_parts, val in results:
            print_leaf(path_parts, val)

    elif cmd == '--show' and len(args) >= 2:
        target = resolve_path(data, args[1])
        if target is None:
            print(f"路径不存在: {args[1]}")
        else:
            for path_parts, val in walk_tree(target, [args[1]]):
                print_leaf(path_parts, val)

    elif cmd.startswith('--'):
        print(f"未知参数: {cmd}")
        print(__doc__)
    else:
        print(f"未知命令: {' '.join(args)}")
        print(__doc__)


def _web_mode(fp, args):
    from web.config import VERSION
    from web.app import app, SAVE_PATH, reload_data
    import web.api  # noqa: F401
    import web.app as wapp

    port = 5000
    host = '0.0.0.0'
    for i, a in enumerate(args):
        if a == '--port' and i + 1 < len(args):
            port = int(args[i + 1])
        elif a == '--host' and i + 1 < len(args):
            host = args[i + 1]

    wapp.SAVE_PATH = os.path.abspath(fp)
    if not os.path.exists(wapp.SAVE_PATH):
        print(f'错误: 文件不存在: {wapp.SAVE_PATH}')
        sys.exit(1)
    reload_data()
    print(f'存档编辑器 V{VERSION} 已启动: http://localhost:{port}')
    app.run(host=host, port=port, debug=False)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    if len(args) < 1:
        print(__doc__)
        sys.exit(1)

    fp = args[0]
    if not os.path.exists(fp):
        print(f"错误: 文件不存在: {fp}")
        sys.exit(1)

    rest = args[1:]
    if '--web' in rest:
        web_args = [a for a in rest if a != '--web']
        _web_mode(fp, web_args)
    else:
        _cli_mode(fp, rest)


if __name__ == '__main__':
    main()
