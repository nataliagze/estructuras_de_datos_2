import heapq
import collections
from pyvis.network import Network

# Usamos heapq para la cola de prioridad de Dijkstra
# Usamos collections.deque para la cola de BFS

class Grafo:
    """
    Representa el mapa como un grafo.
    Usa una lista de adyacencia (diccionario).
    """
    def __init__(self):
        # El grafo se guarda como:
        # { 'ciudad_A': [('ciudad_B', 100), ('ciudad_C', 200)], ... }
        self.adj = {}

    def agregar_ciudad(self, ciudad):
        """Agrega un nodo (ciudad) al grafo."""
        if ciudad not in self.adj:
            self.adj[ciudad] = []

    def agregar_carretera(self, origen, destino, kilometros):
        """Agrega una arista ponderada (carretera)[cite: 5, 8]."""
        # Nos aseguramos que ambas ciudades existan
        self.agregar_ciudad(origen)
        self.agregar_ciudad(destino)
        
        # Grafo no dirigido, agregamos en ambas direcciones
        self.adj[origen].append((destino, kilometros))
        self.adj[destino].append((origen, kilometros))

    def obtener_ciudades(self):
        """Devuelve la lista de todas las ciudades."""
        return list(self.adj.keys())

    def encontrar_ruta_bfs(self, inicio, fin):
        """
        Encuentra el camino más corto en número de paradas (BFS)[cite: 7, 13, 16].
        Ignora los pesos (kilómetros).
        """
        if inicio not in self.adj or fin not in self.adj:
            return None, 0

        cola = collections.deque([(inicio, [inicio])]) # (nodo_actual, camino_hasta_aqui)
        visitados = set([inicio])

        while cola:
            (ciudad_actual, camino) = cola.popleft()

            if ciudad_actual == fin:
                return camino, len(camino) - 1 # Retorna la ruta y el número de paradas

            # Ver vecinos (solo nos importa el nombre, no el peso)
            for vecino, _ in self.adj[ciudad_actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    nuevo_camino = list(camino)
                    nuevo_camino.append(vecino)
                    cola.append((vecino, nuevo_camino))
        
        return None, 0 # No se encontró ruta

    def encontrar_ruta_dijkstra(self, inicio, fin):
        """
        Encuentra el camino de costo mínimo en kilómetros (Dijkstra).
        """
        if inicio not in self.adj or fin not in self.adj:
            return None, 0

        # (costo_acumulado, ciudad_actual, camino_hasta_aqui)
        cola_prioridad = [(0, inicio, [inicio])]
        distancias = {ciudad: float('inf') for ciudad in self.adj}
        distancias[inicio] = 0
        
        visitados = set()

        while cola_prioridad:
            (costo_actual, ciudad_actual, camino) = heapq.heappop(cola_prioridad)

            if ciudad_actual in visitados:
                continue # Ya encontramos un camino mejor a este nodo

            visitados.add(ciudad_actual)

            if ciudad_actual == fin:
                return camino, costo_actual # ¡Ruta encontrada!

            for vecino, peso in self.adj[ciudad_actual]:
                if vecino not in visitados:
                    nuevo_costo = costo_actual + peso
                    if nuevo_costo < distancias[vecino]:
                        distancias[vecino] = nuevo_costo
                        nuevo_camino = list(camino)
                        nuevo_camino.append(vecino)
                        heapq.heappush(cola_prioridad, (nuevo_costo, vecino, nuevo_camino))

        return None, 0 # No se encontró ruta

    def generar_dot(self):
        """Genera un string en formato DOT para Graphviz."""
        dot = "graph OptiRuta {\n"
        dot += "  node [shape=circle, style=filled, fillcolor=lightblue];\n"
        dot += "  edge [fontcolor=darkblue];\n"
        
        aristas_procesadas = set()

        for origen, conexiones in self.adj.items():
            for (destino, peso) in conexiones:
                # Evitar duplicados en grafo no dirigido (A--B y B--A)
                if (destino, origen) not in aristas_procesadas:
                    dot += f'  "{origen}" -- "{destino}" [label="{peso}km"];\n'
                    aristas_procesadas.add((origen, destino))
        
        dot += "}"
        return dot

    def generar_mapa_interactivo(self, nombre_archivo="mapa_rutas.html"):
        """
        Genera un mapa HTML interactivo usando pyvis.
        """
        net = Network(height="750px", width="100%", heading="Mapa de Rutas - OptiRuta")

        # 1. Añadir los nodos (ciudades)
        for ciudad in self.adj.keys():
            net.add_node(ciudad, label=ciudad, title=f"Ciudad: {ciudad}")

        # 2. Añadir las aristas (carreteras)
        aristas_procesadas = set()
        for origen, conexiones in self.adj.items():
            for (destino, peso) in conexiones:
                # Evitar duplicados (A--B y B--A)
                if (destino, origen) not in aristas_procesadas:
                    net.add_edge(
                        origen, 
                        destino, 
                        label=f"{peso}km", 
                        value=peso, # 'value' puede usarse para el grosor
                        title=f"{peso}km" # Tooltip al pasar el mouse
                    )
                    aristas_procesadas.add((origen, destino))

        # 3. Añadir botones para manipular la física (¡muy educativo!)
        net.show_buttons(filter_=['physics'])

        # 4. Guardar el archivo HTML
        try:
            net.save_graph(nombre_archivo)
            return nombre_archivo
        except Exception as e:
            print(f"Error al generar el mapa HTML: {e}")
            return None