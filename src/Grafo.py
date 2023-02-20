class Grafo:
    """
    Estructura de datos que representa un grafo a traves del uso de listas de adyacencia, donde cada lista representa un nodo y cada elemento de cada lista representa el numero del nodo o los hijos a los que estan conectados cada uno

    Atributos:
        - nodos

    Metodos:
        + Grafo(nodes: list[list[int]])
        + get_node(node: int): list[int]
        - paths_recursively(current_node: int, objective_node: int, paths: list[list[int]], path = 0) : tuple[list[list[int]], int]
        + paths(self, start: int, end: int) : list[list[int]]
        + shortest_path(self, start: int, end: int) : list[int]
        + breadth_first_search(self, start: int, end: int) : list[int]
        
    """
    def __init__(self, nodes: list[list[int]]) -> None:
        """
        Constructor donde se especifica el orden y estructura del grafo

        Args:
            nodes (list[list[int]]): _description_ Capa posicion en la lista de listas es cada grafo, y cada sublista es es sus hijos
        """
        self.__nodos = nodes

    def get_node(self, node: int) -> list[int]:
        return self.__nodos[node]

    def __paths_recursively(self, current_node: int, objective_node: int, paths: list[list[int]], path = 0) -> tuple[list[list[int]], int]:
        """
        Retorna todos los caminos posibles desde un punto o nodo inicial hasta el nodo objetivo o hasta que llegue a un nodo hoja

        Args:
            current_node (int): _description_ Nodo en el que se encuentra en el grafo
            objective_node (int): _description_ Nodo final al que se desea llegar
            paths (list[list[int]]): _description_ Lista de caminos posibles
            path (int, optional): _description_. Defaults to 0. Numero de camino posible, sirve como indice para la lista de caminos

        Returns:
            tuple[list[list[int]], int]: _description_ Retorna los caminos y el numero de caminos
        """
        # Si un no ya ha sido recorrido
        if current_node in paths[path]:
            return paths, path + 1

        # Agregamos el nodo que estamos accediendo al recorrido
        paths[path].append(current_node)

        # Si el nodo a recorrer es el nodo objetivo
        if current_node == objective_node:
            return paths, path + 1
        
        # Si el nodo tiene uno o mas de un hijo
        for son_node in self.__nodos[current_node]:
            path = self.__paths_recursively(son_node, objective_node, paths, path)[1]
            
            # Es el ultimo hijo del nodo
            if son_node == self.__nodos[current_node][-1]:
                return paths, path

            # Creando un nuevo camino
            paths.append([])
            
            # Itera la rama padre
            i = 0
            # Punto de quiebre con el nodo padre del nodo actual
            node = -1

            # Copiando la rama padre
            while node != current_node:
                # Agregando al nuevo camino los nodos recorridos anteriores a esta nueva ramificacion
                paths[path].append(paths[path - 1][i])
                # Avanzamos al siguiente nodo en la lista recorrida
                node = paths[path - 1][i]
                # Incrementamos la posicion de la lista de nodos recorridos
                i += 1

        return paths, path + 1

    def paths(self, start: int, end: int) -> list[list[int]]:
        """
        Retorna todos los caminos posibles desde un nodo inicial hasta un nodo final

        Args:
            start (int): _description_ Nodo o punto inicial desde donde se generaran los caminos
            end (int): _description_ Nodo o punto final hasta donde debe recorrerse el camino

        Returns:
            list[list[int]]: _description_ Caminos posibles desde el nodo inicial hasta el nodo final
        """
        # Calculamos todos los caminos por los que se puede mover en el grafo desde el nodo inicial hasta los nodos hoja
        # La funcion retorna la lista de caminos y el numero de caminos, usamos [0] para obtener solo la lista de caminos
        paths_founded = self.__paths_recursively(start, end, [[]])[0]
        
        # Listado de caminos que llegan al nodo final
        valid_paths = list[list[int]]()
        # Obtenemos cada camino posible del grafo
        for path in paths_founded:
            # Un camino es valido si su valor final es el nodo final especificado por parametro
            if len(path) >= 0 and path[-1] == end:
                # Agregamos el camino que llega al nodo final
                valid_paths.append(path)
    
        return valid_paths
    
    def shortest_path(self, start: int, end: int) -> list[int]:
        """
        Retorna el camino mas corto de un nodo a otro dentro de un grafo. Retorna [] si no hay camino

        Args:
            start (int): _description_ Nodo de donde se parte
            end (int): _description_ Nodo final a donde desea llegar

        Returns:
            list[int]: _description_
        """
        # Todos los caminos que llevan del nodo start hasta el nodo end
        paths = self.paths(start, end)

        # Numero de camino mas corto
        shortest = 0

        # Recorremos cada camino posible
        for path in range(1, len(paths)):
            # Camino nuevo es mas corto que el anterior
            if len(paths[path]) < len(paths[shortest]):
                # Elegimos el nuevo camino mas corto
                shortest = path

        return paths[shortest]
    
    def breadth_first_search(self, start: int, end: int) -> list[int]:
        """
        Retorna el primer camino desde el nodo start hasta el nodo end

        Args:
            start (int): _description_ Nodo desde donde empieza el recorrido por el grafo
            end (int): _description_ Nodo donde termina el recorrido del grafo

        Returns:
            list[int]: _description_ Recorrido en orden por cada nodo hasta llegar al nodo end. Retorna [] si no hay camino disponible
        """
        # Camino desde start a end
        paths = [[int(start)]]
        # Lista de nodos visitados
        visited_nodes = list[int]()
        # Nodos vecinos por visitar de cada nodo
        queue = list[int]()
        
        # Se recorrera los nodos vecinos de start
        queue.append(start)
        # Nodo start ya se ha visitado
        visited_nodes.append(start)

        last_path = 0

        # Mientras haya nodos vecinos por recorrer
        while len(queue) > 0:
            # Seleccionamos cada nodo no visitado en el orden que se encuentran
            current_node = queue.pop(0)
            
            # Recorremos todas las rutas para ver con cual conecta
            for path in paths:
                # Verificamos el nodo de conexion directa al nodo actual
                for node in path:
                    # Sigue la conexion del ultimo nodo
                    if current_node in self.__nodos[node] and node == path[-1]:
                        # Incrementamos el camino recorrido
                        path.append(current_node)
                        last_path = paths.index(path)
                    # Bifurcacion de un nodo
                    elif current_node in self.__nodos[node] and node != path[-1]:
                        # Copiamos la ruta anterior a la bifurcacion
                        paths.append(path[:path.index(node) + 1])
                        # Actualizamos el ultimo camino recorrido
                        last_path = len(paths) - 1
            # Se encuentra el nodo objetivo
            if current_node == end:
                # Ultimo camino recorrido
                return paths[last_path]
            
            # Recorremos cada nodo vecino al nodo actual
            for neighbor in self.__nodos[current_node]:
                # Nodo vecino no ha sido visitado
                if neighbor not in visited_nodes:
                    # Nuevo nodo vecino a ser recorrido
                    queue.append(neighbor)
                    # Nodo visitado
                    visited_nodes.append(neighbor)
        
        # No se encontro un camino desde start hasta end
        return []