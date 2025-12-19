import pygame
import os

pygame.init()

# ================== CÀI ĐẶT MÀN HÌNH ==================
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario-like Map")

clock = pygame.time.Clock()

# ================== TILE ==================
TILE_SIZE = 30

# ================== LOAD SPRITE ==================
def load_sprite(filename, width=TILE_SIZE, height=TILE_SIZE):
    try:
        image = pygame.image.load(filename).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    except:
        print("Không tìm thấy:", filename)
        return pygame.Surface((width, height), pygame.SRCALPHA)

# ================== SPRITES ==================
sprites = {
    'dat': load_sprite('dat.png'),
    'cot_xanh': load_sprite('cot_xanh.png', TILE_SIZE, TILE_SIZE * 3),
    'may_co': load_sprite('may_co.png'),
    'hoa': load_sprite('hoa.png'),
    'nam': load_sprite('nam.png'),
    'quai_vat': load_sprite('quai_vat.png'),
    'xu': load_sprite('xu.png'),
    'goombas': load_sprite('goombas_1.png'),
}

# ================== MAP ==================
level_map = [
    "...........................................",
    "...........................................",
    "..............G..............G.............",
    "...........................................",
    "..............W.W..........M...............",
    "...........W.............W.................",
    "...........................................",
    "..........P...............................",
    "...........................................",
    "...........................................",
    "...........................................",
    "...........................................",
    "...........................................",
    "...........................................",
    "...........................................",
    "...........................................",
    "...........................................",
    "...........................................",
    "...........................................",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# ================== VẼ MAP ==================
def draw_map():
    for row_i, row in enumerate(level_map):
        for col_i, tile in enumerate(row):
            x = col_i * TILE_SIZE
            y = row_i * TILE_SIZE

            if tile == 'W':          # đất
                screen.blit(sprites['dat'], (x, y))

            elif tile == 'P':        # cột xanh
                screen.blit(sprites['cot_xanh'], (x, y - TILE_SIZE * 2))

            elif tile == 'G':        # mây / cỏ
                screen.blit(sprites['may_co'], (x, y))

            elif tile == 'M':        # nấm
                screen.blit(sprites['nam'], (x, y))

# ================== GAME LOOP ==================
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # nền trời xanh
    screen.fill((92, 148, 252))

    # vẽ map
    draw_map()

    pygame.display.flip()

pygame.quit()
