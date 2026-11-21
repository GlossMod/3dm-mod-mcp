#!/usr/bin/env python
"""3dm-mod-mcp 发布助手。正常发布由 GitHub Release 触发，Twine 仅用于手动操作。"""

import argparse
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlencode

PROJECT = "3dm-mod-mcp"
RELEASE_URL = f"https://github.com/GlossMod/{PROJECT}/releases/new"
UPLOAD_URLS = {
    "pypi": "https://upload.pypi.org/legacy/",
    "testpypi": "https://test.pypi.org/legacy/",
}
PROJECT_URLS = {
    "pypi": f"https://pypi.org/project/{PROJECT}/",
    "testpypi": f"https://test.pypi.org/project/{PROJECT}/",
}


def run_command(cmd: list[str], description: str) -> bool:
    print(description, flush=True)
    try:
        # 保留终端交互，让 Twine 可以提示输入凭据。
        subprocess.run(cmd, check=True)
        return True
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"操作失败：{exc}", file=sys.stderr)
        return False


def release_tag(version: str) -> str:
    from packaging.version import Version

    # 与 publish.yml 一样，接受 PEP 440 版本并规范化，但不允许本地版本。
    parsed = Version(version)
    if parsed.local is not None:
        raise ValueError("PyPI 发布标签不能包含本地版本标识（+...）。")
    return f"v{parsed}"


def prepare_github_release(tag: str) -> bool:
    if not run_command(["git", "tag", "-a", tag, "-m", f"Release {tag}"], f"创建标签 {tag}"):
        return False
    if not run_command(["git", "push", "origin", f"refs/tags/{tag}"], f"推送标签 {tag} 到 origin"):
        return False

    print(f"请打开链接并点击 Publish release：{RELEASE_URL}?{urlencode({'tag': tag})}")
    print("发布 Release 会触发 publish.yml，由 pypi 环境通过 Trusted Publishing 上传；请勿事先手动上传。")
    return True


def check_distributions() -> list[str]:
    dist_dir = Path("dist")
    wheels = sorted(path for path in dist_dir.glob("3dm_mod_mcp-*.whl") if path.is_file())
    sdists = sorted(path for path in dist_dir.glob("3dm_mod_mcp-*.tar.gz") if path.is_file())
    if not wheels or not sdists:
        print("dist/ 中需要新包的 3dm_mod_mcp-*.whl 和 3dm_mod_mcp-*.tar.gz，请先用 uv build 构建。", file=sys.stderr)
        return []
    return [str(path) for path in (*wheels, *sdists)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"{PROJECT} 发布助手（请从仓库根目录运行）")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--check", action="store_true", help="检查本地构建产物，不上传")
    actions.add_argument("--release", metavar="VERSION", help="创建并推送 Git 标签，然后显示 GitHub Release 链接")
    actions.add_argument("--upload", choices=UPLOAD_URLS, help="手动上传到 PyPI 或 TestPyPI，不创建 Release")
    actions.add_argument("--full", action="store_true", help="显示 GitHub Release 发布指引，不执行操作")
    args = parser.parse_args(argv)

    if args.full:
        print("正常发布请按 docs/PUBLISHING.md 检查目标提交和构建，再运行：")
        print("  uv run --no-project --with packaging python scripts/publish.py --release v1.3.0")
        print("打开输出的链接并点击 Publish release，由 GitHub Actions 上传，不要先手动上传。")
        return 0

    if args.release is not None:
        try:
            tag = release_tag(args.release)
        except ModuleNotFoundError:
            print("缺少 packaging，请运行 python -m pip install packaging。", file=sys.stderr)
            return 1
        except ValueError as exc:
            parser.error(f"无效的发布版本：{exc}（示例：1.3.0、v1.3.0rc1）")
        return 0 if prepare_github_release(tag) else 1

    if args.check or args.upload:
        files = check_distributions()
        twine = [sys.executable, "-m", "twine"]
        if not files or not run_command([*twine, "check", *files], "检查包元数据（需要 Twine）"):
            return 1
        if args.check:
            print("检查通过。正式发布请按 docs/PUBLISHING.md 发布 GitHub Release。")
            return 0
        if args.upload == "pypi":
            print("这是手动发布；不要再发布同版本的 GitHub Release，以免触发重复上传。")
        if not run_command(
            [*twine, "upload", "--repository-url", UPLOAD_URLS[args.upload], *files],
            f"手动上传到 {args.upload}",
        ):
            return 1
        print(f"手动上传成功：{PROJECT_URLS[args.upload]}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
