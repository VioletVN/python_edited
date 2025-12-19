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
pygame.display.set_caption("Mario Game")
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

# Danh sách các tile có vật lý (va chạm)
SOLID_TILES = ['W', 'P', 'T', 'B', 'H', 'O']  # Đất, cột, thùng, bánh mì, hộp quà, ống sắt
# Danh sách các tile quái vật
ENEMY_TILES = ['V', 'C', 'A']  # Goombas, cây ăn thịt, quái vật
# Danh sách các tile có thể nhặt
COLLECTIBLE_TILES = ['X', 'J']  # Xu, hoa

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

def load_sound(filename):
    try:
        filepath = os.path.join(SOUNDS_DIR, filename)
        if not os.path.exists(filepath):
            print(f"⚠️  Không tìm thấy âm thanh: {filepath}")
            return None
        sound = pygame.mixer.Sound(filepath)
        print(f"✓ Đã tải âm thanh: {filename}")
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
        
        if keys[pygame.K_SPACE] and self.on_ground:
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
        
        self.vel_y += self.gravity
        
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED
        
        self.x += self.vel_x
        self.y += self.vel_y
        
        self.on_ground = False
        
        # Kiểm tra va chạm với các tile
        for row_i, row in enumerate(level_map):
            for col_i, tile in enumerate(row):
                tile_x = col_i * TILE_SIZE
                tile_y = row_i * TILE_SIZE
                
                # Kiểm tra va chạm với các tile cứng (đất, cột, thùng, v.v.)
                if tile in SOLID_TILES:
                    # Va chạm từ trên
                    if (self.x + self.width > tile_x and 
                        self.x < tile_x + TILE_SIZE and
                        self.y + self.height > tile_y and 
                        self.y + self.height < tile_y + TILE_SIZE and
                        self.vel_y >= 0):
                        self.y = tile_y - self.height
                        self.vel_y = 0
                        self.on_ground = True
                    
                    # Va chạm từ dưới
                    elif (self.x + self.width > tile_x and 
                          self.x < tile_x + TILE_SIZE and
                          self.y < tile_y + TILE_SIZE and 
                          self.y + self.height > tile_y and
                          self.vel_y < 0):
                        self.y = tile_y + TILE_SIZE
                        self.vel_y = 0
                    
                    # Va chạm từ trái
                    elif (self.x + self.width > tile_x and 
                          self.x + self.width < tile_x + TILE_SIZE and
                          self.y + self.height > tile_y and 
                          self.y < tile_y + TILE_SIZE and
                          self.vel_x > 0):
                        self.x = tile_x - self.width
                    
                    # Va chạm từ phải
                    elif (self.x > tile_x and 
                          self.x < tile_x + TILE_SIZE and
                          self.y + self.height > tile_y and 
                          self.y < tile_y + TILE_SIZE and
                          self.vel_x < 0):
                        self.x = tile_x + TILE_SIZE
                
                # Kiểm tra va chạm với quái vật (mất 1 mạng)
                if tile in ENEMY_TILES:
                    if self.check_collision_with_tile(tile_x, tile_y):
                        print(f"💥 Va chạm với quái vật tại ({col_i}, {row_i})!")
                        if sound_death:
                            sound_death.play()
                        return False  # Trả về False để mất mạng
                
                # Kiểm tra nhặt xu hoặc hoa
                if tile in COLLECTIBLE_TILES:
                    if self.check_collision_with_tile(tile_x, tile_y):
                        if tile == 'X':  # Xu
                            score += 10
                            self.collected_coins += 1
                            print(f"🪙 Nhặt được xu! Tổng: {self.collected_coins}")
                        elif tile == 'J':  # Hoa
                            score += 50
                            print(f"🌸 Nhặt được hoa!")
                        
                        if sound_coin:
                            sound_coin.play()
                        
                        # Xóa tile khỏi map
                        level_map[row_i] = level_map[row_i][:col_i] + '.' + level_map[row_i][col_i+1:]
        
        if self.x < 0:
            self.x = 0
        if self.x + self.width > MAP_WIDTH:
            self.x = MAP_WIDTH - self.width
        
        # Chỉ game over nếu rơi xuống dưới map (không phải ô trống)
        if self.y > MAP_HEIGHT + TILE_SIZE:
            return False
        
        return True
    
    def draw(self, surface, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        if mario_image:
            if self.facing_right:
                surface.blit(mario_image, (screen_x, screen_y))
            else:
                flipped_mario = pygame.transform.flip(mario_image, True, False)
                surface.blit(flipped_mario, (screen_x, screen_y))

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
                elif tile == 'V':
                    screen.blit(sprites['goombas'], (x, y))
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
    screen.fill(BLUE)
    
    draw_parallax_background()
    draw_map()
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
    screen.blit(menu_text, menu_text.get_rect(center=(SCREEN_WIDTH // 2, 380)))

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
        
        camera_x = mario.x - SCREEN_WIDTH // 3
        camera_x = max(0, min(camera_x, MAP_WIDTH - SCREEN_WIDTH))
        
        if score % 5000 == 0 and score > 0:
            current_state = GameState.LEVEL_COMPLETE
            print("🎉 Level Complete!")

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
