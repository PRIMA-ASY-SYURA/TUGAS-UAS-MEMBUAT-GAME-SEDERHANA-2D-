import pygame
import random

def add_vectors(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def subtract_vectors(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def scale_vector(v, scalar):
    return (v[0] * scalar, v[1] * scalar)

class TetrisGame:
    SHAPES = {
        'I': [[1, 1, 1, 1]], 
        'O': [[1, 1], [1, 1]], 
        'T': [[0, 1, 0], [1, 1, 1]],
        'S': [[0, 1, 1], [1, 1, 0]], 
        'Z': [[1, 1, 0], [0, 1, 1]],
        'J': [[1, 0, 0], [1, 1, 1]], 
        'L': [[0, 0, 1], [1, 1, 1]]
    }
    
    def __init__(self):
        pygame.init()
        self.block_size = 30
        self.width, self.height = 300, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simple Tetris")
        self.reset_game()
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.fall_speed = 500  # waktu dalam milidetik
        self.velocity = (0, 1)  # Kecepatan awal (x, y)

    def reset_game(self):
        cols, rows = self.width // self.block_size, self.height // self.block_size
        self.board = [[0] * cols for _ in range(rows)]
        self.colors = [[None] * cols for _ in range(rows)]
        self.new_piece()
        
    def new_piece(self):
        self.current_piece = random.choice(list(self.SHAPES.values()))
        self.current_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.piece_pos = (4, 0)

    def check_collision(self, piece, pos):
        return any(cell and (pos[1] + y >= len(self.board) or 
                             pos[0] + x < 0 or pos[0] + x >= len(self.board[0]) or
                             (pos[1] + y >= 0 and self.board[pos[1] + y][pos[0] + x]))
                   for y, row in enumerate(piece) 
                   for x, cell in enumerate(row))

    def place_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.piece_pos[1] + y][self.piece_pos[0] + x] = 1
                    self.colors[self.piece_pos[1] + y][self.piece_pos[0] + x] = self.current_color
        
        # Cek baris yang penuh
        full_rows = []
        for i, row in enumerate(self.board):
            if all(cell for cell in row):
                full_rows.append(i)
        
        # Hapus baris yang penuh dan tambahkan baris baru di atas
        for row_index in full_rows[::-1]:
            del self.board[row_index]
            del self.colors[row_index]
            self.board.insert(0, [0] * (self.width // self.block_size))
            self.colors.insert(0, [None] * (self.width // self.block_size))
        
        self.new_piece()
        if self.check_collision(self.current_piece, self.piece_pos):
            self.reset_game()

    def draw_trajectory(self):
        trajectory_length = 5  # Panjang lintasan
        for i in range(1, trajectory_length + 1):
            projected_pos = add_vectors(self.piece_pos, scale_vector(self.velocity, i))
            rect = (projected_pos[0] * self.block_size, projected_pos[1] * self.block_size, self.block_size, self.block_size)
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 1)  # Menggambar lintasan dengan warna merah

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_trajectory()  # Menambahkan visualisasi lint asan
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                rect = (x * self.block_size, y * self.block_size, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, self.colors[y][x] or (0, 0, 0), rect, 0)
                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)
        
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    rect = ((self.piece_pos[0] + x) * self.block_size,
                           (self.piece_pos[1] + y) * self.block_size,
                           self.block_size, self.block_size)
                    pygame.draw.rect(self.screen, self.current_color, rect, 0)
                    pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)
        pygame.display.flip()

    def update_position(self):
        new_pos = add_vectors(self.piece_pos, self.velocity)
        if not self.check_collision(self.current_piece, new_pos):
            self.piece_pos = new_pos
        else:
            self.place_piece()

    def run(self):
        while True:
            self.fall_time += self.clock.get_time()
            self.clock.tick()
            
            if self.fall_time >= self.fall_speed:
                self.update_position()
                self.fall_time = 0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not self.check_collision(
                        self.current_piece, (self.piece_pos[0] - 1, self.piece_pos[1])):
                        self.piece_pos = (self.piece_pos[0] - 1, self.piece_pos[1])
                    elif event.key == pygame.K_RIGHT and not self.check_collision(
                        self.current_piece, (self.piece_pos[0] + 1, self.piece_pos[1])):
                        self.piece_pos = (self.piece_pos[0] + 1, self.piece_pos[1])
                    elif event.key == pygame.K_DOWN and not self.check_collision(
                        self.current_piece, (self.piece_pos[0], self.piece_pos[1] + 1)):
                        self.piece_pos = (self.piece_pos[0], self.piece_pos[1] + 1)
                    elif event.key == pygame.K_UP:
                        rotated = list(zip(*self.current_piece[::-1]))
                        if not self.check_collision(rotated, self.piece_pos):
                            self.current_piece = rotated
            self.draw()

if __name__ == "__main__":
    TetrisGame().run()