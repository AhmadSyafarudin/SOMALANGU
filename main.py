import pygame
import random

#List Warna Blok untuk dikeluarkan secara Random
warna = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]


class BlokTetris:
    x = 0
    y = 0

    blok_tetris = [
        [[1, 5, 9, 13], [4, 5, 6, 7]], #bentuk garis lurus
        [[4, 5, 9, 10], [2, 6, 5, 9]], #bentuk Z
        [[6, 7, 9, 10], [1, 5, 6, 10]], #bentuk S
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], #bentuk L
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], #bentuk J
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  #bentuk T
        [[1, 2, 5, 6]], #bentuk O
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bentuk_blok = random.randint(0, len(self.blok_tetris) - 1)
        self.warna_blok = random.randint(1, len(warna) - 1)
        self.ubah_bentuk = 0

    def TampilanBlok(self):
        return self.blok_tetris[self.bentuk_blok][self.ubah_bentuk]

    def Putar(self):
        self.ubah_bentuk = (self.ubah_bentuk + 1) % len(self.blok_tetris[self.bentuk_blok])


class Papan :
    x = 100
    y = 60
    zoom = 20

    def __init__(self, tinggi, lebar):
        self.tinggi = tinggi
        self.lebar = lebar
        self.grid = []
        self.state = "mulai"
        for i in range(tinggi):
            garis_grid = []
            for j in range(lebar):
                garis_grid.append(0)
            self.grid.append(garis_grid)

