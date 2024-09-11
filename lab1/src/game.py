from map import Map
from typing import List
from ghost import Ghost

class Game:
    def __init__(self, map: Map, ghosts: List[Ghost]):
        self.map: Map = map

        self.ghosts = ghosts
        ghost_room_positions = self.map.get_ghost_room_positions()
        for i, ghost in enumerate(self.ghosts):
            ghost.x, ghost.y = ghost_room_positions[i]

        self.ghosts_speed = 12

        self.map.ghosts_positions = [(ghost.x, ghost.y) for ghost in self.ghosts]

        self.frame = 0

    def get_free_neighbours(self, x, y):
        neighbours = self.map.get_free_neighbours(x, y)

        for ghost in self.ghosts:
            if (ghost.x, ghost.y) in neighbours:
                neighbours.remove((ghost.x, ghost.y))

    def on_draw(self, tile_size):
        self.map.on_draw(tile_size)
        for ghost in self.ghosts:
            ghost.on_draw(tile_size)

    def update(self, dt):
        if self.frame % (60 // self.ghosts_speed) == 0:
            for i, ghost in enumerate(self.ghosts):
                ghost.move(self.map)
                self.map.ghosts_positions[i] = (ghost.x, ghost.y)

