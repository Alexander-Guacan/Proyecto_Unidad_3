from Grafo import Grafo

class GraphTextFile:
    """
    Lector de archivos con informacion de grafos

    Methods:
        + read_graph
        + read_devices_current
    """

    @classmethod
    def read_graph(cls, total_nodes: int, filename: str) -> Grafo:
        """
        Construye un grafo en base a la informacion de un archivo txt

        Args:
            total_nodes (int): _description_ Numero de nodos totales del grafo
            filename (str): _description_ Nombre del archivo a leer

        Returns:
            Grafo: _description_ Grafo construido
        """
        # Listado de adyacencia
        graph = [list[int]() for i in range(total_nodes)]
        
        try:
            # Abre el archivo especificado
            file = open("../docs/" + filename, 'r')
            
            # Nodo especifico de la lista de adyacencias
            i = 0
            # Leemos cada linea del archivo
            for line in file.readlines():
                # Eliminamos el salto de linea de la linea leida
                line = line.strip('\n')
                # Separamos cada nodo
                nodes = line.split(',')
                
                # Creamos lista de adyacencia del nodo especificado
                for node in nodes:
                    # Nodo es valido si su string leido tiene uno o mas de un caracter
                    if len(node) > 0:
                        # Agregaos nodo a la lista de adyacencia del nodo especifico
                        graph[i].append(int(node))
                # Seguir con el siguiente nodo
                i += 1
            # Cerrar archivo
            file.close()
        # Archivo no pudo ser encontrado
        except FileNotFoundError:
            # Grafo vacio
            return Grafo(graph)
        
        return Grafo(graph)
    
    @classmethod
    def read_devices_current(cls, filename: str) -> list[float]:
        """
        Retornar lista con la informacion de cada intensidad de los componentes que iran conectados al UPS

        Args:
            filename (str): _description_ Nombre de archivo a leer

        Returns:
            list[float]: _description_ Listado de corrientes de los dispositivos
        """
        # Listado de corrientes
        devices_current = list[float]()

        try:
            # Abrir el archivo
            file = open("../docs/" + filename, 'r')
            
            # Leemos cada valor separado por una coma
            for device_current in file.readline().strip('\n').split(','):
                # Valor leido debe tener uno o mas de un digito
                if len(device_current) > 0:
                    # Agregamos corriente leida
                    devices_current.append(float(device_current))
            # Cerrar archivo
            file.close()
        # Archivo no encontrado
        except FileNotFoundError:
            pass
        
        return devices_current