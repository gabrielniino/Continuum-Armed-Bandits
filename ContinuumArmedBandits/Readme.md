# Responsabilidades

## Definição das funções

- calcular_limite_lipschitz: Calcula o limite de Lipschitz entre dois pontos.
- exploracao_ucb: Realiza a exploração UCB para selecionar o braço com o maior Upper Confidence Bound.
- banditos_armados_continuos: Implementa o algoritmo de bandit armado contínuo com exploração UCB. Realiza as iterações, - seleciona os braços e atualiza as estimativas de recompensa.
- simular_recompensa: Simula a recompensa de um braço selecionado.

## Interface do Streamlit

### Configuração do layout da página do Streamlit com st.set_page_config

- Criação de um menu lateral com parâmetros para o número de braços, número de iterações, constante de Lipschitz e parâmetro de exploração.
- Exibição das tabelas de recompensas médias e número de seleções usando st.dataframe ou st.table.
- Exibição de um gráfico de linha com o arrependimento usando st.line_chart.
- Exibição do braço com a maior recompensa média na tela principal do Streamlit com st.write.
