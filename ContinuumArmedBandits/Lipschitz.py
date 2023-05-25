import numpy as np

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
        print(f"Rodada {t+1}: Recompensa do Braço {braco+1} = {recompensa}, Arrependimento = {arrependimento[t]}")

    # Calcula a porcentagem de escolha de cada braço
    porcentagem_escolha = n_selecoes / np.sum(n_selecoes)

    # Imprime a porcentagem de escolha de cada braço
    print("Porcentagem de Escolha dos Braços:")
    for braco in range(num_bracos):
        print(f"Braço {braco+1}: {porcentagem_escolha[braco]*100}%")

    # Retorna as estimativas médias de recompensa para os braços e o arrependimento
    recompensas_medias = recompensas / n_selecoes

    return recompensas_medias, arrependimento, n_selecoes

def simular_recompensa(braco):
    media = 0.5
    desvio_padrao = 0.1
    return np.random.normal(media, desvio_padrao)

# Exemplo de uso
num_bracos = 2
num_iteracoes = 5
constante_lipschitz = 1.0
parametro_exploracao = 2.0

recompensas_medias, arrependimento, n_selecoes = banditos_armados_continuos(num_bracos, num_iteracoes, constante_lipschitz, parametro_exploracao)

# Imprime a recompensa média para cada braço
print("Recompensas Médias para os Braços:")
for braco in range(num_bracos):
    print(f"Braço {braco+1}: {recompensas_medias[braco]}")

# Imprime o número de vezes que cada braço foi selecionado
print("Número de Seleções para os Braços:")
for braco in range(num_bracos):
    print(f"Braço {braco +1}: {n_selecoes[braco]}")

# Imprime o arrependimento final
print("Arrependimento:")
for t in range(num_iteracoes):
    print(f"Rodada {t+1}: {arrependimento[t]}")

# Imprime o braço com a maior recompensa média
melhor_braco = np.argmax(recompensas_medias)
print(f"Braço com maior recompensa média: {melhor_braco+1}")
