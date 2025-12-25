from abc import ABC, abstractmethod

class BaseConfig(ABC):
    def __init__(self):
        self.validate()
    
    @abstractmethod
    def validate(self):
        pass