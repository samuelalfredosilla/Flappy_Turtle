import pygame
import random

# Konstanta untuk ukuran layar, gravitasi, kecepatan pipa, kecepatan api, dan interval spawn koin
LEBAR_LAYAR = 1000
TINGGI_LAYAR = 660
GRAVITASI = 0.7
KECEPATAN_PIPA = 4
KECEPATAN_API = 10  # Kecepatan Api lebih cepat dari Pipa
SPAWN_KOIN_INTERVAL = 1500  # Interval waktu untuk spawn koin dalam milidetik

# Kelas dasar untuk objek game
class ObjekGame:
    def __init__(self, x, y):
        self._x = x  # Atribut protected untuk posisi X
        self._y = y  # Atribut protected untuk posisi Y

    def update(self):
        pass  # Metode untuk pembaruan (override di kelas turunan)

    def draw(self, surface):
        pass  # Metode untuk menggambar objek (override di kelas turunan)

# Kelas untuk Turtle (karakter utama)
class Turtle(ObjekGame):
    def __init__(self, x, y, gambar_path, lebar=None, tinggi=None):
        super().__init__(x, y)
        self.__kecepatan = 0  # Atribut private untuk kecepatan Turtle
        self.gambar = pygame.image.load(gambar_path).convert_alpha()  # Memuat gambar Turtle
        
        # Mengatur ukuran gambar jika diberikan
        if lebar and tinggi:
            self.gambar = pygame.transform.scale(self.gambar, (lebar, tinggi))
        
        self.lebar = self.gambar.get_width()  # Lebar Turtle
        self.tinggi = self.gambar.get_height()  # Tinggi Turtle

    def lompat(self):
        self.__kecepatan = -10  # Memberikan kecepatan ke atas saat Turtle melompat

    def update(self):
        self.__kecepatan += GRAVITASI  # Menambahkan gravitasi ke kecepatan Turtle
        self._y += self.__kecepatan  # Memperbarui posisi Turtle berdasarkan kecepatan

    def draw(self, surface):
        surface.blit(self.gambar, (self._x, int(self._y)))  # Menggambar Turtle pada layar

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self.lebar, self.tinggi)  # Mendapatkan bounding box Turtle

# Kelas untuk pipa (rintangan)
class Pipa(ObjekGame):
    def __init__(self, x, tinggi):
        super().__init__(x, tinggi)
        self.lebar = 50  # Lebar pipa

    def update(self):
        self._x -= KECEPATAN_PIPA  # Memindahkan pipa ke kiri

    def draw(self, surface):
        # Menggambar pipa atas dan bawah
        pygame.draw.rect(surface, (0, 255, 0), (self._x, 0, self.lebar, self._y))  # Pipa atas
        pygame.draw.rect(surface, (0, 255, 0), (self._x, self._y + 150, self.lebar, TINGGI_LAYAR - self._y - 150))  # Pipa bawah

    def get_rects(self):
        # Mendapatkan bounding box untuk pipa atas dan bawah
        return [
            pygame.Rect(self._x, 0, self.lebar, self._y),  # Pipa atas
            pygame.Rect(self._x, self._y + 150, self.lebar, TINGGI_LAYAR - self._y - 150)  # Pipa bawah
        ]

# Kelas untuk koin (item yang dapat diambil)
class Koin(ObjekGame):
    def __init__(self, x, y, gambar_path, lebar=None, tinggi=None):
        super().__init__(x, y)
        self.gambar = pygame.image.load(gambar_path).convert_alpha()  # Memuat gambar koin
        
        # Mengatur ukuran gambar jika diberikan
        if lebar and tinggi:
            self.gambar = pygame.transform.scale(self.gambar, (lebar, tinggi))
        
        self.lebar = self.gambar.get_width()  # Lebar koin
        self.tinggi = self.gambar.get_height()  # Tinggi koin

    def draw(self, surface):
        surface.blit(self.gambar, (self._x, self._y))  # Menggambar koin pada layar

    def get_rect(self):
        return pygame.Rect(self._x, self._y, self.lebar, self.tinggi)  # Mendapatkan bounding box koin

