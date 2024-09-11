import numpy as np
import pyglet
from map_generator import MapGenerator
import random 

class Map:
    def __init__(self, wall_image, small_apple_image, big_apple_image, size, tile_size):
        self.ghosts_positions = []

        self.map = np.zeros((size, size))
        self.apple_map = np.zeros((size, size))

        self.size = size
        self.generate()

        self.wall_sprites_batch = pyglet.graphics.Batch()
        self.small_apple_sprites_batch = pyglet.graphics.Batch()
        self.big_apple_sprites_batch = pyglet.graphics.Batch()

        self.wall_sprites = []
        self.small_apple_sprites = []
        self.big_apple_sprites = []


        for x, row in enumerate(self.map):
            for y, tile in enumerate(row):
                if tile == 1:
                    wall_sprite = pyglet.sprite.Sprite(img=wall_image, batch=self.wall_sprites_batch)
                    wall_sprite.x = x * tile_size
                    wall_sprite.y = y * tile_size
                    wall_sprite.width, wall_sprite.height = tile_size, tile_size
                    self.wall_sprites.append(wall_sprite)

        for x, row in enumerate(self.apple_map):
            for y, tile in enumerate(row):
                if tile == 1:
                    apple_sprite = pyglet.sprite.Sprite(img=small_apple_image, batch=self.small_apple_sprites_batch)
                    apple_sprite.x = x * tile_size
                    apple_sprite.y = y * tile_size
                    apple_sprite.width, apple_sprite.height = tile_size, tile_size
                    self.small_apple_sprites.append(apple_sprite)
                elif tile == 2:
                    apple_sprite = pyglet.sprite.Sprite(img=big_apple_image, batch=self.big_apple_sprites_batch)
                    apple_sprite.x = x * tile_size
                    apple_sprite.y = y * tile_size
                    apple_sprite.width, apple_sprite.height = tile_size, tile_size
                    self.big_apple_sprites.append(apple_sprite)


    def get_ghost_room_positions(self):
        center = self.size // 2 - 1
        offsets = [(0,0), (1,0), (0,1), (1,1)]
        return [(center + offset[0], center + offset[1]) for offset in offsets]

    def generate(self):
        self.map = np.zeros((self.size, self.size))
        room_positions = self.get_ghost_room_positions()
        
        map = MapGenerator(self.size).generate_map(room_positions)

        self.map = map
        self.apple_map = np.abs(np.ones((self.size, self.size)) - self.map)

        dead_ends = self.find_dead_ends()
        
        big_apple_positions = random.choices(dead_ends, k=len(dead_ends) // 4)

        for x,y in big_apple_positions:
            self.apple_map[x, y] = 2

    def find_dead_ends(self):
        dead_ends = []
        for x in range(self.size):
            for y in range(self.size):
                if self.map[x, y] == 0:
                    free_neighbours = self.get_free_neighbours(x, y)
                    if len(free_neighbours) == 1:
                        dead_ends.append((x, y))

        return dead_ends

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
        self.wall_sprites_batch.draw()
        self.small_apple_sprites_batch.draw()
        self.big_apple_sprites_batch.draw()

