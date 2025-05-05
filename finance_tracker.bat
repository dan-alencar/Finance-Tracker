@echo off
REM Abre o terminal no diretório correto e executa o app

cd /d "%~dp0"
python -m finance_app.main
pause