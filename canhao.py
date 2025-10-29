import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# CONSTANTES FÍSICAS
# ----------------------------------------------------------------------
# Aceleração da gravidade (m/s^2)
G = 9.81 

# ----------------------------------------------------------------------
# DADOS EXPERIMENTAIS DO UTILIZADOR
# NOTA: Os dados foram transcritos e convertidos de cm para metros (m).
# ----------------------------------------------------------------------
dados_exp = {
    '30': {
        'nominal_theta': 30.0,
        'X_cm': np.array([47.5, 52.5, 60, 80, 90, 100]),
        'Y_cm': np.array([38.5, 57.2, 36.3, 26.6, 21.2, 13.3])
    },
    '40': {
        'nominal_theta': 40.0,
        'X_cm': np.array([47.5, 52.5, 60, 70, 80, 90, 100]),
        'Y_cm': np.array([49.5, 48, 45.4, 40.8, 35.7, 28.3, 18.4])
    },
    '50': {
        'nominal_theta': 50.0,
        'X_cm': np.array([47.5, 52.5, 60, 70, 80, 90, 100]),
        'Y_cm': np.array([52.9, 53.7, 51.1, 45.6, 37.0, 27.2, 13.5])
    }
}

# ----------------------------------------------------------------------
# 1. FUNÇÃO DE AJUSTE (EQUAÇÃO DA TRAJETÓRIA)
# ----------------------------------------------------------------------
def equacao_trajetoria(x, y0, v0, theta_rad):
    """
    Equação da trajetória do projétil (y=f(x)):
    y = y0 + tg(theta) * x - 0.5 * g / (v0^2 * cos^2(theta)) * x^2
    """
    if v0 <= 0:
        # Retorna NaN para evitar erros de divisão por zero
        return np.full_like(x, np.nan)

    tan_theta = np.tan(theta_rad)
    cos_theta_sq = (np.cos(theta_rad))**2
    
    # Coeficiente do x^2
    coef_quadratico = (0.5 * G) / (v0**2 * cos_theta_sq)
    
    y = y0 + tan_theta * x - coef_quadratico * (x**2)
    return y

# ----------------------------------------------------------------------
# 2. ANÁLISE E AJUSTE PARA CADA ÂNGULO
# ----------------------------------------------------------------------
resultados_finais = {}
plt.figure(figsize=(15, 10)) # Define o tamanho total da figura para subplots

for i, (key, dados) in enumerate(dados_exp.items()):
    # Conversão para metros
    X_m = dados['X_cm'] / 100.0
    Y_m = dados['Y_cm'] / 100.0
    
    nominal_theta_rad = np.deg2rad(dados['nominal_theta'])
    
    # Estimativas Iniciais: [yo, v0, theta_rad]
    # yo estimado em 0.6m (valor típico para canhão de bancada)
    # v0 estimado em 4.5 m/s (ajustado de acordo com a nossa pré-análise)
    parametros_iniciais = [0.6, 4.5, nominal_theta_rad]

    try:
        # Realiza o ajuste de curva
        popt, pcov = curve_fit(
            equacao_trajetoria, 
            X_m, 
            Y_m, 
            p0=parametros_iniciais
        )

        y0_ajustado, v0_ajustado, theta_rad_ajustado = popt
        theta_graus_ajustado = np.rad2deg(theta_rad_ajustado)

        # Cálculo da incerteza (erro padrão)
        perr = np.sqrt(np.diag(pcov))
        incerteza_y0, incerteza_v0, incerteza_theta_rad = perr
        incerteza_theta_graus = np.rad2deg(incerteza_theta_rad)

        # Armazena os resultados
        resultados_finais[key] = {
            'y0': y0_ajustado, 'inc_y0': incerteza_y0,
            'v0': v0_ajustado, 'inc_v0': incerteza_v0,
            'theta_graus': theta_graus_ajustado, 'inc_theta_graus': incerteza_theta_graus
        }
        
        # ----------------------------------------------------------------------
        # GERAÇÃO DO GRÁFICO (SUBPLOT)
        # ----------------------------------------------------------------------
        ax = plt.subplot(2, 2, i + 1)
        
        # Cria curva suave do modelo
        x_modelo = np.linspace(0, np.max(X_m) * 1.05, 100)
        y_modelo = equacao_trajetoria(x_modelo, *popt)

        ax.scatter(X_m, Y_m, label='Dados Exp.', color='red', marker='o')
        ax.plot(x_modelo, y_modelo, label='Modelo Ajustado', color='blue', linestyle='--')
        
        ax.set_title(f'Trajetória para Ângulo Nominal {key}°')
        ax.set_xlabel('Distância Horizontal, x (m)')
        ax.set_ylabel('Altura, y (m)')
        ax.legend(title=f'v0 = {v0_ajustado:.3f} m/s\ny0 = {y0_ajustado:.3f} m')
        ax.grid(True, linestyle=':', alpha=0.6)

    except RuntimeError:
        print(f"\nERRO: Ajuste para {key}° falhou. Verifique dados ou estimativas iniciais.")
        
# Ajusta o layout para evitar sobreposição
plt.tight_layout()
plt.show()

# ----------------------------------------------------------------------
# 3. IMPRESSÃO DA TABELA DE RESULTADOS FINAIS
# ----------------------------------------------------------------------
print("\n" + "="*70)
print("             TABELA DE PARÂMETROS DE AJUSTE OBTIDOS")
print("="*70)
print("| Ângulo | Altura Inicial (y0) | Velocidade Inicial (v0) | Ângulo Ajustado (θ)")
print("| Nominal |      (m)            |        (m/s)            |      (graus)")
print("|---------|---------------------|-------------------------|--------------------")

for ang, res in resultados_finais.items():
    y0_str = f"{res['y0']:.4f} \u00B1 {res['inc_y0']:.4f}"
    v0_str = f"{res['v0']:.4f} \u00B1 {res['inc_v0']:.4f}"
    theta_str = f"{res['theta_graus']:.2f} \u00B1 {res['inc_theta_graus']:.2f}"
    
    print(f"| {ang.center(7)} | {y0_str.center(19)} | {v0_str.center(23)} | {theta_str.center(18)}")
print("="*70)
