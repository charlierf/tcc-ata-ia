# 📝 Geração Automatizada de Atas de Reunião com IA – TCC UFS

Este repositório contém o projeto de Trabalho de Conclusão de Curso (TCC) de **Charlie Rodrigues Fonseca** no curso de Ciência da Computação da Universidade Federal de Sergipe (UFS), orientado pelo Prof. Dr. Hendrik Macedo.

O objetivo central do projeto é o desenvolvimento de uma **solução institucional de código aberto** capaz de **gerar atas de reuniões automaticamente** a partir de áudios gravados, utilizando técnicas de **Inteligência Artificial**, como transcrição automática, identificação de entidades nomeadas e geração de texto com modelos de linguagem (LLMs).

---

## 🎯 Objetivos

- Processar reuniões gravadas (ex: CONSU e Conepe) e transcrevê-las automaticamente.
- Utilizar IA generativa para **produzir atas institucionais compatíveis com o padrão oficial da UFS**.
- Garantir uma solução **open source**, **on-premise** e **respeitosa às restrições de segurança e privacidade** da instituição.
- Avaliar a qualidade das atas geradas com base em métricas objetivas e comparação com atas reais.

---

## 🧠 Tecnologias e Ferramentas

- **Transcrição de áudio:** a definir ([`whisper.cpp`](https://github.com/ggerganov/whisper.cpp), [`faster-whisper`](https://github.com/guillaumekln/faster-whisper))
- **Modelos de sumarização:** a definir (DistilBART, T5-small, Falcon, Mistral (quantizados e leves))
- **NER / análise semântica:** a definir (spaCy, BERT, token classification)
- **Infraestrutura:** a definir (Python, FastAPI (ou equivalente), scripts em notebooks)
- **Repositório de dados:** Reuniões públicas da UFS extraídas do YouTube

---

## 🗂️ Estrutura do Repositório

```plaintext
tcc-ata-ia/
│
├── docs/                     ← Documentos e monografia (TCC1 e TCC2)
├── data/                     ← Áudios, transcrições e atas geradas
├── notebooks/                ← Análises exploratórias e testes com IA
├── src/                      ← Código-fonte do sistema final
├── models/                   ← Modelos locais (transcrição, sumarização, NER)
├── evaluation/               ← Scripts de avaliação de qualidade da ata
├── diagrams/                 ← Arquitetura e fluxos da solução
├── README.md                 ← Este documento
├── requirements.txt          ← Dependências do projeto
└── .gitignore                ← Arquivos a serem ignorados no versionamento
````

---

## 🧪 Base de Dados

As gravações utilizadas são reuniões reais dos Conselhos Superiores da UFS (CONSU e Conepe), extraídas de fontes públicas, e servirão como **material de teste, validação e avaliação da solução desenvolvida**.

---

## 📄 Documentação do TCC

O desenvolvimento está dividido em duas etapas:

* **TCC1:** Revisão sistemática, proposta de arquitetura, definição de escopo e tecnologias.
* **TCC2:** Desenvolvimento do sistema, testes, avaliação de resultados e escrita final da monografia.

---

## 📫 Contato

Desenvolvido por [Charlie Fonseca](mailto:dev@charliefonseca.com.br)

---

**UFS - Universidade Federal de Sergipe**
**Departamento de Computação – DCOMP**
2025
