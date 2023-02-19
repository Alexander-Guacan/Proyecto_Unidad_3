from UPS import UPS, BatteryStateDisplay
from Grafo import Grafo
from Input import Input
import random

devices = 20
grafo = Grafo([[] for i in range(devices)])
devices_connected = list[int]()

def read_power_supply_voltage() -> float:
    return random.randint(95, 145) + round(random.random(), 2)

def options_of_UPS_main_menu() -> str:
    return "1.- Encender UPS"\
    + "\n2.- Apagar UPS"\
    + "\n3.- Salir"\

def menu() -> None:
    print(options_of_UPS_main_menu())

def setting_ups(ups: UPS) -> None:
    ups.connect_device(0, 5)
    ups.connect_device(1, 5)
    ups.connect_device(2, 5)
    ups.connect_device(3, 5)

def main() -> None:
    ups = UPS(120, 9, 8)
    display_element = BatteryStateDisplay()
    display_element.register_in_observable(ups)
    setting_ups(ups)

    power_supply_voltage = 0
    i = 0
    while i < 20:
        if not ups.is_inverter_mode():
            power_supply_voltage = read_power_supply_voltage()
        print(f"Voltaje de tomacorriente: {power_supply_voltage}")
        ups.power(power_supply_voltage)
        i += 1

if __name__ == "__main__":
    main()