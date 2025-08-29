#!/usr/bin/env python3
"""
Web Crawler Pro - Aplicação Principal
Desenvolvido em Python com interface gráfica moderna

Recursos:
- Interface gráfica moderna com CustomTkinter
- Crawling com requests + BeautifulSoup
- Suporte a JavaScript com Selenium
- Filtros avançados de conteúdo
- Seletores CSS personalizados
- Exportação para Excel, CSV e JSON
- Configurações de proxy e headers
- Respeito ao robots.txt
- Sistema de logging
- Presets para diferentes tipos de sites
"""

import sys
import os

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from crawler_gui import CrawlerGUI
    
    def main():
        """Função principal"""
        print("🕷️ Iniciando Web Crawler Pro...")
        print("Carregando interface gráfica...")
        
        app = CrawlerGUI()
        app.run()

    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("\n📦 Para instalar as dependências, execute:")
    print("pip install -r requirements.txt")
    print("\nOu instale manualmente:")
    print("pip install requests beautifulsoup4 selenium pandas customtkinter fake-useragent webdriver-manager openpyxl lxml")
    sys.exit(1)
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    sys.exit(1)
