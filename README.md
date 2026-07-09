# BF_save - Unity BinaryFormatter Save Editor

一个用于查看和编辑 Unity BinaryFormatter 格式游戏存档的 Python 工具，提供 CLI 命令行和 Web 可视化两种编辑方式。

## 功能特性

- **二进制解析**: 完整解析 Unity BinaryFormatter 序列化的二进制存档文件
- **CLI 模式**: 命令行查看、搜索、修改存档数据
- **Web 编辑器**: 基于 Flask 的可视化编辑器，支持树形浏览和字段修改
- **安全性**: 修改前自动备份原文件（`.bak`）
- **批量修改**: Web 界面支持批量修改多个字段

## 项目结构

```
BF_save/
├── BF_save.py          # 主入口 (CLI + Web 启动)
├── core/
│   ├── parser.py       # BinaryFormatter 二进制解析器
│   ├── stream.py       # 二进制流读写
│   └── constants.py    # 记录类型/基础类型常量定义
├── editor/
│   ├── setter.py       # 字段修改器 (含自动备份)
│   └── formatter.py    # 树遍历 / 格式化输出
├── web/
│   ├── app.py          # Flask 应用 + 数据加载
│   ├── api.py          # REST API 接口
│   ├── config.py       # 版本号配置
│   ├── data.py         # 游戏数据枚举/映射表
│   └── template.py     # 前端 HTML 模板
└── README.md
```

## 安装

### 依赖

- Python 3.8+
- Flask

```bash
pip install flask
```

### 克隆项目

```bash
git clone https://github.com/Cola/BF_save.git
cd BF_save
```

## 用法

### CLI 模式

```bash
# 查看存档概览
python3 BF_save.py <save_file>

# 完整 JSON 输出
python3 BF_save.py <save_file> --json

# 分页列出所有叶子值
python3 BF_save.py <save_file> --list [page] [n]

# 保存全部叶子值到文件
python3 BF_save.py <save_file> --list --save <file>

# 搜索字段
python3 BF_save.py <save_file> --find <keyword>

# 展开指定路径
python3 BF_save.py <save_file> --show <path>

# 修改顶层字段
python3 BF_save.py <save_file> --set <field> <value>

# 修改嵌套路径字段
python3 BF_save.py <save_file> --set --path <path> --value <value>
```

### Web 模式

```bash
# 启动 Web 编辑器 (默认端口 5000)
python3 BF_save.py <save_file> --web

# 指定端口
python3 BF_save.py <save_file> --web --port 8080
```

浏览器打开 `http://localhost:5000` 即可使用可视化编辑器。

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/tree` | GET | 获取存档树形结构 |
| `/api/leaves` | GET | 分页搜索叶子值 (`?q=&page=&per_page=`) |
| `/api/show` | GET | 展开指定路径 (`?path=`) |
| `/api/set` | POST | 修改单个字段 (`{"path":"...","value":...}`) |
| `/api/set_batch` | POST | 批量修改字段 (`{"items":[{...}]}`) |
| `/api/reload` | POST | 重新加载存档数据 |
| `/api/general_state` | GET | 获取通用状态 (灵魂、梦灰等) |
| `/api/magic_sword_state` | GET | 获取魔法剑配置 |
| `/api/potion_state` | GET | 获取药水配置 |
| `/api/rune_state` | GET | 获取符石背包 (`?page=&per_page=`) |

## 技术细节

本工具解析的是 Unity 引擎的 `BinaryFormatter` 序列化格式。解析器实现了以下记录类型的处理:

- `CWMAT` / `SCWMAT` — 类定义与成员值
- `CWI` — 类引用实例
- `BOS` — 二进制字符串
- `BAR` / `ASP` / `ASO` / `ASS` — 数组类型
- `MPT` / `MREF` / `NULL` — 多态类型、引用、空值
- `LIB` / `END` — 库引用和结束标记

## 安全性

- 每次修改前会自动创建 `.bak` 备份文件
- 建议在修改重要存档前手动备份原始文件

## License

[MIT](LICENSE)

## 免责声明

本工具仅供学习和研究 Unity BinaryFormatter 序列化格式使用。请遵守相关游戏的使用条款，修改游戏存档可能违反游戏规则。
