from abc import abstractmethod, ABC
from map import Map
import random
import pyglet 

class GhostState(ABC):
    @abstractmethod
    def move(self, ghost: "Ghost", map: Map):
        pass

class GhostStateBaseMove(GhostState):
    def __init__(self) -> None:
        self.prev_position = None
        self.should_switch_state = False

    def move(self, ghost, map):
        if map.is_position_near_or_inside_pacman(self.prev_position):
            ghost.caught_pacman()
            return

        if self.should_switch_state:
            ghost.randomize_state()
            self.should_switch_state = False

        current_direction = ghost.current_direction
        direction_map = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        free_neighbours = map.get_free_neighbours(ghost.x, ghost.y)
        if self.prev_position == (ghost.x, ghost.y):
            if direction_map[current_direction] in free_neighbours:
                ghost.x += direction_map[current_direction][0]
                ghost.y += direction_map[current_direction][1]
            else:
                if len(free_neighbours) > 0:
                    new_x, new_y = random.choice(free_neighbours)
                    current_direction = -1
                    for i, direction in enumerate(direction_map):
                        if direction + (ghost.x, ghost.y) == (new_x, new_y):
                            current_direction = i
                            break
                    ghost.current_direction = current_direction
                    ghost.x, ghost.y = new_x, new_y
                else:
                    print("GHOST STUCK")
        
        if map.is_position_near_or_inside_pacman(self.prev_position):
            ghost.caught_pacman()

            

class GhostStateWandering(GhostStateBaseMove):
    def __init__(self, difficulty) -> None:
        self.state_length = max(10 - difficulty, 5) + random.randint(0, 5)
        super().__init__()

    def move(self, ghost, map):
        self.state_length -= 1
        if self.state_length < 0:
            self.should_switch_state = True

        current_x, current_y = ghost.x, ghost.y
        neighbours = map.get_free_neighbours(current_x, current_y)
        if len(neighbours) > 0:

            if len(neighbours) > 1 and self.prev_position is not None and self.prev_position in neighbours:
                neighbours.remove(self.prev_position)

            new_x, new_y = random.choice(neighbours)

            ghost.x, ghost.y = new_x, new_y
        
        self.prev_position = (current_x, current_y)

        super().move(ghost, map)

class GhostStateChasing(GhostStateBaseMove):
    def __init__(self, difficulty) -> None:
        self.state_length = min(difficulty, 5)
        super().__init__()

    def move(self, ghost, map):
        self.state_length -= 1
        if self.state_length < 0:
            self.should_switch_state = True

        current_x, current_y = ghost.x, ghost.y
        pacman_position = map.pacman_position
        path = map.bfs((current_x, current_y), pacman_position, map.get_free_neighbours_for_ghost)

        if len(path) > 1:
            ghost.x, ghost.y = path[1]

        self.prev_position = (current_x, current_y)

        super().move(ghost, map)

class Ghost:
    def __init__(self, sprites, n) -> None:
        self.sprites = sprites
        self.n = n
        self.difficulty = 1
        self.restore()

    def restore(self):
        self.x = 0
        self.y = 0
        self.state = GhostStateWandering(self.difficulty)
        self.current_direction = 0
        self.did_catch_pacman = False

    def randomize_state(self):
        state = random.choice([GhostStateWandering(self.difficulty), GhostStateChasing(self.difficulty)])
        self.state = state

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

        number = pyglet.text.Label(str(self.n), font_name='Times New Roman', font_size=12, x=self.x * tile_size, y=self.y * tile_size)
        current_sprite.draw()
        number.draw()

    def caught_pacman(self):
        self.did_catch_pacman = True
        print(f"GHOST {self.n} CAUGHT PACMAN")