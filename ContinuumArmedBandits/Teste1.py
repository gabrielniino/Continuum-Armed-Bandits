import streamlit as st
import pandas as pd
import random

class CAB:
    def __init__(self):
        self.numero_bracos = None
        self.recompensas = {}
        self.constante_L = None

    @staticmethod
    def inserir_numero_bracos():
        numero_bracos = st.sidebar.number_input("Digite o número de braços:", min_value=1, max_value=10000, step=1)
        return numero_bracos

    @staticmethod
    def inserir_numero_rodadas():
        numero_rodadas = st.sidebar.number_input("Digite o número de rodadas:", min_value=1, max_value=10000, step=1)
        return numero_rodadas

    @staticmethod
    def inserir_constante_L():
        constante_L = st.sidebar.slider("Digite o valor da constante Lipschitz:", min_value=0.01, max_value=1.0, step=0.01)
        return constante_L

    @staticmethod
    def gerar_recompensa(num_rodadas, numero_bracos):
        recompensas = {}
        for braco in range(1, numero_bracos + 1):
            recompensas[braco] = [random.uniform(0, 1) for _ in range(num_rodadas)]
        return recompensas

    @staticmethod
    def calcular_media_recompensas(recompensas):
        medias = {}
        if recompensas:
            for braco, valores in recompensas.items():
                media = sum(valores) / len(valores)
                medias[braco] = media
        return medias

    def encontrar_braco_maior_media(self, medias):
        if medias:
            max_media = float('-inf')
            melhor_braco = None

            for braco, media in medias.items():
                if media > max_media:
                    max_media = media
                    melhor_braco = braco

            if melhor_braco is not None:
                st.write(f"Braço com a maior média de recompensas: Braço {melhor_braco} - Recompensa: {max_media}")
            else:
                st.write("Insira 2 ou mais braços para que o agente possa aplicar a condição Lipschitz")
        else:
            st.write("Nenhuma recompensa gerada.")

def main():
    st.sidebar.title("Inserir condições")
    cab = CAB()
    numero_bracos = cab.inserir_numero_bracos()
    numero_rodadas = cab.inserir_numero_rodadas()
    constante_L = cab.inserir_constante_L()
    recompensas = cab.gerar_recompensa(numero_rodadas, numero_bracos)
    medias = cab.calcular_media_recompensas(recompensas)

    botao_gerar = st.sidebar.button("Gerar resultados")

    if botao_gerar:
        
        # Dataframe gerar recompensa
        st.markdown("<h1 style='text-align: center; font-size: 30px;'>Braços e Recompensas</h1>", unsafe_allow_html=True)
        df_recompensas = pd.DataFrame(recompensas)
        df_recompensas.index = [f"Rodada {rodada}" for rodada in range(1, numero_rodadas + 1)]
        df_recompensas.columns = [f"Braço {braco}" for braco in df_recompensas.columns]

        # Verificar se o número de braços ou rodadas é maior ou igual a 10
        if numero_bracos >= 10 or numero_rodadas >= 10:
            # Adicionar barra de rolagem para as colunas
            df_recompensas_styled = df_recompensas.style\
                .set_table_styles([{"selector": ".colHeader", "props": [("max-width", "150px"), ("overflow", "auto")]}])\
                .set_properties(**{"max-height": "600px", "overflow": "auto"}, subset=pd.IndexSlice[:, :])

            st.dataframe(df_recompensas_styled)
        else:
            st.table(df_recompensas)

        # Dataframe média recompensa
        st.markdown("<h1 style='text-align: center; font-size: 30px;'>Recompensas médias</h1>", unsafe_allow_html=True)
        df_medias = pd.DataFrame({"Braço": list(medias.keys()), "Média de Recompensas": list(medias.values())})

        # Verificar se o número de braços é maior que 10
        if numero_bracos > 10:
            # Adicionar barra de rolagem para o dataframe df_medias
            df_medias_styled = df_medias.style\
                .set_properties(**{"max-height": "600px", "overflow": "auto"}, subset=pd.IndexSlice[:, :])
            st.dataframe(df_medias_styled)
        else:
            st.table(df_medias)

        # Encontrar braço com maior média
        cab.encontrar_braco_maior_media(medias)

if __name__ == "__main__":
    main()