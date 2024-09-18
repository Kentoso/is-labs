from abc import abstractmethod, ABC
import random 

class PacmanState(ABC):
    @abstractmethod
    def move(self, pacman, map):
        pass

    @abstractmethod
    def handle_apple(self, pacman, map):
        pass

class PacmanStateBaseMove(PacmanState):
    def move(self, pacman, map):
        pass

    def handle_apple(self, pacman, map, apple):
        if apple == 1:
            pacman.score += 10
        elif apple == 2:
            pacman.score += 50
            pacman.state = PacmanStateBigApple()

class PacmanStateBigApple(PacmanState):
    def move(self, pacman, map):
        pass

    def handle_apple(self, pacman, map, apple):
        if apple == 1:
            pacman.score += 10
                    

class PacmanStateMove(PacmanStateBaseMove):
    def __init__(self) -> None:
        self.prev_position = None
        super().__init__()

    def move(self, pacman, map):
        current_x, current_y = pacman.x, pacman.y
        neighbours = map.get_free_neighbours(current_x, current_y)
        if len(neighbours) > 0:

            if len(neighbours) > 1 and self.prev_position is not None and self.prev_position in neighbours:
                neighbours.remove(self.prev_position)

            new_x, new_y = random.choice(neighbours)

            pacman.x, pacman.y = new_x, new_y
        
        self.prev_position = (current_x, current_y)
    


class Pacman:
    def __init__(self, start_x, start_y, sprites) -> None:
        self.x = start_x
        self.y = start_y
        self.sprites = sprites
        self.current_direction = 0
        self.score = 0

        self.state: PacmanState = PacmanStateMove()

    def move(self, map):
        previous_x, previous_y = self.x, self.y
        self.state.move(self, map)

        apple = map.try_eat_apple(self.x, self.y)
        self.state.handle_apple(self, map, apple)

        if self.x > previous_x:
            self.current_direction = 1
        elif self.x < previous_x:
            self.current_direction = 3
        elif self.y > previous_y:
            self.current_direction = 0
        elif self.y < previous_y:
            self.current_direction = 2
        

    def on_draw(self, tile_size):
        current_sprite = self.sprites[self.current_direction]

        current_sprite.x = self.x * tile_size
        current_sprite.y = self.y * tile_size
        current_sprite.draw()

    def get_score(self):
        return self.score