"""
GlossModMCP - 3DM Mod API MCP 服务器

这是一个完整的 MCP (Model Context Protocol) 服务器实现，
为 Claude 和其他 LLM 应用提供 3DM Mod 网站的数据访问能力。
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("3dm-mod-mcp")
except PackageNotFoundError:
    __version__ = "0+unknown"

__author__ = "小莫"
__email__ = "xiaomo1433675239@outlook.com"
