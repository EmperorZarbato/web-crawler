import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import threading
import json
import os
from datetime import datetime
from web_crawler import WebCrawler
import webbrowser


class CrawlerGUI:
    """Interface gráfica moderna para o Web Crawler"""
    
    def __init__(self):
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Janela principal
        self.root = ctk.CTk()
        self.root.title("Web Crawler Pro - Python")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Instância do crawler
        self.crawler = WebCrawler()
        self.crawl_thread = None
        self.is_crawling = False
        
        # Variáveis
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Pronto")
        
        self.setup_ui()
        self.load_config()
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🕷️ Web Crawler Pro", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Notebook para abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Aba 1: Configuração Básica
        self.setup_basic_tab()
        
        # Aba 2: Configurações Avançadas
        self.setup_advanced_tab()
        
        # Aba 3: Filtros e Seletores
        self.setup_filters_tab()
        
        # Aba 4: Resultados
        self.setup_results_tab()
        
        # Frame inferior com controles
        self.setup_control_frame(main_frame)
    
    def setup_basic_tab(self):
        """Configura a aba de configuração básica"""
        basic_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(basic_frame, text="📋 Configuração Básica")
        
        # URLs para crawling
        urls_label = ctk.CTkLabel(basic_frame, text="URLs para Crawling:", font=ctk.CTkFont(size=16, weight="bold"))
        urls_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        self.urls_text = ctk.CTkTextbox(basic_frame, height=150)
        self.urls_text.pack(fill="x", padx=20, pady=(0, 10))
        self.urls_text.insert("1.0", "https://example.com\nhttps://httpbin.org/html\nhttps://quotes.toscrape.com")
        
        # Frame para configurações em duas colunas
        config_frame = ctk.CTkFrame(basic_frame)
        config_frame.pack(fill="x", padx=20, pady=10)
        
        # Coluna esquerda
        left_frame = ctk.CTkFrame(config_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        # Delay entre requisições
        ctk.CTkLabel(left_frame, text="Delay entre requisições (s):").pack(anchor="w", padx=10, pady=(10, 0))
        self.delay_var = tk.DoubleVar(value=1.0)
        self.delay_scale = ctk.CTkSlider(left_frame, from_=0.1, to=5.0, variable=self.delay_var)
        self.delay_scale.pack(fill="x", padx=10, pady=5)
        self.delay_label = ctk.CTkLabel(left_frame, text="1.0s")
        self.delay_label.pack(anchor="w", padx=10)
        self.delay_scale.configure(command=self.update_delay_label)
        
        # Timeout
        ctk.CTkLabel(left_frame, text="Timeout (s):").pack(anchor="w", padx=10, pady=(10, 0))
        self.timeout_var = tk.IntVar(value=10)
        self.timeout_entry = ctk.CTkEntry(left_frame, textvariable=self.timeout_var)
        self.timeout_entry.pack(fill="x", padx=10, pady=5)
        
        # Coluna direita
        right_frame = ctk.CTkFrame(config_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        # User Agent personalizado
        ctk.CTkLabel(right_frame, text="User Agent:").pack(anchor="w", padx=10, pady=(10, 0))
        self.user_agent_var = tk.StringVar(value="Automático")
        self.user_agent_combo = ctk.CTkComboBox(
            right_frame,
            values=["Automático", "Chrome Desktop", "Firefox Desktop", "Safari Mobile", "Custom"],
            variable=self.user_agent_var
        )
        self.user_agent_combo.pack(fill="x", padx=10, pady=5)
        
        # Checkboxes
        self.respect_robots_var = tk.BooleanVar(value=True)
        self.respect_robots_cb = ctk.CTkCheckBox(
            right_frame, 
            text="Respeitar robots.txt", 
            variable=self.respect_robots_var
        )
        self.respect_robots_cb.pack(anchor="w", padx=10, pady=5)
        
        self.use_selenium_var = tk.BooleanVar(value=False)
        self.use_selenium_cb = ctk.CTkCheckBox(
            right_frame, 
            text="Usar Selenium (para JS)", 
            variable=self.use_selenium_var
        )
        self.use_selenium_cb.pack(anchor="w", padx=10, pady=5)
    
    def setup_advanced_tab(self):
        """Configura a aba de configurações avançadas"""
        advanced_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(advanced_frame, text="⚙️ Avançado")
        
        # Headers personalizados
        headers_label = ctk.CTkLabel(advanced_frame, text="Headers HTTP Personalizados (JSON):", font=ctk.CTkFont(size=16, weight="bold"))
        headers_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        self.headers_text = ctk.CTkTextbox(advanced_frame, height=100)
        self.headers_text.pack(fill="x", padx=20, pady=(0, 10))
        self.headers_text.insert("1.0", '{\n  "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"\n}')
        
        # Proxies
        proxy_label = ctk.CTkLabel(advanced_frame, text="Configurações de Proxy:", font=ctk.CTkFont(size=16, weight="bold"))
        proxy_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        proxy_frame = ctk.CTkFrame(advanced_frame)
        proxy_frame.pack(fill="x", padx=20, pady=10)
        
        # HTTP Proxy
        ctk.CTkLabel(proxy_frame, text="HTTP Proxy:").pack(anchor="w", padx=10, pady=(10, 0))
        self.http_proxy_var = tk.StringVar()
        self.http_proxy_entry = ctk.CTkEntry(proxy_frame, textvariable=self.http_proxy_var, placeholder_text="http://proxy:port")
        self.http_proxy_entry.pack(fill="x", padx=10, pady=5)
        
        # HTTPS Proxy
        ctk.CTkLabel(proxy_frame, text="HTTPS Proxy:").pack(anchor="w", padx=10, pady=(5, 0))
        self.https_proxy_var = tk.StringVar()
        self.https_proxy_entry = ctk.CTkEntry(proxy_frame, textvariable=self.https_proxy_var, placeholder_text="https://proxy:port")
        self.https_proxy_entry.pack(fill="x", padx=10, pady=(5, 10))
        
        # JavaScript personalizado para Selenium
        js_label = ctk.CTkLabel(advanced_frame, text="JavaScript Personalizado (Selenium):", font=ctk.CTkFont(size=16, weight="bold"))
        js_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        self.js_text = ctk.CTkTextbox(advanced_frame, height=80)
        self.js_text.pack(fill="x", padx=20, pady=(0, 10))
        self.js_text.insert("1.0", "// Exemplo: scroll para baixo\n// window.scrollTo(0, document.body.scrollHeight);")
        
        # Tempo de espera do Selenium
        selenium_frame = ctk.CTkFrame(advanced_frame)
        selenium_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(selenium_frame, text="Tempo de espera Selenium (s):").pack(side="left", padx=10, pady=10)
        self.selenium_wait_var = tk.IntVar(value=3)
        self.selenium_wait_entry = ctk.CTkEntry(selenium_frame, textvariable=self.selenium_wait_var, width=100)
        self.selenium_wait_entry.pack(side="left", padx=10, pady=10)
    
    def setup_filters_tab(self):
        """Configura a aba de filtros e seletores"""
        filters_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(filters_frame, text="🔍 Filtros & Seletores")
        
        # Frame principal com scroll
        canvas_frame = ctk.CTkScrollableFrame(filters_frame)
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Seletores CSS
        selectors_label = ctk.CTkLabel(canvas_frame, text="Seletores CSS Personalizados:", font=ctk.CTkFont(size=16, weight="bold"))
        selectors_label.pack(anchor="w", pady=(0, 10))
        
        # Seletor de título
        ctk.CTkLabel(canvas_frame, text="Título:").pack(anchor="w", pady=(5, 0))
        self.title_selector_var = tk.StringVar(value="title, h1, .title, #title")
        self.title_selector_entry = ctk.CTkEntry(canvas_frame, textvariable=self.title_selector_var)
        self.title_selector_entry.pack(fill="x", pady=(0, 5))
        
        # Seletor de descrição
        ctk.CTkLabel(canvas_frame, text="Descrição:").pack(anchor="w", pady=(5, 0))
        self.desc_selector_var = tk.StringVar(value='meta[name="description"], .description, .summary')
        self.desc_selector_entry = ctk.CTkEntry(canvas_frame, textvariable=self.desc_selector_var)
        self.desc_selector_entry.pack(fill="x", pady=(0, 5))
        
        # Seletor de conteúdo
        ctk.CTkLabel(canvas_frame, text="Conteúdo Principal:").pack(anchor="w", pady=(5, 0))
        self.content_selector_var = tk.StringVar(value="article, .content, .post-content, main")
        self.content_selector_entry = ctk.CTkEntry(canvas_frame, textvariable=self.content_selector_var)
        self.content_selector_entry.pack(fill="x", pady=(0, 10))
        
        # Filtros de conteúdo
        filters_label = ctk.CTkLabel(canvas_frame, text="Filtros de Conteúdo:", font=ctk.CTkFont(size=16, weight="bold"))
        filters_label.pack(anchor="w", pady=(20, 10))
        
        # Palavras-chave obrigatórias
        ctk.CTkLabel(canvas_frame, text="Palavras-chave obrigatórias (separadas por vírgula):").pack(anchor="w", pady=(5, 0))
        self.keywords_var = tk.StringVar()
        self.keywords_entry = ctk.CTkEntry(canvas_frame, textvariable=self.keywords_var, placeholder_text="python, web, crawling")
        self.keywords_entry.pack(fill="x", pady=(0, 5))
        
        # Palavras-chave de exclusão
        ctk.CTkLabel(canvas_frame, text="Palavras-chave de exclusão:").pack(anchor="w", pady=(5, 0))
        self.exclude_keywords_var = tk.StringVar()
        self.exclude_keywords_entry = ctk.CTkEntry(canvas_frame, textvariable=self.exclude_keywords_var, placeholder_text="spam, ads, advertisement")
        self.exclude_keywords_entry.pack(fill="x", pady=(0, 5))
        
        # Tamanho mínimo do conteúdo
        ctk.CTkLabel(canvas_frame, text="Tamanho mínimo do conteúdo (caracteres):").pack(anchor="w", pady=(5, 0))
        self.min_length_var = tk.IntVar(value=100)
        self.min_length_entry = ctk.CTkEntry(canvas_frame, textvariable=self.min_length_var)
        self.min_length_entry.pack(fill="x", pady=(0, 5))
        
        # Expressão regular
        ctk.CTkLabel(canvas_frame, text="Filtro por Regex (opcional):").pack(anchor="w", pady=(5, 0))
        self.regex_var = tk.StringVar()
        self.regex_entry = ctk.CTkEntry(canvas_frame, textvariable=self.regex_var, placeholder_text=r"\b(python|django|flask)\b")
        self.regex_entry.pack(fill="x", pady=(0, 10))
        
        # Botões de preset
        preset_frame = ctk.CTkFrame(canvas_frame)
        preset_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(preset_frame, text="Presets:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=10, pady=(10, 5))
        
        preset_buttons_frame = ctk.CTkFrame(preset_frame)
        preset_buttons_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkButton(preset_buttons_frame, text="E-commerce", command=self.load_ecommerce_preset, width=100).pack(side="left", padx=5)
        ctk.CTkButton(preset_buttons_frame, text="Blog/Notícias", command=self.load_blog_preset, width=100).pack(side="left", padx=5)
        ctk.CTkButton(preset_buttons_frame, text="Redes Sociais", command=self.load_social_preset, width=100).pack(side="left", padx=5)
        ctk.CTkButton(preset_buttons_frame, text="Limpar", command=self.clear_filters, width=100).pack(side="left", padx=5)
    
    def setup_results_tab(self):
        """Configura a aba de resultados"""
        results_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(results_frame, text="📊 Resultados")
        
        # Frame superior com estatísticas
        stats_frame = ctk.CTkFrame(results_frame)
        stats_frame.pack(fill="x", padx=20, pady=20)
        
        self.stats_label = ctk.CTkLabel(stats_frame, text="Estatísticas aparecerão aqui após o crawling", font=ctk.CTkFont(size=14))
        self.stats_label.pack(pady=20)
        
        # Frame dos resultados
        results_content_frame = ctk.CTkFrame(results_frame)
        results_content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Treeview para mostrar resultados
        columns = ("URL", "Título", "Status", "Tempo (s)", "Links", "Imagens")
        self.results_tree = ttk.Treeview(results_content_frame, columns=columns, show="headings", height=15)
        
        # Configurar colunas
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(results_content_frame, orient="vertical", command=self.results_tree.yview)
        h_scrollbar = ttk.Scrollbar(results_content_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack dos componentes
        self.results_tree.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
        v_scrollbar.pack(side="right", fill="y", pady=20)
        h_scrollbar.pack(side="bottom", fill="x", padx=20)
        
        # Frame de exportação
        export_frame = ctk.CTkFrame(results_frame)
        export_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(export_frame, text="Exportar Resultados:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=10)
        
        ctk.CTkButton(export_frame, text="Excel", command=lambda: self.export_results('excel'), width=80).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(export_frame, text="CSV", command=lambda: self.export_results('csv'), width=80).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(export_frame, text="JSON", command=lambda: self.export_results('json'), width=80).pack(side="left", padx=5, pady=10)
        
        # Bind para duplo clique
        self.results_tree.bind("<Double-1>", self.on_result_double_click)
    
    def setup_control_frame(self, parent):
        """Configura o frame de controles inferior"""
        control_frame = ctk.CTkFrame(parent)
        control_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        # Frame esquerdo com status
        status_frame = ctk.CTkFrame(control_frame)
        status_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        self.status_label = ctk.CTkLabel(status_frame, textvariable=self.status_var, font=ctk.CTkFont(size=12))
        self.status_label.pack(anchor="w", padx=10, pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(status_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=(0, 10))
        self.progress_bar.set(0)
        
        # Frame direito com botões
        buttons_frame = ctk.CTkFrame(control_frame)
        buttons_frame.pack(side="right", padx=(5, 10), pady=10)
        
        self.start_button = ctk.CTkButton(
            buttons_frame, 
            text="🚀 Iniciar Crawling", 
            command=self.start_crawling,
            font=ctk.CTkFont(size=14, weight="bold"),
            width=150,
            height=40
        )
        self.start_button.pack(side="left", padx=5, pady=10)
        
        self.stop_button = ctk.CTkButton(
            buttons_frame, 
            text="⏹️ Parar", 
            command=self.stop_crawling,
            width=100,
            height=40,
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5, pady=10)
        
        self.config_button = ctk.CTkButton(
            buttons_frame, 
            text="💾 Salvar Config", 
            command=self.save_config,
            width=120,
            height=40
        )
        self.config_button.pack(side="left", padx=5, pady=10)
    
    def update_delay_label(self, value):
        """Atualiza o label do delay"""
        self.delay_label.configure(text=f"{float(value):.1f}s")
    
    def load_ecommerce_preset(self):
        """Carrega preset para e-commerce"""
        self.title_selector_var.set("h1, .product-title, .title, title")
        self.desc_selector_var.set(".product-description, .description, .summary")
        self.content_selector_var.set(".product-details, .product-info, .specifications")
        self.keywords_var.set("price, buy, product, shop")
        self.exclude_keywords_var.set("out of stock, unavailable")
        self.min_length_var.set(50)
    
    def load_blog_preset(self):
        """Carrega preset para blogs/notícias"""
        self.title_selector_var.set("h1, .post-title, .article-title, title")
        self.desc_selector_var.set(".excerpt, .summary, meta[name='description']")
        self.content_selector_var.set("article, .post-content, .entry-content, .article-body")
        self.keywords_var.set("article, post, news")
        self.exclude_keywords_var.set("advertisement, ads, spam")
        self.min_length_var.set(200)
    
    def load_social_preset(self):
        """Carrega preset para redes sociais"""
        self.title_selector_var.set("h1, .title, .post-title")
        self.desc_selector_var.set(".bio, .description, .about")
        self.content_selector_var.set(".post, .content, .feed-item")
        self.keywords_var.set("social, profile, post")
        self.exclude_keywords_var.set("")
        self.min_length_var.set(20)
    
    def clear_filters(self):
        """Limpa todos os filtros"""
        self.title_selector_var.set("")
        self.desc_selector_var.set("")
        self.content_selector_var.set("")
        self.keywords_var.set("")
        self.exclude_keywords_var.set("")
        self.min_length_var.set(0)
        self.regex_var.set("")
    
    def get_urls(self):
        """Obtém a lista de URLs do campo de texto"""
        urls_text = self.urls_text.get("1.0", tk.END).strip()
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        return urls
    
    def get_selectors(self):
        """Obtém os seletores CSS configurados"""
        selectors = {}
        
        if self.title_selector_var.get().strip():
            selectors['title'] = [s.strip() for s in self.title_selector_var.get().split(',')]
        
        if self.desc_selector_var.get().strip():
            selectors['description'] = [s.strip() for s in self.desc_selector_var.get().split(',')]
        
        if self.content_selector_var.get().strip():
            selectors['content'] = [s.strip() for s in self.content_selector_var.get().split(',')]
        
        return selectors
    
    def get_filters(self):
        """Obtém os filtros de conteúdo configurados"""
        filters = {}
        
        if self.keywords_var.get().strip():
            filters['keywords'] = [k.strip() for k in self.keywords_var.get().split(',')]
        
        if self.exclude_keywords_var.get().strip():
            filters['exclude_keywords'] = [k.strip() for k in self.exclude_keywords_var.get().split(',')]
        
        if self.min_length_var.get() > 0:
            filters['min_length'] = self.min_length_var.get()
        
        if self.regex_var.get().strip():
            filters['regex'] = self.regex_var.get().strip()
        
        return filters
    
    def get_headers(self):
        """Obtém os headers personalizados"""
        try:
            headers_text = self.headers_text.get("1.0", tk.END).strip()
            if headers_text:
                return json.loads(headers_text)
            return None
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "Headers JSON inválido!")
            return None
    
    def get_proxies(self):
        """Obtém as configurações de proxy"""
        proxies = {}
        
        if self.http_proxy_var.get().strip():
            proxies['http'] = self.http_proxy_var.get().strip()
        
        if self.https_proxy_var.get().strip():
            proxies['https'] = self.https_proxy_var.get().strip()
        
        return proxies if proxies else None
    
    def start_crawling(self):
        """Inicia o processo de crawling"""
        urls = self.get_urls()
        if not urls:
            messagebox.showerror("Erro", "Por favor, insira pelo menos uma URL!")
            return
        
        # Configura interface
        self.is_crawling = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.progress_bar.set(0)
        
        # Limpa resultados anteriores
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Configura o crawler
        headers = self.get_headers()
        proxies = self.get_proxies()
        
        self.crawler.setup_session(
            headers=headers,
            proxies=proxies,
            timeout=self.timeout_var.get(),
            delay=self.delay_var.get()
        )
        
        # Inicia thread de crawling
        self.crawl_thread = threading.Thread(target=self.run_crawling, args=(urls,))
        self.crawl_thread.daemon = True
        self.crawl_thread.start()
    
    def run_crawling(self, urls):
        """Executa o crawling em thread separada"""
        try:
            selectors = self.get_selectors()
            filters = self.get_filters()
            
            total_urls = len(urls)
            
            for i, url in enumerate(urls):
                if not self.is_crawling:
                    break
                
                # Atualiza status
                self.status_var.set(f"Processando: {url} ({i+1}/{total_urls})")
                progress = (i / total_urls) * 100
                self.progress_bar.set(progress / 100)
                
                # Faz crawling
                if self.use_selenium_var.get():
                    js_code = self.js_text.get("1.0", tk.END).strip()
                    js_code = js_code if js_code and not js_code.startswith("//") else None
                    
                    result = self.crawler.crawl_with_selenium(
                        url, 
                        wait_time=self.selenium_wait_var.get(),
                        execute_js=js_code
                    )
                else:
                    result = self.crawler.crawl_url(
                        url,
                        selectors=selectors,
                        content_filters=filters,
                        respect_robots=self.respect_robots_var.get()
                    )
                
                # Adiciona resultado à interface
                if result:
                    self.root.after(0, self.add_result_to_tree, result)
            
            # Finaliza
            self.root.after(0, self.crawling_finished)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro durante o crawling: {str(e)}"))
            self.root.after(0, self.crawling_finished)
    
    def add_result_to_tree(self, result):
        """Adiciona um resultado à árvore de resultados"""
        self.results_tree.insert("", "end", values=(
            result.url[:50] + "..." if len(result.url) > 50 else result.url,
            result.title[:30] + "..." if len(result.title) > 30 else result.title,
            result.status_code,
            f"{result.response_time:.2f}",
            len(result.links),
            len(result.images)
        ))
    
    def crawling_finished(self):
        """Finaliza o processo de crawling"""
        self.is_crawling = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.progress_bar.set(1.0)
        self.status_var.set("Crawling concluído!")
        
        # Atualiza estatísticas
        self.update_statistics()
    
    def stop_crawling(self):
        """Para o processo de crawling"""
        self.is_crawling = False
        self.status_var.set("Parando crawling...")
    
    def update_statistics(self):
        """Atualiza as estatísticas na interface"""
        stats = self.crawler.get_statistics()
        if stats:
            stats_text = f"""
📊 Estatísticas do Crawling:
• Total de páginas: {stats['total_pages']}
• Tempo médio de resposta: {stats['average_response_time']}s
• Total de links encontrados: {stats['total_links_found']}
• Total de imagens encontradas: {stats['total_images_found']}
• URLs visitadas: {stats['total_urls_visited']}
            """.strip()
            self.stats_label.configure(text=stats_text)
    
    def on_result_double_click(self, event):
        """Manipula duplo clique nos resultados"""
        selection = self.results_tree.selection()
        if selection:
            item = self.results_tree.item(selection[0])
            url = item['values'][0]
            # Remove "..." se existir
            if url.endswith("..."):
                # Encontra a URL completa nos resultados
                for result in self.crawler.results:
                    if result.url.startswith(url[:-3]):
                        url = result.url
                        break
            
            # Abre no navegador
            webbrowser.open(url)
    
    def export_results(self, format_type):
        """Exporta os resultados"""
        if not self.crawler.results:
            messagebox.showwarning("Aviso", "Nenhum resultado para exportar!")
            return
        
        # Escolhe o arquivo
        filetypes = {
            'excel': [("Excel files", "*.xlsx")],
            'csv': [("CSV files", "*.csv")],
            'json': [("JSON files", "*.json")]
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=f".{format_type}",
            filetypes=filetypes[format_type]
        )
        
        if filename:
            try:
                self.crawler.export_results(filename, format_type)
                messagebox.showinfo("Sucesso", f"Resultados exportados para: {filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
    
    def save_config(self):
        """Salva a configuração atual"""
        config = {
            'urls': self.urls_text.get("1.0", tk.END).strip(),
            'delay': self.delay_var.get(),
            'timeout': self.timeout_var.get(),
            'user_agent': self.user_agent_var.get(),
            'respect_robots': self.respect_robots_var.get(),
            'use_selenium': self.use_selenium_var.get(),
            'headers': self.headers_text.get("1.0", tk.END).strip(),
            'http_proxy': self.http_proxy_var.get(),
            'https_proxy': self.https_proxy_var.get(),
            'js_code': self.js_text.get("1.0", tk.END).strip(),
            'selenium_wait': self.selenium_wait_var.get(),
            'title_selector': self.title_selector_var.get(),
            'desc_selector': self.desc_selector_var.get(),
            'content_selector': self.content_selector_var.get(),
            'keywords': self.keywords_var.get(),
            'exclude_keywords': self.exclude_keywords_var.get(),
            'min_length': self.min_length_var.get(),
            'regex': self.regex_var.get()
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Sucesso", "Configuração salva com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar configuração: {str(e)}")
    
    def load_config(self):
        """Carrega configuração salva"""
        config_file = "crawler_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # Aplica configurações
                if 'delay' in config:
                    self.delay_var.set(config['delay'])
                if 'timeout' in config:
                    self.timeout_var.set(config['timeout'])
                # ... etc
                    
            except Exception as e:
                print(f"Erro ao carregar configuração: {e}")
    
    def run(self):
        """Inicia a aplicação"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Manipula o fechamento da aplicação"""
        if self.is_crawling:
            if messagebox.askokcancel("Fechar", "Crawling em andamento. Deseja realmente fechar?"):
                self.is_crawling = False
                self.root.destroy()
        else:
            self.root.destroy()


if __name__ == "__main__":
    app = CrawlerGUI()
    app.run()
