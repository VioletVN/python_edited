import pygame
import sys
import os
from Const import FPS, GRAVITY, JUMP_POWER, MAX_FALL_SPEED

pygame.init()
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, "Mario", "sounds")
MARIO_IMAGES_DIR = os.path.join(BASE_DIR, "Mario", "images", "Mario")

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Game By Team 4")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 40, 40)
BLUE = (92, 148, 252)
GREEN = (34, 139, 34)

font_title = pygame.font.SysFont("arial", 72)
font_big = pygame.font.SysFont("arial", 48)
font_mid = pygame.font.SysFont("arial", 32)
font_small = pygame.font.SysFont("arial", 24)

class GameState:
    MENU = "MENU"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"
    LEVEL_COMPLETE = "LEVEL_COMPLETE"

current_state = GameState.MENU
score = 0
lives = 3
level = 1
game_over = False
paused = False

WIN_SCORE = 760

TILE_SIZE = 30
MAP_WIDTH = 1400
MAP_HEIGHT = 600

level_map = [
    ".....G...............G......................G..",
    "X.........G...................G................",
    "W.X....................................A.H.A...",
    "..W..X.....G.....I...J.A..............TTTTTT...",
    ".....W..X........W.W.W.W.W.....................",
    "........W....A................X.V..............",
    "H...........TTT.....J..J......BBB..........G...",
    "......G.............W..W...........JJJJ........",
    ".................V...........X.....WWWW........",
    "P.X.X.X..........W..........WWW................",
    "WWWWW...X.X.X........G.............H...........",
    ".......WWWW...X.X........V........TTT..........",
    "X............WWWW.......WW..............J.J....",
    "W.................X.............I.......W.W....",
    "....J......X.....WWW.C..........O..............",
    ".C..W.....WW....................O..............",
    "J......I........................O............H.",
    "W..V...TT...QXQXQXQXQPV.V.V.V...O...V.V.V.V.TTT",
    "WPWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWPWWWWWWWWWWWWWWWWWWWWWWWWW",
]

camera_x = 0
camera_y = 0

goombas = []


SOLID_TILES = ['W', 'P', 'T', 'B', 'H', 'O'] 

ENEMY_TILES = ['C', 'A']

COLLECTIBLE_TILES = ['X', 'J']  

def load_sprite(filename, width=TILE_SIZE, height=TILE_SIZE):
    try:
        image = pygame.image.load(filename).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    except Exception as e:
        print(f"⚠️  Không tìm thấy: {filename}")
        return pygame.Surface((width, height), pygame.SRCALPHA)

print("\n" + "=" * 50)
print("ĐANG TẢI TÀI NGUYÊN...")
print("=" * 50)

sprites = {
    'dat': load_sprite('dat.png'),
    'cot_xanh': load_sprite('cot_xanh.png', TILE_SIZE, TILE_SIZE * 3),
    'may': load_sprite('may.png'),
    'co': load_sprite('co.png'),
    'hoa': load_sprite('hoa.png'),
    'nam': load_sprite('nam.png'),
    'quai_vat': load_sprite('quai_vat.png'),
    'xu': load_sprite('xu.png'),
    'goombas': load_sprite('goombas_1.png'),
    'banh_mi': load_sprite('banh_mi.png'),
    'cay_an_thit': load_sprite('cay_an_thit.png'),
    'hop_qua': load_sprite('hop_qua.png'),
    'cay_an_thit2': load_sprite('cay_an_thit2.png'),
    'ong_sat': load_sprite('ong_sat.png'),
    'thung_go': load_sprite('thung_go.png'),
    'thanh_sang': load_sprite('thanh_sang.png'),
}

try:
    mario_image = pygame.image.load(os.path.join(MARIO_IMAGES_DIR, "mario.png")).convert_alpha()
    mario_image = pygame.transform.scale(mario_image, (40, 60))
    print("✓ Đã tải: mario.png")
except Exception as e:
    print(f"⚠️  Không tìm thấy mario.png: {e}")
    mario_image = pygame.Surface((40, 60))
    mario_image.fill((200, 0, 0))

