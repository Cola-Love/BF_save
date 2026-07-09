# BF_save - 暖雪存档编辑器

一款专为 **《暖雪》(Warm Snow)** 打造的存档编辑工具，同时支持任意 Unity BinaryFormatter 格式的二进制存档文件的查看与修改。提供 CLI 命令行和 Web 可视化两种操作方式。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/Version-1.89-orange" alt="Version">
</p>

## 暖雪专版功能

Web 编辑器针对《暖雪》提供了深度整合的可视化面板：

| 面板 | 可配置项 |
|------|---------|
| **通用状态** | 红魂、蓝魂、梦灰、时序之辉、通关次数 |
| **魔法剑** | 剑名、等级、5 个词条插槽（条目 ID / 等级 / 数值 / 梦魇） |
| **药水** | 4 个药水槽位（药水 ID / 等级 / 元素类型） |
| **符石背包** | 分页查看全部符石（锁定状态、5 个修饰符键值） |
| **树形浏览器** | 完整存档树形结构浏览，任意路径展开 |
| **字段搜索** | 全局搜索存档中任意字段名或值 |

## 功能特性

- **暖雪全参数编辑**: 红魂、蓝魂、梦灰、魔法剑、药水、符石一站式修改
- **通用 BinaryFormatter 解析**: 完整支持 Unity BinaryFormatter 序列化格式的读取与编辑
- **CLI 模式**: 命令行查看、搜索、修改任意存档数据
- **Web 可视化编辑器**: 基于 Flask 的图形界面，直观操作
- **自动备份**: 修改前自动生成带时间戳的 `.bak` 备份文件
- **批量修改**: Web 界面一次提交多个字段修改
- **路径定位**: 支持 `> ` 分隔的嵌套路径，精确定位深层字段

## 项目结构

```
BF_save/
├── BF_save.py          # 主入口 (CLI + Web 启动)
├── core/
│   ├── parser.py       # BinaryFormatter 二进制解析器
│   ├── stream.py       # 二进制流读写
│   └── constants.py    # 记录类型 / 基础类型常量定义
├── editor/
│   ├── setter.py       # 字段修改器 (含自动备份)
│   └── formatter.py    # 树遍历 / 格式化输出
├── web/
│   ├── app.py          # Flask 应用 + 数据加载
│   ├── api.py          # REST API 接口
│   ├── config.py       # 版本号配置
│   ├── data.py         # 暖雪游戏数据枚举 / 映射表
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
git clone https://github.com/Cola-Love/BF_save.git
cd BF_save
```

## 用法

### 暖雪存档编辑（Web 模式，推荐）

```bash
# 启动 Web 编辑器
python3 BF_save.py your_save.dat --web

# 指定端口
python3 BF_save.py your_save.dat --web --port 8080
```

浏览器打开 `http://localhost:5000`，即可在可视化界面中修改灵魂、魔法剑、药水、符石等全部参数。

### CLI 模式（通用 BinaryFormatter 存档）

```bash
# 查看存档概览
python3 BF_save.py <save_file>

# 完整 JSON 输出
python3 BF_save.py <save_file> --json

# 分页列出所有字段值
python3 BF_save.py <save_file> --list [page] [n]

# 将所有字段值保存到文件
python3 BF_save.py <save_file> --list --save output.txt

# 搜索字段（按名称模糊匹配）
python3 BF_save.py <save_file> --find keyword

# 展开指定路径
python3 BF_save.py <save_file> --show "path > to > field"

# 修改顶层字段
python3 BF_save.py <save_file> --set field_name new_value

# 修改嵌套路径字段
python3 BF_save.py <save_file> --set --path "path > to > field" --value new_value
```

### 修改示例

```bash
# 红魂 999999
python3 BF_save.py save.dat --set souls 999999

# 蓝魂 999999
python3 BF_save.py save.dat --set redsouls 999999

# 梦灰 999999
python3 BF_save.py save.dat --set dreamAsh 999999

# 嵌套路径修改（魔法剑等级）
python3 BF_save.py save.dat --set --path "magicSword > Level" --value 99
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/tree` | GET | 获取存档完整树形结构 |
| `/api/leaves` | GET | 分页搜索所有叶子值 `?q=&page=&per_page=` |
| `/api/show` | GET | 展开指定路径 `?path=` |
| `/api/set` | POST | 修改单个字段 `{"path":"...","value":...}` |
| `/api/set_batch` | POST | 批量修改 `{"items":[{"path":"...","value":...}]}` |
| `/api/reload` | POST | 重新加载存档数据 |
| `/api/general_state` | GET | 获取通用状态（红魂/蓝魂/梦灰等） |
| `/api/magic_sword_state` | GET | 获取魔法剑完整配置 |
| `/api/potion_state` | GET | 获取 4 个药水槽位 |
| `/api/rune_state` | GET | 分页获取符石背包 `?page=&per_page=` |

## BinaryFormatter 支持

本工具完整实现了 Unity `BinaryFormatter` 序列化格式的解析，支持以下记录类型：

- `CWMAT` / `SCWMAT` — 类定义与成员值
- `CWI` — 类引用实例
- `BOS` — 二进制字符串
- `BAR` / `ASP` / `ASO` / `ASS` — 数组类型
- `MPT` / `MREF` / `NULL` — 多态类型、引用、空值
- `LIB` / `END` — 库引用和结束标记

因此除了《暖雪》以外，任何使用 Unity BinaryFormatter 序列化的游戏存档都可以用 CLI 模式查看和修改。

## 安全性

- 每次修改前自动创建 `文件名.YYYYMMDD_HHMMSS.bak` 备份
- 修改重要存档前建议额外手动备份

## License

本项目采用 [MIT](LICENSE) 许可证开源。

## 免责声明

本工具仅供学习和研究 Unity BinaryFormatter 序列化格式使用。使用本工具修改游戏存档可能违反相关游戏的使用条款，使用者需自行承担风险。
