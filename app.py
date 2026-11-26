import streamlit as st
import pandas as pd
from database import consultar_dados

st.set_page_config(
    page_title="BoveCore",
    page_icon="📊",
    layout="wide"
)

st.html("""
    <div style="margin-bottom: 5px;">
        <span style="font-size: 52px; font-weight: 900; color: #FFFFFF;">BOVE</span><span style="font-size: 52px; font-weight: 900; color: #DC2626;">CORE</span>
    </div>
    <div style="font-size: 19px; color: #D1D5DB;">
        Inteligência que transforma operações.
    </div>
""")

st.caption("Plataforma de Inteligência Operacional e Financeira")
st.caption("Hackathon Tech FMU 2026.2 | Bovinu's Grill & Beer — Unidade Augusta")

st.divider()
        <span style="font-size: 52px; font-weight: 900; color: #FFFFFF;">BOVI</span><span style="font-size: 52px; font-weight: 900; color: #DC2626;">360</span>
    </div>
    <div style="font-size: 19px; color: #D1D5DB;">
        Plataforma de Inteligência Operacional e Financeira
    </div>
""")

st.caption("Hackathon Tech FMU 2026.2 | Bovinu's Grill & Beer — Unidade Augusta")

st.divider()

dados = consultar_dados()

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

# Indicadores financeiros

receita = dados["receita_total"].sum()
custo = dados["custo_total"].sum()
margem = receita - custo
margem_pct = margem / receita * 100 if receita else 0

st.header("Indicadores Financeiros")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Receita estimada", moeda(receita))
c2.metric("CMV estimado", moeda(custo))
c3.metric("Margem estimada", moeda(margem))
c4.metric("Margem percentual", f"{margem_pct:.1f}%")

st.divider()

# Analise do mix de pratos

st.header("Análise do Mix de Pratos")

mix = dados.groupby("prato")[
    ["receita_total", "custo_total", "margem_contribuicao"]
].sum()

st.bar_chart(
    mix,
    stack=False,
    color=["#DC2626", "#9CA3AF", "#22C55E"]
)
st.dataframe(mix, use_container_width=True)

# Simulador de pesagem

st.header("Simulador de Mix e Margem")

peso = st.slider("Peso do prato em gramas", 100, 1500, 500)

proteina = st.slider("Percentual de proteínas", 0, 100, 40)

preco_kg = st.number_input(
    "Preço por quilo (R$)", min_value=1.0, value=85.0
)

peso_kg = peso / 1000

receita_prato = peso_kg * preco_kg

custo_prato = peso_kg * (
    (proteina / 100) * 59
    + (1 - proteina / 100) * 19
)

margem_prato = receita_prato - custo_prato

c1, c2, c3 = st.columns(3)

c1.metric("Valor do prato", moeda(receita_prato))
c2.metric("Custo estimado", moeda(custo_prato))
c3.metric("Margem estimada", moeda(margem_prato))

st.divider()

# Monitoramento de filas

st.header("Monitoramento de Filas")

filas = dados.groupby("setor")["tempo_minutos"].mean()

st.bar_chart(filas)

for nome, tempo in filas.items():

    if tempo >= 5:
        st.error(f"🔴 {nome}: {tempo:.1f} minutos")

        if nome == "Caixa":
            st.warning("Recomendação: abrir caixa auxiliar.")

    elif tempo >= 3:
        st.warning(f"🟡 {nome}: {tempo:.1f} minutos")

    else:
        st.success(f"🟢 {nome}: {tempo:.1f} minutos")

st.divider()

# Monitoramento dos saloes

st.header("Monitoramento das 90 Mesas")

st.caption("Simulação interativa da ocupação dos salões.")

saloes = {
    "Principal": 30,
    "Pista/Inferior": 20,
    "Superior": 40
}

for nome, total in saloes.items():

    st.subheader(nome)

    ocupadas = st.slider(
        f"Mesas ocupadas - {nome}",
        0, total, int(total * 0.7)
    )

    limpeza = st.slider(
        f"Aguardando limpeza - {nome}",
        0, total - ocupadas, 0
    )

    livres = total - ocupadas - limpeza

    c1, c2, c3 = st.columns(3)

    c1.metric("Ocupadas", ocupadas)
    c2.metric("Limpeza pendente", limpeza)
    c3.metric("Disponíveis", livres)

    st.progress(ocupadas / total)

    html = """
    <div style="display:grid;
    grid-template-columns:repeat(10,1fr);
    gap:8px;margin:15px 0;">
    """

    for mesa in range(1, total + 1):

        if mesa <= ocupadas:
            cor = "#DC2626"
            status = "Ocupada"

        elif mesa <= ocupadas + limpeza:
            cor = "#EAB308"
            status = "Aguardando limpeza"

        else:
            cor = "#22C55E"
            status = "Disponível"

        html += f"""
        <div title="Mesa {mesa}: {status}"
        style="background:{cor};
        padding:12px 2px;
        border-radius:6px;
        text-align:center;
        font-weight:bold;
        color:#111111;">
        {mesa:02d}
        </div>
        """

    html += "</div>"

    st.html(html)

    st.caption(
        "🟢 Disponível | 🔴 Ocupada | 🟡 Limpeza pendente"
    )

    if limpeza >= 3:
        st.warning("Acionar equipe de limpeza.")

st.divider()

# Desperdicio e reposicao

st.header("Desperdício e Reposição")

producao = st.number_input(
    "Alimentos produzidos (kg)", min_value=1.0, value=100.0
)

sobras = st.number_input(
    "Sobras de alimentos (kg)",
    min_value=0.0,
    max_value=producao,
    value=min(5.0, producao)
)

desperdicio = sobras / producao * 100

st.metric("Índice de desperdício", f"{desperdicio:.1f}%")

if desperdicio > 5:
    st.warning("Reavaliar produção e reposição.")

for cuba in ["Saladas", "Pratos quentes", "Proteínas"]:

    nivel = st.slider(f"Nível da cuba - {cuba}", 0, 100, 70)

    if nivel <= 20:
        st.error(f"Reposição necessária: {cuba}")

    elif nivel <= 40:
        st.warning(f"Monitorar reposição: {cuba}")

    else:
        st.success(f"Nível adequado: {cuba}")

st.divider()

# Base de dados

st.header("Base de Dados Operacionais")

st.dataframe(dados, use_container_width=True)

st.download_button(
    "Exportar dados em CSV",
    dados.to_csv(index=False).encode("utf-8"),
    "relatorio_smartflow.csv",
    "text/csv"
)

st.info(
    "MVP acadêmico com dados sintéticos e simulações "
    "interativas. Não conectado à operação real do restaurante."
)
