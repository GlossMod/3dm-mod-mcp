# GlossModMCP - 3DM Mod API MCP 服务器

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)[![MCP](https://img.shields.io/badge/MCP-1.x-green.svg)](https://modelcontextprotocol.io)[![Status](https://img.shields.io/badge/Status-✅%20Production%20Ready-brightgreen.svg)](#)[![License](https://img.shields.io/badge/License-MIT-blue.svg)](#)

**3DM Mod 站的  MCP 服务器**


</div>

---

## ✨ 项目简介

**GlossModMCP** 是一个完整的 **MCP (Model Context Protocol) 服务器实现**，为 Claude 和其他 LLM 应用提供 3DM Mod 网站的数据访问能力。


## ⚡ 快速开始 (3分钟)

### 前置条件
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) 
- [3DM Mod API 密钥](https://mod.3dmgame.com/Workshop/Api)

### 安装
```bash
pip install 3dm-mod-mcp
```


### 更新
```bash
pip install --upgrade 3dm-mod-mcp
```


从 `glossmod-mcp` 迁移时，请将客户端的 `uvx` 参数更新为 `3dm-mod-mcp`。已有的 `GLOSSMOD_API_KEY` 可以继续使用。

### 配置

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

## 发布到 PyPI

首次发布前，在 PyPI 为项目 `3dm-mod-mcp` 添加 GitHub Trusted Publisher。项目尚未创建时，可以在账户的 [Publishing 设置](https://pypi.org/manage/account/publishing/) 中预先登记。

| PyPI 配置项 | 值 |
| --- | --- |
| Owner | `GlossMod` |
| Repository | `3dm-mod-mcp` |
| Workflow filename | `publish.yml` |
| Environment | `pypi` |

将工作流合入 `main` 后，在 GitHub 的 **Releases → Draft a new release** 中为目标提交选择版本标签，例如 `v1.3.0`，然后点击 **Publish release**。GitHub Actions 会构建并校验 wheel 和源码包，再将 `3dm-mod-mcp` 的 `1.3.0` 版本发布到 PyPI。预发布可使用 `v1.3.0rc1` 这样的标签。