# Kelas untuk api (rintangan tambahan dengan kecepatan lebih tinggi)
class Api(Pipa):
    def __init__(self, x, tinggi, gambar_path, lebar=None, tinggi_api=None):
        super().__init__(x, tinggi)
        self.gambar = pygame.image.load(gambar_path).convert_alpha()  # Memuat gambar api
        
        # Mengatur ukuran gambar jika diberikan
        if lebar and tinggi_api:
            self.gambar = pygame.transform.scale(self.gambar, (lebar, tinggi_api))
        
        self.lebar = self.gambar.get_width()  # Lebar gambar api
        self.tinggi = self.gambar.get_height()  # Tinggi gambar api

    def update(self):
        self._x -= KECEPATAN_API  # Memindahkan api ke kiri dengan kecepatan lebih tinggi

    def draw(self, surface):
        surface.blit(self.gambar, (self._x, self._y))  # Menggambar api pada layar

# Kelas untuk latar belakang permainan
class LatarBelakang(ObjekGame):
    def __init__(self, gambar_path):
        super().__init__(0, 0)
        self.gambar = pygame.image.load(gambar_path).convert()  # Memuat gambar latar belakang

    def draw(self, surface):
        surface.blit(self.gambar, (0, 0))  # Menggambar latar belakang pada layar

