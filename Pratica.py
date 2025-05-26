def contar_7():
    termos = [2]
    termo = 2
    for _ in range(20):
        termo += 7
        termos.append(termo)
    return termos

# Exemplo de uso
#print(contar_7())



def contar():
    termos = [1,2]
    for _ in range(18):
        termo = termos[-1] * termos[-2]
        termos.append(termo)
    return termos

# Exemplo de uso
#print(contar())


def somaPares(l,x):
    for i in range(len(l)-1):
        for j in range(i+1,len(l)):
            if l[i] + l[j]== x:
                return True
    return False
#print(somaPares([1,2,3,-1], 2))


def hist2list(h):
    lista = []
    for k,v in sorted(h.items()):
        lista += [k] *v
    return lista

#print(hist2list({10:4,20:2}))


def is_valid_coloring(graph, coloring):
    for node in graph:
        for neighbor in graph[node]:
            if coloring[node] == coloring[neighbor]:
                return False
    return True

# Example graph (adjacency list)
graph = {
    1: [2, 3],
    2: [1, 3],
    3: [1, 2],
    4: [5],
    5: [4],
    6: [7],
    7: [6, 8],
    8: [7]
}

# Example coloring
coloring = {
    1: 'azul',
    2: 'amarelo',
    3: 'verde',
    4: 'azul',
    5: 'amarelo',
    6: 'verde',
    7: 'azul',
    8: 'verde'
}

coloring2 = {
    1:'azul',
    2:'azul',
    3:'azul',
    4:'amarelo',
    5:'amarelo',
    6:'azul',
    7:'azul',
    8:'azul'
    }

# Check if the coloring is valid’
is_valid = is_valid_coloring(graph, coloring2)

# Print the result
print(f"The coloring is {'valid' if is_valid else 'invalid'}.")

import matplotlib.pyplot as plt
import numpy as np

# Criação do grid de traço (tau) e determinante (delta)
traco = np.linspace(-5, 5, 400)
det = np.linspace(-5, 5, 400)
T, D = np.meshgrid(traco, det)

# Discriminante
disc = T**2 - 4*D

# Criar a figura
fig, ax = plt.subplots(figsize=(10, 8))

# Plotar regiões com diferentes classificações
# Sela: delta < 0
saddle = D < 0
ax.contourf(T, D, saddle, levels=[0.5, 1], colors=['#fbb4ae'], alpha=0.6)

# Nó real (estável ou instável): delta > 0, discriminante > 0
node_real = (D > 0) & (disc > 0)
ax.contourf(T, D, node_real, levels=[0.5, 1], colors=['#b3cde3'], alpha=0.6)

# Espiral (estável ou instável): delta > 0, discriminante < 0
spiral = (D > 0) & (disc < 0)
ax.contourf(T, D, spiral, levels=[0.5, 1], colors=['#ccebc5'], alpha=0.6)

# Centro: delta > 0, discriminante < 0, traço = 0
ax.plot(0, 1, 'ko', label='Centro (traço = 0)')

# Linhas de referência
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)
ax.plot(traco, (traco**2)/4, 'k--', label=r'$D=0$ (raízes reais iguais)')  # Discriminante = 0

# Anotações das regiões
ax.text(-4, 3, 'Nodo estável\n(valores próprios reais < 0)', fontsize=10)
ax.text(2.2, 3, 'Nodo instável\n(valores próprios reais > 0)', fontsize=10)
ax.text(-4.5, -3, 'Sela\n(valores próprios reais de sinais opostos)', fontsize=10)
ax.text(-3.5, 1.5, 'Espiral estável\n(complexos, parte real < 0)', fontsize=10)
ax.text(1.0, 1.5, 'Espiral instável\n(complexos, parte real > 0)', fontsize=10)

# Rótulos e título
ax.set_xlabel('Traço (t)', fontsize=12)
ax.set_ylabel('Determinante (det)', fontsize=12)
ax.set_title('Diagrama Traço-Determinante para Sistemas Lineares 2x2', fontsize=14)
ax.legend()
ax.grid(True)

#plt.show()


def coloração_valida(grafo, coloração):
    visitados = set()

    def dfs(vértice, componente):
        visitados.add(vértice)
        componente.append(vértice)
        for vizinho in grafo.get(vértice, []):
            if vizinho not in visitados:
                dfs(vizinho, componente)

    for vértice in grafo:
        if vértice not in visitados:
            componente = []
            dfs(vértice, componente)
            cores = {coloração[v] for v in componente}
            if len(cores) > 1:
                return False
    return True

     


print(coloração_valida(graph,coloring2))