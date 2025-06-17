import pandas as pd
import numpy as np
import zipfile
import os
from typing import Dict, Any, List
import streamlit as st
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.schema import AgentAction, AgentFinish
from langchain.agents import AgentExecutor, BaseMultiActionAgent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import logging

class NotasFiscaisAnalyzer:
    """
    Analisador de Notas Fiscais com capacidades de chat usando LangChain e OpenAI
    """
    
    def __init__(self, openai_api_key: str):
        """
        Inicializa o analisador com a chave da API do OpenAI
        """
        self.openai_api_key = openai_api_key
        self.llm = ChatOpenAI(
            api_key=openai_api_key,
            model_name="gpt-4",
            temperature=0.1
        )
        # DataFrames para armazenar os dados
        self.df_cabecalho = None
        self.df_itens = None
        
        # Agente para análise de dados
        self.agent = None
        
        # Memória da conversa
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.setup_logging()

    def setup_logging(self):
        """Configura o sistema de logging"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def extract_and_load_data(self, zip_path: str = None, csv_paths: Dict[str, str] = None):
        """
        Extrai dados de arquivo ZIP ou carrega CSVs diretamente
        
        Args:
            zip_path: Caminho para arquivo ZIP (opcional)
            csv_paths: Dicionário com caminhos dos CSVs {'cabecalho': path, 'itens': path}
        """
        try:
            if zip_path:
                self._extract_from_zip(zip_path)
            elif csv_paths:
                self._load_from_paths(csv_paths)
            else:
                raise ValueError("Forneça zip_path ou csv_paths")
                
            self._process_data()
            self._create_agent()
            
            self.logger.info("Dados carregados e agente criado com sucesso!")
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar dados: {str(e)}")
            raise

    def _extract_from_zip(self, zip_path: str):
        """Extrai CSVs do arquivo ZIP"""
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("temp_data")
            
        # Procura pelos arquivos CSV
        for root, dirs, files in os.walk("temp_data"):
            for file in files:
                if "cabecalho" in file.lower() and file.endswith('.csv'):
                    self.df_cabecalho = pd.read_csv(os.path.join(root, file))
                elif "itens" in file.lower() and file.endswith('.csv'):
                    self.df_itens = pd.read_csv(os.path.join(root, file))
        print(self.df_cabecalho)
        print(self.df_itens)
    def _load_from_paths(self, csv_paths: Dict[str, str]):
        """Carrega CSVs dos caminhos fornecidos"""
        self.df_cabecalho = pd.read_csv(csv_paths['cabecalho'])
        self.df_itens = pd.read_csv(csv_paths['itens'])

    def _process_data(self):
        """Processa e limpa os dados"""
        # Limpa dados vazios
        self.df_cabecalho = self.df_cabecalho.dropna(subset=['CHAVE DE ACESSO'])
        self.df_itens = self.df_itens.dropna(subset=['CHAVE DE ACESSO'])
        
        # Converte tipos de dados
        self.df_cabecalho['DATA EMISSÃO'] = pd.to_datetime(self.df_cabecalho['DATA EMISSÃO'])
        self.df_itens['DATA EMISSÃO'] = pd.to_datetime(self.df_itens['DATA EMISSÃO'])
        # Garante tipos numéricos
        numeric_cols_cabecalho = ['VALOR NOTA FISCAL']
        numeric_cols_itens = ['QUANTIDADE', 'VALOR UNITÁRIO', 'VALOR TOTAL']
        
        for col in numeric_cols_cabecalho:
            if col in self.df_cabecalho.columns:
                self.df_cabecalho[col] = pd.to_numeric(self.df_cabecalho[col], errors='coerce')
                
        for col in numeric_cols_itens:
            if col in self.df_itens.columns:
                self.df_itens[col] = pd.to_numeric(self.df_itens[col], errors='coerce')
        
        
        self.logger.info(f"Dados processados: {len(self.df_cabecalho)} notas, {len(self.df_itens)} itens")

    def _create_agent(self):
        """Cria o agente LangChain para análise dos dados usando apenas df_itens"""
        
        # Template de prompt personalizado para o contexto brasileiro
        prompt_prefix = f"""
Você é um assistente especializado em análise de notas fiscais brasileiras.
Você tem acesso a um DataFrame chamado 'df' que contém dados de itens de notas fiscais.

