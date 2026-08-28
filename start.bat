@echo off
setlocal enabledelayedexpansion
title AutoCopyright-AI Launcher

echo ========================================================
echo       AutoCopyright-AI 软著生成系统 启动器
echo ========================================================
echo.

cd /d "%~dp0"
echo 当前工作目录: %cd%

:: 1. 查找 Python 路径
set "PYTHON_EXE=C:\Users\kinca\AppData\Local\Programs\Python\Python312\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

echo [1/3] 检查 Python 运行环境...
"%PYTHON_EXE%" --version
if errorlevel 1 (
    echo [错误] 未能找到可用的 Python，请确认已安装 Python。
    pause
    exit /b 1
)

:: 2. 查找 Node / NPM 路径
set "NPM_CMD=npm.cmd"
where npm >nul 2>nul
if errorlevel 1 (
    if exist "C:\Program Files\nodejs\npm.cmd" (
        set "NPM_CMD=C:\Program Files\nodejs\npm.cmd"
    ) else if exist "C:\Program Files (x86)\nodejs\npm.cmd" (
        set "NPM_CMD=C:\Program Files (x86)\nodejs\npm.cmd"
    )
)

echo [2/3] 检查 Node/NPM 运行环境...
call %NPM_CMD% --version
if errorlevel 1 (
    echo [错误] 未能找到 npm 命令，请确认已安装 Node.js。
    pause
    exit /b 1
)

echo.
echo [3/3] 正在启动前后端服务...
echo   - 正在启动后端服务 (FastAPI 端口 8000)...
start "AutoCopyright-AI Backend" cmd /k "cd /d "%~dp0backend" && "%PYTHON_EXE%" run.py"

timeout /t 2 >nul

echo   - 正在启动前端服务 (Vue 3 端口 5188)...
start "AutoCopyright-AI Frontend" cmd /k "cd /d "%~dp0frontend" && call %NPM_CMD% run dev"

timeout /t 3 >nul

echo.
echo ========================================================
echo   全部服务已启动完成！
echo   前端访问地址: http://localhost:5188
echo   后端接口文档: http://localhost:8000/docs
echo ========================================================
echo.
echo 正在为你自动打开浏览器...
start http://localhost:5188

echo.
echo 本窗口可关闭，前后端服务将在各自弹出的窗口中持续运行。
echo.
pause
