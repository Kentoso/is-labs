import numpy as np

class Map:
    def __init__(self, wall_sprite, size):
        self.map = np.zeros((size, size))
        self.size = size
        self.wall_sprite = wall_sprite
        self.ghosts_positions = []

    def get_ghost_room_positions(self):
        center = self.size // 2 - 1
        offsets = [(0,0), (1,0), (0,1), (1,1)]
        return [(center + offset[0], center + offset[1]) for offset in offsets]

    def generate(self):
        self.map = np.random.randint(0, 2, (self.size, self.size))
        # self.map = np.zeros((self.size, self.size))
        room_positions = self.get_ghost_room_positions()

        for x, y in room_positions:
            self.map[x, y] = 0

    def get_free_neighbours(self, x, y):
        neighbours = []
        if x > 0 and self.map[x-1, y] == 0:
            neighbours.append((x-1, y))
        if x < self.size - 1 and self.map[x+1, y] == 0:
            neighbours.append((x+1, y))
        if y > 0 and self.map[x, y-1] == 0:
            neighbours.append((x, y-1))
        if y < self.size - 1 and self.map[x, y+1] == 0:
            neighbours.append((x, y+1))

        for ghost_x, ghost_y in self.ghosts_positions:
            if (ghost_x, ghost_y) in neighbours:
                neighbours.remove((ghost_x, ghost_y))
        
        return neighbours
    
    def on_draw(self, tile_size):
        for x, row in enumerate(self.map):
            for y, tile in enumerate(row):
                if tile == 1:
                    self.wall_sprite.x = x * tile_size
                    self.wall_sprite.y = y * tile_size
                    self.wall_sprite.draw()
