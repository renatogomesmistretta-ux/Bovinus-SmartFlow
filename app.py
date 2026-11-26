import streamlit as st
import pandas as pd
from database import consultar_dados

st.set_page_config(
    page_title="BoviCore",
    page_icon="📊",
    layout="wide"
)

st.html("""
<div style="margin-bottom: 5px;">
    <span style="font-size:52px;font-weight:900;color:#FFFFFF;">BOVI</span><span style="font-size:52px;font-weight:900;color:#DC2626;">CORE</span>
</div>
<div style="font-size:19px;color:#D1D5DB;">
    Inteligência que transforma operações.
</div>
""")

st.caption("Plataforma de Inteligência Operacional e Financeira")
st.caption("Hackathon Tech FMU 2026.2 | Unidade Augusta")

st.divider()

dados = consultar_dados()
if dados.empty:
    st.warning("Nenhum registro disponível.")
    st.stop()

st.sidebar.markdown(
    """
    <div style="font-size:30px;font-weight:900;">
        BOVI<span style="color:#DC2626;">CORE</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.caption("Inteligência Operacional e Financeira")

st.sidebar.divider()

st.sidebar.header("Navegação")

st.sidebar.caption("BoviCore 2.0 • MVP acadêmico")

st.sidebar.caption("Selecione um módulo nas abas do painel.")
st.sidebar.divider()
with st.sidebar.expander("Metas gerenciais"):
    meta_margem = st.slider("Margem mínima (%)", 0, 100, 60)
    meta_desperdicio = st.slider("Desperdício máximo (%)", 0, 100, 5)
    limite_fila = st.slider("Espera crítica (min)", 3, 30, 5)
    cenario = st.selectbox("Cenário de filas", ["Base", "Pico (+50%)", "Melhoria (-30%)"])
st.sidebar.divider()

st.sidebar.header("Filtros")

setor = st.sidebar.selectbox(
    "Setor",
    ["Todos"] + sorted(dados["setor"].unique().tolist())
)

if setor != "Todos":
    dados = dados[dados["setor"] == setor]

def moeda(valor):
    return f"R$ {valor:,.2f}".replace(
        ",", "X"
    ).replace(".", ",").replace("X", ".")

with financeiro:
    # Indicadores financeiros

    receita = dados["receita_total"].sum()
    custo = dados["custo_total"].sum()
    margem = receita - custo
    margem_pct = margem / receita * 100 if receita else 0

    st.header("Indicadores Financeiros", anchor="indicadores-financeiros")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Receita estimada", moeda(receita))
    c2.metric("CMV estimado", moeda(custo))
    c3.metric("Margem estimada", moeda(margem))
    c4.metric("Margem percentual", f"{margem_pct:.1f}%")

    st.caption("Margem estimada = receita menos CMV; não representa lucro líquido.")
    st.divider()

    # Analise do mix de pratos

    st.header("Análise do Mix de Pratos", anchor="analise-do-mix-de-pratos")

    mix = dados.groupby("prato")[
        ["receita_total", "custo_total", "margem_contribuicao"]
