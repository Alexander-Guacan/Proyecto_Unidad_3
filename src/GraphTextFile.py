from Grafo import Grafo

class GraphTextFile:
    @classmethod
    def read_graph(cls, total_nodes: int, filename: str) -> Grafo:
        graph = [list[int]() for i in range(total_nodes)]

        try:
            file = open("../docs/" + filename, 'r')
        
            i = 0
            for line in file.readlines():
                line = line.strip('\n')
                nodes = line.split(',')
                
                for node in nodes:
                    if len(node) > 0:
                        graph[i].append(int(node))

                i += 1

            file.close()
        except FileNotFoundError:
            return Grafo(graph)

        return Grafo(graph)
    
    @classmethod
    def read_devices_current(cls, filename: str) -> list[float]:
        devices_current = list[float]()

        try:
            file = open("../docs/" + filename, 'r')

            for device_current in file.readline().strip('\n').split(','):
                if len(device_current) > 0:
                    devices_current.append(float(device_current))

            file.close()
        except FileNotFoundError:
            pass
        
        return devices_current