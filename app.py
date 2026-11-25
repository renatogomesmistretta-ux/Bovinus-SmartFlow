import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Bovinu's SmartFlow",
    page_icon="🥩",
    layout="wide"
)

# Título
st.title("🥩 Bovinu's SmartFlow & Margin Analytics")
st.subheader("Monitoramento operacional — Unidade Augusta")

st.info(
    "Projeto desenvolvido para o Hackathon Tech FMU 2026.2. "
    "Este dashboard utiliza dados demonstrativos."
)

# Indicadores principais
st.header("Indicadores Operacionais")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Clientes simulados", "1.240")
col2.metric("Ticket médio", "R$ 85,00")
col3.metric("Tempo médio de fila", "12 min")
col4.metric("Ocupação das mesas", "68%")

st.divider()

# Análise do mix de pratos
st.header("Análise do Mix de Pratos")

dados_mix = pd.DataFrame({
    "Perfil": [
        "Saladas e acompanhamentos",
        "Mix equilibrado",
        "Proteínas nobres"
    ],
    "Quantidade": [320, 450, 280],
    "Custo estimado (R$)": [19.00, 35.60, 59.00],
    "Receita estimada (R$)": [42.50, 42.50, 42.50]
})

st.bar_chart(
    dados_mix.set_index("Perfil")["Quantidade"]
)

st.dataframe(
    dados_mix,
    use_container_width=True,
    hide_index=True
)

st.divider()

# Monitoramento das filas
st.header("Monitoramento de Filas")

dados_filas = pd.DataFrame({
    "Etapa": ["Balança", "Churrasqueira", "Caixa"],
    "Tempo (minutos)": [6.5, 5.5, 5.0]
})

st.bar_chart(
    dados_filas.set_index("Etapa")
)

st.dataframe(
    dados_filas,
    use_container_width=True,
    hide_index=True
)

st.divider()

# Status da operação
st.header("Alertas Operacionais")

col1, col2, col3 = st.columns(3)

col1.warning("⚠️ Balança: fila acima do ideal")
col2.warning("⚠️ Churrasqueira: monitorar atendimento")
col3.success("✅ Monitoramento do salão ativo")

st.divider()

# Status das mesas
st.header("Monitoramento das Mesas")

dados_mesas = pd.DataFrame({
    "Salão": ["Principal", "Pista/Inferior", "Superior"],
    "Total de mesas": [30, 20, 40],
    "Mesas ocupadas": [22, 14, 28],
    "Mesas disponíveis": [8, 6, 12]
})

st.bar_chart(
    dados_mesas.set_index("Salão")[
        ["Mesas ocupadas", "Mesas disponíveis"]
    ]
)

st.dataframe(
    dados_mesas,
    use_container_width=True,
    hide_index=True
)

# Rodapé
st.caption(
    "Hackathon Tech FMU 2026.2 | Ciência de Dados e Inteligência Artificial | "
    "Dados demonstrativos, não reais."
)
