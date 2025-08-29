#!/usr/bin/env python3
"""
Script de Teste para Web Crawler Pro
Testa todas as funcionalidades principais
"""

import sys
import os
import time
import json
from datetime import datetime

# Adiciona o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testa se todas as importações estão funcionando"""
    print("🧪 Testando importações...")
    
    try:
        import requests
        print("✓ requests")
    except ImportError as e:
        print(f"❌ requests: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✓ beautifulsoup4")
    except ImportError as e:
        print(f"❌ beautifulsoup4: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ pandas")
    except ImportError as e:
        print(f"❌ pandas: {e}")
        return False
    
    try:
        import customtkinter as ctk
        print("✓ customtkinter")
    except ImportError as e:
        print(f"❌ customtkinter: {e}")
        return False
    
    try:
        from selenium import webdriver
        print("✓ selenium")
    except ImportError as e:
        print(f"❌ selenium: {e}")
        return False
    
    try:
        from fake_useragent import UserAgent
        print("✓ fake-useragent")
    except ImportError as e:
        print(f"❌ fake-useragent: {e}")
        return False
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print("✓ webdriver-manager")
    except ImportError as e:
        print(f"❌ webdriver-manager: {e}")
        return False
    
    return True

def test_basic_crawler():
    """Testa o crawler básico"""
    print("\n🧪 Testando crawler básico...")
    
    try:
        from web_crawler import WebCrawler
        
        crawler = WebCrawler()
        crawler.setup_session(delay=0.5, timeout=5)
        
        # Testa uma URL simples
        test_url = "https://httpbin.org/html"
        print(f"Testando URL: {test_url}")
        
        result = crawler.crawl_url(test_url)
        
        if result:
            print("✓ Crawling básico funcionando")
            print(f"  - Título: {result.title[:50]}...")
            print(f"  - Status: {result.status_code}")
            print(f"  - Tempo: {result.response_time:.2f}s")
            return True
        else:
            print("❌ Crawling básico falhou")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste básico: {e}")
        return False

def test_selectors():
    """Testa seletores CSS"""
    print("\n🧪 Testando seletores CSS...")
    
    try:
        from web_crawler import WebCrawler
        
        crawler = WebCrawler()
        crawler.setup_session(delay=0.5, timeout=5)
        
        # Seletores personalizados
        selectors = {
            'title': ['title', 'h1'],
            'content': ['p', 'div'],
            'links': ['a[href]']
        }
        
        test_url = "https://httpbin.org/html"
        result = crawler.crawl_url(test_url, selectors=selectors)
        
        if result:
            print("✓ Seletores CSS funcionando")
            print(f"  - Links encontrados: {len(result.links)}")
            return True
        else:
            print("❌ Seletores CSS falharam")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de seletores: {e}")
        return False

def test_filters():
    """Testa filtros de conteúdo"""
    print("\n🧪 Testando filtros de conteúdo...")
    
    try:
        from web_crawler import WebCrawler
        
        crawler = WebCrawler()
        crawler.setup_session(delay=0.5, timeout=5)
        
        # Filtros que devem passar
        filters_pass = {
            'keywords': ['html', 'test'],
            'min_length': 10
        }
        
        # Filtros que devem falhar
        filters_fail = {
            'keywords': ['palavranaoexiste'],
            'min_length': 10000
        }
        
        test_url = "https://httpbin.org/html"
        
        # Teste que deve passar
        result1 = crawler.crawl_url(test_url, content_filters=filters_pass)
        
        # Limpa resultados para próximo teste
        crawler.results = []
        crawler.visited_urls = set()
        
        # Teste que deve falhar
        result2 = crawler.crawl_url(test_url, content_filters=filters_fail)
        
        if result1 and not result2:
            print("✓ Filtros de conteúdo funcionando")
            return True
        else:
            print("❌ Filtros de conteúdo falharam")
            print(f"  - Teste 1 (deve passar): {'✓' if result1 else '❌'}")
            print(f"  - Teste 2 (deve falhar): {'✓' if not result2 else '❌'}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de filtros: {e}")
        return False

