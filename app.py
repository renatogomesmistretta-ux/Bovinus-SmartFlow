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

st.sidebar.markdown("""
📊 [Visão financeira](#indicadores-financeiros)

🍽️ [Análise de pratos](#analise-do-mix-de-pratos)

📈 [Simulador de margem](#simulador-de-mix-e-margem)

⏱️ [Gestão de filas](#monitoramento-de-filas)

🪑 [Gestão de salões](#monitoramento-das-90-mesas)

♻️ [Buffet e desperdício](#controle-de-desperdicio)

🎯 [Central de inteligência](#central-de-inteligencia-operacional)

🗃️ [Base de dados](#base-de-dados-operacionais)
""")
- [Visão financeira](#indicadores-financeiros)
- [Análise de pratos](#analise-do-mix-de-pratos)
- [Simulador de margem](#simulador-de-mix-e-margem)
- [Gestão de filas](#monitoramento-de-filas)
- [Gestão de salões](#monitoramento-das-90-mesas)
- [Buffet e desperdício](#controle-de-desperdicio) - [Central de inteligência](#central-de-inteligencia-operacional)
- [Base de dados](#base-de-dados-operacionais)
""")

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

status_saloes = {}

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

    status_saloes[nome] = {
        "total": total,
        "ocupadas": ocupadas,
        "limpeza": limpeza,
        "livres": livres
    }

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

status_cubas = {}

for cuba in ["Saladas", "Pratos quentes", "Proteínas"]:

    nivel = st.slider(f"Nível da cuba - {cuba}", 0, 100, 70)

    status_cubas[cuba] = nivel

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

# Central de Inteligencia Operacional

st.divider()

st.header("Central de Inteligência Operacional")

st.caption(
    "Diagnóstico automatizado e recomendações gerenciais."
)

alertas = []

# Analise dos niveis das cubas

for cuba, nivel in status_cubas.items():

    if nivel <= 20:
        alertas.append(("Critico", cuba,
            f"Nível de {nivel}%. Realizar reposição imediata."))

    elif nivel <= 40:
        alertas.append(("Atencao", cuba,
            f"Nível de {nivel}%. Preparar reposição."))

    else:
        alertas.append(("Adequado", cuba,
            f"Nível de {nivel}%. Abastecimento adequado."))

# Analise de ocupacao dos saloes

for nome, info in status_saloes.items():

    ocupacao = info["ocupadas"] / info["total"] * 100

    if ocupacao >= 90 or info["livres"] == 0:
        alertas.append(("Critico", nome,
            f"Ocupação de {ocupacao:.1f}%. "
            f"Apenas {info['livres']} mesas disponíveis. Gerenciar fluxo de clientes."))

    elif info["limpeza"] >= 3:
        alertas.append(("Atencao", nome,
            f"{info['limpeza']} mesas aguardando limpeza. Acionar equipe de limpeza."))

    elif ocupacao >= 80:
        alertas.append(("Atencao", nome,
            f"Ocupação de {ocupacao:.1f}%. Monitorar disponibilidade."))

    else:
        alertas.append(("Adequado", nome,
            f"Ocupação de {ocupacao:.1f}%. "
            f"{info['livres']} mesas disponíveis."))

# Analise financeira

margem_atual = margem / receita * 100 if receita > 0 else 0

if receita <= 0:
    alertas.append(("Atencao", "Receita", 
        "Não há receita disponível para análise."))
elif margem_atual < 60:
    alertas.append(("Atencao", "Margem financeira",
        f"Margem de {margem_atual:.1f}%. Reavaliar custos e mix de pratos."))
else:
    alertas.append(("Adequado", "Margem financeira",
        f"Margem de {margem_atual:.1f}% dentro da meta."))

# Analise de filas

for nome, tempo in filas.items():

    if tempo >= 5:
        alertas.append(("Critico", nome,
            f"Espera de {tempo:.1f} minutos. Reforçar atendimento."))

    elif tempo >= 3:
        alertas.append(("Atencao", nome,
            f"Espera de {tempo:.1f} minutos. Monitorar fluxo."))

    else:
        alertas.append(("Adequado", nome,
            f"Espera de {tempo:.1f} minutos. Fluxo adequado."))

# Analise de desperdicio

if desperdicio > 5:
    alertas.append(("Atencao", "Desperdício",
        f"Índice de {desperdicio:.1f}%. Reavaliar produção e reposição."))
else:
    alertas.append(("Adequado", "Desperdício",
        f"Índice de {desperdicio:.1f}% dentro da meta."))

# Resumo gerencial

criticos = sum(a[0] == "Critico" for a in alertas)
atencao = sum(a[0] == "Atencao" for a in alertas)
adequados = sum(a[0] == "Adequado" for a in alertas)

c1, c2, c3 = st.columns(3)

c1.metric("Alertas críticos", criticos)
c2.metric("Pontos de atenção", atencao)
c3.metric("Indicadores adequados", adequados)

st.subheader("Recomendações gerenciais")

for prioridade in ["Critico", "Atencao", "Adequado"]:

    for status, titulo, mensagem in alertas:

        if status == prioridade:

            if status == "Critico":
                st.error(f"🔴 {titulo}: {mensagem}")

            elif status == "Atencao":
                st.warning(f"🟡 {titulo}: {mensagem}")

            else:
                st.success(f"🟢 {titulo}: {mensagem}")
