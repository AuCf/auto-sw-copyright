$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir
Write-Host "正在启动 AutoCopyright-AI 系统..." -ForegroundColor Cyan
python "$ScriptDir\start.py"