class Nilai(Papan) :

  def __init__ (self, tinggi, lebar) :
    super().__init__(tinggi, lebar) 
    self.nilai = 0
    self.jumlah_baris = 0 
    
  def BarisHilang(self):
        baris = 0
        for i in range(1, self.tinggi):
            zeros = 0
            for j in range(self.lebar):
                if self.grid[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                baris += 1
                self.jumlah_baris += 1
                for k in range(i, 1, -1):
                    for l in range(self.lebar):
                        self.grid[k][l] = self.grid[k - 1][l]
        
        if self.jumlah_baris <= 3 :
            if baris == 2 :
                self.nilai += (baris ** 2) -1
            if baris == 3 :
                self.nilai += (baris ** 2) -2
            if baris == 1 :
                self.nilai += (baris ** 2) 
        else :
            self.nilai += 2 * self.jumlah_baris  
            self.jumlah_baris = 0

class Menu(Nilai) :
    def __init__ (self, tinggi, lebar) :
        super().__init__(tinggi, lebar)

    def MenuUtama (self) :
        self.jenis_huruf = pygame.font.SysFont('Sans-Serrif', 23, True, False)
        self.menu_1 = self.jenis_huruf.render("> Tekan Arah Bawah Untuk Permainan Baru", True, (255, 125, 0))
        self.menu_2 = self.jenis_huruf.render("> Tekan Tombol 'C' Untuk Keluar", True, (255, 125, 0))
        return self.menu_1, self.menu_2

    def AmbilAksi (self) :
        for event in pygame.event.get():
            if event.type == pygame.KEYUP :
                if event.key == pygame.K_DOWN :
                    return True
                if event.key == pygame.K_c :
                    pygame.quit()

            if event.type == pygame.QUIT :
                pygame.quit()
                
        return None
        

class Tetris(Menu):
    level = 2
    blok = None

    def __init__(self, tinggi, lebar):
       super().__init__(tinggi, lebar)

    def BuatBlok(self):
        self.blok = BlokTetris(3, 0)

    def CekLayar(self):
        batas_atas_layar = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.blok.TampilanBlok():
                    if i + self.blok.y > self.tinggi - 1 or \
                            j + self.blok.x > self.lebar - 1 or \
                            j + self.blok.x < 0 or \
                            self.grid[i + self.blok.y][j + self.blok.x] > 0:
                        batas_atas_layar = True
        return batas_atas_layar


    def BlokJatuh(self):
        self.blok.y += 1
        if self.CekLayar():
            self.blok.y -= 1
            self.BlokBerhenti()

    def BlokBerhenti(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.blok.TampilanBlok():
                    self.grid[i + self.blok.y][j + self.blok.x] = self.blok.warna_blok
        self.BarisHilang()
        self.BuatBlok()
        if self.CekLayar():
            self.state = "berakhir"

    def GerakSamping(self, dx):
        blok_sebelum_pindah = self.blok.x
        self.blok.x += dx
        if self.CekLayar():
            self.blok.x = blok_sebelum_pindah

    def Putar(self):
        blok_sebelum_diubah = self.blok.ubah_bentuk
        self.blok.Putar()
        if self.CekLayar():
            self.blok.ubah_bentuk = blok_sebelum_diubah


pygame.init()

hitam = (0, 0, 0)
putih = (255, 255, 255)
abu = (128, 128, 128)

ukuran_layar = (400, 500)
layar = pygame.display.set_mode(ukuran_layar)

pygame.display.set_caption("Tetris")


clock = pygame.time.Clock()
fps = 25
tetris = Tetris(20, 10)
menu_1, menu_2 = tetris.MenuUtama()
layar.blit(menu_1, [20, 200 ])
layar.blit(menu_2, [25, 265])

while tetris.AmbilAksi() == None:
    pygame.display.update()
    clock.tick()

berakhir = False
counter = 0

tekan_arah_bawah = False

while not berakhir:
    if tetris.blok is None:
        tetris.BuatBlok()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // tetris.level // 2) == 0 or tekan_arah_bawah:
        if tetris.state == "mulai":
            tetris.BlokJatuh()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            berakhir = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                tetris.Putar()
            if event.key == pygame.K_DOWN:
                tekan_arah_bawah = True
            if event.key == pygame.K_LEFT:
                tetris.GerakSamping(-1)
            if event.key == pygame.K_RIGHT:
                tetris.GerakSamping(1)
            if event.key == pygame.K_ESCAPE:
                tetris = Tetris(20, 10)
            if event.key == pygame.K_c :
                pygame.quit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                tekan_arah_bawah = False

    layar.fill(putih)

    for i in range(tetris.tinggi):
        for j in range(tetris.lebar):
            pygame.draw.rect(layar, abu, [tetris.x + tetris.zoom * j, tetris.y + tetris.zoom * i, tetris.zoom, tetris.zoom], 1)
            if tetris.grid[i][j] > 0:
                pygame.draw.rect(layar, warna[tetris.grid[i][j]],
                                 [tetris.x + tetris.zoom * j + 1, tetris.y + tetris.zoom * i + 1, tetris.zoom - 2, tetris.zoom - 1])

    if tetris.blok is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in tetris.blok.TampilanBlok():
                    pygame.draw.rect(layar, warna[tetris.blok.warna_blok],
                                     [tetris.x + tetris.zoom * (j + tetris.blok.x) + 1,
                                      tetris.y + tetris.zoom * (i + tetris.blok.y) + 1,
                                      tetris.zoom - 2, tetris.zoom - 2])

    jenis_huruf = pygame.font.SysFont('Sans-Serrif', 25, True, False)
    jenis_huruf_2 = pygame.font.SysFont('Sans-Serrif', 30, True, False)
    jenis_huruf_3 = pygame.font.SysFont('Sans-Serrif', 20, True, False)
    score = jenis_huruf.render("Score: " + str(tetris.nilai), True, hitam)
    permainan_berakhir = jenis_huruf_2.render("Permainan Berakhir", True, (232, 18, 18))
    pilihan_1 = jenis_huruf_3.render("> Tekan 'ESC' untuk Permainan Baru", True, (255, 215, 0))
    pilihan_2 = jenis_huruf_3.render("> Tekan 'C' untuk Keluar", True, (255, 215, 0))

    layar.blit(score, [150, 0])
    if tetris.state == "berakhir":
        layar.blit(permainan_berakhir, [90, 20])
        layar.blit(pilihan_1, [75, 460])
        layar.blit(pilihan_2, [75, 475])
        

    pygame.display.flip()
    clock.tick(fps)
