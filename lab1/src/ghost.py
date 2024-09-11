from abc import abstractmethod, ABC
from map import Map
import random

class GhostState(ABC):
    @abstractmethod
    def move(self, ghost: "Ghost", map: Map):
        pass

class GhostStateWandering(GhostState):
    def __init__(self) -> None:
        self.prev_position = None

    def move(self, ghost, map):
        current_x, current_y = ghost.x, ghost.y
        neighbours = map.get_free_neighbours(current_x, current_y)
        if len(neighbours) > 0:

            if len(neighbours) > 1 and self.prev_position is not None and self.prev_position in neighbours:
                neighbours.remove(self.prev_position)

            new_x, new_y = random.choice(neighbours)

            ghost.x, ghost.y = new_x, new_y
        
        self.prev_position = (current_x, current_y)

class Ghost:
    def __init__(self, start_x, start_y, sprites) -> None:
        self.x = start_x
        self.y = start_y
        self.sprites = sprites
        self.current_direction = 0
        self.state: GhostState = GhostStateWandering()

    def move(self, map):
        previous_x, previous_y = self.x, self.y
        self.state.move(self, map)
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