COLUNAS DISPONÍVEIS NO DATAFRAME:
{list(self.df_itens.columns)}

INFORMAÇÕES IMPORTANTES:
- O DataFrame tem {len(self.df_itens)} registros de itens
- Sempre use 'df' para referenciar o DataFrame
- Principais colunas para análise:
  * Para empresas: RAZÃO SOCIAL EMITENTE, NOME DESTINATÁRIO
  * Para valores: VALOR TOTAL, VALOR UNITÁRIO, QUANTIDADE
  * Para produtos: DESCRIÇÃO DO PRODUTO/SERVIÇO, DESCRIÇÃO PRODUTO
  * Para datas: DATA EMISSÃO, DATA EMISSAO
  * Para localização: UF EMITENTE, UF DESTINATÁRIO

INSTRUÇÕES:
- Use sempre os dados do DataFrame 'df' para responder
- Formate valores monetários em Real (R$) usando formatação brasileira
- Seja preciso com os cálculos
- Explique brevemente como chegou ao resultado
- Se não encontrar dados suficientes, informe isso claramente
- Sempre use df.column_name para acessar colunas
- Use métodos pandas como groupby, sum, max, etc.

EXEMPLO DE USO:
Para encontrar a empresa que mais gastou:
```python
resultado = df.groupby('NOME DESTINATÁRIO')['VALOR TOTAL'].sum().sort_values(ascending=False)
print(resultado.head())
```
        """
        # Cria agente para análise do DataFrame de itens
        self.agent = create_pandas_dataframe_agent(
            llm=self.llm,
            df=self.df_itens,
            verbose=True,
            agent_type="openai-functions",
            allow_dangerous_code=True,
            prefix=prompt_prefix,
            handle_parsing_errors=True,
            max_iterations=5
        )

    def ask_question(self, question: str) -> str:
        """
        Processa uma pergunta do usuário e retorna a resposta
        
        Args:
            question: Pergunta do usuário
            
        Returns:
            Resposta baseada na análise dos dados
        """
        # try:
        if not self.agent:
            return "Erro: Sistema não inicializado. Carregue os dados primeiro."
        
        # Processa a pergunta diretamente
        first_question = question
        print(question)
        response = self.agent.invoke(question)
        print(response)
        # Salva na memória
        self.memory.save_context(
            {"input": response['input']},
            {"outputs": response['output']}
        )
        print(response)
        return response
            
        # except Exception as e:
        #     error_msg = f"Erro ao processar pergunta: {str(e)}"
        #     self.logger.error(error_msg)
            
        #     # Tenta uma abordagem mais simples em caso de erro
        #     try:
        #         # Fallback: resposta básica baseada em análise simples
        #         if "maior" in question.lower() and "empresa" in question.lower():
        #             if self.df_cabecalho is not None:
        #                 top_empresa = self.df_cabecalho.groupby('RAZÃO SOCIAL EMITENTE')['VALOR NOTA FISCAL'].sum().idxmax()
        #                 valor = self.df_cabecalho.groupby('RAZÃO SOCIAL EMITENTE')['VALOR NOTA FISCAL'].sum().max()
        #                 return f"A empresa que mais recebeu foi: {top_empresa} com R$ {valor:,.2f}"
                
        #         return f"Desculpe, ocorreu um erro ao processar sua pergunta. Tente reformular ou simplifique a pergunta."
                
        #     except:
        #         return error_msg

    def get_data_summary(self) -> Dict[str, Any]:
        """Retorna um resumo dos dados carregados"""
        if self.df_cabecalho is None or self.df_itens is None:
            return {"erro": "Dados não carregados"}
            
        return {
            "total_notas": len(self.df_cabecalho),
            "total_itens": len(self.df_itens),
            "periodo": {
                "inicio": self.df_cabecalho['DATA EMISSÃO'].min().strftime('%d/%m/%Y'),
                "fim": self.df_cabecalho['DATA EMISSÃO'].max().strftime('%d/%m/%Y')
            },
            "valor_total_periodo": self.df_cabecalho['VALOR NOTA FISCAL'].sum(),
            "fornecedores_unicos": self.df_cabecalho['RAZÃO SOCIAL EMITENTE'].nunique(),
            "clientes_unicos": self.df_cabecalho['NOME DESTINATÁRIO'].nunique()
        }
