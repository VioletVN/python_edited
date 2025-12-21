import pygame
from Const import GRAVITY, MAX_FALL_SPEED, MAX_MOVE_SPEED, MAX_FASTMOVE_SPEED


class RuaKoopa(pygame.sprite.Sprite):
    """
    Koopa states and behaviour:
    - DI_CHUYEN: walking left/right, animated.
    - MAI_DUNG_YEN: shell is stationary after being stomped.
    - MAI_TRUOT: shell slides fast after being kicked.

    Methods to control behaviour externally:
    - bi_dam(): call when Mario stomps from above -> enters MAI_DUNG_YEN.
    - da_mai(mario_x): call when Mario kicks the shell -> enters MAI_TRUOT and moves
      away from Mario's x position.
    - dao_huong(): reverse horizontal direction (e.g., when hitting a wall).

    Update requires a list of solid blocks for collisions. Each item can be either
    a pygame.Rect or any object with a .rect attribute that is a Rect.
    """

    DI_CHUYEN = 0
    MAI_DUNG_YEN = 1
    MAI_TRUOT = 2

    WALK_SIZE = (30, 30)
    SHELL_SIZE = (30, 24)

    def __init__(self, x: int, y: int, huong_trai=True):
        super().__init__()

        # Load images
        walk0 = pygame.image.load("images/koopa_0.png").convert_alpha()
        walk1 = pygame.image.load("images/koopa_1.png").convert_alpha()
        shell = pygame.image.load("images/koopa_dead.png").convert_alpha()

        self.khung_di = [
            pygame.transform.scale(walk0, self.WALK_SIZE),
            pygame.transform.scale(walk1, self.WALK_SIZE),
        ]
        self.hinh_mai = pygame.transform.scale(shell, self.SHELL_SIZE)

        # Visuals/rect
        self.image = self.khung_di[0]
        self.rect = self.image.get_rect(topleft=(x, y))

        # Animation
        self.chi_so_khung = 0
        self.dem_khung = 0
        self.do_tre_khung = 10

        # Physics
        self.trong_luc = GRAVITY
        self.van_toc_roi_toi_da = MAX_FALL_SPEED
        self.toc_do_di = MAX_MOVE_SPEED
        self.toc_do_mai = MAX_FASTMOVE_SPEED

        self.vx = -self.toc_do_di if huong_trai else self.toc_do_di
        self.vy = 0
        self.trang_thai = RuaKoopa.DI_CHUYEN

    @staticmethod
    def _as_rect(obj):
        return obj if isinstance(obj, pygame.Rect) else getattr(obj, "rect", None)

    def _collide_vertical(self, blocks):
        self.vy += self.trong_luc
        if self.vy > self.van_toc_roi_toi_da:
            self.vy = self.van_toc_roi_toi_da
        self.rect.y += self.vy

        for b in blocks:
            r = self._as_rect(b)
            if not r:
                continue
            if self.rect.colliderect(r):
                if self.vy > 0:  # falling -> land on top
                    self.rect.bottom = r.top
                    self.vy = 0
                elif self.vy < 0:  # moving up -> hit head
                    self.rect.top = r.bottom
                    self.vy = 0

    def _collide_horizontal(self, blocks):
        self.rect.x += self.vx
        for b in blocks:
            r = self._as_rect(b)
            if not r:
                continue
            if self.rect.colliderect(r):
                if self.vx > 0:
                    self.rect.right = r.left
                elif self.vx < 0:
                    self.rect.left = r.right

                # Reaction on side collision
                if self.trang_thai in (RuaKoopa.DI_CHUYEN, RuaKoopa.MAI_TRUOT):
                    # bounce back
                    self.vx *= -1
                else:
                    # stationary shell should not move
                    self.vx = 0

    def update(self, danh_sach_khoi):
        # Vertical physics
        self._collide_vertical(danh_sach_khoi)

        # Horizontal movement depending on state
        if self.trang_thai == RuaKoopa.DI_CHUYEN:
            self._collide_horizontal(danh_sach_khoi)
            self.cap_nhat_animation()
        elif self.trang_thai == RuaKoopa.MAI_TRUOT:
            self._collide_horizontal(danh_sach_khoi)
            self.image = self.hinh_mai
        else:  # MAI_DUNG_YEN
            self.image = self.hinh_mai
            # frictionless stop already applied (vx == 0)

    def cap_nhat_animation(self):
        self.dem_khung += 1
        if self.dem_khung >= self.do_tre_khung:
            self.dem_khung = 0
            self.chi_so_khung = (self.chi_so_khung + 1) % len(self.khung_di)
            self.image = self.khung_di[self.chi_so_khung]

    def _chuyen_sang_mai(self):
        """Change sprite/rect to shell while keeping feet position (bottom)."""
        old_bottom = self.rect.bottom
        self.image = self.hinh_mai
        self.rect = self.image.get_rect()
        self.rect.bottom = old_bottom

    def dao_huong(self):
        if self.trang_thai in (RuaKoopa.DI_CHUYEN, RuaKoopa.MAI_TRUOT):
            self.vx *= -1

    def bi_dam(self):
        """Call this when Mario stomps the Koopa from above."""
        if self.trang_thai == RuaKoopa.DI_CHUYEN:
            self.trang_thai = RuaKoopa.MAI_DUNG_YEN
            self._chuyen_sang_mai()
            self.vx = 0
        elif self.trang_thai == RuaKoopa.MAI_TRUOT:
            # Stomp a sliding shell -> stop it
            self.trang_thai = RuaKoopa.MAI_DUNG_YEN
            self._chuyen_sang_mai()
            self.vx = 0
        # If already stationary shell, keep as is

    def da_mai(self, vi_tri_mario_x: int):
        """Kick the shell. Mario's x is used to determine direction away from him."""
        if self.trang_thai == RuaKoopa.MAI_DUNG_YEN:
            self.trang_thai = RuaKoopa.MAI_TRUOT
            # Move away from Mario
            if vi_tri_mario_x < self.rect.centerx:
                self.vx = self.toc_do_mai  # Mario on the left -> slide right
            else:
                self.vx = -self.toc_do_mai  # Mario on the right -> slide left
        elif self.trang_thai == RuaKoopa.MAI_TRUOT:
            # If already sliding and player interacts again, stop it
            self.trang_thai = RuaKoopa.MAI_DUNG_YEN
            self.vx = 0
