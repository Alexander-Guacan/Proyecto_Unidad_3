from Observable import Observable, Observer, abstractmethod

class UPS(Observable):
    """
    Simula el funcionamiento de un Uninterruptable Power Supply (UPS)
    
    Attributes:
        - min_battery_voltage : float
        - max_battery_voltage : float
        - max_battery_current : float
        - min_input_voltage : float
        - max_input_voltage : float
        - output_voltage : float
        - ports : int
        - battery_voltage : float
        - initial_battery_voltage : float
        - devices_current : list[float]
        - has_started_charging : bool
        - has_started_battery_usage : bool
        - inverter_mode : bool
        - observers : list[Observer]
    
    Methods:
        + UPS(output_voltage: float, max_battery_current: float, ports: int, max_charging_time: float)
        + add_observer(observer: Observer) : None
        + delete_observer(observer: Observer) : None
        + notify_observers() : None
        - regular_voltage(in_voltage: float): float
        - charge_battery(in_voltage: float): None
        + battery_percentage(): float
        - use_battery(): float
        - reverse_charge(in_voltage: float): float
        + connect_device(port: int, current: float): bool
        + power(in_voltage: float): float
        + is_inverter_mode(self) : bool
    """

    def __init__(self, output_voltage: float, max_battery_current: float, ports: int) -> None:
        """
        Constructor por defecto

        Args:
            output_voltage (float): _description_ Voltaje de salida del UPS, comunmente 120V o 240V
            max_battery_current (float): _description_ Intensidad maxima por hora de la bateria del UPS
            ports (int): _description_ Numero de conectores hacia el UPS
        """
        # Voltaje minimo que otorga la bateria para alimentar los dispositivos conectados a los puertos
        self.__min_battery_voltage = float(10)
        # Voltaje minimo que otorga la bateria para alimentar los dispositivos conectados a los puertos
        self.__max_battery_voltage = float(12)
        # Intensidad maxima que otorga la bateria
        self.__max_battery_current = max_battery_current
        self.__min_input_voltage = float(100)
        self.__max_input_voltage = float(140)
        # Voltaje de salida del UPS
        self.__output_voltage = output_voltage
        # Numero de dispositivos que pueden conectarse al UPS
        self.__ports = ports
        # Voltaje que genera la bateria
        self.__battery_voltage = self.__max_battery_voltage
        # Voltaje que tiene la bateria antes de comenzar su carga o descarga
        self.__initial_battery_voltage = self.__max_battery_voltage
        # Dispositivos conectados con su respectiva intensidad
        self.__devices_current = [float() for i in range(ports)]
        # Verifica si ha comenzado el proceso de carga de la bateria
        self.__has_started_charging = False
        # Verifica si se cambia al modo inversor, donde se utiliza la energia de la bateria
        self.__has_started_battery_usage = False
        # Verifica si se mantiene el modo inversor
        self.__inverter_mode = False
        # Listado de dispositivos que toman lectura de los datos arrojados por el UPS que se actualizan con cada cambio
        self.__observers = list[Observer]()

    def add_observer(self, observer: "Observer") -> None:
        if observer not in self.__observers:
            self.__observers.append(observer)

    def delete_observer(self, observer: "Observer") -> None:
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observers(self) -> None:
        for observer in self.__observers:
            observer.update(self)

    def __regular_voltage(self, in_voltage: float) -> float:
        """
        Regula las oscilaciones del voltaje de entrada al UPS (entre 100 y 140V) a uno estable de 120V o 240V segun las especificaciones del fabricante

        Args:
            in_voltage (float): _description_ Voltaje de entrada al UPS desde el tomacorriente

        Returns:
            float: _description_ Voltaje estabilizado
        """
        # Voltaje mayor al voltaje de salida estable
        if in_voltage > self.__output_voltage:
            # Disminuimos exceso de voltaje
            return in_voltage - (in_voltage - self.__output_voltage)
        # Voltaje menor al voltaje de salida estable
        elif in_voltage < self.__output_voltage:
            # Incrementamos voltaje de salida
            return in_voltage + (self.__output_voltage - in_voltage)
        # Voltaje igual al voltaje de salida estable
        else:
            return in_voltage
        
    def __charge_battery(self, in_voltage: float) -> None:
        """
        Carga la bateria

        Args:
            in_voltage (float): _description_ Voltaje necesario para cargar la bateria especificado por el fabricante
        """
        
        # Bateria cargado completamente
        if self.__battery_voltage >= self.__max_battery_voltage:
            return
        
        # Comienza el modo de carga
        if not self.__has_started_charging:
            # Indica que comienza el modo de carga
            self.__has_started_charging = True
            # Voltaje inicial de la bateria antes de comenzar la carga
            self.__initial_battery_voltage = self.__battery_voltage
        
        # Transformar tiempo de horas a minutos
        time_in_minuts = 60

        # Tiempo de carga estimado de la bateria segun el voltaje inicial de la misma
        charging_time = (self.__max_battery_voltage - self.__initial_battery_voltage) * self.__max_battery_voltage * time_in_minuts / (self.__max_battery_voltage - self.__min_battery_voltage)

        # Incrementamos voltaje de carga de la bateria
        self.__battery_voltage += (self.__max_battery_voltage - self.__initial_battery_voltage) / charging_time

    def battery_percentage(self) -> float:
        """
        Retorna el porcentaje de carga de la bateria en una escala de 100%

        Returns:
            float: _description_ Porcentaje de carga de la bateria
        """
        percentage_scale = 100
        # Funcion lineal que calcula el porcentaje de bateria segun el voltaje de carga de la bateria
        return percentage_scale * (self.__battery_voltage - self.__min_battery_voltage) / (self.__max_battery_voltage - self.__min_battery_voltage)

    def __use_battery(self) -> float:
        """
        Retorna el voltaje suministrado por la bateria. Se desgasta cada vez que se llama a esta funcion

        Returns:
            float: _description_ voltaje suministrado por la bateria segun su porcentaje de carga
        """

        # Voltaje de bateria es menor al aceptable
        if self.__battery_voltage <= self.__min_battery_voltage:
            return 0
        
        # Inicia el modo de uso de bateria
        if not self.__has_started_battery_usage:
            # No es el primer ciclo de uso de la bateria
            self.__has_started_battery_usage = True
            # Voltaje inicial con el que cuenta la bateria antes de su uso
            self.__initial_battery_voltage = self.__battery_voltage

        # Intensidad de la bateria segun el voltaje inicial de la bateria
        battery_current = self.__initial_battery_voltage / (self.__max_battery_voltage / self.__max_battery_current)

        # Intensidad total de los dispositivos conectados al UPS
        total_devices_current = 0
        # Cada intensidad de los dispositivos conectados
        for device_current in self.__devices_current:
            # Sumatoria de todas las intensidades
            total_devices_current += device_current
        
        if total_devices_current <= 0:
            return self.__battery_voltage

        # Transforma tiempo en horas a minutos
        time_in_minuts = 60
        # Tiempo estimado de descarga de la bateria en 
        discharge_time = battery_current / total_devices_current * time_in_minuts

        # Decrementamos el voltaje almacenado en la bateria
        self.__battery_voltage -= (self.__initial_battery_voltage - self.__min_battery_voltage) / discharge_time

        return self.__battery_voltage
    
    def __reverse_charge(self, in_voltage: float) -> float:
        """
        Retorna el voltaje de la bateria de corriente directa en corriente alterna. Ademas se potencia el voltaje hasta alcanzar el valor de self.__output_voltage

        Args:
            in_voltage (float): _description_ Voltaje suministrada por la bateria

        Returns:
            float: _description_ Voltaje de salida necesario para alimentar a los dispositivos conectados al UPS
        """
        if in_voltage <= 0:
            return 0
        
        return in_voltage + (self.__output_voltage - in_voltage)
    
    def connect_device(self, port: int, current: float) -> bool:
        """
        Conecta un dispositivo al UPS

        Args:
            port (int): numero de puerto que va de 0 hasta self.__ports - 1
            current (float): _description_ Intensidad de corriente que consume el dispositivo a conectar

        Returns:
            bool: _description_ True: es posible conectar el dispositivo, False: Puerto de conexion no existe
        """
        # Puerto no existe
        if port < 0 or port >= self.__ports:
            return False
        
        # Cambiamos la intensidad de corriente por la del nuevo dispositivo conectado
        self.__devices_current[port] = current

        return True
    
    def power(self, in_voltage: float) -> float:
        """
        Enciende el UPS

        Args:
            in_voltage (float): _description_ Voltaje suminstrado por el tomacorriente

        Returns:
            float: _description_ Voltaje de salida necesario para alimentar los dispositivos especificado por el fabricante
        """
        # Voltaje de salida que sera tomado del tomacorriente o por la bateria del UPS
        out_voltage = float()

        # Voltaje dentro de los limites que no generan un cortocircuito o sobrecarga establecidos por el fabricante
        if in_voltage >= self.__min_input_voltage and in_voltage <= self.__max_input_voltage:
            self.__has_started_battery_usage = False
            self.__inverter_mode = False
            # Voltaje de salida tomado del tomacorriente y regulado por el estabilizador
            out_voltage = self.__regular_voltage(in_voltage)

            # Bateria con carga incompleta
            if self.battery_percentage() < 100:
                # Cargar bateria con voltaje regulado por estabilizador
                self.__charge_battery(self.__regular_voltage(in_voltage))
        
        # Voltaje del tomacorriente no valido y la bateria tiene carga
        elif self.battery_percentage() > 0:
            self.__has_started_charging = False
            self.__inverter_mode = True
            # Voltaje de salida tomado por la bateria e incrementado por el inversor
            out_voltage = self.__reverse_charge(self.__use_battery())
        # Voltaje de tomacorriente no optimo y no hay bateria disponible
        else:
            out_voltage = 0

        self.notify_observers()

        return out_voltage
    
    def is_inverter_mode(self) -> bool:
        return self.__inverter_mode
    
