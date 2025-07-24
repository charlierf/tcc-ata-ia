#!/usr/bin/env python3
"""
Script para auxiliar na busca e organização de artigos científicos
================================================================

Este script ajuda a:
1. Gerar links de busca para diferentes bases de dados
2. Organizar a estrutura de diretórios para artigos
3. Criar templates de resumos
4. Gerar lista de pendências

Autor: Charlie Rodrigues Fonseca
Data: 24/07/2025
"""

import os
import urllib.parse
from pathlib import Path
from typing import List, Dict
import webbrowser


class ArticleManager:
    """Gerenciador para busca e organização de artigos científicos."""
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            base_dir = Path(__file__).parent.parent.parent
        
        self.base_dir = Path(base_dir)
        self.refs_dir = self.base_dir / "docs" / "referencias"
        
        # Artigos prioritários para o projeto
        self.priority_articles = {
            "whisper": {
                "title": "Robust Speech Recognition via Large-Scale Weak Supervision",
                "authors": "Radford, Kim, Xu, Brockman, McLeavey, Sutskever",
                "year": 2022,
                "category": "asr/whisper",
                "priority": "ALTA",
                "keywords": ["whisper", "speech recognition", "weak supervision"]
            },
            "wav2vec2": {
                "title": "wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations",
                "authors": "Baevski, Zhou, Mohamed, Auli",
                "year": 2020,
                "category": "asr/wav2vec",
                "priority": "MÉDIA",
                "keywords": ["wav2vec", "self-supervised", "speech representations"]
            },
            "bart": {
                "title": "BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation",
                "authors": "Lewis, Liu, Goyal",
                "year": 2019,
                "category": "nlp/summarization",
                "priority": "MÉDIA",
                "keywords": ["BART", "sequence-to-sequence", "text generation"]
            },
            "t5": {
                "title": "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer",
                "authors": "Raffel, Shazeer, Roberts",
                "year": 2019,
                "category": "nlp/summarization",
                "priority": "MÉDIA",
                "keywords": ["T5", "transfer learning", "text-to-text"]
            },
            "bertimbau": {
                "title": "BERTimbau: Portuguese BERT for Brazilian Portuguese",
                "authors": "Souza, Nogueira, Lotufo",
                "year": 2020,
                "category": "nlp/ner",
                "priority": "ALTA",
                "keywords": ["BERT", "Portuguese", "Brazilian", "BERTimbau"]
            },
            "rouge": {
                "title": "ROUGE: A Package for Automatic Evaluation of Summaries",
                "authors": "Lin",
                "year": 2004,
                "category": "evaluation",
                "priority": "ALTA",
                "keywords": ["ROUGE", "evaluation", "summarization", "metrics"]
            }
        }
        
        # Bases de dados para busca
        self.databases = {
            "arxiv": "https://arxiv.org/search/?query={}&searchtype=all",
            "google_scholar": "https://scholar.google.com/scholar?q={}",
            "ieee": "https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={}",
            "acl": "https://aclanthology.org/search/?q={}",
            "papers_with_code": "https://paperswithcode.com/search?q={}",
            "semantic_scholar": "https://www.semanticscholar.org/search?q={}"
        }
    
    def create_directory_structure(self):
        """Cria a estrutura de diretórios para organizar os artigos."""
        categories = [
            "asr/whisper",
            "asr/wav2vec", 
            "asr/general",
            "nlp/summarization",
            "nlp/ner",
            "nlp/llm",
            "evaluation",
            "related-work"
        ]
        
        for category in categories:
            dir_path = self.refs_dir / category
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Criado: {dir_path}")
    
    def generate_search_urls(self, article_key: str) -> Dict[str, str]:
        """Gera URLs de busca para um artigo específico."""
        if article_key not in self.priority_articles:
            print(f"❌ Artigo '{article_key}' não encontrado")
            return {}
        
        article = self.priority_articles[article_key]
        
        # Criar query de busca otimizada
        query_parts = [
            article["title"],
            article["authors"].split(",")[0],  # Primeiro autor
            str(article["year"])
        ]
        query = " ".join(query_parts)
        
        # Gerar URLs para cada base
        urls = {}
        for db_name, url_template in self.databases.items():
            encoded_query = urllib.parse.quote(query)
            urls[db_name] = url_template.format(encoded_query)
        
        return urls
    
    def open_search_urls(self, article_key: str, databases: List[str] = None):
        """Abre URLs de busca no navegador."""
        if databases is None:
            databases = ["arxiv", "google_scholar", "papers_with_code"]
        
        urls = self.generate_search_urls(article_key)
        
        if not urls:
            return
        
        article = self.priority_articles[article_key]
        print(f"\n🔍 Buscando: {article['title']}")
        print(f"📝 Autores: {article['authors']}")
        print(f"📅 Ano: {article['year']}")
        print(f"⭐ Prioridade: {article['priority']}")
        print("\n🌐 Abrindo URLs:")
        
        for db_name in databases:
            if db_name in urls:
                print(f"   {db_name}: {urls[db_name]}")
                webbrowser.open(urls[db_name])
    
    def create_article_template(self, article_key: str):
        """Cria template de resumo para um artigo específico."""
        if article_key not in self.priority_articles:
            print(f"❌ Artigo '{article_key}' não encontrado")
            return
        
        article = self.priority_articles[article_key]
        category_dir = self.refs_dir / article["category"]
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Nome do arquivo de resumo
        first_author = article["authors"].split(",")[0].strip()
        filename = f"{first_author.lower()}_{article['year']}_resumo.md"
        file_path = category_dir / filename
        
        if file_path.exists():
            print(f"⚠️  Resumo já existe: {file_path}")
            return
        
        # Conteúdo do template personalizado
        template_content = f"""# Resumo: {article['title']}

---

## 📄 **Informações Básicas**

- **Título:** {article['title']}
- **Autores:** {article['authors']}
- **Ano:** {article['year']}
- **Venue:** [A COMPLETAR após encontrar o artigo]
- **DOI/URL:** [A COMPLETAR após encontrar o artigo]
- **Arquivo Local:** `{first_author.lower()}_{article['year']}_título-curto.pdf` *(a ser baixado)*

---

## 🎯 **Relevância para o Projeto**

**Por que este artigo é importante para o TCC?**
- [ ] Fundamenta escolhas técnicas
- [ ] Fornece métricas de avaliação
- [ ] Apresenta baseline para comparação
- [ ] Oferece metodologia similar
- [ ] Outro: ___________

**Seção do TCC que este artigo suporta:**
- [ ] Revisão de Literatura
- [ ] Metodologia
- [ ] Implementação
- [ ] Avaliação
- [ ] Trabalhos Relacionados

---

## 📊 **Resumo Executivo**

### **Problema Abordado**
[A COMPLETAR após leitura do artigo]

### **Solução Proposta**
[A COMPLETAR após leitura do artigo]

### **Principais Contribuições**
1. [A COMPLETAR]
2. [A COMPLETAR]
3. [A COMPLETAR]

### **Resultados Principais**
[A COMPLETAR após leitura do artigo]

---

## 🔧 **Detalhes Técnicos Relevantes**

[A COMPLETAR com detalhes específicos após leitura]

---

## 💡 **Insights para o Projeto**

### **O que podemos aplicar diretamente:**
- [A COMPLETAR]

### **O que adaptar:**
- [A COMPLETAR]

### **O que evitar:**
- [A COMPLETAR]

---

## 📝 **Citações Importantes**

[A COMPLETAR com quotes específicos]

---

## 🔗 **Trabalhos Relacionados Citados**

[A COMPLETAR após leitura das referências]

---

## 📋 **Checklist de Aproveitamento**

- [ ] Resumo criado
- [ ] PDF baixado
- [ ] Artigo lido completamente
- [ ] Citações relevantes extraídas
- [ ] Aplicações identificadas
- [ ] Integrado ao texto do TCC
- [ ] Referência adicionada à bibliografia
- [ ] Trabalhos relacionados identificados

---

**Data de criação:** 24/07/2025  
**Criado por:** Charlie Rodrigues Fonseca  
**Status:** 🔍 PENDENTE DE BUSCA  
**Prioridade:** ⭐ {article['priority']} 
**Keywords:** {', '.join(article['keywords'])}"""
        
        # Salvar template
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        print(f"✅ Template criado: {file_path}")
        return file_path
    
    def show_priority_list(self):
        """Mostra lista de artigos por prioridade."""
        print("\n📚 ARTIGOS PRIORITÁRIOS PARA O TCC")
        print("=" * 50)
        
        # Agrupar por prioridade
        by_priority = {}
        for key, article in self.priority_articles.items():
            priority = article["priority"]
            if priority not in by_priority:
                by_priority[priority] = []
            by_priority[priority].append((key, article))
        
        # Mostrar por prioridade
        for priority in ["ALTA", "MÉDIA", "BAIXA"]:
            if priority in by_priority:
                print(f"\n⭐ {priority} PRIORIDADE:")
                for key, article in by_priority[priority]:
                    print(f"   {key}: {article['title']}")
                    print(f"      📝 {article['authors']} ({article['year']})")
                    print(f"      📂 {article['category']}")
    
    def generate_search_script(self):
        """Gera script para busca automatizada."""
        script_content = f"""#!/bin/bash
# Script de busca automatizada de artigos
# Gerado automaticamente em 24/07/2025

echo "🔍 Iniciando busca de artigos prioritários..."

# URLs de busca para artigos de ALTA prioridade
"""
        
        for key, article in self.priority_articles.items():
            if article["priority"] == "ALTA":
                urls = self.generate_search_urls(key)
                script_content += f"""
echo "📖 Buscando: {article['title']}"
echo "   ArXiv: {urls.get('arxiv', 'N/A')}"
echo "   Google Scholar: {urls.get('google_scholar', 'N/A')}"
echo ""
"""
        
        script_path = self.refs_dir / "buscar_artigos.sh"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"✅ Script de busca criado: {script_path}")


