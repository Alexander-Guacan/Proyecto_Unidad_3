from abc import ABC, abstractmethod

class Observable(ABC):
    
    @abstractmethod
    def add_observer(self, observer: "Observer") -> None:
        pass

    @abstractmethod
    def delete_observer(self, observer: "Observer") -> None:
        pass

    @abstractmethod
    def notify_observers(self) -> None:
        pass
        
class Observer(ABC):
    
    @abstractmethod
    def update(self, observable: Observable) -> None:
        pass