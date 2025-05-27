from collections import deque, defaultdict

#visited = set()
def mais_frequente(g):
    def bfs(node, visited):
        queue = deque([node])
        visited.add(node)
        size = 0
        while queue:
            current = queue.popleft()
            size += 1
            print(f"Visiting: {current} ")
            for neighbour in g.get(current,[]):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)
                    print(f"  Queued: {neighbour}")
        return size

    visited = set()
    tamanho_comp = defaultdict(int)
    for node in g:
        if node not in visited:
            size = bfs(node,visited)
            tamanho_comp[size] += 1
    max_freq = max(tamanho_comp.values())
    most_freq = [size for size, freq in tamanho_comp.items() if freq == max_freq]
    return max(most_freq)


graph = {
    1: [2],
2: [1, 3],
3: [2],
4: [5],
5: [4, 6],
6: [5],
7: [8],
8: [7]
}

#print(mais_frequente(graph))



def cor_valida(g,colorir):
    def bfs(node, visited):
        queue = deque([node])
        visited.add(node)
        cor = colorir[node]
        while queue:
            current = queue.popleft()
            print(f"Visiting: {current} ")
            for neighbour in g.get(current,[]):
                if neighbour not in visited:
                    if colorir[neighbour] != cor:
                        return False
                    visited.add(neighbour)
                    queue.append(neighbour)
                    print(f"Queued: {neighbour}")
        return True

    visited = set()
    for node in g:
        if node not in visited:
            if not bfs(node,visited):
                return False
    return True


coloring = {
1: 'azul', 2: 'azul', 3: 'azul',
4: 'amarelo', 5: 'amarelo', 6: 'azul',
7: 'azul', 8: 'azul'
}

#print(cor_valida(graph, coloring))

def verifica_coloração(g, coloring):
    visited = set()

    def dfs(vertice, cor_ref):
        queue = deque([vertice])
        while queue:
            current = queue.pop()
            if current in visited:
                continue
            if coloring[current] != cor_ref:
                return False
            visited.add(current)
            for neighbour in g[current]:
                if neighbour not in visited:
                    queue.append(neighbour)
        return True

    for v in g:
        if v not in visited:
            cor_componente = coloring[v]
            if not dfs(v, cor_componente):
                return False
    return True

print(verifica_coloração(graph, coloring))



from collections import defaultdict, Counter

def componente_mais_frequente(grafo):
    visitado = set()

    def dfs(no):
        stack = [no]
        tamanho = 0
        while stack:
            atual = stack.pop()
            if atual not in visitado:
                visitado.add(atual)
                tamanho += 1
                stack.extend(grafo[atual])
        return tamanho

    tamanhos = []
    for no in grafo:
        if no not in visitado:
            tamanhos.append(dfs(no))
    
    frequencias = Counter(tamanhos)
    max_frequencia = max(frequencias.values())
    
    # Obter os tamanhos com frequência máxima
    candidatos = [t for t, f in frequencias.items() if f == max_frequencia]
    return max(candidatos)

# Exemplo de grafo baseado na imagem:
grafo = {
    1: [2],
    2: [1, 3],
    3: [2],
    4: [5],
    5: [4],
    6: [7],
    7: [6, 8],
    8: [7]
}

print(componente_mais_frequente(grafo)) 



def tamanho_maior_componente(grafo):
    visitado = set()

    def dfs(no):
        stack = [no]
        tamanho = 0
        while stack:
            atual = stack.pop()
            if atual not in visitado:
                visitado.add(atual)
                tamanho += 1
                stack.extend(grafo[atual])
        return tamanho

    maior = 0
    for no in grafo:
        if no not in visitado:
            maior = max(maior, dfs(no))
    
    return maior

# Exemplo de grafo baseado na imagem:
grafo = {
    1: [2],
    2: [1, 3],
    3: [2],
    4: [5],
    5: [4],
    6: [7],
    7: [6, 8],
    8: [7]
}

print(tamanho_maior_componente(grafo))  # Saída: 3