def main():
    """Função principal com menu interativo."""
    import sys
    
    manager = ArticleManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup":
            print("🚀 Configurando estrutura de artigos...")
            manager.create_directory_structure()
            manager.show_priority_list()
            
        elif command == "search" and len(sys.argv) > 2:
            article_key = sys.argv[2]
            manager.open_search_urls(article_key)
            
        elif command == "template" and len(sys.argv) > 2:
            article_key = sys.argv[2]
            manager.create_article_template(article_key)
            
        elif command == "list":
            manager.show_priority_list()
            
        else:
            print("❌ Comando inválido")
            print("Uso: python article_manager.py [setup|search|template|list] [artigo]")
    
    else:
        # Menu interativo
        print("📚 Gerenciador de Artigos Científicos")
        print("=" * 40)
        print("1. Configurar estrutura")
        print("2. Listar artigos prioritários") 
        print("3. Buscar artigo específico")
        print("4. Criar template de resumo")
        print("5. Sair")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == "1":
            manager.create_directory_structure()
        elif choice == "2":
            manager.show_priority_list()
        elif choice == "3":
            manager.show_priority_list()
            article_key = input("\nDigite a chave do artigo: ")
            manager.open_search_urls(article_key)
        elif choice == "4":
            manager.show_priority_list()
            article_key = input("\nDigite a chave do artigo: ")
            manager.create_article_template(article_key)
        elif choice == "5":
            print("👋 Até logo!")
        else:
            print("❌ Opção inválida")


if __name__ == "__main__":
    main()
