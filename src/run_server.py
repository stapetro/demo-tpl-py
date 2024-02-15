"""
Dev config for uvicorn
"""

from argparse import ArgumentParser

import uvicorn

from app.core.config import LoggingConfig, get_settings

if __name__ == "__main__":
    if get_settings().PYDEVD:
        import pydevd_pycharm

        pydevd_pycharm.settrace(
            get_settings().PYDEVD_HOST,
            port=get_settings().PYDEVD_PORT,
            stdoutToServer=True,
            stderrToServer=True,
        )

    parser = ArgumentParser()
    parser.add_argument(
        "-r",
        "--reload",
        metavar="DIRS",
        default=None,
        help="enable auto-reloading of this base dir (e.g. '--reload src/'); "
        "also enabled DEBUG mode",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8080,
        help="port to listen on (default: 8080)",
    )
    config = parser.parse_args()

    uvicorn_config: dict = {
        "log_config": LoggingConfig.get_config(get_settings().ENV_NAME),
    }
    if get_settings().ENV_NAME == "loc":
        reload_dirs = config.reload.split(",") if config.reload else []
        reload_enabled = bool(reload_dirs)
        uvicorn_config = {
            **uvicorn_config,
            "reload": reload_enabled,
            "reload_dirs": reload_dirs,
            "use_colors": True,
        }

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=config.port,
        **uvicorn_config,
    )
