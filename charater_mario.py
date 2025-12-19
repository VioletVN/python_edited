import pygame
pygame.init()
kich_thuoc = (1000, 600)
man_hinh = pygame.display.set_mode(kich_thuoc)
pygame.display.set_caption("may thang chim be")
font = pygame.font.SysFont("texge", 100)
# di chuyển  MARIO
class mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.van_toc = 0
        self.gravity = 0.9
        self.on_ground = False
        self.width = 40
        self.height = 60
    def jump(self):      
        self.van_toc = -15
        self.on_ground = False
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP] and self.on_ground:
            self.jump()
        #trong luc
        self.y += self.van_toc
        self.van_toc += self.gravity
        if self.y + self.height >= ground_y:
            self.y = ground_y - self.height
            self.van_toc = 0
            self.on_ground = True
# MẶT ĐẤT
ground_y = 500  # chiều cao mặt đất
ground_height = 10 # độ dày mặt đất

running =True
while running:
    for tat in pygame.event.get():
        if tat.type == pygame.QUIT :
            running = False
    
    
    
    pygame.display.flip()
pygame.quit()#cho nó chay cai man hinh pygame di