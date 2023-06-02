import streamlit as st
import pandas as pd
import numpy as np

def main():

    def calcular_limite_lipschitz(constante_lipschitz, x, y):
        return constante_lipschitz * np.abs(x - y)

    def exploracao_ucb(estimativas_recompensa, n_selecoes, parametro_exploracao, constante_lipschitz, t):
        termo_exploracao = np.sqrt(np.log(t + 1) / n_selecoes)
        limites_superiores_confianca = estimativas_recompensa + parametro_exploracao * termo_exploracao

        # Aplica a condição de Lipschitz aos limites superiores de confiança
        for i in range(len(limites_superiores_confianca)):
            for j in range(i+1, len(limites_superiores_confianca)):
                limite_lipschitz = calcular_limite_lipschitz(constante_lipschitz, i, j)
                limites_superiores_confianca[i] = min(limites_superiores_confianca[i], limites_superiores_confianca[j] + limite_lipschitz)
                limites_superiores_confianca[j] = min(limites_superiores_confianca[j], limites_superiores_confianca[i] + limite_lipschitz)

        return np.argmax(limites_superiores_confianca)

    def banditos_armados_continuos(num_bracos, num_iteracoes, constante_lipschitz, parametro_exploracao):
        recompensas = np.zeros(num_bracos)
        n_selecoes = np.zeros(num_bracos)
        arrependimento = np.zeros(num_iteracoes)

        melhor_braco = np.random.randint(num_bracos)  # Escolhe aleatoriamente o melhor braço
        melhor_recompensa = simular_recompensa(melhor_braco)

        dados_rodadas = []

        for t in range(num_iteracoes):
            if t < num_bracos:
                # Exploração inicial: seleciona cada braço pelo menos uma vez
                braco = t
            else:
                # Seleciona o braço com o maior Upper Confidence Bound (UCB)
                braco = exploracao_ucb(recompensas, n_selecoes, parametro_exploracao, constante_lipschitz, t)

            # Simula a recompensa do braço selecionado
            recompensa = simular_recompensa(braco)

            # Atualiza as estimativas de recompensa e o número de seleções do braço
            recompensas[braco] = (recompensas[braco] * n_selecoes[braco] + recompensa) / (n_selecoes[braco] + 1)
            n_selecoes[braco] += 1

            # Calcula o arrependimento
            arrependimento[t] = melhor_recompensa - recompensa

            # Exibe a recompensa do braço selecionado e o índice da rodada
            dados_rodada = {"Rodada": t+1, "Braço": braco+1, "Recompensa": recompensa}
            dados_rodadas.append(dados_rodada)

        # Exibir a tabela de recompensas de cada rodada
        st.title("Recompensas por Rodada")
        df = pd.DataFrame(dados_rodadas)
        st.table(df)

        # Retorna as estimativas médias de recompensa para os braços e o arrependimento
        recompensas_medias = recompensa / n_selecoes

        return recompensas_medias, arrependimento, n_selecoes

    def simular_recompensa(braco):
        media = 0.5
        desvio_padrao = 0.1
        return np.random.normal(media, desvio_padrao)     

    # LAYOUT
    # Configurando a largura do menu lateral
    st.set_page_config(layout="wide")

    # Criando um menu lateral vazio
    st.sidebar.title("Insira os parametros")

    # Input para o número de braços
    num_bracos = st.sidebar.number_input("Número de Braços", min_value=1, max_value=10000, step=1)

    # Input para o número de iterações
    num_iteracoes = st.sidebar.number_input("Número de Iterações", min_value=1, max_value=10000, step=1)

    # Input para a constante de Lipschitz
    constante_lipschitz = st.sidebar.slider("Constante de Lipschitz", min_value=0.01, step=0.1)

    # Input para o parâmetro de exploração
    parametro_exploracao = st.sidebar.slider("Parâmetro de Exploração", min_value=0.01, max_value=1.00, step=0.1)

    # Botão para iniciar o algoritmo
    if st.sidebar.button("Iniciar Algoritmo"):
        recompensas_medias, arrependimento, n_selecoes = banditos_armados_continuos(num_bracos, num_iteracoes, constante_lipschitz, parametro_exploracao)

        # Criar um DataFrame para as recompensas médias
        st.title("Média")
        data = []
        for braco in range(num_bracos):
            data.append({"Braço": braco+1, "Recompensa Média": recompensas_medias[braco]})
        df = pd.DataFrame(data)

        # Exibir a tabela de recompensas médias
        # Verificar se é necessário adicionar um botão de rolagem
        if num_bracos > 10:
            st.write("Recompensas médias:")
            st.dataframe(df, height=400)  # Altura da tabela é definida como 400 pixels
        else:
            st.table(df)

        # Criar um DataFrame para o número de seleções
        st.title("Seleções")
        data = []
        for braco in range(num_bracos):
            data.append({"Braço": braco+1, "Número de Seleções": n_selecoes[braco]})
        df = pd.DataFrame(data)

        # Exibir a tabela de número de seleções
        # Verificar se é necessário adicionar um botão de rolagem
        if num_bracos > 10:
            st.write("Número de Seleções para os Braços:")
            st.dataframe(df, height=400)  # Altura da tabela é definida como 400 pixels
        else:
            st.table(df)

        # Criar uma lista com os dados do arrependimento
        st.title("Arrependimento")
        dados_arrependimento = []
        for t in range(num_iteracoes):
            dados_arrependimento.append({"Rodada": t+1, "Arrependimento": arrependimento[t]})

        # Exibir o gráfico de linha com o arrependimento
        st.line_chart(dados_arrependimento, x="Rodada", y="Arrependimento")

        # Encontre o braço com a maior recompensa média
        melhor_braco = np.argmax(recompensas_medias)

        # Exibir o braço com a maior recompensa média na tela principal do Streamlit
        st.write(f"Braço com maior recompensa média: {melhor_braco+1}")

if __name__ == "__main__":
    main()