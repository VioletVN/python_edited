import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Game")
clock = pygame.time.Clock()
# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (220, 40, 40)
blue = (92, 148, 252)
# font
font_title = pygame.font.SysFont("arial", 72)
font_big = pygame.font.SysFont("arial", 48)
font_mid = pygame.font.SysFont("arial", 32)
font_small = pygame.font.SysFont("arial", 24)
# bien
score = 0
lives = 3
game_state = "MENU"
game_over = False

def draw_menu():
    screen.fill(blue)
    title = font_title.render("MARIO GAME", True, red)
    start_text = font_big.render("Enter to Start", True, white)
    
    quit_text = font_big.render("Esc to Quit", True, white)
    
    screen.blit(title, title.get_rect(center=(WIDTH//2, 200)))
    screen.blit(start_text, start_text.get_rect(center=(WIDTH//2, 360)))
    screen.blit(quit_text, quit_text.get_rect(center=(WIDTH//2, 430)))


def draw_hud():
    score_text = font_small.render(f"Score: {score}", True, white)
    lives_text = font_small.render(f"Lives: {lives}", True, white)

    screen.blit(score_text, (30, 20))
    screen.blit(lives_text, (200, 20))

def draw_game_over():
    screen.fill(black)
    over_text = font_big.render("GAME OVER", True, red)
    score_text = font_mid.render(f"Your Score: {score}", True, white)
    restart_text = font_mid.render("R to Restart", True, white)
    quit_text = font_mid.render("Esc to Quit", True, white)

    screen.blit(over_text, over_text.get_rect(center=(WIDTH//2, 200)))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH//2, 300)))
    screen.blit(restart_text, restart_text.get_rect(center=(WIDTH//2, 400)))
    screen.blit(quit_text, quit_text.get_rect(center=(WIDTH//2, 450)))
    
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:

            if game_state == "MENU":
                if event.key == pygame.K_RETURN:
                    game_state = "PLAYING"
                    score = 0
                    lives = 3
                    game_over = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif game_state == "GAME_OVER":
                    if event.key == pygame.K_r:
                        score = 0
                        lives = 3
                        game_over = False
                        game_state = "MENU"
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    if game_state == "MENU":
        draw_menu()
    elif game_state == "PLAYING":
        screen.fill((92, 148, 252))
    
        if not game_over:
            score += 1
            # Ví dụ thay ham mario die
            if score % 100 == 0:
                lives -= 1

            if lives <= 0:
                game_state = "GAME_OVER"
                game_over = True

        draw_hud()

    elif game_state == "GAME_OVER":
        draw_game_over()

    pygame.display.update()
   

        


                    


                    



                                 

