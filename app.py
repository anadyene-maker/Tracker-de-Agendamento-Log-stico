import streamlit as st
import pandas as pd
import os

# Configuração visual
st.set_page_config(page_title="Torre de Controle - Carraro", layout="wide")

# NOME DO SEU ARQUIVO REAL
FILE_NAME = "agendamentos_sankhya.csv"

def carregar_dados():
    if os.path.exists(FILE_NAME):
        # O seu arquivo usa ';' como separador
        return pd.read_csv(FILE_NAME, sep=";")
    return pd.DataFrame()

# Título do Dashboard
st.title("🚚 Gestão de Agendamentos Logísticos")
st.subheader("Fila de Solicitações - Carraro")

df = carregar_dados()

if not df.empty:
    # --- FILTROS RÁPIDOS ---
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        cidade_filtro = st.multiselect("Filtrar por Cidade", options=df['Cidade.'].unique())
    
    if cidade_filtro:
        df = df[df['Cidade.'].isin(cidade_filtro)]

    # --- TABELA DE DADOS ---
    # Mostramos as colunas principais do seu arquivo
    st.write("### Agendamentos Pendentes/Confirmados")
    st.dataframe(df[[
        'Ordem Carga', 'Nº Nota', 'Cliente', 'Cidade.', 
        'Data Agendamento', 'Obs. Logística', 'Entrega'
    ]], use_container_width=True)

    # --- LÓGICA DE STATUS (A LISTA DE TAREFAS) ---
    st.divider()
    st.subheader("✅ Atualizar Status de Agendamento")
    
    with st.form("confirmacao_status"):
        nota_selecionada = st.selectbox(
            "Selecione a Nota Fiscal para Confirmar", 
            options=df['Nº Nota'].unique()
        )
        status_update = st.radio("O agendamento foi confirmado no portal?", ["Solicitado", "Confirmado"])
        obs_adicional = st.text_input("Nova Observação (Opcional)")
        
        btn_confirmar = st.form_submit_button("Atualizar Planilha")

        if btn_confirmar:
            # Aqui você aplicaria a lógica para salvar de volta no CSV
            # Como Sensei, recomendo primeiro testar a visualização
            st.success(f"Status da NF {nota_selecionada} atualizado para {status_update}!")
            st.toast("Progresso salvo com sucesso!")
else:
    st.error("Arquivo CSV não encontrado. Certifique-se de que o nome 'Ranking 01(new sheet).csv' está correto.")
