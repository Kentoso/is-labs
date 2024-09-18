import numpy as np
import pyglet
from map_generator import MapGenerator
import random 

class Map:
    def __init__(self, wall_image, small_apple_image, big_apple_image, size, tile_size):
        self.ghosts_positions = []
        self.pacman_position = None

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
        self.apple_sprites = [[None] * size for _ in range(size)]

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
                    self.apple_sprites[x][y] = apple_sprite
                elif tile == 2:
                    apple_sprite = pyglet.sprite.Sprite(img=big_apple_image, batch=self.big_apple_sprites_batch)
                    apple_sprite.x = x * tile_size
                    apple_sprite.y = y * tile_size
                    apple_sprite.width, apple_sprite.height = tile_size, tile_size
                    self.apple_sprites[x][y] = apple_sprite


    def get_ghost_room_positions(self):
        center = self.size // 2 - 1
        offsets = [(0,0), (1,0), (0,1), (1,1)]
        return [(center + offset[0], center + offset[1]) for offset in offsets]

    def get_random_empty_space(self):
        x = random.randint(0, self.size - 1)
        y = random.randint(0, self.size - 1)
        while self.map[x, y] == 1:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
        return x, y

    def try_eat_apple(self, x, y):
        apple = self.apple_map[x, y]
        self.apple_map[x, y] = 0
        if self.apple_sprites[x][y]:
            self.apple_sprites[x][y].delete()
            self.apple_sprites[x][y] = None
        return apple

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

    def get_random_apple(self):
        big_apples = np.argwhere(self.apple_map == 2)
        if len(big_apples) > 0:
            return tuple(big_apples[0].astype(int))
        
        small_apples = np.argwhere(self.apple_map == 1)
        if len(small_apples) > 0:
            return tuple(small_apples[0].astype(int))
        
        return None
    
    def get_nearest_apple(self, position):
        apples = np.argwhere(self.apple_map == 1)
        big_apples = np.argwhere(self.apple_map == 2)
        merged_apples = np.concatenate((apples, big_apples), axis=0)
        if len(apples) == 0:
            return None
        return tuple(min(merged_apples, key=lambda x: abs(x[0] - position[0]) + abs(x[1] - position[1])))

    def bfs(self, start, finish):
        queue = [start]
        visited = np.zeros((self.size, self.size))
        visited[start] = 1
        parent = np.zeros((self.size, self.size, 2))

        while len(queue) > 0:
            current = tuple(queue.pop(0))
            if current == finish:
                path = []
                while current != start:
                    path.append(current)
                    current = tuple(parent[current[0], current[1]].astype(int))
                path.append(start)
                return path[::-1]

            for neighbour in self.get_free_neighbours(*current):
                if visited[neighbour] == 0:
                    visited[neighbour] = 1
                    parent[neighbour[0], neighbour[1]] = current
                    queue.append(neighbour)

        return []

    def dijkstra(self, start, finish):
        distances = np.ones((self.size, self.size)) * np.inf
        distances[start] = 0

        visited = np.zeros((self.size, self.size))
        parent = np.zeros((self.size, self.size, 2))

        while True:
            current = np.unravel_index(np.argmin(distances), distances.shape)
            if current == finish:
                path = []
                while current != start:
                    path.append(current)
                    current = tuple(parent[current[0], current[1]].astype(int))
                path.append(start)
                return path[::-1]

            visited[current] = 1
            neighbours = self.get_free_neighbours(*current)
            if len(neighbours) == 0:
                return []

            for neighbour in neighbours:
                if visited[neighbour] == 0:
                    new_distance = distances[current] + 1
                    if new_distance < distances[neighbour]:
                        distances[neighbour] = new_distance
                        parent[neighbour[0], neighbour[1]] = current
            
            distances[current] = np.inf

    
    def a_star(self, start, finish):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        open_set = {start}
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, finish)}

        while len(open_set) > 0:
            current = min(open_set, key=lambda x: f_score[x])
            if current == finish:
                path = []
                while current != start:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            open_set.remove(current)
            for neighbour in self.get_free_neighbours(*current):
                tentative_g_score = g_score[current] + 1
                if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = g_score[neighbour] + heuristic(neighbour, finish)
                    open_set.add(neighbour)

        return []