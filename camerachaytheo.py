import pygame
pygame.init()

# Màn hình hiển thị
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Camera Follow")

clock = pygame.time.Clock()

# Mario properties
mario_x = 100         # vị trí trong world
mario_y = 300
mario_speed = 5
mario_width = 40
mario_height = 60

# World length
WORLD_WIDTH = 3000    # thế giới dài 3000px

# Camera offset
camera_x = 0

# Màu
BLUE = (50, 150, 255)
GREEN = (50, 200, 50)
RED = (255, 0, 0)


running = True
while running:
    dt = clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -------- XỬ LÝ PHÍM BẤM --------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        mario_x += mario_speed
    if keys[pygame.K_LEFT]:
        mario_x -= mario_speed

    # Giới hạn Mario không vượt khỏi world
    mario_x = max(0, min(mario_x, WORLD_WIDTH - mario_width))

    # -------- CẬP NHẬT CAMERA --------
    # Camera luôn giữ Mario ở giữa màn hình
    camera_x = mario_x - SCREEN_WIDTH // 2

    # Camera không ra khỏi world
    camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))

    # -------- VẼ MÀN HÌNH --------
    screen.fill(BLUE)   # nền trời

    # Đất
    pygame.draw.rect(screen, GREEN, (0 - camera_x, 360, WORLD_WIDTH, 40))

    # Vẽ Mario (đã trừ camera offset)
    pygame.draw.rect(screen, RED,
                     (mario_x - camera_x, mario_y, mario_width, mario_height))

    pygame.display.flip()

pygame.quit()
