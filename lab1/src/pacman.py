from abc import abstractmethod, ABC

class PacmanState(ABC):
    @abstractmethod
    def move(self, pacman):
        pass

class PacmanStateMove(PacmanState):
    def move(self, pacman):
        pass


class Pacman:
    def __init__(self, start_x, start_y) -> None:
        self.x = start_x
        self.y = start_y