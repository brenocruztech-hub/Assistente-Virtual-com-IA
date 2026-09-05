"""
Léo — Assistente de Orçamento Pessoal
=======================================

Aplicação funcional (Streamlit) que integra:
- Base de dados mockada (data/*.json)
- Motor de regras determinístico (motor_regras.py)
- Detecção de edge cases (edge_cases.py)
- Interface de chat com memória de contexto (st.session_state)

Para rodar:
    streamlit run app.py
"""

import json
import re
import streamlit as st

from motor_regras import analisar_orcamento
from edge_cases import verificar_edge_cases


# ---------------------------------------------------------------------------
# Carregamento de dados (uma vez por sessão)
# ---------------------------------------------------------------------------

def carregar_dados():
    with open("../data/dados_mockados.json", encoding="utf-8") as f:
        dados = json.load(f)
    with open("../data/limiares.json", encoding="utf-8") as f:
        limiares = json.load(f)
    with open("../data/base_conhecimento.json", encoding="utf-8") as f:
        base_conhecimento = json.load(f)
    return dados, limiares, base_conhecimento


if "inicializado" not in st.session_state:
    dados, limiares, base_conhecimento = carregar_dados()

    st.session_state.limiares = limiares
    st.session_state.base_conhecimento = base_conhecimento
    st.session_state.renda_mensal = None
    st.session_state.despesas_informadas = []
    st.session_state.historico = []
    st.session_state.inicializado = True


# ---------------------------------------------------------------------------
# Parser simples de linguagem natural (extrai valores e categorias)
# ---------------------------------------------------------------------------

CATEGORIAS_CONHECIDAS = [
    "aluguel", "alimentacao", "transporte", "cartao_credito", "lazer", "assinaturas"
]

APELIDOS_CATEGORIA = {
    "cartão": "cartao_credito", "cartao": "cartao_credito",
    "comida": "alimentacao", "mercado": "alimentacao",
    "uber": "transporte", "onibus": "transporte", "ônibus": "transporte",
}


def extrair_renda(mensagem: str):
    if "recebo" in mensagem.lower() or "renda" in mensagem.lower():
        match = re.search(r"(\d+[.,]?\d*)", mensagem)
        if match:
            return float(match.group(1).replace(",", "."))
    return None


def extrair_despesa(mensagem: str):
    match_valor = re.search(r"(\d+[.,]?\d*)", mensagem)
    if not match_valor:
        return None

    valor = float(match_valor.group(1).replace(",", "."))
    mensagem_lower = mensagem.lower()

    for categoria in CATEGORIAS_CONHECIDAS:
        if categoria.replace("_", " ") in mensagem_lower or categoria in mensagem_lower:
            return {"categoria": categoria, "valor": valor}

    for apelido, categoria in APELIDOS_CATEGORIA.items():
        if apelido in mensagem_lower:
            return {"categoria": categoria, "valor": valor}

    return None


# ---------------------------------------------------------------------------
# Geração de resposta (fluxo normal, sem edge case)
# ---------------------------------------------------------------------------

def processar_mensagem(mensagem: str) -> str:
    renda_extraida = extrair_renda(mensagem)
    if renda_extraida:
        st.session_state.renda_mensal = renda_extraida
        return (
            f"Entendi, anotei sua renda: R$ {renda_extraida:.2f}. Agora me "
            f"conta, quais são suas despesas fixas?"
        )

    despesa_extraida = extrair_despesa(mensagem)
    if despesa_extraida:
        st.session_state.despesas_informadas.append(despesa_extraida)

        if st.session_state.renda_mensal is None:
            return (
                "Anotei essa despesa! Mas antes de eu calcular alguma coisa, "
                "me conta: qual sua renda mensal?"
            )

        resultado = analisar_orcamento(
            st.session_state.despesas_informadas,
            st.session_state.renda_mensal,
            st.session_state.limiares,
        )

        categoria_legivel = despesa_extraida["categoria"].replace("_", " ")
        resposta = f"Anotado! {categoria_legivel.capitalize()}: R$ {despesa_extraida['valor']:.2f}. "

        # Se essa categoria específica está fora do padrão, inclui o alerta
        for item in resultado["detalhamento"]:
            if item["categoria"] == despesa_extraida["categoria"] and item["status"] == "fora_do_padrao":
                resposta += (
                    f"Só um ponto que percebi: isso é {item['percentual_renda']}% "
                    f"da sua renda — um pouco acima do que costuma ser saudável "
                    f"({item['limiar']}%). Não é motivo pra alarme, só algo "
                    f"pra gente ficar de olho junto."
                )
                break
        else:
            resposta += "Isso está dentro do esperado pra sua renda. Tem mais alguma despesa?"

        return resposta

    return (
        "Não consegui identificar um valor ou categoria nessa mensagem. "
        "Pode me contar de novo, tipo 'gasto 500 com alimentação'?"
    )


# ---------------------------------------------------------------------------
# Interface Streamlit
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Léo — Assistente de Orçamento", page_icon="💰")
st.title("💰 Léo — Assistente de Orçamento Pessoal")
st.caption(
    "Uso educativo, não substitui um consultor financeiro certificado. "
    "Não compartilhe dados sensíveis como número de cartão ou CPF."
)

for autor, texto in st.session_state.historico:
    with st.chat_message(autor):
        st.write(texto)

if not st.session_state.historico:
    saudacao = (
        "Oi! Eu sou o Léo, vou te ajudar a organizar suas contas com calma, "
        "sem julgamento. Pode me contar o que está rolando no seu orçamento?"
    )
    st.session_state.historico.append(("assistant", saudacao))
    st.rerun()

mensagem_usuario = st.chat_input("Digite sua mensagem...")

if mensagem_usuario:
    st.session_state.historico.append(("user", mensagem_usuario))

    contexto = {"renda_mensal": st.session_state.renda_mensal}
    resposta_edge_case = verificar_edge_cases(mensagem_usuario, contexto)

    if resposta_edge_case:
        resposta = resposta_edge_case
    else:
        resposta = processar_mensagem(mensagem_usuario)

    st.session_state.historico.append(("assistant", resposta))
    st.rerun()
