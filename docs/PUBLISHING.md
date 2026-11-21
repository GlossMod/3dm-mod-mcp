# 3dm-mod-mcp 发布指南

正式发布入口是 **GitHub Release**：在 `GlossMod/3dm-mod-mcp` 点击 **Publish release** 后，`.github/workflows/publish.yml` 响应 `release: published`，以该 Release 的 Git 标签为版本构建 wheel 和源码包，再由 `pypi` 环境通过 PyPI Trusted Publishing 上传。只推送标签或保存草稿不会发布到 PyPI。

PyPI 包名和 CLI 均为 `3dm-mod-mcp`；Python 导入仍为 `glossmod_mcp`。不要手工修改 `pyproject.toml`、Python 模块或发布脚本中的版本号。

## 首次配置 Trusted Publishing

在 GitHub 仓库 **Settings → Environments** 中配置名为 `pypi` 的环境。然后在 PyPI 添加 GitHub Actions Trusted Publisher，字段须与工作流匹配：

| PyPI 字段 | 值 |
| --- | --- |
| PyPI Project Name（若尚未创建项目） | `3dm-mod-mcp` |
| Owner | `GlossMod` |
| Repository name | `3dm-mod-mcp` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

若 PyPI 项目尚未创建，使用账户的 [Pending Publishers 配置](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/)；若已存在，在该项目的 [Publishing 设置](https://docs.pypi.org/trusted-publishers/adding-a-publisher/)中添加。正常发布不需要配置 PyPI API Token secret。

## 发布前检查：在本地构建，不上传

从仓库根目录操作；确认发布目标提交已经包含 `publish.yml` 和要发布的改动。新标签采用 PEP 440 版本：`v1.3.0` 表示正式版 `1.3.0`，`v1.3.0rc1` 表示预发布版 `1.3.0rc1`。发布助手会规范化 PEP 440 写法，例如将 `1.3.0-rc.1` 转成标签 `v1.3.0rc1`；不接受 `+local` 版本。

可以在不创建标签的情况下试构建。确保 `dist/` 中没有旧产物；下面的示例使用 `--clear` 清理该目录，并临时指定预期版本，模拟 CI 去掉 `v` 后使用的构建版本。预发布测试把示例中的版本换成 `1.3.0rc1`。

```powershell
$env:SETUPTOOLS_SCM_PRETEND_VERSION_FOR_3DM_MOD_MCP = '1.3.0'
try {
    uv build --clear
} finally {
    Remove-Item Env:SETUPTOOLS_SCM_PRETEND_VERSION_FOR_3DM_MOD_MCP
}
uv run --no-project --with twine python scripts/publish.py --check
```

在 Bash 中对应的构建命令为 `SETUPTOOLS_SCM_PRETEND_VERSION_FOR_3DM_MOD_MCP=1.3.0 uv build --clear`。检查产物名（版本换成此次实际版本）：`dist/3dm_mod_mcp-1.3.0-py3-none-any.whl` 和 `dist/3dm_mod_mcp-1.3.0.tar.gz`。可在隔离环境中安装 wheel，验证导入、版本和入口点：

```bash
uv run --no-project --with ./dist/3dm_mod_mcp-1.3.0-py3-none-any.whl python -I -c "import glossmod_mcp; from importlib.metadata import distribution; d = distribution('3dm-mod-mcp'); assert d.version == '1.3.0'; assert any(e.name == '3dm-mod-mcp' and e.value == 'glossmod_mcp.server:main' for e in d.entry_points)"
```

## 正式发布：创建并发布 GitHub Release

1. 确认 `HEAD` 是要发布的提交，`origin` 指向 `GlossMod/3dm-mod-mcp`，该版本尚未上传至正式 PyPI。
2. 运行以下命令创建并推送注解标签。任选一个对应的版本；脚本也接受不带 `v` 的输入，如 `1.3.0`。

   ```bash
   uv run --no-project --with packaging python scripts/publish.py --release v1.3.0
   # 预发布示例（替代上一行）
   uv run --no-project --with packaging python scripts/publish.py --release v1.3.0rc1
   ```

   如果标签已经推送，直接在 GitHub 创建 Release 时选用现有标签，不要重建或移动标签。脚本的 `--full` 仅显示发布指引，不执行任何操作。
3. 打开脚本输出的 Release 链接，确认使用的是对应标签，填写发布说明。对于 `v1.3.0rc1` 勾选 **Set as a pre-release**。点击 **Publish release**；不必手工向 Release 附加本地构建产物，也不要先上传到正式 PyPI。
4. 在 Actions 查看 **Publish to PyPI** 的构建和发布结果（如果 `pypi` 环境要求审核，在 GitHub 上批准部署）。成功后检查 PyPI 的 `3dm-mod-mcp` 项目页，并在干净环境安装验证。稳定版用 `python -m pip install 3dm-mod-mcp==1.3.0`，预发布版验证时可明确指定 `3dm-mod-mcp==1.3.0rc1`。

## 可选：TestPyPI 和例外手动上传

手动上传只使用本地 `dist/` 中的 `3dm_mod_mcp-*.whl` 和 `3dm_mod_mcp-*.tar.gz`，不打标签、不创建 GitHub Release。上传前确认没有混入其他版本的新包产物，并使用目标索引的凭据（TestPyPI 和正式 PyPI 的令牌不通用）。

```bash
# 可选：用 TestPyPI 演练，不影响正式发布
uv run --no-project --with twine python scripts/publish.py --upload testpypi

# 仅当明确改用手动流程且项目允许 API token 上传时
uv run --no-project --with twine python scripts/publish.py --upload pypi
```

已经手动上传到正式 PyPI 的版本不要再发布同版本的 GitHub Release，否则工作流会尝试重复上传。发布失败时先检查 PyPI 是否已收到任何产物，再决定是否安全重跑；不要为重试而把同一标签改指到新提交。

用户安装和 MCP 客户端配置见 [快速开始](QUICKSTART.md)。
