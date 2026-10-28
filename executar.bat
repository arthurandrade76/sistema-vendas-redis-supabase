@echo off
cd /d "%~dp0"
echo Iniciando Sistema de Vendas (Supabase + Redis)...
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocorreu um erro ao executar a aplicacao.
    pause
)
