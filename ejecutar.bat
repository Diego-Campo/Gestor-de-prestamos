@echo off
echo Iniciando Gestor de Préstamos...
"%~dp0.venv\Scripts\python.exe" "%~dp0app.py"
if errorlevel 1 pause