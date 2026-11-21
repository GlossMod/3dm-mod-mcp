# 📋 GlossModMCP 发布速查表

> **已归档：旧发布速查表。** 下方包名、版本和手动上传步骤仅用于保留历史，不适用于当前发布。请使用 [当前发布指南](PUBLISHING.md)。

## 🎯 最快发布（只需这 3 行代码）

```powershell
# 注册 PyPI（第一次）
# 访问 https://pypi.org/account/register/

# 上传包
twine upload dist/*

# 完成！用户现在可以：pip install glossmod-mcp
```

---

## 📦 包信息

| 项     | 值                                         |
| ------ | ------------------------------------------ |
| 包名   | `glossmod-mcp`                             |
| 版本   | `1.0.0`                                    |
| Wheel  | `dist/glossmod_mcp-1.0.0-py3-none-any.whl` |
| Source | `dist/glossmod_mcp-1.0.0.tar.gz`           |
| 大小   | 7.8 KB + 7.3 KB                            |

---

## 🔗 关键链接

- **PyPI**: https://pypi.org/
- **MCP Registry**: https://modelcontextprotocol.io/servers
- **GitHub**: https://github.com/GlossMod/gloss-mod-mcp

---

## 📚 生成的新文件

```
PUBLISH_READY.md           发布总结（开始看这个）
docs/PUBLISHING.md         详细指南
RELEASE_CHECKLIST.md       检查清单
scripts/publish.py         自动工具
PUBLISH_NOW.txt            快速参考
```

---

## ✨ 已做好的准备

- ✅ 标准包结构（glossmod_mcp/）
- ✅ pyproject.toml 已更新
- ✅ LICENSE 和 MANIFEST.in
- ✅ 构建成功（wheel + tar.gz）
- ✅ 所有文档已生成

---

## 🚀 三种发布方式

| 方式             | 命令                         | 时间   |
| ---------------- | ---------------------------- | ------ |
| **PyPI**         | `twine upload dist/*`        | 2 分钟 |
| **GitHub**       | `git tag v1.0.0 && git push` | 3 分钟 |
| **MCP Registry** | 网页表单                     | 5 分钟 |

---

## ⚡ 一分钟快速检查

```powershell
python scripts/publish.py --check
```

---

## 💾 本地测试（可选）

```powershell
```powershell
pip install dist/glossmod_mcp-1.0.0-py3-none-any.whl
```
python -c "import glossmod_mcp; print(glossmod_mcp.__version__)"
```

---

## 🎉 就这样！

你的 MCP 服务器已完全准备好发布了！

**下一步**: 选择上面的任一方式发布即可。
