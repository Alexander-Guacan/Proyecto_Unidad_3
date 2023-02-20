from abc import ABC, abstractmethod

class Observable(ABC):
    """
    Interfaz de un objeto observable que actualizara a los objetos Observers asociados a este, cuando haya un cambio

    Methods:
        + add_observer(observer: Observer) : None
        + delete_observer(observer: Observer) : None
        + notify_observers() : None
    """
    
    @abstractmethod
    def add_observer(self, observer: "Observer") -> None:
        """
        Agregamos un observador que sera notificado cuando haya un cambio que afecte a dicho observador
        Args:
            observer (Observer): _description_ Objeto observador a agregar
        """

    @abstractmethod
    def delete_observer(self, observer: "Observer") -> None:
        """
        Eliminar un observador. Dicho observador ya no sera notificado de cambios

        Args:
            observer (Observer): _description_ Objeto observador a eliminar
        """

    @abstractmethod
    def notify_observers(self) -> None:
        """
        Actualizar de los cambios a los observadores
        """
        
class Observer(ABC):
    """
    Objeto que sera notificado de cambios importantes de aquellos objetos Observable a los que este suscrito

    Methods:
        + update(observable: Observable) : None
    """
    
    @abstractmethod
    def update(self, observable: Observable) -> None:
        """
        Toma los datos actualizados del objeto Observable cuando haya un cambio importante

        Args:
            observable (Observable): _description_ Objeto observador del cual se extraera los datos actualizados
        """