class DisplayElement(Observer):
    """
    Interfaz de objetos que funjiran como pantalla de datos del UPS

    Methods:
        + display(): None
    """

    @abstractmethod
    def display(self) -> None:
        """
        Desplegar en pantalla las actualizaciones de datos del UPS
        """

class BatteryStateDisplay(DisplayElement):
    """
    Informa de las actualizaciones del estado y/o porcentaje de la bateria

    Attributes:
        - has_changed_mode : bool
        - battery_percentage : float

    Methods:
        + BatteryStateDisplay()
        + register_in_observable(observable: Observable): None
        + update(observable: Observable): None
        + display(): None
    """

    def __init__(self) -> None:
        """
        Constructor por defecto
        """
        # Verifica si ha cambiado el modo de regulador a inversor
        self.__has_changed_mode = False
        # Guarda el ultimo estado del porcentaje de la bateria
        self.__battery_percentage = float()
    
    def register_in_observable(self, observable: Observable) -> None:
        """
        Agregar este dispositivo a la lista de suscriptores a ser notificados por las actualizacion del UPS

        Args:
            observable (Observable): _description_
        """
        # Objeto observable no pertence a la clase UPS
        if not isinstance(observable, UPS):
            return
        # Agregar este objeto para ser informado por el UPS
        observable.add_observer(self)
        # Estado inicial del porcentaje de bateria del UPS
        self.__battery_percentage = observable.battery_percentage()

    def update(self, observable: Observable) -> None:
        """
        Imprime las actualizaciones de la bateria del UPS

        Args:
            observable (Observable): _description_ UPS del cual toma los datos
        """
        # Objeto observable no pertence a la clase UPS
        if not isinstance(observable, UPS):
            return
        
        # Primer cambio al modo inversor
        if observable.is_inverter_mode() and not self.__has_changed_mode:
            print("Cambiando a modo inversor")
            self.__has_changed_mode = True
        # Se termino el modo inversor
        elif not observable.is_inverter_mode() and self.__has_changed_mode:
            self.__has_changed_mode = False
        
        # UPS se encuentra en el modo inversor
        if self.__has_changed_mode:
            # Actualizamos el porcentaje de bateria
            self.__battery_percentage = observable.battery_percentage()
            # Imprimir actualizaciones
            self.display()
        # UPS en modo carga
        elif observable.battery_percentage() > self.__battery_percentage:
            print("Cargando bateria")
            # Actualizamos el porcentaje de bateria
            self.__battery_percentage = observable.battery_percentage()
            # Imprimir actualizaciones
            self.display()
            
    def display(self) -> None:
        """
        Imprimir actualizaciones de la bateria
        """
        print(f"Porcentaje de bateria: {self.__battery_percentage if self.__battery_percentage > 0 else 0}")
