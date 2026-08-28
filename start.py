import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = ROOT_DIR / "backend"
FRONTEND_DIR = ROOT_DIR / "frontend"

def main():
    print("=" * 60)
    print("       AutoCopyright-AI | 软著资料一键生成系统 启动器")
    print("=" * 60)
    print()

    # 1. Start Backend
    print("[1/3] 正在启动后端服务 (FastAPI / 端口 8000)...")
    backend_cmd = [sys.executable, str(BACKEND_DIR / "run.py")]
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=str(BACKEND_DIR)
    )

    # 2. Start Frontend
    print("[2/3] 正在启动前端服务 (Vue 3 / Vite / 端口 5188)...")
    npm_executable = "npm.cmd" if os.name == "nt" else "npm"
    frontend_cmd = [npm_executable, "run", "dev"]
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=str(FRONTEND_DIR),
        shell=True
    )

    print("[3/3] 等待服务初始化...")
    time.sleep(2)

    print()
    print("✅ 系统已成功启动！")
    print("👉 前端访问地址: http://localhost:5188")
    print("👉 后端 API 文档: http://localhost:8000/docs")
    print()
    print("正在自动打开浏览器...")
    webbrowser.open("http://localhost:5188")

    print()
    print("提示：按 Ctrl+C 可停止全部服务。")

    try:
        backend_proc.wait()
    except KeyboardInterrupt:
        print("\n正在关闭服务...")
        backend_proc.terminate()
        frontend_proc.terminate()
        print("服务已停止。")

if __name__ == "__main__":
    main()
