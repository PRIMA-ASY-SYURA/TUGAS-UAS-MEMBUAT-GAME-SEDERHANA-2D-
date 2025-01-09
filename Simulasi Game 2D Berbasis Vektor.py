import pygame
import random

# Fungsi untuk menambahkan dua vektor
def add_vectors(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

# Fungsi untuk mengurangi dua vektor
def subtract_vectors(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

# Fungsi untuk mengalikan vektor dengan skalar
def scale_vector(v, scalar):
    return (v[0] * scalar, v[1] * scalar)

class TetrisGame:
    # Mendefinisikan bentuk-bentuk Tetris
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
        # Inisialisasi Pygame dan pengaturan awal permainan
        pygame.init()
        self.block_size = 30  # Ukuran setiap blok
        self.width, self.height = 300, 600  # Ukuran layar
        self.screen = pygame.display.set_mode((self.width, self.height))  # Membuat layar
        pygame.display.set_caption("Simple Tetris")  # Judul jendela
        self.reset_game()  # Mengatur ulang permainan
        self.clock = pygame.time.Clock()  # Mengatur jam untuk kontrol waktu
        self.fall_time = 0  # Waktu jatuh untuk kontrol kecepatan jatuh
        self.fall_speed = 500  # Kecepatan jatuh dalam milidetik
        self.velocity = (0, 1)  # Kecepatan awal (x, y)

    def reset_game(self):
        # Mengatur ulang papan permainan
        cols, rows = self.width // self.block_size, self.height // self.block_size
        self.board = [[0] * cols for _ in range(rows)]  # Membuat papan kosong
        self.colors = [[None] * cols for _ in range(rows)]  # Menyimpan warna untuk setiap blok
        self.new_piece()  # Menghasilkan potongan baru
        
    def new_piece(self):
        # Menghasilkan potongan baru secara acak
        self.current_piece = random.choice(list(self.SHAPES.values()))  # Memilih bentuk acak
        self.current_color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))  # Warna acak
        self.piece_pos = (4, 0)  # Posisi awal potongan

    def check_collision(self, piece, pos):
        # Memeriksa apakah potongan bertabrakan dengan papan
        return any(cell and (pos[1] + y >= len(self.board) or 
                             pos[0] + x < 0 or pos[0] + x >= len(self.board[0]) or
                             (pos[1] + y >= 0 and self.board[pos[1] + y][pos[0] + x]))
                   for y, row in enumerate(piece) 
                   for x, cell in enumerate(row))

    def place_piece(self):
        # Menempatkan potongan di papan
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[self.piece_pos[1] + y][self.piece_pos[0] + x] = 1  # Menandai blok terisi
                    self.colors[self.piece_pos[1] + y][self.piece_pos[0] + x] = self.current_color  # Menyimpan warna
        
        # Cek baris yang penuh
        full_rows = []
        for i, row in enumerate(self.board):
            if all(cell for cell in row):  # Jika semua sel terisi
                full_rows.append(i)  # Tambahkan indeks baris penuh
        
        # Hapus baris yang penuh dan tambahkan baris baru di atas
        for row_index in full_rows[::-1]:  # Hapus dari bawah ke atas
            del self.board[row_index]
            del self.colors[row_index]  # Hapus warna baris yang penuh
            self.board.insert(0, [0] * (self.width // self.block_size))  # Tambahkan baris baru kosong di atas
            self.colors.insert(0, [None] * (self.width // self.block_size))  # Tambahkan warna None untuk baris baru
        
        self.new_piece()  # Menghasilkan potongan baru
        if self.check_collision(self.current_piece, self.piece_pos):  # Cek jika potongan baru bertabrakan
            self.reset_game()  # Reset permainan jika bertabrakan

    def draw_trajectory(self):
        # Menggambar lintasan potongan yang jatuh
        trajectory_length = 5  # Panjang lintasan
        for i in range(1, trajectory_length + 1):
            projected_pos = add_vectors(self.piece_pos, scale_vector(self.velocity, i))  # Posisi yang diproyeksikan
            rect = (projected_pos[0] * self.block_size, projected_pos[1] * self.block_size, self.block_size, self.block_size)  # Menghitung ukuran dan posisi
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 1)  # Menggambar lintasan dengan warna merah

    def draw(self):
        # Menggambar papan permainan dan potongan
        self.screen.fill((0, 0, 0))  # Mengisi latar belakang dengan warna hitam
        self.draw_trajectory()  # Menambahkan visualisasi lintasan
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                rect = (x * self.block_size, y * self.block_size, self.block_size, self.block_size)  # Menghitung posisi setiap blok
                pygame.draw.rect(self.screen, self.colors[y][x] or (0, 0, 0), rect, 0)  # Menggambar blok dengan warna yang sesuai
                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)  # Menggambar garis tepi blok
        
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    rect = ((self.piece_pos[0] + x) * self.block_size,
                           (self.piece_pos[1] + y) * self.block_size,
                           self.block_size, self.block_size)  # Menghitung posisi potongan saat ini
                    pygame.draw.rect(self.screen, self.current_color, rect, 0)  # Menggambar potongan dengan warna saat ini
                    pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)  # Menggambar garis tepi potongan
        pygame.display.flip()  # Memperbarui tampilan layar

    def update_position(self):
        # Memperbarui posisi potongan
        new_pos = add_vectors(self.piece_pos, self.velocity)  # Menghitung posisi baru
        if not self .check_collision(self.current_piece, new_pos):  # Cek tabrakan
            self.piece_pos = new_pos  # Jika tidak bertabrakan, perbarui posisi
        else:
            self.place_piece()  # Jika bertabrakan, tempatkan potongan di papan

    def run(self):
        # Fungsi utama untuk menjalankan permainan
        while True:
            self.fall_time += self.clock.get_time()  # Menghitung waktu jatuh
            self.clock.tick()  # Mengatur kecepatan frame
            
            if self.fall_time >= self.fall_speed:  # Jika waktu jatuh melebihi kecepatan jatuh
                self.update_position()  # Perbarui posisi potongan
                self.fall_time = 0  # Reset waktu jatuh
            
            for event in pygame.event.get():  # Mengambil semua event
                if event.type == pygame.QUIT:  # Jika jendela ditutup
                    pygame.quit()  # Keluar dari Pygame
                    return
                if event.type == pygame.KEYDOWN:  # Jika tombol ditekan
                    if event.key == pygame.K_LEFT and not self.check_collision(
                        self.current_piece, (self.piece_pos[0] - 1, self.piece_pos[1])):  # Cek tabrakan saat bergerak ke kiri
                        self.piece_pos = (self.piece_pos[0] - 1, self.piece_pos[1])  # Pindah ke kiri
                    elif event.key == pygame.K_RIGHT and not self.check_collision(
                        self.current_piece, (self.piece_pos[0] + 1, self.piece_pos[1])):  # Cek tabrakan saat bergerak ke kanan
                        self.piece_pos = (self.piece_pos[0] + 1, self.piece_pos[1])  # Pindah ke kanan
                    elif event.key == pygame.K_DOWN and not self.check_collision(
                        self.current_piece, (self.piece_pos[0], self.piece_pos[1] + 1)):  # Cek tabrakan saat bergerak ke bawah
                        self.piece_pos = (self.piece_pos[0], self.piece_pos[1] + 1)  # Pindah ke bawah
                    elif event.key == pygame.K_UP:  # Jika tombol atas ditekan
                        rotated = list(zip(*self.current_piece[::-1]))  # Memutar potongan
                        if not self.check_collision(rotated, self.piece_pos):  # Cek tabrakan setelah rotasi
                            self.current_piece = rotated  # Jika tidak bertabrakan, terapkan rotasi
            self.draw()  # Menggambar papan permainan dan potongan

if __name__ == "__main__":
    TetrisGame().run()  # Menjalankan permainan Tetris