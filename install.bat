@echo off
echo ==========================================
echo   Web Crawler Pro - Script de Instalacao
echo ==========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python 3.7+ em: https://python.org
    pause
    exit /b 1
)

echo Python encontrado!
python --version

echo.
echo Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: pip nao encontrado!
    echo Reinstale Python com pip incluido.
    pause
    exit /b 1
)

echo pip encontrado!
echo.

echo Atualizando pip...
python -m pip install --upgrade pip

echo.
echo Instalando dependencias...
echo.

echo [1/13] Instalando requests...
pip install requests

echo [2/13] Instalando beautifulsoup4...
pip install beautifulsoup4

echo [3/13] Instalando selenium...
pip install selenium

echo [4/13] Instalando pandas...
pip install pandas

echo [5/13] Instalando customtkinter...
pip install customtkinter

echo [6/13] Instalando fake-useragent...
pip install fake-useragent

echo [7/13] Instalando webdriver-manager...
pip install webdriver-manager

echo [8/13] Instalando openpyxl...
pip install openpyxl

echo [9/13] Instalando lxml...
pip install lxml

echo [10/13] Instalando urllib3...
pip install urllib3

echo [11/13] Instalando pillow...
pip install pillow

echo [12/13] Instalando ttkthemes...
pip install ttkthemes

echo [13/13] Instalando todas as dependencias do requirements.txt...
pip install -r requirements.txt

echo.
echo ==========================================
echo   Instalacao Concluida!
echo ==========================================
echo.

echo Testando importacoes...
python -c "import requests, bs4, selenium, pandas, customtkinter; print('✓ Todas as bibliotecas importadas com sucesso!')"

if errorlevel 1 (
    echo.
    echo AVISO: Algumas bibliotecas podem nao ter sido instaladas corretamente.
    echo Verifique as mensagens de erro acima.
    echo.
) else (
    echo.
    echo ✓ Instalacao bem-sucedida!
    echo.
    echo Para executar o Web Crawler:
    echo   python main.py          (Interface grafica)
    echo   python exemplo.py       (Exemplos via linha de comando)
    echo.
)

echo Pressione qualquer tecla para continuar...
pause >nul
