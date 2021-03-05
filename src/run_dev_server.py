"""
Dev config for uvicorn
"""
import uvicorn


def main():
    print("Hello from main")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
