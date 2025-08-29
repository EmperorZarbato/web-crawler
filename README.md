# Web Crawler Pro 🕷️

Uma aplicação completa de Web Crawler desenvolvida em Python com interface gráfica moderna e recursos avançados.

## ✨ Características

### 🎯 Interface Gráfica Moderna
- Interface desenvolvida com CustomTkinter
- Design responsivo e intuitivo
- Abas organizadas por funcionalidade
- Tema escuro moderno

### 🔧 Recursos de Crawling
- **HTTP Requests**: Crawling básico com requests + BeautifulSoup
- **JavaScript Support**: Selenium para sites que usam JavaScript
- **Múltiplas URLs**: Processamento em lote
- **Delay configurável**: Controle de velocidade entre requisições
- **Headers personalizados**: User-Agent e headers HTTP customizáveis
- **Proxy Support**: Suporte a proxies HTTP/HTTPS
- **Robots.txt**: Respeita automaticamente o robots.txt

### 🎛️ Filtros e Seletores
- **Seletores CSS**: Configuração personalizável para extração
- **Filtros de conteúdo**: Por palavras-chave, tamanho, regex
- **Presets**: Configurações prontas para e-commerce, blogs, redes sociais
- **Exclusão de conteúdo**: Filtros para remover spam/ads

### 📊 Resultados e Exportação
- **Visualização em tabela**: Resultados organizados e navegáveis
- **Estatísticas detalhadas**: Métricas de performance
- **Exportação múltipla**: Excel, CSV, JSON
- **Sistema de logs**: Rastreamento completo de atividades

## 🚀 Instalação

### 1. Clone ou baixe o projeto
```bash
git clone <url-do-repositorio>
cd Web\ Crawler
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute a aplicação
```bash
# Interface gráfica
python main.py

# Exemplo via linha de comando
python exemplo.py
```

## 📦 Dependências

- `requests` - HTTP requests
- `beautifulsoup4` - Parsing HTML
- `selenium` - JavaScript rendering
- `pandas` - Manipulação de dados
- `customtkinter` - Interface gráfica moderna
- `fake-useragent` - User agents aleatórios
- `webdriver-manager` - Gerenciamento automático do ChromeDriver
- `openpyxl` - Exportação Excel
- `lxml` - Parser XML/HTML rápido

## 🎮 Como Usar

### Interface Gráfica

1. **Configuração Básica**
   - Insira as URLs que deseja fazer crawling
   - Configure delay, timeout e User-Agent
   - Escolha entre crawling normal ou com Selenium

2. **Configurações Avançadas**
   - Headers HTTP personalizados
   - Configurações de proxy
   - JavaScript personalizado para Selenium

3. **Filtros e Seletores**
   - Configure seletores CSS para extração específica
   - Defina filtros por palavras-chave
   - Use presets para diferentes tipos de sites

4. **Execute e Visualize**
   - Clique em "Iniciar Crawling"
   - Acompanhe o progresso em tempo real
   - Visualize resultados e estatísticas
   - Exporte em diferentes formatos

### Uso Programático

```python
from web_crawler import WebCrawler

# Cria crawler
crawler = WebCrawler()

# Configura sessão
crawler.setup_session(delay=1.0, timeout=10)

# Crawling simples
result = crawler.crawl_url("https://example.com")

# Crawling com filtros
selectors = {
    'title': ['h1', 'title'],
    'content': ['article', '.content']
}

filters = {
    'keywords': ['python', 'web'],
    'min_length': 100
}

result = crawler.crawl_url(
    "https://example.com",
    selectors=selectors,
    content_filters=filters
)

# Exporta resultados
crawler.export_results("resultados.xlsx", "excel")
```

## 🏗️ Estrutura do Projeto

```
Web Crawler/
├── main.py              # Aplicação principal (GUI)
├── exemplo.py           # Exemplos de uso
├── web_crawler.py       # Classe principal do crawler
├── crawler_gui.py       # Interface gráfica
├── requirements.txt     # Dependências
├── README.md           # Este arquivo
├── crawler.log         # Logs (criado automaticamente)
└── resultados/         # Diretório para resultados (criado automaticamente)
```

## 🔧 Configurações Avançadas

### Seletores CSS Personalizados
```json
{
  "title": ["h1", ".title", "#title"],
  "description": ["meta[name='description']", ".summary"],
  "content": ["article", ".post-content", "main"],
  "links": ["a[href]"],
  "images": ["img[src]"]
}
```

### Filtros de Conteúdo
```json
{
  "keywords": ["python", "web", "crawling"],
  "exclude_keywords": ["spam", "ads"],
  "min_length": 100,
  "regex": "\\b(python|django|flask)\\b"
}
```

### Headers Personalizados
```json
{
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}
```

## 🎯 Presets Incluídos

### E-commerce
- Foco em produtos, preços e descrições
- Seletores para títulos de produtos e especificações
- Filtros para remover itens fora de estoque

### Blog/Notícias
- Extração de artigos e posts
- Seletores para títulos, resumos e conteúdo principal
- Filtros para remover anúncios

### Redes Sociais
- Perfis e posts de redes sociais
- Seletores para bio, descrições e feeds
- Filtros mínimos para máxima captura

## 🚀 Recursos Futuros

- [ ] Crawling distribuído
- [ ] API REST
- [ ] Mais formatos de exportação
- [ ] Agendamento de crawls
- [ ] Dashboard web
- [ ] Suporte a mais navegadores (Firefox, Edge)
- [ ] Integração com bancos de dados

## 🐛 Solução de Problemas

### Erro de importação do Selenium
```bash
pip install selenium
# Certifique-se de ter o Chrome instalado
```

### Erro de ChromeDriver
O webdriver-manager baixa automaticamente o ChromeDriver, mas certifique-se de ter o Chrome instalado.

### Erro de CustomTkinter
```bash
pip install customtkinter
```

### Sites que não carregam
- Tente usar o modo Selenium para sites com JavaScript
- Verifique se o site permite crawling (robots.txt)
- Ajuste o delay entre requisições

## 📄 Licença

Este projeto é open source. Use livremente para fins educacionais e comerciais.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir melhorias
- Enviar pull requests

---

**Desenvolvido com ❤️ em Python**

*Lembre-se de sempre respeitar o robots.txt dos sites e usar o crawler de forma ética!*
