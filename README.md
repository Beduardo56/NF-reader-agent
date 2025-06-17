# 🤖 NF Reader Agent - Analisador Inteligente de Notas Fiscais

Um sistema de análise inteligente de notas fiscais brasileiras que utiliza IA para responder perguntas sobre dados de vendas e compras através de uma interface web intuitiva.

## 📋 Descrição

O **NF Reader Agent** é uma aplicação web que permite analisar dados de notas fiscais de forma inteligente usando Inteligência Artificial. O sistema processa arquivos CSV contendo informações de cabeçalho e itens das notas fiscais, e permite fazer perguntas em linguagem natural sobre os dados.

### ✨ Principais Funcionalidades

- 📊 **Interface Web Intuitiva**: Interface moderna e responsiva usando Streamlit
- 🤖 **Análise com IA**: Utiliza GPT-4 para responder perguntas em linguagem natural
- 📁 **Múltiplos Formatos de Upload**: Suporte para arquivos CSV individuais ou arquivo ZIP
- 💬 **Chat Interativo**: Sistema de conversação com memória de contexto
- 📈 **Dashboard de Resumo**: Métricas e estatísticas dos dados carregados
- 🐳 **Containerização**: Suporte completo para Docker e Docker Compose

## 🚀 Tecnologias Utilizadas

- **Python 3.11**
- **Streamlit** - Interface web
- **LangChain** - Framework para aplicações de IA
- **OpenAI GPT-4** - Modelo de linguagem
- **Pandas** - Manipulação de dados
- **Docker** - Containerização
- **NumPy** - Computação numérica

## 📦 Instalação e Configuração

### Pré-requisitos

- Python 3.11 ou superior
- Chave da API do OpenAI
- Docker (opcional, para execução em container)

### Método 1: Instalação Local

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd NF-reader-agent
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure a API Key**
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave da OpenAI:
     ```
     OPENAI_API_KEY=sua-chave-aqui
     ```

4. **Execute a aplicação**
   ```bash
   streamlit run app.py
   ```

### Método 2: Usando Docker

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd NF-reader-agent
   ```

2. **Configure a API Key**
   ```bash
   export OPENAI_API_KEY="sua-chave-aqui"
   ```

3. **Execute com Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Acesse a aplicação**
   - Abra seu navegador em: `http://localhost:8501`

## 📁 Estrutura do Projeto

```
NF-reader-agent/
├── app.py                 # Aplicação principal Streamlit
├── src/
│   └── main.py           # Classe principal do analisador
├── requirements.txt      # Dependências Python
├── Dockerfile           # Configuração Docker
├── docker-compose.yaml  # Orquestração Docker
├── temp_data/           # Dados temporários
└── README.md           # Este arquivo
```

## 🎯 Como Usar

### 1. Preparação dos Dados

O sistema aceita dados de notas fiscais em formato CSV. Você pode fornecer:

- **Arquivos CSV separados**:
  - `cabecalho.csv` - Dados do cabeçalho das notas fiscais
  - `itens.csv` - Dados dos itens das notas fiscais

- **Arquivo ZIP** contendo os CSVs

### 2. Estrutura dos Dados

Os arquivos CSV devem conter as seguintes colunas principais:

**Cabeçalho (cabecalho.csv)**:
- `CHAVE DE ACESSO` - Chave única da nota fiscal
- `DATA EMISSÃO` - Data de emissão
- `VALOR NOTA FISCAL` - Valor total da nota
- `RAZÃO SOCIAL EMITENTE` - Nome da empresa emissora
- `NOME DESTINATÁRIO` - Nome do cliente/destinatário

**Itens (itens.csv)**:
- `CHAVE DE ACESSO` - Chave única da nota fiscal
- `DESCRIÇÃO DO PRODUTO/SERVIÇO` - Descrição do item
- `QUANTIDADE` - Quantidade vendida
- `VALOR UNITÁRIO` - Preço unitário
- `VALOR TOTAL` - Valor total do item

### 3. Interface Web

1. **Acesse a aplicação** no navegador
2. **Insira sua API Key** do OpenAI na barra lateral
3. **Faça upload dos dados**:
   - Escolha entre arquivos CSV separados ou arquivo ZIP
   - Clique em "Carregar Dados"
4. **Visualize o resumo** dos dados carregados
5. **Faça perguntas** em linguagem natural sobre os dados

### 4. Exemplos de Perguntas

- "Qual empresa mais gastou?"
- "Quanto a empresa X gastou no total?"
- "Qual foi o produto com maior quantidade vendida?"
- "Quais são os 5 maiores fornecedores por valor?"
- "Quantas notas foram emitidas em janeiro de 2024?"
- "Qual o valor médio das notas fiscais?"
- "Quais produtos têm NCM 49019900?"

## 🔧 Configuração Avançada

### Variáveis de Ambiente

- `OPENAI_API_KEY`: Chave da API do OpenAI (obrigatória)
- `STREAMLIT_SERVER_PORT`: Porta do servidor Streamlit (padrão: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Endereço do servidor (padrão: 0.0.0.0)

### Personalização do Modelo

Para alterar o modelo de IA, edite o arquivo `src/main.py`:

```python
self.llm = ChatOpenAI(
    api_key=openai_api_key,
    model_name="gpt-4",  # Altere para outro modelo
    temperature=0.1      # Ajuste a criatividade (0-1)
)
```

## 🐛 Solução de Problemas

### Erro de API Key
- Verifique se a chave da OpenAI está correta
- Certifique-se de que a chave tem créditos disponíveis

### Erro ao Carregar Dados
- Verifique se os arquivos CSV estão no formato correto
- Certifique-se de que as colunas obrigatórias estão presentes
- Verifique se os arquivos não estão corrompidos

### Problemas com Docker
- Verifique se o Docker está instalado e rodando
- Execute `docker-compose down` antes de `docker-compose up --build`
- Verifique se a porta 8501 não está sendo usada por outro processo

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para dúvidas, sugestões ou problemas:

1. Abra uma [Issue](https://github.com/seu-usuario/NF-reader-agent/issues) no GitHub
2. Entre em contato através do email: beduardo56@gmail.com

## 🔄 Changelog

### v1.0.0
- ✅ Interface web com Streamlit
- ✅ Integração com OpenAI GPT-4
- ✅ Suporte a múltiplos formatos de upload
- ✅ Sistema de chat com memória
- ✅ Containerização com Docker
- ✅ Dashboard de métricas

---

**Desenvolvido com ❤️ para facilitar a análise de notas fiscais brasileiras**