# Load Mario animation frames
try:
    mario_st_frame = pygame.image.load(os.path.join(MARIO_IMAGES_DIR, "mario_st.png")).convert_alpha()
    mario_st_frame = pygame.transform.scale(mario_st_frame, (40, 60))
    mario_walk_frames = []
    for fname in ["mario_move0.png", "mario_move1.png", "mario_move2.png"]:
        img = pygame.image.load(os.path.join(MARIO_IMAGES_DIR, fname)).convert_alpha()
        mario_walk_frames.append(pygame.transform.scale(img, (40, 60)))
    mario_jump_frame = pygame.image.load(os.path.join(MARIO_IMAGES_DIR, "mario_jump.png")).convert_alpha()
    mario_jump_frame = pygame.transform.scale(mario_jump_frame, (40, 60))
    print("✓ Đã tải bộ ảnh animation của Mario")
except Exception as e:
    print(f"⚠️  Không đủ ảnh animation Mario: {e}")
    mario_st_frame = mario_image
    mario_walk_frames = [mario_image]
    mario_jump_frame = mario_image

try:
    BG_PATH = os.path.join(BASE_DIR, "background.png")
    background_image = pygame.image.load(BG_PATH).convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    print("✓ Đã tải: background.png")
except Exception as e:
    print(f"⚠️  Không tìm thấy background.png: {e}")
    background_image = None

def load_sound(filename):
    try:
        filepath = os.path.join(SOUNDS_DIR, filename)
        if not os.path.exists(filepath):
            print(f"⚠️  Không tìm thấy âm thanh: {filepath}")
            return None
        sound = pygame.mixer.Sound(filepath)
        print(f"✓ Đã tải ��m thanh: {filename}")
        return sound
    except Exception as e:
        print(f"❌ Lỗi tải âm thanh {filename}: {e}")
        return None

def load_music(filename):
    try:
        filepath = os.path.join(SOUNDS_DIR, filename)
        if not os.path.exists(filepath):
            print(f"⚠️  Không tìm thấy nhạc: {filepath}")
            return False
        pygame.mixer.music.load(filepath)
        print(f"✓ Đã tải nhạc: {filename}")
        return True
    except Exception as e:
        print(f"❌ Lỗi tải nhạc {filename}: {e}")
        return False

sound_jump = load_sound("jump.wav")
sound_coin = load_sound("coin.wav")
sound_death = load_sound("death.wav")
sound_levelend = load_sound("levelend.wav")
sound_gameover = load_sound("gameover.wav")

if load_music("overworld.wav"):
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    print("✓ Nhạc nền đang phát!")

print("=" * 50 + "\n")

