"""
Motor de Regras do Léo
=======================

Componente determinístico: calcula percentuais de renda por categoria e
decide se cada uma está "dentro do esperado" ou "fora do padrão", com base
nos limiares definidos em data/limiares.json.

Nenhum número aqui vem do LLM -- tudo é calculado em Python puro, o que
elimina o risco de "alucinação" nos valores mostrados ao usuário.
"""


def calcular_percentuais(despesas: list[dict], renda_mensal: float) -> list[dict]:
    """
    Recebe a lista de despesas (cada uma com 'categoria' e 'valor') e a
    renda mensal, devolve uma lista com o percentual de renda que cada
    categoria representa.
    """
    resultado = []
    for despesa in despesas:
        percentual = (despesa["valor"] / renda_mensal) * 100
        resultado.append({
            "categoria": despesa["categoria"],
            "valor": despesa["valor"],
            "percentual_renda": round(percentual, 1)
        })
    return resultado


def classificar_status(percentuais: list[dict], limiares: dict) -> list[dict]:
    """
    Compara cada percentual calculado com o limiar da categoria
    correspondente (data/limiares.json) e marca como 'dentro_do_esperado'
    ou 'fora_do_padrao'.
    """
    limiares_pct = limiares["limiares_percentuais_da_renda"]
    resultado = []
    for item in percentuais:
        limiar = limiares_pct.get(item["categoria"])
        if limiar is None:
            status = "sem_limiar_definido"
        elif item["percentual_renda"] > limiar:
            status = "fora_do_padrao"
        else:
            status = "dentro_do_esperado"

        resultado.append({**item, "limiar": limiar, "status": status})
    return resultado


def gerar_alertas(dados_classificados: list[dict]) -> list[str]:
    """
    Gera as mensagens de alerta proativo (usando o template de prompts.md)
    para cada categoria marcada como 'fora_do_padrao'.
    """
    alertas = []
    for item in dados_classificados:
        if item["status"] == "fora_do_padrao":
            categoria_legivel = item["categoria"].replace("_", " ")
            alertas.append(
                f"Percebi que {categoria_legivel} está em "
                f"{item['percentual_renda']}% da sua renda esse mês — um "
                f"pouco acima do que costuma ser saudável ({item['limiar']}%). "
                f"Não é motivo pra alarme, só um ponto pra gente ficar de "
                f"olho junto. Quer que eu te ajude a pensar numa forma de "
                f"reduzir isso aos poucos?"
            )
    return alertas


def analisar_orcamento(despesas: list[dict], renda_mensal: float, limiares: dict) -> dict:
    """Função de conveniência: roda o pipeline completo de uma vez."""
    percentuais = calcular_percentuais(despesas, renda_mensal)
    classificados = classificar_status(percentuais, limiares)
    alertas = gerar_alertas(classificados)
    return {
        "detalhamento": classificados,
        "alertas": alertas,
        "total_despesas": sum(d["valor"] for d in despesas),
        "saldo": renda_mensal - sum(d["valor"] for d in despesas)
    }


if __name__ == "__main__":
    import json

    with open("../data/dados_mockados.json", encoding="utf-8") as f:
        dados = json.load(f)
    with open("../data/limiares.json", encoding="utf-8") as f:
        limiares = json.load(f)

    resultado = analisar_orcamento(
        dados["despesas"], dados["sessao"]["renda_mensal"], limiares
    )

    print(f"Total de despesas: R$ {resultado['total_despesas']:.2f}")
    print(f"Saldo: R$ {resultado['saldo']:.2f}\n")

    for item in resultado["detalhamento"]:
        print(f"- {item['categoria']}: {item['percentual_renda']}% "
              f"(limiar {item['limiar']}%) -> {item['status']}")

    print("\nAlertas gerados:")
    for alerta in resultado["alertas"]:
        print(f"⚠️  {alerta}\n")