# Kelas utama untuk permainan
class PermainanFlappyBird:
    def __init__(self):
        pygame.init()  # Inisialisasi pygame
        self.layar = pygame.display.set_mode((LEBAR_LAYAR, TINGGI_LAYAR))  # Membuat layar permainan
        self.jam = pygame.time.Clock()  # Untuk mengatur frame rate
        # Membuat objek permainan
        self.Turtle = Turtle(100, 300, "turtle.png", lebar=50, tinggi=50)  
        self.pipa = []  # Daftar pipa
        self.api = []  # Daftar api
        self.koin = []  # Daftar koin
        self.latar_belakang = LatarBelakang("sky3.jpg")  # Gambar latar belakang
        self.score = 0  # Skor awal
        self.spawn_pipa()  # Spawn pipa pertama
        self.spawn_api()  # Spawn api pertama
        self.last_koin_spawn_time = pygame.time.get_ticks()  # Waktu terakhir koin spawn
        self.game_over = False  # Status game over
        self.game_started = False  # Status permainan dimulai

    def reset(self):
        # Reset status permainan ke awal
        self.__init__()

    def spawn_pipa(self):
        # Menambahkan pipa baru ke dalam daftar
        tinggi = random.randint(100, 400)
        self.pipa.append(Pipa(LEBAR_LAYAR, tinggi))

    def spawn_api(self):
        # Menambahkan api baru ke dalam daftar
        tinggi = random.randint(0, TINGGI_LAYAR - 20)
        self.api.append(Api(LEBAR_LAYAR, tinggi, "fire.png", lebar=40, tinggi_api=40))

    def spawn_koin(self):
        # Menambahkan koin baru ke dalam daftar
        x = LEBAR_LAYAR
        y = random.randint(50, TINGGI_LAYAR - 50)
        self.koin.append(Koin(x, y, "koin.png", lebar=40, tinggi=40))

    def cek_tabrakan(self):
        # Mengecek apakah Turtle bertabrakan dengan pipa atau api
        for pipa in self.pipa:
            for rect in pipa.get_rects():
                if self.Turtle.get_rect().colliderect(rect):
                    return True
        for api in self.api:
            if self.Turtle.get_rect().colliderect(pygame.Rect(api._x, api._y, api.lebar, api.tinggi)):
                return True
        return False

    def cek_koin_diambil(self):
        # Mengecek apakah Turtle mengambil koin
        for koin in self.koin:
            if self.Turtle.get_rect().colliderect(koin.get_rect()):
                self.koin.remove(koin)  # Menghapus koin dari daftar
                self.score += 1  # Menambahkan skor

    def run(self):
        berjalan = True  # Variabel untuk menentukan apakah permainan berjalan
        while berjalan:  # Loop utama permainan
            # Mengolah event dari pengguna
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Jika pengguna menutup jendela
                    berjalan = False
                if event.type == pygame.KEYDOWN:  # Jika tombol ditekan
                    if event.key == pygame.K_SPACE:  # Jika tombol SPACE ditekan
                        if not self.game_started:  # Jika permainan belum dimulai
                            self.game_started = True  # Memulai permainan
                        elif self.game_over:  # Jika permainan telah berakhir
                            self.reset()  # Mengatur ulang permainan
                        else:  # Jika permainan sedang berlangsung
                            self.Turtle.lompat()  # Membuat Turtle melompat

            if self.game_started:  # Jika permainan telah dimulai
                if not self.game_over:  # Jika permainan belum berakhir
                    self.Turtle.update()  # Mengupdate posisi Turtle
                    # Mengupdate posisi pipa
                    for pipa in self.pipa:
                        pipa.update()
                        if pipa._x < -pipa.lebar:  # Jika pipa keluar dari layar
                            self.pipa.remove(pipa)  # Menghapus pipa
                            self.spawn_pipa()  # Menambah pipa baru
                    # Mengupdate posisi api
                    for api in self.api:
                        api.update()
                        if api._x < -api.lebar:  # Jika api keluar dari layar
                            self.api.remove(api)  # Menghapus api
                            self.spawn_api()  # Menambah api baru
                    # Mengatur spawn koin berdasarkan waktu
                    current_time = pygame.time.get_ticks()  # Waktu sekarang
                    if current_time - self.last_koin_spawn_time > SPAWN_KOIN_INTERVAL:
                        self.spawn_koin()  # Menambah koin baru
                        self.last_koin_spawn_time = current_time
                    # Mengupdate posisi koin
                    for koin in self.koin:
                        koin._x -= KECEPATAN_PIPA  # Menggerakkan koin ke kiri
                        if koin._x < -koin.lebar:  # Jika koin keluar dari layar
                            self.koin.remove(koin)  # Menghapus koin
                    self.cek_koin_diambil()  # Mengecek apakah Turtle mengambil koin
                    # Mengecek apakah Turtle jatuh ke bawah layar
                    if self.Turtle._y + self.Turtle.tinggi >= TINGGI_LAYAR:
                        self.Turtle._y = 0  # Mengatur ulang posisi Turtle
                    if self.cek_tabrakan():  # Mengecek apakah terjadi tabrakan
                        self.game_over = True  # Mengakhiri permainan
                # Menggambar latar belakang dan semua objek permainan
                self.layar.fill((135, 206, 235))  # Membersihkan layar
                self.latar_belakang.draw(self.layar)  # Menggambar latar belakang
                self.Turtle.draw(self.layar)  # Menggambar Turtle
                for pipa in self.pipa:
                    pipa.draw(self.layar)  # Menggambar semua pipa
                for api in self.api:
                    api.draw(self.layar)  # Menggambar semua api
                for koin in self.koin:
                    koin.draw(self.layar)  # Menggambar semua koin
                # Menampilkan skor pada layar
                font = pygame.font.Font(None, 36)
                text = font.render(f"Score: {self.score}", True, (255, 255, 255))
                self.layar.blit(text, (10, 10))  # Menampilkan skor di pojok kiri atas
                if self.game_over:  # Jika permainan berakhir
                    font = pygame.font.Font(None, 74)
                    text = font.render("Game Over", True, (255, 0, 0))
                    self.layar.blit(text, (LEBAR_LAYAR // 2.86, TINGGI_LAYAR // 2.5))  # Menampilkan teks "Game Over"
                    font_small = pygame.font.Font(None, 36)
                    text_restart = font_small.render("Press Space to Restart", True, (255, 255, 255))
                    self.layar.blit(text_restart, (LEBAR_LAYAR // 2.8, TINGGI_LAYAR // 2))  # Menampilkan teks restart
            else:
                # Jika permainan belum dimulai, menampilkan pesan "Press Space to Start"
                font = pygame.font.Font(None, 74)
                text = font.render("Press Space to Start", True, (255, 255, 255))
                self.layar.blit(text, (LEBAR_LAYAR // 4, TINGGI_LAYAR // 2))
            pygame.display.flip()  # Memperbarui layar
            self.jam.tick(60)  # Menjaga kecepatan frame tetap stabil
        pygame.quit()  # Mengakhiri permainan dan keluar dari loop utama

if __name__ == "__main__":
    permainan = PermainanFlappyBird()  # Membuat instance permainan
    permainan.run()  # Menjalankan permainan