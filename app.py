import pandas as pd
import numpy as np
import zipfile
import os
from typing import Dict, Any, List
import streamlit as st
from src.main import NotasFiscaisAnalyzer

# Interface Streamlit
def create_streamlit_app():
    """Cria a interface web usando Streamlit"""
    
    st.set_page_config(
        page_title="Chat Análise de Notas Fiscais",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("🤖 Chat para Análise de Notas Fiscais")
    st.markdown("---")
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Input da API Key
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Insira sua chave da API do OpenAI"
        )
        
        # Upload de arquivos
        st.subheader("📁 Upload de Dados")
        
        upload_type = st.radio(
            "Tipo de Upload:",
            ["Arquivos CSV Separados", "Arquivo ZIP"]
        )
        
        if upload_type == "Arquivos CSV Separados":
            csv_cabecalho = st.file_uploader(
                "CSV Cabeçalho das Notas",
                type=['csv'],
                key="cabecalho"
            )
            csv_itens = st.file_uploader(
                "CSV Itens das Notas", 
                type=['csv'],
                key="itens"
            )
        else:
            zip_file = st.file_uploader(
                "Arquivo ZIP com CSVs",
                type=['zip']
            )
    
    # Inicialização do sistema
    if api_key:
        if 'analyzer' not in st.session_state:
            st.session_state.analyzer = NotasFiscaisAnalyzer(api_key)
        
        # Carregamento de dados
        data_loaded = False
        
        if upload_type == "Arquivos CSV Separados" and csv_cabecalho and csv_itens:
            if st.button("🔄 Carregar Dados CSV"):
                with st.spinner("Carregando dados..."):
                    try:
                        # Salva arquivos temporariamente
                        with open("temp_cabecalho.csv", "wb") as f:
                            f.write(csv_cabecalho.getbuffer())
                        with open("temp_itens.csv", "wb") as f:
                            f.write(csv_itens.getbuffer())
                        
                        st.session_state.analyzer.extract_and_load_data(
                            csv_paths={
                                'cabecalho': 'temp_cabecalho.csv',
                                'itens': 'temp_itens.csv'
                            }
                        )
                        
                        st.success("✅ Dados carregados com sucesso!")
                        data_loaded = True
                        
                    except Exception as e:
                        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        
        elif upload_type == "Arquivo ZIP" and zip_file:
            if st.button("🔄 Carregar Dados ZIP"):
                with st.spinner("Extraindo e carregando dados..."):
                    # try:
                        with open("temp_data.zip", "wb") as f:
                            f.write(zip_file.getbuffer())
                        
                        st.session_state.analyzer.extract_and_load_data(
                            zip_path="temp_data.zip"
                        )
                        
                        st.success("✅ Dados carregados com sucesso!")
                        data_loaded = True
                        
                    # except Exception as e:
                    #     st.error(f"❌ Erro ao carregar dados: {str(e)}")
        
        # Interface principal de chat
        if hasattr(st.session_state, 'analyzer') and st.session_state.analyzer.agent:
            
            # Resumo dos dados
            st.subheader("📈 Resumo dos Dados")
            summary = st.session_state.analyzer.get_data_summary()
            
            if "erro" not in summary:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total de Notas", summary['total_notas'])
                with col2:
                    st.metric("Total de Itens", summary['total_itens'])
                with col3:
                    st.metric("Fornecedores", summary['fornecedores_unicos'])
                with col4:
                    st.metric("Clientes", summary['clientes_unicos'])
                
                st.info(f"📅 Período: {summary['periodo']['inicio']} a {summary['periodo']['fim']}")
                st.info(f"💰 Valor Total: R$ {summary['valor_total_periodo']:,.2f}")
            
            st.markdown("---")
            
            # Interface de chat
            st.subheader("💬 Chat - Faça suas Perguntas")
            
            # Exemplos de perguntas
            with st.expander("💡 Exemplos de Perguntas"):
                st.markdown("""
                - Qual empresa mais gastou?
                - Quanto a empresa X gastou no total?
                - Qual foi o produto com maior quantidade vendida?
                - Quais são os 5 maiores fornecedores por valor?
                - Quantas notas foram emitidas em janeiro de 2024?
                - Qual o valor médio das notas fiscais?
                - Quais produtos têm NCM 49019900?
                """)
            
            # Input da pergunta
            user_question = st.text_input(
                "🔍 Sua pergunta:",
                placeholder="Ex: Qual empresa mais gastou?",
                key="user_input"
            )
            
            # Botão para processar pergunta
            if st.button("🚀 Perguntar") and user_question:
                with st.spinner("🤔 Analisando dados..."):
                    # try:
                        response = st.session_state.analyzer.ask_question(user_question)
                        
                        st.subheader("🤖 Resposta:")
                        st.write(response)
                        
                    # except Exception as e:
                    #     st.error(f"❌ Erro ao processar pergunta: {str(e)}")
            
            # Histórico de conversas
            if hasattr(st.session_state, 'analyzer') and st.session_state.analyzer.memory:
                history = st.session_state.analyzer.memory.chat_memory.messages
                if history:
                    with st.expander("📜 Histórico de Conversas"):
                        for i in range(0, len(history), 2):
                            if i + 1 < len(history):
                                st.write(f"**Você:** {history[i].content}")
                                st.write(f"**Assistente:** {history[i+1].content}")
                                st.markdown("---")
    
    else:
        st.warning("⚠️ Por favor, insira sua chave da API do OpenAI na barra lateral.")

# Função principal para executar o sistema
def main():
    """Função principal do sistema"""
    
    # Exemplo de uso programático
    if __name__ == "__main__":
        # Para usar via Streamlit: streamlit run script.py
        create_streamlit_app()
        
        # Exemplo de uso direto:
        """
        # Inicializa o analisador
        analyzer = NotasFiscaisAnalyzer("sua-api-key-aqui")
        
        # Carrega dados
        analyzer.extract_and_load_data(csv_paths={
            'cabecalho': 'caminho/para/cabecalho.csv',
            'itens': 'caminho/para/itens.csv'
        })
        
        # Faz perguntas
        resposta = analyzer.ask_question("Qual empresa mais gastou?")
        print(resposta)
        
        # Obtém resumo
        resumo = analyzer.get_data_summary()
        print(resumo)
        """

if __name__ == "__main__":
    main()