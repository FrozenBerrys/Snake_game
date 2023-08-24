import pygame, sys, math, random
from collections import deque

pygame.init()
screen = pygame.display.set_mode((400,450))
pygame.display.set_caption('python')
clock = pygame.time.Clock()

largefont = pygame.font.Font("pixel.ttf", 50)
font = pygame.font.Font("pixel.ttf", 35)
smallfont = pygame.font.Font("pixel.ttf", 20)
tinyfont = pygame.font.Font("pixel.ttf", 15)
#####################################################################################

welcome_surf = font.render("Welcome to Python", False, 'White')
welcome_rect = welcome_surf.get_rect(center = (200, 200))
menu_surf = pygame.Surface((400,400))
menu_rect = menu_surf.get_rect(topleft = (0, 0))
pygame.draw.line(menu_surf, "White", (0,400), (400,400), 5)

play = smallfont.render("PLAY", False, "Lime")
play_rect = play.get_rect(center = (200, 250))
quitgame = smallfont.render("QUIT", False, "Red")
quit_rect = quitgame.get_rect(center = (200, 280))
#####################################################################################

game_surf = pygame.Surface((400,400))
game_rect = game_surf.get_rect(topleft = (0,0))
pygame.Surface.fill(game_surf, "Black")
pygame.draw.line(game_surf, "White", (0,400), (400,400), 5)

#####################################################################################
highscoreint = 0
scoreint = 0
highscore = smallfont.render("Highscore: " + str(highscoreint), False, "White")
highscore_rect = highscore.get_rect(bottomright = (390,440))
score = smallfont.render(str(scoreint), False, "White")
score_rect = score.get_rect(bottomleft = (45,440))

pause_text = largefont.render("GAME PAUSED", False, 'White')
pause_text_rect = pause_text.get_rect(center = (200,200))
gameover_surface = pygame.Surface((500,500))
gameover_surface.set_alpha(60)
gameover_text = largefont.render("GAME OVER", False, 'Red')
gameover_text_rect = gameover_text.get_rect(center = (200,200))

def paused():
    global pausee 
    pausee = True
    while pausee:
        for event in pygame.event.get():
            screen.blit(pause_text, pause_text_rect)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pausee = False
        pygame.display.flip()
        clock.tick(10)  

def gameover():
    global lose, time
    lose = True
    time = 0
    while lose:
        screen.blit(gameover_surface, (0,0))
        screen.blit(gameover_text,gameover_text_rect)

        pygame.display.flip()
        clock.tick(5)  
        time += 1
        if time == 20:
            lose = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

#####################################################################################
body = pygame.transform.scale(pygame.image.load("lime.png"), (25, 25))
apple_score = pygame.transform.scale(pygame.image.load("apple.png"), (25,25))
scoreapple_rect = apple_score.get_rect(bottomleft = (10,436.5))
#####################################################################################

Menu = True
Game = False

while True:
    while Menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(pos):

                    snake = deque([
                        pygame.Rect(175,175,25,25)
                    ])
                    direction = (25,0)
                    apple_present = False
                    grow = False
                    goldeaten = 0
                    collision = False
                    scoreint = 0
                    Menu = False
                    Game = True
                    break
                if quit_rect.collidepoint(pos):
                    pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(pos):
                    play = smallfont.render("PLAY", False, "White")
                    screen.blit(play, play_rect)
                if quit_rect.collidepoint(pos):
                    quitgame = smallfont.render("QUIT", False, "White")
                    screen.blit(quitgame, quit_rect)
                if play_rect.collidepoint(pos) == False:
                    play = smallfont.render("PLAY", False, "Lime")
                    screen.blit(play, play_rect)
                if quit_rect.collidepoint(pos) == False:
                    quitgame = smallfont.render("QUIT", False, "Red")
                    screen.blit(quitgame, quit_rect)

        screen.blit(menu_surf, menu_rect)
        screen.blit(welcome_surf, welcome_rect)
        screen.blit(play, play_rect)
        screen.blit(quitgame, quit_rect)
        screen.blit(highscore, highscore_rect)
        pygame.display.flip()
    while Game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused()
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if direction != (0, 25):
                        direction = (0, -25)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if direction != (-25, 0):
                        direction = (25, 0)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    if direction != (0, -25):
                        direction = (0, 25)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if direction != (25, 0):
                        direction = (-25, 0)

        if apple_present == False:
            a_x = 25* math.floor(random.randrange(0,16))
            a_y = 25* math.floor(random.randrange(0,16))
            if random.randrange(0,10) < 1:
                gold = 1
                apple = pygame.transform.scale(pygame.image.load("goldenapple.png"), (25,25))
                apple = pygame.transform.scale(apple, (25, 25))

            else:
                gold = 0
                apple = pygame.transform.scale(pygame.image.load("apple.png"), (25,25))
                apple = pygame.transform.scale(apple, (25, 25))
            apple_rect = apple.get_rect(topleft = (a_x, a_y))
            apple_present = True
        
        if snake[0][0] == a_x and snake[0][1] == a_y:
            if gold == 1:
                goldeaten = 1
                scoreint += 2
            else:
                goldeaten = 0
                scoreint += 1
            apple_present = False
            grow = True

        new_head = pygame.Rect(snake[0].x + direction[0], snake[0].y + direction[1], 25, 25)
        snake.appendleft(new_head)
        if grow:
            grow = False
        else:
            snake.pop()

        if snake[0][0] == -25 or snake[0][0] == 400 or snake[0][1] == -25 or snake[0][1] == 400:
            collision = True
        for i in range(len(snake)):
            if i != 0:
                if snake[i].colliderect(snake[0]):
                    collision = True
        if collision:
            if scoreint > highscoreint:
                highscoreint = scoreint
            highscore = smallfont.render("Highscore: " + str(highscoreint), False, "White")
            highscore_rect = highscore.get_rect(bottomright = (390,440))
            
            gameover()
            Menu = True
            Game = False




        screen.blit(game_surf, game_rect)
        screen.blit(highscore, highscore_rect)
        score = smallfont.render(str(scoreint), False, "White")
        score_rect = score.get_rect(bottomleft = (45,440))
        screen.blit(score, score_rect)
        screen.blit(apple_score, scoreapple_rect)
        screen.blit(apple, apple_rect)
        for i in snake:
            screen.blit(body, i)

        if goldeaten:
            clock.tick(10)
        else:
            clock.tick(5)  
        pygame.display.flip()

        
    


        

