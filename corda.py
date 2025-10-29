import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# --- CONSTANTES GLOBAIS ---
g = 9.81  # Aceleração da gravidade (m/s^2)

# Valores de literatura do ANEXO A para comparação na Parte B
LITERATURA_VB = {
    "Vidro (Pyrex)": 5640,
    "Vidro (Flint)": 4000,
    "Ferro": 5130,
    "Cobre": 3560,
    "Latão": 4700,
    "Alumínio": 5100
}

# --- PARTE A: CORDA VIBRANTE ---
def parte_a_corda_vibrante_analise():
    """
    Realiza a análise da Parte A (Corda Vibrante) com os dados fornecidos.
    O foco é o gráfico $f^2 = g(T)$ para determinar a massa linear ($\mu$).
    """
    print("=" * 60)
    print("### PARTE A: CORDA VIBRANTE - ANÁLISE DE DADOS ###")
    print("=" * 60)

    # --- Dados de Entrada do Novo Protocolo ---
    
    # Comprimento do fio (l) em metros - **VALOR ASSUMIDO (0.80 m)!**
    L = 0.80  
    print(f"-> Comprimento do fio (L) ASSUMIDO: {L:.2f} m")
    
    # Conversão das massas de gramas para kg e cálculo da Tensão (T = m*g)
    massas_g = np.array([100, 200, 300, 400, 500])
    T_exp = (massas_g / 1000) * g  # Tensão em Newtons (N)
    
    # Frequências em Hz para o MODO FUNDAMENTAL (n=1)
    n_fixo = 1
    f_exp = np.array([21.215, 28.25, 32.30, 36.50, 40.80])
    f_quadrado = f_exp**2

    # --- Análise: Gráfico de $f^2 = g(T)$ para n Fixo ---
    # $f^2 = \left(\frac{n^2}{4L^2\mu}\right) \cdot T \quad \rightarrow \quad y = \text{slope} \cdot x$
    
    # 1. Ajuste linear para $f^2 = g(T)$
    slope, intercept = np.polyfit(T_exp, f_quadrado, 1)
    
    # 2. Determinação da Massa Linear ($\mu$)
    # $\mu = \frac{n^2}{4L^2 \cdot \text{slope}}$
    mu_calculado = (n_fixo**2) / (4 * L**2 * slope)

    # --- Resultados ---
    print("\n--- Resultados do Ajuste Linear $f^2 = g(T)$ ---")
    print(f"Modo de Vibração (n) fixo: n = {n_fixo}")
    print(f"Coeficiente angular (slope): {slope:.3f} $Hz^2/N$")
    print(f"Interceção: {intercept:.3f} $Hz^2$")
    print(f"**Massa Linear ($\mu$) calculada**: {mu_calculado * 1000:.3f} g/m (ou {mu_calculado:.6f} kg/m)")

    # 3. Determinação da Velocidade da Onda ($v$)
    # $v = \sqrt{T/\mu}$
    v_exp = np.sqrt(T_exp / mu_calculado)
    v_media = np.mean(v_exp)
    print(f"Velocidade Média da Onda ($v$) calculada: {v_media:.3f} m/s")
    
    # --- Gráfico de $f^2 = g(T)$ ---
    plt.figure(figsize=(10, 6))
    plt.plot(T_exp, f_quadrado, 'o', label=f'Dados Experimentais (n={n_fixo})')
    
    # Linha de ajuste
    T_fit = np.linspace(min(T_exp) * 0.9, max(T_exp) * 1.1, 100)
    f_quadrado_fit = slope * T_fit + intercept
    plt.plot(T_fit, f_quadrado_fit, '-', label=f'Ajuste Linear: $f^2 = {slope:.2f}T + {intercept:.2f}$')
    
    plt.title(f'Quadrado da Frequência ($f^2$) vs. Tensão (T) para n={n_fixo} ($L={L:.2f}m$ ASSUMIDO)')
    plt.xlabel('Tensão, T (N)')
    plt.ylabel('Frequência ao Quadrado, $f^2 (Hz^2)$')
    plt.grid(True)
    plt.legend()
    plt.show()


