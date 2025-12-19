import pygame
import os
pygame.init()
#cấu trúc màn hình
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("map1_sieu_cap_pro_max")
clock = pygame.time.Clock()
#số phông ảnh
TILE_SIZE = 30
def load_sprite(filename, width=TILE_SIZE, height=TILE_SIZE):
    try:
        image = pygame.image.load(filename).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    except:
        print("Không tìm thấy:", filename)
        return pygame.Surface((width, height), pygame.SRCALPHA)
# in ảnh.png ra 
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
#ma trận map1: hoa mắt vai
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
#hàm vẽ map
def draw_map():
    for row_i, row in enumerate(level_map):
        for col_i, tile in enumerate(row):
            x = col_i * TILE_SIZE
            y = row_i * TILE_SIZE


            if tile == 'W':          # đất
                screen.blit(sprites['dat'], (x, y))


            elif tile == 'P':        # cột xanh
                screen.blit(sprites['cot_xanh'], (x, y - TILE_SIZE * 2))


            elif tile == 'G':        # mây 
                screen.blit(sprites['may'], (x, y))
                
                
            elif tile == 'Q':        # cỏ 
                screen.blit(sprites['co'], (x, y))


            elif tile == 'M':        # nấm
                screen.blit(sprites['nam'], (x, y))


            elif tile == 'B':        # bánh mì
                screen.blit(sprites['banh_mi'], (x, y))


            elif tile == 'C':        # cây ăn thịt
                screen.blit(sprites['cay_an_thit'], (x, y))


            elif tile == 'H':        # hộp quà
                screen.blit(sprites['hop_qua'], (x, y))


            elif tile == 'O':        # ống sắt
                screen.blit(sprites['ong_sat'], (x, y))


            elif tile == 'T':        # thùng gỗ
                screen.blit(sprites['thung_go'], (x, y))


            elif tile == 'S':        # thanh sáng
                screen.blit(sprites['thanh_sang'], (x, y)) 
                
                
            elif tile == 'J':        # hoa
                screen.blit(sprites['hoa'], (x, y))
                
                
            elif tile == 'V':        # goombas
                screen.blit(sprites['goombas'], (x, y))
                
            
            
            elif tile == 'X':        # xu
                screen.blit(sprites['xu'], (x, y))
                
                
            elif tile == 'A':        # quái vật
                screen.blit(sprites['quai_vat'], (x, y))
            
            elif tile == 'I':        # nấm
                screen.blit(sprites['nam'], (x, y))
#hàm vòng lặp
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # vẽ phông nền 
    screen.fill((92, 148, 252))#nền xanh
    draw_map()
    pygame.display.flip()
pygame.quit()