class Goomba:
    def __init__(self, x, y, move_right=True):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.vel_x = 1 if move_right else -1
        self.image = sprites['goombas']
        self.is_dead = False
        self.dead_timer = 0

    def update(self, level_map):
        if self.is_dead:
            self.dead_timer -= 1
            return "dead" if self.dead_timer <= 0 else "dying"

        # Di chuyển
        self.rect.x += self.vel_x

        # --- XỬ LÝ QUAY ĐẦU ---
        # 1. Kiểm tra va chạm tường (Wall)
        # Tính toán ô lưới (grid) tại vị trí đầu của Goomba
        if self.vel_x > 0:
            col_check = int((self.rect.right + 2) // TILE_SIZE) # Nhìn về phía trước bên phải
        else:
            col_check = int((self.rect.left - 2) // TILE_SIZE) # Nhìn về phía trước bên trái
        
        row_center = int(self.rect.centery // TILE_SIZE)
        row_bottom = int((self.rect.bottom + 2) // TILE_SIZE) # Nhìn xuống dưới chân

        # Nếu đi ra ngoài map -> quay đầu
        if col_check < 0 or col_check >= len(level_map[0]):
            self.vel_x *= -1
            return "alive"

        # Nếu gặp tường -> quay đầu
        if level_map[row_center][col_check] in SOLID_TILES:
            self.vel_x *= -1
        
        # 2. Kiểm tra hết đất (Cliff) -> quay đầu
        # Nếu ô bên dưới chân (phía trước) không phải là vật rắn -> quay đầu
        elif row_bottom < len(level_map) and level_map[row_bottom][col_check] not in SOLID_TILES:
            self.vel_x *= -1

        return "alive"

    def draw(self, surface, camera_x, camera_y):
        surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.width = 40
        self.height = 60
        self.on_ground = False
        self.facing_right = True
        self.move_speed = 2.0
        self.jump_power = JUMP_POWER
        self.gravity = GRAVITY
        self.collected_coins = 0
        self.is_flying = False
        self.flight_timer = 0
        # Animation state
        self.anim_index = 0
        self.anim_timer = 0
        self.anim_delay = 8
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.vel_x = -self.move_speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.vel_x = self.move_speed
            self.facing_right = True
        else:
            self.vel_x = 0
        
        if self.is_flying:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.vel_y = -self.move_speed
            elif keys[pygame.K_DOWN]:
                self.vel_y = self.move_speed
        elif keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
            if sound_jump:
                sound_jump.play()
    
    def check_collision_with_tile(self, tile_x, tile_y):
        """Kiểm tra va chạm với một tile"""
        return (self.x + self.width > tile_x and 
                self.x < tile_x + TILE_SIZE and
                self.y + self.height > tile_y and 
                self.y < tile_y + TILE_SIZE)
    
    def update(self):
        global score, lives, current_state, game_over
        
        if not self.is_flying:
            self.vel_y += self.gravity
        else:
            self.vel_y *= 0.95
            self.flight_timer -= 1
            if self.flight_timer <= 0:
                self.is_flying = False
        
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED
        
        self.x += self.vel_x
        self.y += self.vel_y
        
        self.on_ground = False

        for row_i, row in enumerate(level_map):
            for col_i, tile in enumerate(row):
                tile_x = col_i * TILE_SIZE
                tile_y = row_i * TILE_SIZE


                if tile == 'P':
                    solid_tx = tile_x
                    solid_ty = tile_y - 2 * TILE_SIZE
                    solid_tw = TILE_SIZE
                    solid_th = 3 * TILE_SIZE
                else:
                    solid_tx = tile_x
                    solid_ty = tile_y
                    solid_tw = TILE_SIZE
                    solid_th = TILE_SIZE
                if tile in SOLID_TILES:

                    if (self.x + self.width > solid_tx and 
                        self.x < solid_tx + solid_tw and
                        self.y + self.height > solid_ty and 
                        self.y + self.height < solid_ty + solid_th and
                        self.vel_y >= 0):
                        self.y = solid_ty - self.height
                        self.vel_y = 0
                        self.on_ground = True
                        if tile == 'H':
                            self.is_flying = True
                            self.flight_timer = FPS * 3
                            level_map[row_i] = level_map[row_i][:col_i] + '.' + level_map[row_i][col_i+1:]
                            if sound_coin:
                                sound_coin.play()

                    elif (self.x + self.width > solid_tx and 
                          self.x < solid_tx + solid_tw and
                          self.y < solid_ty + solid_th and 
                          self.y + self.height > solid_ty and
                          self.vel_y < 0):
                        self.y = solid_ty + solid_th
                        self.vel_y = 0
                        if tile == 'H':
                            self.is_flying = True
                            self.flight_timer = FPS * 3
                            level_map[row_i] = level_map[row_i][:col_i] + '.' + level_map[row_i][col_i+1:]
                            if sound_coin:
                                sound_coin.play()

                    elif (self.x + self.width > solid_tx and 
                          self.x + self.width < solid_tx + solid_tw and
                          self.y + self.height > solid_ty and 
                          self.y < solid_ty + solid_th and
                          self.vel_x > 0):
                        self.x = solid_tx - self.width
                        if tile == 'H':
                            self.is_flying = True
                            self.flight_timer = FPS * 3
                            level_map[row_i] = level_map[row_i][:col_i] + '.' + level_map[row_i][col_i+1:]
                            if sound_coin:
                                sound_coin.play()

                    elif (self.x > solid_tx and 
                          self.x < solid_tx + solid_tw and
                          self.y + self.height > solid_ty and 
                          self.y < solid_ty + solid_th and
                          self.vel_x < 0):
                        self.x = solid_tx + solid_tw
                        if tile == 'H':
                            self.is_flying = True
                            self.flight_timer = FPS * 3
                            level_map[row_i] = level_map[row_i][:col_i] + '.' + level_map[row_i][col_i+1:]
                            if sound_coin:
                                sound_coin.play()
                
                elif tile in ['C', 'A']:
                    if self.check_collision_with_tile(tile_x, tile_y):
                        print(f"💥 Va chạm với quái vật tại ({col_i}, {row_i})!")
                        if sound_death:
                            sound_death.play()
                        return False
                

                if tile in COLLECTIBLE_TILES:
                    if self.check_collision_with_tile(tile_x, tile_y):
                        if tile == 'X':
                            score += 10
                            self.collected_coins += 1
                            print(f"🪙 Nhặt được xu! Tổng: {self.collected_coins}")
                        elif tile == 'J': 
                            score += 50
                            print(f"🌸 Nhặt được hoa!")

                        if sound_coin:
                            sound_coin.play()

                        level_map[row_i] = level_map[row_i][:col_i] + '.' + level_map[row_i][col_i+1:]
        
        # Entity-based Goomba collisions
        mario_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for g in goombas:
            if mario_rect.colliderect(g.rect):
                if self.vel_y > 0 and (self.y + self.height - self.vel_y) <= g.rect.top + 10:
                    g.is_dead = True
                    g.dead_timer = 10
                    self.vel_y = -self.jump_power * 0.5
                    if sound_coin:
                        sound_coin.play()
                else:
                    print("💥 Va chạm với Goomba!")
                    if sound_death:
                        sound_death.play()
                    return False

        if self.x < 0:
            self.x = 0
        if self.x + self.width > MAP_WIDTH:
            self.x = MAP_WIDTH - self.width

        if self.y > MAP_HEIGHT + TILE_SIZE:
            return False
        
        return True
    
    def draw(self, surface, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Choose sprite based on state
        on_air = (not self.on_ground) or self.is_flying or abs(self.vel_y) > 0.1
        if on_air:
            current_img = mario_jump_frame
            # reset walk cycle while in air
            self.anim_index = 0
            self.anim_timer = 0
        elif abs(self.vel_x) > 0.01:
            # walking animation
            self.anim_timer += 1
            if self.anim_timer >= self.anim_delay:
                self.anim_timer = 0
                self.anim_index = (self.anim_index + 1) % len(mario_walk_frames)
            current_img = mario_walk_frames[self.anim_index]
        else:
            current_img = mario_st_frame
            self.anim_index = 0
            self.anim_timer = 0

        if self.facing_right:
            surface.blit(current_img, (screen_x, screen_y))
        else:
            flipped = pygame.transform.flip(current_img, True, False)
            surface.blit(flipped, (screen_x, screen_y))
        # Optional: draw a small indicator while flying
        if self.is_flying:
            pygame.draw.circle(surface, (255, 255, 0), (int(screen_x + self.width/2), int(screen_y - 6)), 4)

def draw_parallax_background():
    cloud_offset = (camera_x * 0.3) % (SCREEN_WIDTH * 2)
    pygame.draw.circle(screen, WHITE, (int(100 - cloud_offset), 50), 30)
    pygame.draw.circle(screen, WHITE, (int(150 - cloud_offset), 50), 25)
    pygame.draw.circle(screen, WHITE, (int(200 - cloud_offset), 50), 30)
    
    pygame.draw.circle(screen, WHITE, (int(400 - cloud_offset), 80), 25)
    pygame.draw.circle(screen, WHITE, (int(450 - cloud_offset), 80), 30)
    pygame.draw.circle(screen, WHITE, (int(500 - cloud_offset), 80), 25)

def draw_map():
    for row_i, row in enumerate(level_map):
        for col_i, tile in enumerate(row):
            x = col_i * TILE_SIZE - camera_x
            y = row_i * TILE_SIZE - camera_y
            
            if -TILE_SIZE < x < SCREEN_WIDTH and -TILE_SIZE < y < SCREEN_HEIGHT:
                if tile == 'W':
                    screen.blit(sprites['dat'], (x, y))
                elif tile == 'P':
                    screen.blit(sprites['cot_xanh'], (x, y - TILE_SIZE * 2))
                elif tile == 'G':
                    screen.blit(sprites['may'], (x, y))
                elif tile == 'Q':
                    screen.blit(sprites['co'], (x, y))
                elif tile == 'M':
                    screen.blit(sprites['nam'], (x, y))
                elif tile == 'B':
                    screen.blit(sprites['banh_mi'], (x, y))
                elif tile == 'C':
                    screen.blit(sprites['cay_an_thit'], (x, y))
                elif tile == 'H':
                    screen.blit(sprites['hop_qua'], (x, y))
                elif tile == 'O':
                    screen.blit(sprites['ong_sat'], (x, y))
                elif tile == 'T':
                    screen.blit(sprites['thung_go'], (x, y))
                elif tile == 'S':
                    screen.blit(sprites['thanh_sang'], (x, y))
                elif tile == 'J':
                    screen.blit(sprites['hoa'], (x, y))
                elif tile == 'X':
                    screen.blit(sprites['xu'], (x, y))
                elif tile == 'A':
                    screen.blit(sprites['quai_vat'], (x, y))
                elif tile == 'I':
                    screen.blit(sprites['nam'], (x, y))

def draw_menu():
    screen.fill(BLUE)
    
    title = font_title.render("MARIO GAME", True, RED)
    screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 80)))
    
    start_text = font_big.render("Press ENTER to Start", True, WHITE)
    screen.blit(start_text, start_text.get_rect(center=(SCREEN_WIDTH // 2, 200)))
    
    controls_text = font_mid.render("LEFT/RIGHT: Move | SPACE: Jump", True, WHITE)
    screen.blit(controls_text, controls_text.get_rect(center=(SCREEN_WIDTH // 2, 280)))
    
    quit_text = font_big.render("Press ESC to Quit", True, WHITE)
    screen.blit(quit_text, quit_text.get_rect(center=(SCREEN_WIDTH // 2, 360)))
    
    version_text = font_small.render("v3.0 - Full Physics & Enemies", True, WHITE)
    screen.blit(version_text, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 30))

def draw_hud():
    hud_surface = pygame.Surface((SCREEN_WIDTH, 40))
    hud_surface.fill(BLACK)
    
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    lives_text = font_small.render(f"Lives: {lives}", True, WHITE)
    level_text = font_small.render(f"Level: {level}", True, WHITE)
    pause_text = font_small.render("P: Pause", True, WHITE)
    
    hud_surface.blit(score_text, (20, 8))
    hud_surface.blit(lives_text, (250, 8))
    hud_surface.blit(level_text, (450, 8))
    hud_surface.blit(pause_text, (SCREEN_WIDTH - 150, 8))
    
    screen.blit(hud_surface, (0, 0))

def draw_game(mario):
    if 'background_image' in globals() and background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(BLUE)
        draw_parallax_background()
    draw_map()
    for g in goombas:
        g.draw(screen, camera_x, camera_y)
    mario.draw(screen, camera_x, camera_y)
    draw_hud()

def draw_pause(mario):
    draw_game(mario)
    
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    pause_text = font_title.render("PAUSED", True, RED)
    screen.blit(pause_text, pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))
    
    resume_text = font_mid.render("Press P to Resume", True, WHITE)
    screen.blit(resume_text, resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))
    
    menu_text = font_mid.render("Press M for Menu", True, WHITE)
    screen.blit(menu_text, menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)))

def draw_game_over():
    screen.fill(BLACK)
    
    over_text = font_title.render("GAME OVER", True, RED)
    screen.blit(over_text, over_text.get_rect(center=(SCREEN_WIDTH // 2, 80)))
    
    score_text = font_mid.render(f"Final Score: {score}", True, WHITE)
    screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, 180)))
    
    level_text = font_mid.render(f"Level Reached: {level}", True, WHITE)
    screen.blit(level_text, level_text.get_rect(center=(SCREEN_WIDTH // 2, 240)))
    
    restart_text = font_mid.render("Press R to Restart", True, WHITE)
    screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH // 2, 320)))
    
    menu_text = font_mid.render("Press M for Menu", True, WHITE)
    screen.blit(menu_text, screen.blit(menu_text, menu_text.get_rect(center=(SCREEN_WIDTH // 2, 380))))

def draw_level_complete():
    screen.fill(BLUE)
    
    complete_text = font_title.render("LEVEL COMPLETE!", True, GREEN)
    screen.blit(complete_text, complete_text.get_rect(center=(SCREEN_WIDTH // 2, 80)))
    
    score_text = font_mid.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, 180)))
    
    next_text = font_mid.render("Press SPACE for Next Level", True, WHITE)
    screen.blit(next_text, next_text.get_rect(center=(SCREEN_WIDTH // 2, 280)))
    
    menu_text = font_mid.render("Press M for Menu", True, WHITE)
    screen.blit(menu_text, menu_text.get_rect(center=(SCREEN_WIDTH // 2, 340)))

def handle_events():
    global current_state, score, lives, level, game_over, paused
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if current_state == GameState.MENU:
                if event.key == pygame.K_RETURN:
                    current_state = GameState.PLAYING
                    score = 0
                    lives = 3
                    level = 1
                    game_over = False
                    paused = False
                    print("✓ Game Started!")
                
                elif event.key == pygame.K_ESCAPE:
                    return False
            
            elif current_state == GameState.PLAYING:
                if event.key == pygame.K_p:
                    current_state = GameState.PAUSED
                    paused = True
                    print("⏸ Game Paused!")
                
                elif event.key == pygame.K_ESCAPE:
                    current_state = GameState.MENU
                    print("← Returned to Menu!")
            
            elif current_state == GameState.PAUSED:
                if event.key == pygame.K_p:
                    current_state = GameState.PLAYING
                    paused = False
                    print("▶ Game Resumed!")
                
                elif event.key == pygame.K_m:
                    current_state = GameState.MENU
                    print("← Returned to Menu!")
            
            elif current_state == GameState.GAME_OVER:
                if event.key == pygame.K_r:
                    current_state = GameState.PLAYING
                    score = 0
                    lives = 3
                    level = 1
                    game_over = False
                    paused = False
                    print("✓ Game Restarted!")
                
                elif event.key == pygame.K_m:
                    current_state = GameState.MENU
                    print("← Returned to Menu!")
                
                elif event.key == pygame.K_ESCAPE:
                    return False
            
            elif current_state == GameState.LEVEL_COMPLETE:
                if event.key == pygame.K_SPACE:
                    level += 1
                    score += 1000
                    current_state = GameState.PLAYING
                    print(f"✓ Level {level} Started!")
                
                elif event.key == pygame.K_m:
                    current_state = GameState.MENU
                    print("← Returned to Menu!")
    
    return True

def update_game(mario):
    global score, lives, current_state, game_over, camera_x, camera_y
    
    if current_state == GameState.PLAYING:
        mario.handle_input()
        
        if not mario.update():
            lives -= 1
            if lives <= 0:
                current_state = GameState.GAME_OVER
                game_over = True
                print("💀 Game Over!")
                if sound_gameover:
                    sound_gameover.play()
            else:
                mario.x = 100
                mario.y = 300
                mario.vel_x = 0
                mario.vel_y = 0
                print(f"⚠️  Mất 1 mạng! Còn lại: {lives}")
        
        # Update Goombas
        to_remove = []
        for g in goombas:
            if g.update(level_map) == "dead":
                to_remove.append(g)
        for g in to_remove:
            goombas.remove(g)

        camera_x = mario.x - SCREEN_WIDTH // 3
        camera_x = max(0, min(camera_x, MAP_WIDTH - SCREEN_WIDTH))
        if score >= WIN_SCORE:
            current_state = GameState.LEVEL_COMPLETE
            if sound_levelend:
                sound_levelend.play()
            print("🎉 Level Complete! Đã đạt đủ điểm để thắng.")

def draw_frame(mario):
    if current_state == GameState.MENU:
        draw_menu()
    elif current_state == GameState.PLAYING:
        draw_game(mario)
    elif current_state == GameState.PAUSED:
        draw_pause(mario)
    elif current_state == GameState.GAME_OVER:
        draw_game_over()
    elif current_state == GameState.LEVEL_COMPLETE:
        draw_level_complete()
    
    pygame.display.update()

def main():
    running = True
    mario = Mario(100, 300)

    # Instantiate Goombas from map and clear their tiles
    for row_i, row in enumerate(level_map):
        row_list = list(row)
        for col_i, tile in enumerate(row):
            if tile == 'V':
                x = col_i * TILE_SIZE
                y = row_i * TILE_SIZE
                goombas.append(Goomba(x, y, (col_i % 2 == 0)))
                row_list[col_i] = '.'
        level_map[row_i] = ''.join(row_list)
    
    print("=" * 50)
    print("🎮 MARIO GAME - MAIN LOOP STARTED")
    print("=" * 50)
    print(f"Window Size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"FPS: {FPS}")
    print(f"Map Size: {MAP_WIDTH}x{MAP_HEIGHT}")
    print("Controls: LEFT/RIGHT - Move, SPACE - Jump, P - Pause")
    print("=" * 50)
    print("Vật lý:")
    print("- Đất (W), Cột (P), Thùng (T), Bánh mì (B), Hộp quà (H), Ống sắt (O)")
    print("- Quái vật (V, C, A) - Mất 1 mạng khi va chạm")
    print("- Xu (X) - +10 điểm, Hoa (J) - +50 điểm")
    print("=" * 50)
    
    while running:
        clock.tick(FPS)
        running = handle_events()
        update_game(mario)
        draw_frame(mario)
    
    print("=" * 50)
    print("🛑 GAME ENDED")
    print(f"Final Score: {score}")
    print(f"Final Level: {level}")
    print("=" * 50)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
