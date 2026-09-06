"""
Edge Cases do Léo
=================

Implementa a árvore de decisão do diagrama Mermaid: antes de seguir o fluxo
normal do agente (organizar dados -> motor de regras -> resposta), a
mensagem do usuário passa por essas verificações, na ordem definida.

Cada função de detecção retorna True/False. A função verificar_edge_cases()
percorre todas na ordem e devolve a resposta pronta assim que uma bater --
ou None se nenhuma bater (sinal para seguir o fluxo normal).
"""


def pede_numero_inventado(mensagem: str) -> bool:
    """Detecta se o usuário está pedindo um valor 'chutado', sem dado real."""
    gatilhos = ["chuta", "chute", "estimativa", "não precisa ser exato", "arredonda"]
    mensagem = mensagem.lower()
    return any(g in mensagem for g in gatilhos)


def contradiz_contexto(mensagem: str, contexto: dict) -> tuple[bool, str]:
    """
    Detecta se um valor mencionado contradiz algo já registrado no contexto.
    Versão simplificada: compara apenas a renda mensal, como exemplo.
    Retorna (True, mensagem_de_confirmacao) ou (False, "").
    """
    import re

    renda_anterior = contexto.get("renda_mensal")
    if renda_anterior is None:
        return False, ""

    match = re.search(r"(\d+)\s*(?:reais|por mês|mensal)?", mensagem.lower())
    if match and "recebo" in mensagem.lower():
        novo_valor = float(match.group(1))
        if novo_valor != renda_anterior:
            return True, (
                f"Percebi essa diferença também. Só pra eu ter certeza e não "
                f"bagunçar as contas: sua renda mensal é R$ {novo_valor:.2f} "
                f"ou R$ {renda_anterior:.2f}? Pode ser que tenha mudado, ou "
                f"que um dos dois estava errado — sem problema, só preciso "
                f"confirmar antes de seguir."
            )
    return False, ""


def pede_conselho_fora_de_escopo(mensagem: str) -> bool:
    """Detecta pedido de recomendação de investimento específico."""
    gatilhos = ["ação da bolsa", "qual ação", "indica uma ação", "onde investir", "que investimento"]
    mensagem = mensagem.lower()
    return any(g in mensagem for g in gatilhos)


def contem_dado_sensivel(mensagem: str) -> bool:
    """Detecta menção a número de cartão, CPF ou conta bancária."""
    import re
    # Sequência de 4+ dígitos junto de palavras como "cartão", "final", "cpf", "conta"
    padrao_numero = re.search(r"\d{4,}", mensagem)
    palavras_sensiveis = ["cartão", "final", "cpf", "conta", "agência"]
    mensagem_lower = mensagem.lower()
    return bool(padrao_numero) and any(p in mensagem_lower for p in palavras_sensiveis)


def indica_sofrimento_emocional(mensagem: str) -> bool:
    """
    Detecta sinais de sofrimento emocional sério que exigem interromper
    o fluxo financeiro e priorizar o encaminhamento de ajuda.
    """
    gatilhos = [
        "não aguento mais", "quero sumir", "seria mais fácil se eu",
        "não vejo saída", "quero desistir de tudo", "não vale a pena viver"
    ]
    mensagem = mensagem.lower()
    return any(g in mensagem for g in gatilhos)


def verificar_edge_cases(mensagem: str, contexto: dict) -> str | None:
    """
    Percorre os edge cases na ordem do diagrama. Retorna a resposta pronta
    do primeiro caso que bater, ou None se nenhum bateu (segue fluxo normal).
    """

    # Edge case mais crítico primeiro: sofrimento emocional sempre tem prioridade
    if indica_sofrimento_emocional(mensagem):
        return (
            "Eu realmente sinto muito que você esteja passando por um "
            "momento tão pesado assim — isso é muito mais importante do "
            "que qualquer conta ou planilha agora. Eu não sou a pessoa "
            "certa pra te ajudar com o que você está sentindo, e eu me "
            "preocupo com você: por favor, considere conversar com o "
            "Centro de Valorização da Vida (CVV), pelo telefone 188, "
            "disponível 24h — eles têm gente preparada pra te ouvir de "
            "verdade agora. Podemos voltar às finanças quando fizer "
            "sentido pra você, sem pressa nenhuma."
        )

    if pede_numero_inventado(mensagem):
        return (
            "Entendo a vontade de ter uma resposta rápida, mas prefiro ser "
            "honesto com você: eu não trabalho com 'chute' quando o "
            "assunto é seu dinheiro, mesmo que pareça mais prático agora. "
            "Se você me passar os dados certos, eu calculo certinho em "
            "segundos."
        )

    contradiz, resposta_contradicao = contradiz_contexto(mensagem, contexto)
    if contradiz:
        return resposta_contradicao

    if pede_conselho_fora_de_escopo(mensagem):
        return (
            "Isso já foge um pouco do que eu posso te ajudar com "
            "segurança — recomendação de investimento específico exige "
            "análise de perfil de risco e não é algo que eu, como "
            "assistente educativo, devo te indicar. O que eu posso fazer "
            "é te ajudar a pensar em quanto desse valor faz sentido "
            "guardar como reserva antes de pensar em investir."
        )

    if contem_dado_sensivel(mensagem):
        return (
            "Só um aviso: não preciso nem guardo número de cartão, CPF ou "
            "conta — pode ficar tranquilo em me contar só os valores e "
            "categorias dos gastos, isso já é o suficiente pra eu te "
            "ajudar."
        )

    return None  # nenhum edge case bateu -> segue fluxo normal do agente


if __name__ == "__main__":
    contexto_exemplo = {"renda_mensal": 3000.0}

    testes = [
        "só me dá uma estimativa aí, não precisa ser exato",
        "recebo 2500 por mês",
        "me indica uma ação da bolsa pra investir",
        "meu cartão é o final 4521, gastei 800 nele",
        "não aguento mais essa dívida, às vezes penso que seria mais fácil se eu sumisse",
        "gastei 300 com mercado esse mês",  # nenhum edge case -> fluxo normal
    ]

    for msg in testes:
        resultado = verificar_edge_cases(msg, contexto_exemplo)
        print(f"Mensagem: {msg}")
        print(f"Edge case disparado: {'Sim' if resultado else 'Não'}")
        if resultado:
            print(f"Resposta: {resultado}")
        print("-" * 60)
