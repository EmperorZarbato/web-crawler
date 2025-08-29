import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import pandas as pd
import time
import re
import urllib.parse
from urllib.robotparser import RobotFileParser
from typing import List, Dict, Optional
import json
import logging
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CrawlResult:
    """Classe para armazenar resultados do crawling"""
    url: str
    title: str
    description: str
    content: str
    links: List[str]
    images: List[str]
    timestamp: datetime
    status_code: int
    response_time: float


class WebCrawler:
    """Classe principal do Web Crawler com recursos avançados"""
    
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.results = []
        self.visited_urls = set()
        self.setup_logging()
        
    def setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(
            filename='crawler.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_session(self, headers: Dict = None, proxies: Dict = None, 
                     timeout: int = 10, delay: float = 1.0):
        """Configura a sessão HTTP com headers e proxies personalizados"""
        if headers:
            self.session.headers.update(headers)
        else:
            self.session.headers.update({
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            })
        
        if proxies:
            self.session.proxies.update(proxies)
        
        self.timeout = timeout
        self.delay = delay
    
    def check_robots_txt(self, url: str, user_agent: str = '*') -> bool:
        """Verifica se é permitido fazer crawling baseado no robots.txt"""
        try:
            base_url = urllib.parse.urljoin(url, '/')
            robots_url = urllib.parse.urljoin(base_url, '/robots.txt')
            
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            return rp.can_fetch(user_agent, url)
        except:
            return True  # Se não conseguir verificar, permite por padrão
    
    def extract_content(self, soup: BeautifulSoup, selectors: Dict) -> Dict:
        """Extrai conteúdo baseado em seletores CSS personalizados"""
        content = {}
        
        # Título
        title_selectors = selectors.get('title', ['title', 'h1', '.title', '#title'])
        title = self._extract_by_selectors(soup, title_selectors)
        content['title'] = title
        
        # Descrição
        desc_selectors = selectors.get('description', [
            'meta[name="description"]', 
            '.description', 
            '.summary',
            'p:first-of-type'
        ])
        description = self._extract_by_selectors(soup, desc_selectors)
        content['description'] = description
        
        # Conteúdo principal
        content_selectors = selectors.get('content', [
            'article', 
            '.content', 
            '.post-content',
            '.entry-content',
            'main',
            '#content'
        ])
        main_content = self._extract_by_selectors(soup, content_selectors)
        content['content'] = main_content
        
        # Links
        links = []
        link_selectors = selectors.get('links', ['a[href]'])
        for selector in link_selectors:
            elements = soup.select(selector)
            for element in elements:
                href = element.get('href')
                if href:
                    links.append(href)
        content['links'] = list(set(links))  # Remove duplicatas
        
        # Imagens
        images = []
        img_selectors = selectors.get('images', ['img[src]'])
        for selector in img_selectors:
            elements = soup.select(selector)
            for element in elements:
                src = element.get('src')
                if src:
                    images.append(src)
        content['images'] = list(set(images))
        
        return content
    
    def _extract_by_selectors(self, soup: BeautifulSoup, selectors: List[str]) -> str:
        """Extrai texto usando uma lista de seletores CSS"""
        for selector in selectors:
            try:
                if selector.startswith('meta'):
                    element = soup.select_one(selector)
                    if element:
                        return element.get('content', '')
                else:
                    element = soup.select_one(selector)
                    if element:
                        return element.get_text(strip=True)
            except:
                continue
        return ""
    
    def filter_content(self, content: str, filters: Dict) -> bool:
        """Aplica filtros de conteúdo"""
        if not filters:
            return True
        
        # Filtro por palavras-chave
        keywords = filters.get('keywords', [])
        if keywords:
            content_lower = content.lower()
            if not any(keyword.lower() in content_lower for keyword in keywords):
                return False
        
        # Filtro por tamanho mínimo
        min_length = filters.get('min_length', 0)
        if len(content) < min_length:
            return False
        
        # Filtro por expressão regular
        regex_pattern = filters.get('regex')
        if regex_pattern:
            if not re.search(regex_pattern, content, re.IGNORECASE):
                return False
        
        # Filtro de exclusão
        exclude_keywords = filters.get('exclude_keywords', [])
        if exclude_keywords:
            content_lower = content.lower()
            if any(keyword.lower() in content_lower for keyword in exclude_keywords):
                return False
        
        return True
    
    def crawl_url(self, url: str, selectors: Dict = None, 
                  content_filters: Dict = None, respect_robots: bool = True) -> Optional[CrawlResult]:
        """Faz crawling de uma URL específica"""
        try:
            # Verifica robots.txt
            if respect_robots and not self.check_robots_txt(url):
                self.logger.warning(f"Crawling não permitido pelo robots.txt: {url}")
                return None
            
            # Evita URLs duplicadas
            if url in self.visited_urls:
                return None
            
            self.visited_urls.add(url)
            
            # Delay entre requisições
            time.sleep(self.delay)
            
            # Faz a requisição
            start_time = time.time()
            response = self.session.get(url, timeout=self.timeout)
            response_time = time.time() - start_time
            
            response.raise_for_status()
            
            # Parse do HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extrai conteúdo
            if selectors is None:
                selectors = {}
            
            extracted_content = self.extract_content(soup, selectors)
            
            # Aplica filtros
            if content_filters:
                full_content = f"{extracted_content['title']} {extracted_content['description']} {extracted_content['content']}"
                if not self.filter_content(full_content, content_filters):
                    return None
            
            # Cria resultado
            result = CrawlResult(
                url=url,
                title=extracted_content['title'],
                description=extracted_content['description'],
                content=extracted_content['content'],
                links=extracted_content['links'],
                images=extracted_content['images'],
                timestamp=datetime.now(),
                status_code=response.status_code,
                response_time=response_time
            )
            
            self.results.append(result)
            self.logger.info(f"Crawling bem-sucedido: {url}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao fazer crawling de {url}: {str(e)}")
            return None
    
    def crawl_multiple_urls(self, urls: List[str], **kwargs) -> List[CrawlResult]:
        """Faz crawling de múltiplas URLs"""
        results = []
        total_urls = len(urls)
        
        for i, url in enumerate(urls, 1):
            print(f"Processando {i}/{total_urls}: {url}")
            result = self.crawl_url(url, **kwargs)
            if result:
                results.append(result)
        
        return results
    
    def crawl_with_selenium(self, url: str, wait_time: int = 3, 
                           execute_js: str = None) -> Optional[CrawlResult]:
        """Faz crawling usando Selenium para sites com JavaScript"""
        try:
            # Configura o Chrome
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument(f'--user-agent={self.ua.random}')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            try:
                start_time = time.time()
                driver.get(url)
                
                # Aguarda carregar
                time.sleep(wait_time)
                
                # Executa JavaScript personalizado se fornecido
                if execute_js:
                    driver.execute_script(execute_js)
                    time.sleep(1)
                
                response_time = time.time() - start_time
                
                # Obtém o HTML renderizado
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extrai conteúdo
                extracted_content = self.extract_content(soup, {})
                
                result = CrawlResult(
                    url=url,
                    title=extracted_content['title'],
                    description=extracted_content['description'],
                    content=extracted_content['content'],
                    links=extracted_content['links'],
                    images=extracted_content['images'],
                    timestamp=datetime.now(),
                    status_code=200,
                    response_time=response_time
                )
                
                self.results.append(result)
                return result
                
            finally:
                driver.quit()
                
        except Exception as e:
            self.logger.error(f"Erro no crawling com Selenium: {str(e)}")
            return None
    
    def export_results(self, filename: str, format: str = 'excel'):
        """Exporta os resultados para diferentes formatos"""
        if not self.results:
            print("Nenhum resultado para exportar.")
            return
        
        # Converte resultados para DataFrame
        data = []
        for result in self.results:
            data.append({
                'URL': result.url,
                'Título': result.title,
                'Descrição': result.description,
                'Conteúdo': result.content[:500] + '...' if len(result.content) > 500 else result.content,
                'Número de Links': len(result.links),
                'Número de Imagens': len(result.images),
                'Status Code': result.status_code,
                'Tempo de Resposta (s)': round(result.response_time, 2),
                'Timestamp': result.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        df = pd.DataFrame(data)
        
        if format.lower() == 'excel':
            df.to_excel(filename, index=False)
        elif format.lower() == 'csv':
            df.to_csv(filename, index=False, encoding='utf-8')
        elif format.lower() == 'json':
            df.to_json(filename, orient='records', indent=2, force_ascii=False)
        
        print(f"Resultados exportados para: {filename}")
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas dos resultados"""
        if not self.results:
            return {}
        
        total_results = len(self.results)
        avg_response_time = sum(r.response_time for r in self.results) / total_results
        total_links = sum(len(r.links) for r in self.results)
        total_images = sum(len(r.images) for r in self.results)
        
        status_codes = {}
        for result in self.results:
            status_codes[result.status_code] = status_codes.get(result.status_code, 0) + 1
        
        return {
            'total_pages': total_results,
            'average_response_time': round(avg_response_time, 2),
            'total_links_found': total_links,
            'total_images_found': total_images,
            'status_codes': status_codes,
            'total_urls_visited': len(self.visited_urls)
        }
