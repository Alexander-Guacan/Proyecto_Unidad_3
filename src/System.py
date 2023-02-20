from UPS import UPS, BatteryStateDisplay
from GraphTextFile import GraphTextFile
from Input import Input
import time
import os
import random

class System:
    """
    Interfaz de UPS

    Atributos:
        System()
        self.__devices : int
        self.__ports : int
        self.__ups : UPS
        self.__display_element : BatteryStateDisplay
        self.__is_ups_configured : bool
        self.__graph : Grafo
        self.__devices_current : list[float]
        self.__main_device : int()
    """

    def __init__(self) -> None:
        """
        Constructor por defecto
        """
        # Voltaje de salida del UPS
        output_voltage = 120
        # Corriente maxima proporcionada por la bateria
        max_battery_current = 9
        # Dispositivos que pueden conectarse al UPS
        self.__devices = 20
        # Tomacorrientes disponibles del UPS
        self.__ports = 4
        # Crear objeto UPS
        self.__ups = UPS(output_voltage, max_battery_current, self.__ports)
        # Pantalla del estado de la bateria del UPS
        self.__display_element = BatteryStateDisplay()
        # Notificar de cualquier cambio a la pantalla del estado de la bateria
        self.__display_element.register_in_observable(self.__ups)
        # Verifica si se ha configurado el UPS
        self.__is_ups_configured = False
        # Leer grafo del archivo txt
        self.__graph = GraphTextFile.read_graph(self.__devices, "grafo.txt")
        # Leer corriente de cada dispositivo en el archivo txt
        self.__devices_current = GraphTextFile.read_devices_current("intensidades.txt")
        # Calcular corriente total que le llega a cada tomacorriente
        self.__compute_current_of_devices()
        # Conector principal el cual debe recibir mas corriente de la bateria
        self.__main_device = int()

    def __compute_current_of_port(self, port: int) -> float:
        """
        Calcula la corriente total que necesita un tomacorriente especifico

        Args:
            port (int): _description_ Puerto especifico a medir su corriente

        Returns:
            float: _description_ Corriente total al tomacorriente
        """
        # Corriente total del tomacorriente especificado
        total_current = self.__devices_current[port]
        # Lista de nodos visitados
        visited_nodes = list[int]()
        # Nodos vecinos por visitar de cada nodo
        queue = list[int]()
        
        # Se recorrera los nodos vecinos del tomacorriente especifico
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
                    # Incrementamos la corriente que consume el nuevo dispositivo encontrado
                    total_current += self.__devices_current[neighbor]

        return total_current
        
    def __compute_current_of_devices(self) -> None:
        """
        Configura el UPS con la corriente total de cada tomacorriente
        """
        # Tomacorriente a configurar
        port = 0
        # Recorrer cada arbol de los dispositivos conectados directamente al UPS
        for device in self.__graph.get_node(0):
            # Definir la corriente total de cada tomacorriente
            self.__ups.connect_device(port, self.__compute_current_of_port(device))

    def __read_power_supply_voltage(self) -> float:
        """
        Simula la lectura del voltaje del tomacorriente

        Returns:
            float: _description_
        """
        # Valor randomico entre 95 y 145 con 2 decimales
        return random.randint(95, 145) + round(random.random(), 2)

    def __options_of_UPS_main_menu(self) -> str:
        """
        Retorna el mensaje de la pantalla del menu principal

        Returns:
            str: _description_ Texto del menu principal
        """
        # Mensaje de pantalla de menu principal
        return "1.- Encender UPS"\
        + "\n2.- Configurar UPS"\
        + "\n3.- Salir"\

    def __setting_ups(self) -> None:
        """
        Especificar cual es la computadora principal
        """
        self.__main_device = Input.integer("Dispositivo principal: ", 2)
        self.__is_ups_configured = True

    def power_ups(self) -> None:
        """
        Comenzar las operaciones del UPS
        """
        # No se configuro el ups
        if not self.__is_ups_configured:
            return print("UPS no configurado")
        
        # Lectura del tomacorriente
        power_supply_voltage = 0
        # Camino por algoritmo de busqueda por profundidad
        deep_path = self.__graph.shortest_path(0, self.__main_device)
        # Camino por algoritmo de busqueda por anchura
        breadth_path = self.__graph.breadth_first_search(0, self.__main_device)

        # Seguir operando mientras exista bateria
        while self.__ups.battery_percentage() > 0:
            # Limpiar pantalla
            os.system("cls")
            # Voltaje del tomacorriente dentro de los limites permitidos
            if not self.__ups.is_inverter_mode():
                # Leer voltaje del tomacorriente
                power_supply_voltage = self.__read_power_supply_voltage()
                print(f"Voltaje de tomacorriente: {power_supply_voltage}")
            # Sobrecarga o cortocircuito del tomacorriente de pared. Se deja de leer el voltaje del tomacorriente
            else:
                print("Busqueda en profundidad:", deep_path)
                print("Busqueda en anchura:", breadth_path)
            
            # Enviar dato del voltaje del tomacorriente
            self.__ups.power(power_supply_voltage)
            # Pausar ejecucion del programa por un segundo
            time.sleep(1)

    def menu(self) -> None:
        """
        Menu interactivo del UPS
        """
        # Seguir operando mientras exista bateria
        while self.__ups.battery_percentage() > 0:
            # Limpiar pantalla
            os.system("cls")
            # Imprimir opicones del menu
            print(self.__options_of_UPS_main_menu())
            # Seleccionar una opcion del menu
            option = Input.integer("Seleccionar opcion: ", 1)
            
            # Accionar la opcion seleccionada
            match option:
                case 1:
                    self.power_ups()
                case 2:
                    self.__setting_ups()
                case 3:
                    break
                case _:
                    print("Opcion no existe")

            # Pausar la ejecucion del programa hasta presionar cualquier tecla
            os.system("pause > nul")