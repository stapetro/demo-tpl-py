"""
Dev config for uvicorn
"""
import uvicorn

from app.core.config import settings

if __name__ == "__main__":
    print(settings.PYDEVD)
    if settings.PYDEVD:
        import pydevd_pycharm

        pydevd_pycharm.settrace(
            settings.PYDEVD_HOST,
            port=settings.PYDEVD_PORT,
            stdoutToServer=True,
            stderrToServer=True,
        )

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
