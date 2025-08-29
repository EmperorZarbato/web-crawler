#!/usr/bin/env python3
"""
Web Crawler Simples - Apenas com bibliotecas padrão
Para testar sem dependências externas
"""

import urllib.request
import urllib.parse
import urllib.error
import html.parser
import json
import time
import re
from datetime import datetime
import os


class SimpleHTMLParser(html.parser.HTMLParser):
    """Parser HTML simples usando apenas bibliotecas padrão"""
    
    def __init__(self):
        super().__init__()
        self.title = ""
        self.links = []
        self.images = []
        self.text_content = []
        self.in_title = False
        self.in_body = False
    
    def handle_starttag(self, tag, attrs):
        if tag == 'title':
            self.in_title = True
        elif tag == 'body':
            self.in_body = True
        elif tag == 'a':
            for attr_name, attr_value in attrs:
                if attr_name == 'href' and attr_value:
                    self.links.append(attr_value)
        elif tag == 'img':
            for attr_name, attr_value in attrs:
                if attr_name == 'src' and attr_value:
                    self.images.append(attr_value)
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'body':
            self.in_body = False
    
    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()
        elif self.in_body:
            clean_text = data.strip()
            if clean_text:
                self.text_content.append(clean_text)


class SimpleCrawler:
    """Web Crawler simples usando apenas bibliotecas padrão do Python"""
    
    def __init__(self):
        self.results = []
        self.visited_urls = set()
        self.user_agent = "SimpleCrawler/1.0 (Python)"
    
    def crawl_url(self, url, delay=1.0, timeout=10):
        """Faz crawling de uma URL"""
        try:
            # Evita URLs duplicadas
            if url in self.visited_urls:
                print(f"URL já visitada: {url}")
                return None
            
            self.visited_urls.add(url)
            
            # Delay entre requisições
            if delay > 0:
                time.sleep(delay)
            
            print(f"Fazendo crawling: {url}")
            
            # Cria a requisição
            req = urllib.request.Request(
                url,
                headers={
                    'User-Agent': self.user_agent,
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8'
                }
            )
            
            # Faz a requisição
            start_time = time.time()
            with urllib.request.urlopen(req, timeout=timeout) as response:
                response_time = time.time() - start_time
                status_code = response.getcode()
                
                # Lê o conteúdo
                content = response.read()
                
                # Detecta encoding
                encoding = 'utf-8'
                if response.headers.get_content_charset():
                    encoding = response.headers.get_content_charset()
                
                html_content = content.decode(encoding, errors='ignore')
            
            # Parse do HTML
            parser = SimpleHTMLParser()
            parser.feed(html_content)
            
            # Cria resultado
            result = {
                'url': url,
                'title': parser.title or 'Sem título',
                'content': ' '.join(parser.text_content[:10]),  # Primeiras 10 partes de texto
                'links': list(set(parser.links)),  # Remove duplicatas
                'images': list(set(parser.images)),
                'status_code': status_code,
                'response_time': round(response_time, 2),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'content_length': len(html_content)
            }
            
            self.results.append(result)
            
            print(f"✓ Sucesso: {result['title'][:50]}...")
            print(f"  Status: {status_code}, Tempo: {response_time:.2f}s")
            print(f"  Links: {len(result['links'])}, Imagens: {len(result['images'])}")
            
            return result
            
        except urllib.error.HTTPError as e:
            print(f"❌ Erro HTTP {e.code}: {url}")
            return None
        except urllib.error.URLError as e:
            print(f"❌ Erro de URL: {e.reason}")
            return None
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            return None
    
    def crawl_multiple_urls(self, urls, delay=1.0, timeout=10):
        """Faz crawling de múltiplas URLs"""
        results = []
        total = len(urls)
        
        print(f"🕷️ Iniciando crawling de {total} URLs...")
        print("=" * 50)
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{total}] ", end="")
            result = self.crawl_url(url, delay, timeout)
            if result:
                results.append(result)
        
        return results
    
    def save_results_json(self, filename="resultados_simples.json"):
        """Salva resultados em JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Resultados salvos em: {filename}")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
            return False
    
    def show_statistics(self):
        """Mostra estatísticas dos resultados"""
        if not self.results:
            print("Nenhum resultado disponível.")
            return
        
        total_results = len(self.results)
        avg_response_time = sum(r['response_time'] for r in self.results) / total_results
        total_links = sum(len(r['links']) for r in self.results)
        total_images = sum(len(r['images']) for r in self.results)
        
        print(f"\n📊 ESTATÍSTICAS DO CRAWLING")
        print("=" * 30)
        print(f"Total de páginas: {total_results}")
        print(f"Tempo médio de resposta: {avg_response_time:.2f}s")
        print(f"Total de links encontrados: {total_links}")
        print(f"Total de imagens encontradas: {total_images}")
        print(f"URLs visitadas: {len(self.visited_urls)}")
        
        # Status codes
        status_codes = {}
        for result in self.results:
            code = result['status_code']
            status_codes[code] = status_codes.get(code, 0) + 1
        
        print(f"\nStatus Codes:")
        for code, count in status_codes.items():
            print(f"  {code}: {count} páginas")
    
    def filter_results(self, keyword=None, min_links=0, min_images=0):
        """Filtra resultados por critérios"""
        filtered = []
        
        for result in self.results:
            # Filtro por palavra-chave
            if keyword:
                text_to_search = f"{result['title']} {result['content']}".lower()
                if keyword.lower() not in text_to_search:
                    continue
            
            # Filtro por número mínimo de links
            if len(result['links']) < min_links:
                continue
            
            # Filtro por número mínimo de imagens
            if len(result['images']) < min_images:
                continue
            
            filtered.append(result)
        
        return filtered


def demonstracao():
    """Demonstração do crawler simples"""
    print("🕷️ WEB CRAWLER SIMPLES - DEMONSTRAÇÃO")
    print("Usando apenas bibliotecas padrão do Python")
    print("=" * 50)
    
    # Cria crawler
    crawler = SimpleCrawler()
    
    # URLs para testar
    test_urls = [
        "https://httpbin.org/html",
        "https://example.com",
        "https://www.python.org",
        "https://github.com"
    ]
    
    print(f"URLs para teste: {len(test_urls)}")
    for i, url in enumerate(test_urls, 1):
        print(f"  {i}. {url}")
    
    # Faz crawling
    results = crawler.crawl_multiple_urls(test_urls, delay=0.5, timeout=10)
    
    # Mostra estatísticas
    crawler.show_statistics()
    
    # Salva resultados
    crawler.save_results_json()
    
    # Exemplo de filtros
    print(f"\n🔍 EXEMPLOS DE FILTROS:")
    
    # Filtrar por palavra-chave
    python_results = crawler.filter_results(keyword="python")
    print(f"Páginas com 'python': {len(python_results)}")
    
    # Filtrar por links
    link_rich_results = crawler.filter_results(min_links=5)
    print(f"Páginas com 5+ links: {len(link_rich_results)}")
    
    # Mostrar alguns resultados detalhados
    print(f"\n📋 DETALHES DOS RESULTADOS:")
    for i, result in enumerate(results[:3], 1):  # Mostra apenas os primeiros 3
        print(f"\n--- Resultado {i} ---")
        print(f"URL: {result['url']}")
        print(f"Título: {result['title']}")
        print(f"Conteúdo: {result['content'][:100]}...")
        print(f"Links: {len(result['links'])}")
        print(f"Imagens: {len(result['images'])}")
        print(f"Status: {result['status_code']}")
        print(f"Tempo: {result['response_time']}s")
    
    print(f"\n🎉 Demonstração concluída!")
    print(f"Arquivo de resultados: resultados_simples.json")
    
    return crawler


if __name__ == "__main__":
    try:
        crawler = demonstracao()
        
        print(f"\n" + "=" * 50)
        print(f"CRAWLER SIMPLES EXECUTADO COM SUCESSO!")
        print(f"Para usar a versão completa com interface gráfica,")
        print(f"certifique-se de instalar as dependências:")
        print(f"pip install -r requirements.txt")
        print(f"python main.py")
        
    except KeyboardInterrupt:
        print(f"\n\n⏹️ Execução interrompida pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
