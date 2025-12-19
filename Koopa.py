import pygame

class RuaKoopa(pygame.sprite.Sprite):
    DI_CHUYEN = 0
    MAI_DUNG_YEN = 1
    MAI_TRUOT = 2

    def __init__(self, x, y, cau_hinh):
        super().__init__()

        self.khung_di = [
            pygame.image.load("images/koopa_0.png").convert_alpha(),
            pygame.image.load("images/koopa_1.png").convert_alpha()
        ]
        self.khung_di = [
            pygame.transform.scale(img, (32, 32)) for img in self.khung_di
        ]
        self.hinh_mai = pygame.image.load("images/koopa_dead.png")
        ).convert_alpha()
        self.hinh_mai = pygame.transform.scale(self.hinh_mai, (32, 24))

        self.image = self.khung_di[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.chi_so_khung = 0
        self.dem_khung = 0
        self.do_tre_khung = 10  

        self.trong_luc = cau_hinh.GRAVITY
        self.van_toc_roi_toi_da = cau_hinh.MAX_FALL_SPEED

        self.toc_do_di = cau_hinh.MAX_MOVE_SPEED
        self.toc_do_mai = cau_hinh.MAX_FASTMOVE_SPEED

        self.vx = -self.toc_do_di
        self.vy = 0
        self.trang_thai = RuaKoopa.DI_CHUYEN

    def update(self, nen):
        self.vy += self.trong_luc
        if self.vy > self.van_toc_roi_toi_da:
            self.vy = self.van_toc_roi_toi_da
        self.rect.y += self.vy

        for mat_dat in nen:
            if self.rect.colliderect(mat_dat.rect):
                if self.vy > 0:
                    self.rect.bottom = mat_dat.rect.top
                    self.vy = 0

        if self.trang_thai == RuaKoopa.DI_CHUYEN:
            self.rect.x += self.vx
            self.cap_nhat_animation()
        elif self.trang_thai == RuaKoopa.MAI_TRUOT:
            self.rect.x += self.vx
            self.image = self.hinh_mai
        else:
            self.image = self.hinh_mai

    def cap_nhat_animation(self):
        self.dem_khung += 1
        if self.dem_khung >= self.do_tre_khung:
            self.dem_khung = 0
            self.chi_so_khung = (self.chi_so_khung + 1) % len(self.khung_di)
            self.image = self.khung_di[self.chi_so_khung]

    def dao_huong(self):
        self.vx *= -1

    def bi_dam(self):
        if self.trang_thai == RuaKoopa.DI_CHUYEN:
            self.trang_thai = RuaKoopa.MAI_DUNG_YEN
            self.image = self.hinh_mai
            self.vx = 0

    def da_mai(self, vi_tri_mario_x):
        if self.trang_thai == RuaKoopa.MAI_DUNG_YEN:
            self.trang_thai = RuaKoopa.MAI_TRUOT
            if vi_tri_mario_x < self.rect.centerx:
                self.vx = self.toc_do_mai
            else:
                self.vx = -self.toc_do_mai
