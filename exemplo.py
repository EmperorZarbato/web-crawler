#!/usr/bin/env python3
"""
Exemplo Simples de Uso do Web Crawler
Para casos onde você não precisa da interface gráfica
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_crawler import WebCrawler
import json

def exemplo_basico():
    """Exemplo básico de crawling"""
    print("🕷️ Exemplo Básico de Web Crawling")
    print("=" * 50)
    
    # Cria instância do crawler
    crawler = WebCrawler()
    
    # Configura sessão básica
    crawler.setup_session(delay=1.0, timeout=10)
    
    # URLs para testar
    urls = [
        "https://httpbin.org/html",
        "https://quotes.toscrape.com",
        "https://example.com"
    ]
    
    print(f"Fazendo crawling de {len(urls)} URLs...\n")
    
    # Faz crawling
    results = crawler.crawl_multiple_urls(urls)
    
    # Mostra resultados
    print(f"\n✅ Crawling concluído! {len(results)} páginas processadas.")
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Resultado {i} ---")
        print(f"URL: {result.url}")
        print(f"Título: {result.title}")
        print(f"Descrição: {result.description[:100]}..." if result.description else "Descrição: N/A")
        print(f"Status: {result.status_code}")
        print(f"Tempo: {result.response_time:.2f}s")
        print(f"Links encontrados: {len(result.links)}")
        print(f"Imagens encontradas: {len(result.images)}")
    
    # Estatísticas
    stats = crawler.get_statistics()
    print(f"\n📊 Estatísticas:")
    print(f"Total de páginas: {stats['total_pages']}")
    print(f"Tempo médio: {stats['average_response_time']}s")
    print(f"Total de links: {stats['total_links_found']}")
    print(f"Total de imagens: {stats['total_images_found']}")
    
    # Exporta resultados
    print(f"\n💾 Exportando resultados...")
    crawler.export_results("exemplo_resultados.xlsx", "excel")
    crawler.export_results("exemplo_resultados.csv", "csv")
    crawler.export_results("exemplo_resultados.json", "json")
    print("Arquivos exportados: exemplo_resultados.xlsx, .csv, .json")

def exemplo_avancado():
    """Exemplo com filtros e seletores personalizados"""
    print("\n🔧 Exemplo Avançado com Filtros")
    print("=" * 50)
    
    crawler = WebCrawler()
    
    # Headers personalizados
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"
    }
    
    crawler.setup_session(headers=headers, delay=0.5)
    
    # Seletores CSS personalizados
    selectors = {
        'title': ['h1', 'title', '.title'],
        'description': ['meta[name="description"]', '.description'],
        'content': ['article', '.content', 'main', 'p'],
        'links': ['a[href]'],
        'images': ['img[src]']
    }
    
    # Filtros de conteúdo
    filters = {
        'keywords': ['python', 'web', 'quotes'],  # Deve conter pelo menos uma
        'min_length': 50,  # Conteúdo mínimo
        'exclude_keywords': ['spam', 'ads']  # Excluir se contiver
    }
    
    # URL de exemplo
    url = "https://quotes.toscrape.com"
    
    print(f"Fazendo crawling de: {url}")
    print(f"Com seletores: {selectors}")
    print(f"Com filtros: {filters}")
    
    result = crawler.crawl_url(
        url, 
        selectors=selectors, 
        content_filters=filters,
        respect_robots=True
    )
    
    if result:
        print(f"\n✅ Sucesso!")
        print(f"Título: {result.title}")
        print(f"Conteúdo (primeiros 200 chars): {result.content[:200]}...")
        print(f"Links: {len(result.links)}")
        print(f"Imagens: {len(result.images)}")
    else:
        print(f"\n❌ Nenhum resultado (possivelmente filtrado)")

def exemplo_selenium():
    """Exemplo usando Selenium para sites com JavaScript"""
    print("\n🌐 Exemplo com Selenium (JavaScript)")
    print("=" * 50)
    
    try:
        crawler = WebCrawler()
        
        # URL que requer JavaScript
        url = "https://quotes.toscrape.com/js/"
        
        print(f"Fazendo crawling com Selenium: {url}")
        print("Aguardando carregamento do JavaScript...")
        
        # JavaScript personalizado para executar
        js_code = "window.scrollTo(0, document.body.scrollHeight);"
        
        result = crawler.crawl_with_selenium(
            url, 
            wait_time=3,
            execute_js=js_code
        )
        
        if result:
            print(f"\n✅ Crawling com JavaScript bem-sucedido!")
            print(f"Título: {result.title}")
            print(f"Conteúdo encontrado: {len(result.content)} caracteres")
            print(f"Links: {len(result.links)}")
        else:
            print(f"\n❌ Falha no crawling com Selenium")
            
    except Exception as e:
        print(f"\n⚠️ Erro no Selenium: {e}")
        print("Certifique-se de ter o Chrome instalado e selenium configurado")

if __name__ == "__main__":
    try:
        # Executa exemplos
        exemplo_basico()
        exemplo_avancado()
        exemplo_selenium()
        
        print(f"\n🎉 Todos os exemplos executados!")
        print(f"Verifique os arquivos de resultado gerados.")
        print(f"\nPara usar a interface gráfica, execute: python main.py")
        
    except KeyboardInterrupt:
        print(f"\n\n⏹️ Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print(f"Certifique-se de instalar as dependências: pip install -r requirements.txt")
