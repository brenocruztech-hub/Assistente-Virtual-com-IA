# 🚀 Pitch — Léo, Assistente de Orçamento Pessoal

## O problema

Muitas pessoas endividadas não têm clareza de para onde vai o próprio dinheiro. Ferramentas tradicionais (planilhas, apps financeiros complexos) exigem disciplina e conhecimento técnico que parte desse público não tem — ou não quer ter. O resultado é evitar olhar para o problema, o que só o agrava.

## A solução

O Léo é um assistente conversacional que elimina essa barreira: a pessoa só precisa contar, em linguagem natural, quanto ganha e quanto gasta. O Léo organiza essas informações, calcula automaticamente se cada categoria de gasto está saudável em relação à renda, e — de forma proativa — avisa quando algo foge do padrão, sem esperar ser perguntado.

## Por que funciona

- **Barreira de entrada quase zero**: conversa, não planilha.
- **Proatividade**: identifica problemas antes que o usuário precise procurá-los.
- **Tom acolhedor**: pensado especificamente para um público que já se sente vulnerável ao falar de dinheiro — nunca julga, sempre propõe.
- **Confiável**: todo número vem de um motor de regras determinístico, nunca "inventado" por IA — resolvendo o principal medo de usar IA em finanças (alucinação).

## Para quem

Pessoas endividadas ou com dificuldade de controle financeiro que já buscam ajuda ativamente, mas se sentem intimidadas por ferramentas financeiras tradicionais.

## Como foi construído

- **Base de conhecimento**: dados mockados de receitas/despesas + limiares de alerta + FAQ de conceitos financeiros (`data/`)
- **Motor de regras**: cálculo determinístico de percentual de renda por categoria (`src/motor_regras.py`)
- **Edge cases**: tratamento de 5 situações-limite (número inventado, contradição, fora de escopo, dado sensível, sofrimento emocional) (`src/edge_cases.py`)
- **Aplicação**: interface de chat em Streamlit com memória de contexto (`src/app.py`)

## Demonstração

```
Usuário: recebo 3000 por mês
Léo: Entendi, anotei sua renda: R$ 3000.00. Agora me conta, quais são suas despesas fixas?

Usuário: gasto 800 no cartão de crédito
Léo: Anotado! Cartao credito: R$ 800.00. Só um ponto que percebi: isso é 26.7%
     da sua renda — um pouco acima do que costuma ser saudável (20%). Não é
     motivo pra alarme, só algo pra gente ficar de olho junto.
```

## Próximos passos

- Integrar um LLM real (Ollama, local) para tornar a conversa mais natural fora do roteiro testado.
- Expandir a base de conhecimento com mais conceitos financeiros.
- Testar com usuários reais para validar o tom e a utilidade percebida.