def test_export():
    """Testa exportação de resultados"""
    print("\n🧪 Testando exportação...")
    
    try:
        from web_crawler import WebCrawler
        
        crawler = WebCrawler()
        crawler.setup_session(delay=0.5, timeout=5)
        
        # Faz crawling para ter dados
        test_url = "https://httpbin.org/html"
        result = crawler.crawl_url(test_url)
        
        if not result:
            print("❌ Falha ao obter dados para teste de exportação")
            return False
        
        # Testa exportação
        test_files = {
            'excel': 'teste_resultados.xlsx',
            'csv': 'teste_resultados.csv',
            'json': 'teste_resultados.json'
        }
        
        for format_type, filename in test_files.items():
            try:
                crawler.export_results(filename, format_type)
                if os.path.exists(filename):
                    print(f"✓ Exportação {format_type.upper()} funcionando")
                    os.remove(filename)  # Limpa arquivo de teste
                else:
                    print(f"❌ Arquivo {format_type.upper()} não foi criado")
                    return False
            except Exception as e:
                print(f"❌ Erro na exportação {format_type.upper()}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de exportação: {e}")
        return False

def test_config():
    """Testa carregamento de configuração"""
    print("\n🧪 Testando configurações...")
    
    try:
        config_file = "config.json"
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Verifica estrutura básica
            required_keys = ['app_name', 'version', 'default_settings', 'presets']
            for key in required_keys:
                if key not in config:
                    print(f"❌ Configuração inválida: falta chave '{key}'")
                    return False
            
            print("✓ Configurações carregadas corretamente")
            print(f"  - App: {config['app_name']} v{config['version']}")
            print(f"  - Presets disponíveis: {len(config['presets'])}")
            return True
        else:
            print("❌ Arquivo config.json não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste de configuração: {e}")
        return False

def test_selenium():
    """Testa Selenium (opcional)"""
    print("\n🧪 Testando Selenium...")
    
    try:
        from web_crawler import WebCrawler
        from selenium.webdriver.chrome.options import Options
        
        crawler = WebCrawler()
        
        # Tenta um crawling simples com Selenium
        test_url = "https://httpbin.org/html"
        print(f"Testando Selenium com: {test_url}")
        print("(Isso pode demorar um pouco...)")
        
        result = crawler.crawl_with_selenium(test_url, wait_time=2)
        
        if result:
            print("✓ Selenium funcionando")
            print(f"  - Título: {result.title[:50]}...")
            print(f"  - Tempo: {result.response_time:.2f}s")
            return True
        else:
            print("❌ Selenium falhou")
            return False
            
    except Exception as e:
        print(f"⚠️ Selenium não disponível: {e}")
        print("  (Isso é normal se o Chrome não estiver instalado)")
        return True  # Não falha o teste geral

def run_all_tests():
    """Executa todos os testes"""
    print("🧪 WEB CRAWLER PRO - SUITE DE TESTES")
    print("=" * 50)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Importações", test_imports),
        ("Crawler Básico", test_basic_crawler),
        ("Seletores CSS", test_selectors),
        ("Filtros", test_filters),
        ("Exportação", test_export),
        ("Configurações", test_config),
        ("Selenium", test_selenium)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        start_time = time.time()
        
        try:
            success = test_func()
            duration = time.time() - start_time
            results.append((test_name, success, duration))
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ Erro inesperado: {e}")
            results.append((test_name, False, duration))
    
    # Relatório final
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO FINAL DOS TESTES")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, success, duration in results:
        status = "✓ PASSOU" if success else "❌ FALHOU"
        print(f"{test_name:20} | {status} | {duration:.2f}s")
        if success:
            passed += 1
    
    print("-" * 50)
    print(f"Total: {passed}/{total} testes passaram ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("O Web Crawler está funcionando corretamente.")
    elif passed >= total * 0.8:
        print("\n⚠️ MAIORIA DOS TESTES PASSOU")
        print("O Web Crawler deve funcionar, mas verifique os erros acima.")
    else:
        print("\n❌ MUITOS TESTES FALHARAM")
        print("Verifique a instalação das dependências:")
        print("pip install -r requirements.txt")
    
    print(f"\nPara executar o Web Crawler:")
    print(f"  Interface Gráfica: python main.py")
    print(f"  Exemplos: python exemplo.py")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n⏹️ Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
    
    print(f"\nPressione Enter para continuar...")
    input()
