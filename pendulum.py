import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import norm

# ====================================================================
# FUNÇÕES DE ANÁLISE ESTATÍSTICA
# ====================================================================

def analise_estatistica(data):
    """Calcula a média, desvio padrão e desvio padrão da média."""
    N = len(data)
    media = np.mean(data)
    desvio_padrao = np.std(data, ddof=1) # ddof=1 para desvio padrão da amostra
    desvio_padrao_media = desvio_padrao / np.sqrt(N) # Expressão (5.66)
    
    return media, desvio_padrao, desvio_padrao_media

def metodo_agrupamento(data, n_grupos=10, n_medicoes_por_grupo=10):
    """
    Estima a incerteza pelo método de agrupamento (10 grupos de 10).
    Parte 1, Ponto 5.b)
    """
    if len(data) != n_grupos * n_medicoes_por_grupo:
        print("Aviso: O número de dados não corresponde ao total de grupos * medições.")
        return None, None

    # Redimensiona os 100 dados em 10 grupos de 10
    grupos = data.reshape(n_grupos, n_medicoes_por_grupo)
    
    # Calcula o valor médio de cada um dos 10 conjuntos
    medias_dos_grupos = np.mean(grupos, axis=1)
    
    # Calcula o desvio padrão dos 10 valores médios (incerteza estimada)
    dp_das_medias = np.std(medias_dos_grupos, ddof=1)
    
    return medias_dos_grupos, dp_das_medias

def calcula_g_e_incerteza(T, L, dT, dL):
    """
    Calcula a aceleração da gravidade (g) e a sua incerteza (dg).
    Parte 2 - Propagação da Incerteza.
    """
    # Fórmula: g = 4 * pi^2 * L / T^2
    g = 4 * (np.pi**2) * L / (T**2)
    
    # Fórmula de propagação da incerteza: 
    # (dg/g)^2 = (dL/L)^2 + (2 * dT/T)^2
    
    # Incerteza relativa ao quadrado
    incerteza_relativa_quadrado = (dL/L)**2 + 4 * (dT/T)**2
    
    dg = g * np.sqrt(incerteza_relativa_quadrado)
    
    return g, dg

# ====================================================================
# SIMULAÇÃO DE DADOS (Para Teste - SUBSTITUIR PELOS SEUS DADOS REAIS)
# ====================================================================

# Simula 100 medições de T (período) com média ~2.00s e desvio padrão ~0.05s
np.random.seed(42) # Para resultados reproduzíveis
T_100_medicoes = np.random.normal(loc=2.00, scale=0.05, size=100)

# Dados da Parte 2 (Medição de L)
L_pêndulo = 1.000 # Comprimento (em metros)
dL_pêndulo = 0.001 # Incerteza de L (1 mm, como sugerido)

# Dados da Parte 1, Ponto 6 (Medição de 10 oscilações repetida 10 vezes)
# t_10_oscilacoes: 10 medições do tempo total (em segundos) para 10 oscilações
t_10_oscilacoes = np.random.normal(loc=20.0, scale=0.1, size=10)


# ====================================================================
# EXECUTAR ANÁLISES (PARTE 1)
# ====================================================================

print("### 1. ANÁLISE DAS 100 MEDIÇÕES DIRETAS (T) ###")
T_media, T_dp, T_dp_media = analise_estatistica(T_100_medicoes)
print(f"Média (T): {T_media:.4f} s")
print(f"Desvio Padrão (σ): {T_dp:.4f} s")
print(f"Desvio Padrão da Média (σ<T>): {T_dp_media:.5f} s (Incerteza)")

print("\n### 2. ESTIMATIVA DA INCERTEZA PELO MÉTODO DE AGRUPAMENTO (10x10) ###")
medias_grupos, dp_agrupamento = metodo_agrupamento(T_100_medicoes)
print(f"Desvio Padrão das 10 Médias dos Grupos (Incerteza): {dp_agrupamento:.5f} s")
print(f"Comparar {T_dp_media:.5f} s com {dp_agrupamento:.5f} s")

print("\n### 3. CÁLCULO PELO MÉTODO DAS VÁRIAS OSCILAÇÕES (10x10) ###")
# t_10_oscilacoes/10 dá o T para cada uma das 10 medições
T_10x10_medicoes = t_10_oscilacoes / 10
T_media_10x10, T_dp_10x10, T_dp_media_10x10 = analise_estatistica(T_10x10_medicoes)
print(f"Média (T, 10x10): {T_media_10x10:.4f} s")
print(f"Desvio Padrão da Média (σ<T>, 10x10): {T_dp_media_10x10:.5f} s (Incerteza)")
print(f"Conclusão: A incerteza {T_dp_media_10x10:.5f} s deve ser menor que {T_dp_media:.5f} s")

# ====================================================================
# VISUALIZAÇÃO (HISTOGRAMA E AJUSTE GAUSSIANO)
# ====================================================================

# Função Gaussiana para ajuste
def gaussian(x, a, mu, sigma):
    return a * np.exp(-((x - mu) / sigma)**2 / 2)

# Gera o Histograma
n, bins, patches = plt.hist(T_100_medicoes, bins=15, density=True, alpha=0.6, color='g', label='Frequência de Medições')

# Ajuste da função Gaussiana
bin_centers = (bins[:-1] + bins[1:]) / 2
try:
    popt, pcov = curve_fit(gaussian, bin_centers, n, p0=[np.max(n), T_media, T_dp])
    
    # Plot da Gaussiana
    x_fit = np.linspace(min(T_100_medicoes), max(T_100_medicoes), 100)
    plt.plot(x_fit, gaussian(x_fit, *popt), 'r-', 
             label=f'Ajuste Gaussiano:\nμ={popt[1]:.4f}s, σ={np.abs(popt[2]):.4f}s')

except RuntimeError:
    print("\nAVISO: O ajuste da curva Gaussiana falhou.")


plt.title('Distribuição da Frequência do Período (T) e Ajuste Gaussiano')
plt.xlabel('Período T (s)')
plt.ylabel('Frequência Normalizada')
plt.legend()
plt.grid(True)
plt.show()


# ====================================================================
# EXECUTAR CÁLCULOS (PARTE 2)
# ====================================================================

print("\n### 4. CÁLCULO DA ACELERAÇÃO DA GRAVIDADE (g) ###")

# Usar a melhor estimativa de T e a incerteza correspondente
T_final = T_media_10x10 # A incerteza é menor no método 10x10, logo é a melhor estimativa
dT_final = T_dp_media_10x10

g_calc, dg_calc = calcula_g_e_incerteza(T_final, L_pêndulo, dT_final, dL_pêndulo)

print(f"Comprimento do Pêndulo (L): {L_pêndulo:.3f} ± {dL_pêndulo:.3f} m")
print(f"Período Estimado (T): {T_final:.4f} ± {dT_final:.5f} s")
print("-" * 50)
print(f"Aceleração da Gravidade (g) calculada: {g_calc:.4f} m/s²")
print(f"Incerteza de g (Δg): {dg_calc:.4f} m/s²")
print(f"Resultado Final: g = ({g_calc:.4f} ± {dg_calc:.4f}) m/s²")
print(f"Incerteza Relativa (Δg/g): {(dg_calc/g_calc)*100:.3f} %")

# Verifica se o objetivo de Δg/g < 0.1% foi atingido (como pedido no protocolo)
if (dg_calc/g_calc)*100 < 0.1:
    print("OBJETIVO ATINGIDO: Δg/g é menor que 0.1%.")
else:
    print("OBJETIVO NÃO ATINGIDO: É necessário mais medições para Δg/g ser menor que 0.1%.")