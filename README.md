# 💰 Léo — Assistente Virtual de Orçamento Pessoal

Assistente conversacional que ajuda pessoas endividadas ou com dificuldade de controle financeiro a organizar receitas e despesas, entender para onde vai o dinheiro, e identificar de forma proativa quando um gasto está fora do padrão saudável.

Projeto desenvolvido para o Lab **"Construa Seu Assistente Virtual Com Inteligência Artificial"**.

## 📁 Estrutura do projeto

```
assistente-virtual-ia/
  README.md
  data/
    dados_mockados.json      # renda e despesas simuladas
    limiares.json            # regras de % máximo por categoria
    base_conhecimento.json   # FAQ de conceitos financeiros
  docs/
    documentacao.md          # persona, problema, arquitetura, componentes
    prompts.md                # system prompt e exemplos de interação
    avaliacao.md              # critérios e resultados de teste
    pitch.md                  # apresentação final do projeto
  src/
    app.py                    # aplicação Streamlit (interface de chat)
    motor_regras.py           # cálculo determinístico de % e status
    edge_cases.py              # detecção das 5 situações-limite
```

## 🚀 Como rodar

```bash
cd src
pip install streamlit
streamlit run app.py
```

## 📖 Os 6 passos do desafio

1. **Documentação** → [`docs/documentacao.md`](./docs/documentacao.md)
2. **Base de Conhecimento** → [`data/`](./data/)
3. **Prompts** → [`docs/prompts.md`](./docs/prompts.md)
4. **Aplicação Funcional** → [`src/`](./src/)
5. **Avaliação e Métricas** → [`docs/avaliacao.md`](./docs/avaliacao.md)
6. **Pitch** → [`docs/pitch.md`](./docs/pitch.md)

## 🧠 Resumo rápido

- **Nome:** Léo
- **Problema:** planejamento de orçamento pessoal
- **Público-alvo:** pessoas endividadas ou com dificuldade de controle financeiro
- **Diferencial:** alerta proativo de padrão de gasto + motor de regras determinístico (sem alucinação de números)
- **Personalidade:** acolhedor, paciente, propositivo, transparente
