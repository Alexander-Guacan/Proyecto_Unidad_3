from UPS import UPS, BatteryStateDisplay
from GraphTextFile import GraphTextFile, Grafo
from Input import Input
import time
import os
import random

class System:
    def __init__(self) -> None:
        output_voltage = 120
        max_battery_current = 9
        self.__devices = 20
        self.__ports = 4
        self.__ups = UPS(output_voltage, max_battery_current, self.__ports)
        self.__display_element = BatteryStateDisplay()
        self.__display_element.register_in_observable(self.__ups)
        self.__is_ups_configured = False
        self.__graph = GraphTextFile.read_graph(self.__devices, "grafo.txt")
        self.__devices_current = GraphTextFile.read_devices_current("intensidades.txt")
        self.__compute_current_of_devices()
        self.__main_device = int()

    def __compute_current_of_port(self, port: int) -> float:
        # Camino desde start a end
        total_current = self.__devices_current[port]
        # Lista de nodos visitados
        visited_nodes = list[int]()
        # Nodos vecinos por visitar de cada nodo
        queue = list[int]()
        
        # Se recorrera los nodos vecinos de start
        queue.append(port)
        # Nodo port ya se ha visitado
        visited_nodes.append(port)

        # Mientras haya nodos vecinos por recorrer
        while len(queue) > 0:
            # Seleccionamos cada nodo no visitado en el orden que se encuentran
            current_node = queue.pop(0)
            
            # Recorremos cada nodo vecino al nodo actual
            for neighbor in self.__graph.get_node(current_node):
                # Nodo vecino no ha sido visitado
                if neighbor not in visited_nodes:
                    # Nuevo nodo vecino a ser recorrido
                    queue.append(neighbor)
                    # Nodo visitado
                    visited_nodes.append(neighbor)

                    total_current += self.__devices_current[neighbor]

        # No se encontro un camino desde start hasta end
        return total_current
        
    def __compute_current_of_devices(self) -> None:
        port = 0
        for device in self.__graph.get_node(0):
            self.__ups.connect_device(port, self.__compute_current_of_port(device))

    def __read_power_supply_voltage(self) -> float:
        return random.randint(95, 145) + round(random.random(), 2)

    def __options_of_UPS_main_menu(self) -> str:
        return "1.- Encender UPS"\
        + "\n2.- Configurar UPS"\
        + "\n3.- Salir"\

    def __setting_ups(self) -> None:
        self.__main_device = Input.integer("Dispositivo principal: ", 2)
        self.__is_ups_configured = True

    def power_ups(self) -> None:
        if not self.__is_ups_configured:
            return print("UPS no configurado")
        
        power_supply_voltage = 0
        deep_path = self.__graph.shortest_path(0, self.__main_device)
        breadth_path = self.__graph.breadth_first_search(0, self.__main_device)

        while self.__ups.battery_percentage() > 0:
            os.system("cls")
            if not self.__ups.is_inverter_mode():
                power_supply_voltage = self.__read_power_supply_voltage()
                print(f"Voltaje de tomacorriente: {power_supply_voltage}")
            else:
                print("Busqueda en profundidad:", deep_path)
                print("Busqueda en anchura:", breadth_path)

            self.__ups.power(power_supply_voltage)
            time.sleep(1)

    def menu(self) -> None:
        
        while self.__ups.battery_percentage() > 0:
            os.system("cls")
            print(self.__options_of_UPS_main_menu())
            option = Input.integer("Seleccionar opcion: ", 1)
            match option:
                case 1:
                    self.power_ups()
                case 2:
                    self.__setting_ups()
                case 3:
                    break
                case _:
                    print("Opcion no existe")
            os.system("pause > nul")