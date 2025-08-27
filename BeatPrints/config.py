"""配置管理模块"""
import tomli
from pathlib import Path
from typing import Dict, Any

_CONFIG_CACHE: Dict[str, Any] | None = None

def load_config() -> Dict[str, Any]:
    """加载配置文件"""
    global _CONFIG_CACHE
    if _CONFIG_CACHE is not None:
        return _CONFIG_CACHE

    config_path = Path("pyproject.toml")
    if config_path.exists():
        with open(config_path, "rb") as f:
            _CONFIG_CACHE = tomli.load(f).get("tool", {}).get("beatprints", {})
    else:
        _CONFIG_CACHE = {}
    return _CONFIG_CACHE

def get_theme_config():
    """获取主题配置"""
    config = load_config()
    return {
        "default": config.get("default_theme", "Light"),
        "themes": config.get("themes", {})
    }

def get_output_config():
    """获取输出配置"""
    config = load_config()
    output = config.get("output", {})
    return {
        "save_to": output.get("save_to", "./"),
        "width": output.get("width", 1080),
        "height": output.get("height", 1920)
    } 