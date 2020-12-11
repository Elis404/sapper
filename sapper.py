import pygame
from random import randint


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[-1] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 35

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        color = pygame.Color(255, 255, 255)
        for j in range(self.height):
            for i in range(self.width):
                if self.board[j][i] == 10:
                    pygame.draw.rect(screen, pygame.Color('red'), (
                        self.left + i * self.cell_size + 1, self.top + j * self.cell_size + 1,
                        self.cell_size - 1,
                        self.cell_size - 1))
                pygame.draw.rect(screen, color, (
                    self.left + i * self.cell_size, self.top + j * self.cell_size, self.cell_size,
                    self.cell_size), 1)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if (0 <= cell_x < self.width) and (0 <= cell_y < self.height):
            return (cell_x, cell_y)

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class Sapper(Board):
    def __init__(self, width, height, mines=10):
        super().__init__(width, height)
        count = 0
        while count != mines:
            x = randint(0, width - 1)
            y = randint(0, height - 1)
            if self.board[y][x] == -1:
                self.board[y][x] = 10
                count += 1

    def on_click(self, cell_coords):
        super().on_click(cell_coords)
        if cell_coords:
            count = self.count_near_mines(cell_coords[0], cell_coords[1])
            self.open_cell(cell_coords, count)

    def count_near_mines(self, x, y):
        count = 0
        deltas = [(delta_x, delta_y) for delta_x in [-1, 0, 1] for delta_y in [-1, 0, 1] if
                  delta_x != 0 or delta_y != 0]
        for delta_x, delta_y in deltas:
            new_x, new_y = x + delta_x, y + delta_y
            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                if self.board[y + delta_y][x + delta_x] == 10:
                    count += 1
        return count

    def open_cell(self, cell_coords, count):
        pass


if __name__ == '__main__':
    pygame.init()
    size = 600, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Дедушка сапёра')
    board = Sapper(10, 15)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
    pygame.quit()
