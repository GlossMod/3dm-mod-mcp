# 3DM Mod MCP

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)[![MCP](https://img.shields.io/badge/MCP-1.x-green.svg)](https://modelcontextprotocol.io)[![Status](https://img.shields.io/badge/Status-✅%20Production%20Ready-brightgreen.svg)](#)[![License](https://img.shields.io/badge/License-MIT-blue.svg)](#)

**3DM Mod 站的  MCP 服务器**


</div>

---

## ✨ 项目简介

**3DM ModMCP** 是一个完整的 **MCP (Model Context Protocol) 服务器实现**，为 Claude 和其他 LLM 应用提供 3DM Mod 网站的数据访问能力。


## ⚡ 快速开始 (3分钟)

### 连接 3DM Mod 站远程 MCP（24 个工具）

在 VS Code 的 `.vscode/mcp.json` 中添加以下配置，启动服务器时输入 [3DM Mod API 密钥](https://mod.3dmgame.com/Workshop/Api)。客户端通过 `Authorization` 请求头发送密钥值。

```json
{
    "servers": {
        "3dm-mod-remote": {
            "type": "http",
            "url": "https://mod.3dmgame.com/mcp",
            "headers": { "Authorization": "${input:GLOSSMOD_API_KEY}" }
        }
    },
    "inputs": [
        {
            "type": "promptString",
            "id": "GLOSSMOD_API_KEY",
            "description": "输入 3DM Mod API 密钥",
            "password": true
        }
    ]
}
```

### 运行本地 Python 服务（4 个工具）

#### 前置条件
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) 
- [3DM Mod API 密钥](https://mod.3dmgame.com/Workshop/Api)

#### 安装
```bash
pip install 3dm-mod-mcp
```


#### 更新
```bash
pip install --upgrade 3dm-mod-mcp
```


从 `glossmod-mcp` 迁移时，请将客户端的 `uvx` 参数更新为 `3dm-mod-mcp`。已有的 `GLOSSMOD_API_KEY` 可以继续使用。

#### 配置

```json
{
    "servers": {
        "3dm-mod-mcp": {
            "type": "stdio",
            "command": "uvx",
            "args": ["3dm-mod-mcp"],
            "env": {
                "GLOSSMOD_API_KEY": "${input:GLOSSMOD_API_KEY}"
            }
        }
    },
    "inputs": [
        {
            "type": "promptString",
            "id": "GLOSSMOD_API_KEY",
            "description": "输入你的Mod站 API",
            "default": "",
            "password": true
        }
    ]
}


```

## 🧰 工具列表

### 远程 HTTP 服务 · 24 个工具

2026-11-21 使用 API 密钥向 `https://mod.3dmgame.com/mcp` 请求 `tools/list`。服务端 `3DM Mods MCP`（`1.0.0`）在一页内返回全部 24 个工具。表中参数保留服务端的拼写和大小写。

#### 游戏、Mod 与 GMM 插件

| 工具 | 必填参数 | 可选参数 | 用途 |
| --- | --- | --- | --- |
| `get-game-list` | — | `page`、`pageSize`、`gameType`、`search`、`sortBy`、`sortOrder` | 按游戏名、英文名或描述搜索游戏。默认按 Mod 总数降序排列。 |
| `get-game-detail` | `id` | — | 查询单个游戏的详情和 Mod 数量统计。 |
| `get-mod-list` | — | `page`、`pageSize`、`search`、`original`、`time`、`order`、`key`、`gameId`、`gameTypeId`、`mods_publish`、`support_gmm`、`local` | 按游戏、标签、发布者等筛选 Mod。`gameId` 可传单个 ID 或数组，`order=2` 按下载量排序。 |
| `get-mod-detail` | `id` | — | 按 Mod ID 查询详情。 |
| `check-mod-update` | `modId` | — | 批量查询版本信息，`modId` 为 Mod ID 数组。 |
| `get-gmm-plugins` | — | `game_id`、`from` | 按游戏或来源筛选 Gloss Mod Manager 插件。 |

#### Minecraft Mod

| 工具 | 必填参数 | 可选参数 | 用途 |
| --- | --- | --- | --- |
| `get-minecraft-mod-list` | — | `page`、`pageSize`、`modules`、`types`、`startTime`、`endTime`、`search`、`sortBy`、`sortOrder` | 按加载器、分类、关键词或更新时间筛选 Minecraft Mod。 |
| `get-minecraft-mod-detail` | `id` | — | 按 ID 查询 Minecraft Mod 详情。 |
| `publish-minecraft-mod` | `data` | — | 发布或更新 Minecraft Mod。`data` 对象必须包含 `files`。 |

#### 地图、标记类型与点位

| 工具 | 必填参数 | 可选参数 | 用途 |
| --- | --- | --- | --- |
| `get-map-list` | — | `keyword`、`state` | 列出当前用户可管理的地图。 |
| `get-map-mark-list` | `mapId` | `ids`、`includeDeleted`、`includePoints` | 列出地图的标记类型。设置 `includePoints=true` 可同时获取各类型下的点位。 |
| `get-map-point-list` | `mapId` | `ids`、`markIds`、`state`、`type`、`keyword`、`includeDeleted`、`page`、`pageSize` | 分页查询地图点位，可按标记类型、点位状态或关键词筛选。 |
| `batch-import-map-marks` | `mapId`、`marks` | — | 为指定地图批量导入标记类型。 |
| `batch-import-map-points` | `markId`、`points` | — | 批量导入点位。`markId` 指定所属标记类型，单个点位可用 `parent` 指定类型。 |
| `batch-update-map-marks` | `mapId`、`updates` | — | 批量编辑地图标记类型。`updates` 中每项须包含标记类型的 `id`。 |
| `batch-update-map-points` | `mapId`、`updates` | — | 批量编辑地图点位。`updates` 中每项须包含点位的 `id` 和要修改的字段。 |

#### 搜索、Wiki、阅读与账号

| 工具 | 必填参数 | 可选参数 | 用途 |
| --- | --- | --- | --- |
| `search-v3-content` | `q` | `type`、`page`、`pageSize` | 跨游戏、Mod、Wiki、阅读和 Minecraft 内容搜索。用 `type` 限定范围后可分页。 |
| `get-hot-content` | — | `type`、`limit`、`period` | 按内容类型和时间范围获取热门内容，默认返回本周 10 条。 |
| `get-stats-summary` | — | — | 获取 3DM Mod 站的平台统计汇总。 |
| `get-wiki-list` | — | `page`、`pageSize`、`tags`、`search`、`sortBy`、`sortOrder` | 按标签或关键词查找 Wiki 并排序。 |
| `get-wiki-detail` | `id` | — | 按 ID 查询单个 Wiki 详情。 |
| `get-read-list` | — | `page`、`pageSize`、`readType`、`tags`、`search`、`sortBy`、`sortOrder` | 按阅读类型、标签或关键词查找文章并排序。 |
| `get-read-detail` | `id` | — | 按 ID 查询单篇阅读内容。 |
| `login-user` | `username`、`password` | — | 校验 3DM 账号登录信息，返回用户公开资料。 |

### 本地 stdio 服务 · 4 个工具

通过 `uvx 3dm-mod-mcp` 启动时，使用下列工具名和参数。

| 工具              | 主要参数                                                                 | 用途                                                                                                     |
| ----------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| `get_games`       | 可选 `search`、`game_type`、`sort_by`、`sort_order`、`page`、`page_size` | 搜索或浏览游戏，取得后续查询需要的游戏 `id`。默认按 Mod 数量降序排列。                                   |
| `get_game_detail` | `game_id`                                                                | 获取指定游戏的详情、Mod 数量统计和用于定位游戏页面的 `game_path`。                                       |
| `get_mods`        | 可选 `game_id`、`search`、`order`、`time`、`page`、`page_size`           | 按关键词浏览 Mod。`game_id` 可传单个 ID 或 ID 列表；例如 `order=2` 按下载量排序，`time=2` 限定最近一周。 |
| `get_mod_detail`  | `mod_id`                                                                 | 按 Mod 的 `id` 获取详情，包括站点返回的作者与所属游戏信息。                                              |

例如，先用 `get_games(search="Skyrim")` 确认游戏 ID，再用 `get_mods` 搜索该游戏的 Mod，最后将选中结果的 `id` 传给 `get_mod_detail`。两个列表工具均从第 1 页开始，默认每页 20 条。

## 发布到 PyPI

首次发布前，在 PyPI 为项目 `3dm-mod-mcp` 添加 GitHub Trusted Publisher。项目尚未创建时，可以在账户的 [Publishing 设置](https://pypi.org/manage/account/publishing/) 中预先登记。

| PyPI 配置项       | 值            |
| ----------------- | ------------- |
| Owner             | `GlossMod`    |
| Repository        | `3dm-mod-mcp` |
| Workflow filename | `publish.yml` |
| Environment       | `pypi`        |

将工作流合入 `main` 后，在 GitHub 的 **Releases → Draft a new release** 中为目标提交选择版本标签，例如 `v1.3.0`，然后点击 **Publish release**。GitHub Actions 会构建并校验 wheel 和源码包，再将 `3dm-mod-mcp` 的 `1.3.0` 版本发布到 PyPI。预发布可使用 `v1.3.0rc1` 这样的标签。