# --- PARTE B: TUBO DE KUNDT ---
def parte_b_tubo_de_kundt_analise():
    """
    Realiza a análise da Parte B (Tubo de Kundt) com os dados fornecidos.
    Determina a velocidade do som no ar (v_ar) e na haste (v_b).
    """
    print("\n" + "=" * 60)
    print("### PARTE B: TUBO DE KUNDT - ANÁLISE DE DADOS ###")
    print("=" * 60)

    # --- Dados de Entrada do Novo Protocolo ---
    dist_nodos_cm = 8.5
    dist_nodos_m = dist_nodos_cm / 100.0  # $\text{m}$
    
    L_haste_cm = 60.0
    L_haste_m = L_haste_cm / 100.0 # $\text{m}$
    
    T_sala_celsius = 23.0 
    
    print(f"-> Distância média entre Nodos ($\lambda_{{ar}}/2$): {dist_nodos_cm} cm")
    print(f"-> Comprimento da Haste ($L_b = \lambda_b$): {L_haste_cm} cm")
    print(f"-> Temperatura da Sala (T): {T_sala_celsius:.1f} °C")

    # --- Análise e Cálculo ---
    
    # 1. Velocidade do Som no Ar ($v_{ar}$) a partir da temperatura (Equação 10: $v_{ar} = 331.45 + 0.6 \cdot T[^{\circ}C]$) 
    v_ar_calc_temp = 331.45 + 0.6 * T_sala_celsius
    
    # 2. Comprimento de Onda no Ar ($\lambda_{ar} = 2 \times \text{distância entre nodos}$) 
    lambda_ar = 2 * dist_nodos_m 
    
    # 3. Frequência da Onda ($f = v_{ar} / \lambda_{ar}$) (Equação 6) 
    f = v_ar_calc_temp / lambda_ar
    
    # 4. Comprimento de Onda na Haste ($\lambda_b = L_b$) 
    lambda_b = L_haste_m
    
    # 5. Velocidade do Som na Haste ($v_b = f \times \lambda_b$) (Equação 7) 
    v_b_calc = f * lambda_b

    # --- Resultados ---
    print("\n--- Resultados da Análise de Kundt ---")
    print(f"Velocidade do Som no Ar (por T): $v_{{ar}} = {v_ar_calc_temp:.3f} m/s")
    print(f"Comprimento de Onda no Ar ($\lambda_{{ar}}$): {lambda_ar:.3f} m")
    print(f"**Frequência da Onda ($f$)**: {f:.3f} Hz")
    print(f"Comprimento de Onda na Haste ($\lambda_{{b}}$): {lambda_b:.3f} m")
    print(f"**Velocidade do Som na Haste ($v_{{b}}$)**: {v_b_calc:.3f} m/s")
    
    # 6. Comparação com a Literatura (ANEXO A)
    print("\n--- Comparação para Identificação do Material (ANEXO A) ---")
    
    df_comparacao = pd.DataFrame(
        list(LITERATURA_VB.items()), columns=['Material', '$v_{b, lit}$ (m/s)'])
    df_comparacao['$v_{b, calc}$ (m/s)'] = v_b_calc
    df_comparacao['Desvio %'] = (np.abs(v_b_calc - df_comparacao['$v_{b, lit}$ (m/s)']) / df_comparacao['$v_{b, lit}$ (m/s)']) * 100
    
    df_comparacao = df_comparacao.round(2)
    df_comparacao['Desvio %'] = df_comparacao['Desvio %'].astype(str) + '%'
    df_comparacao.sort_values(by='Desvio %', inplace=True)

    print(df_comparacao.to_markdown(index=False))


# --- Execução do Programa ---
if __name__ == "__main__":
    
    # Configurar para que os números de ponto flutuante sejam exibidos com clareza
    np.set_printoptions(precision=4, suppress=True)

    # Executa a análise para a Parte A - Corda Vibrante
    parte_a_corda_vibrante_analise()
    
    # Executa a análise para a Parte B - Tubo de Kundt
    parte_b_tubo_de_kundt_analise()