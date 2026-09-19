
#Создай собственный Шутер!
from pygame import *
from random import randint,choice
import sys
import os
from time import time as get_time
init()
WIDTH = 700
HEIGHT = 500
FPS = 60

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class GameSprite(sprite.Sprite):
    def __init__(self, f, width, height, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(resource_path(f)), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def reset(self,):
        mw.blit(self.image, (self.rect.x, self.rect.y))
        #draw.rect(mw, (0, 0, 0), self.rect, 3)

class Player1(GameSprite):
    def __init__(self, f, width, height, x, y, speed,):
        super().__init__(f, width, height, x, y, speed)
    def move(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            
            
class Player2(GameSprite):
    def __init__(self, f, width, height, x, y, speed,):
        super().__init__(f, width, height, x, y, speed)
    def move(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
  
class Ball(GameSprite):
    def __init__(self, f, width, height, x, y, speed):
        super().__init__(f, width, height, x, y, speed)
        self.speed_x = speed
        self.speed_y = speed

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.bottom >= HEIGHT:
            self.speed_y = -1 * abs(self.speed_y)
        if self.rect.y <= 0:
            self.speed_y = abs(self.speed_y)
    def start(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = choice((1, -1)) * abs(self.speed_x)
        self.speed_y = choice((1, -1)) * abs(self.speed_y)


mw = display.set_mode((WIDTH, HEIGHT))
display.set_caption('PING-PONG')
clock = time.Clock()


bg = transform.scale(image.load(resource_path('table.jpg')), (WIDTH, HEIGHT))

font_score = font.Font(None,46)
font_main = font.Font(None,36)
font_small = font.Font(None,24)
text_color = (255, 255, 255)


player1 = Player1('racket1.png', 20, 80, 20, HEIGHT//2 - 40, 5)
player2 = Player2('racket2.png', 20, 80, WIDTH - 40, HEIGHT//2 - 40, 5)
ball = Ball('red_ball.png',40,40,WIDTH//2,HEIGHT//2,3)

score1 = 0
score2 = 0
game = True
finish = False
win = False

score_text1 = font_score.render(str(score1) , True, text_color)
score_text2 = font_score.render(str(score2) , True, text_color)
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ball.start()
            
            if e.key == K_r and finish:
                score1 = 0
                score2 = 0
                finish = False
                ball.start()


    if not finish:
        mw.blit(bg,(0,0))
            
        player1.move()
        player1.reset()
        player2.move()
        player2.reset()
        ball.update()
        ball.reset()
        if sprite.collide_rect(ball, player2):
            ball.speed_x = -1 * abs(ball.speed_x)
        if sprite.collide_rect(ball, player1):
            ball.speed_x = abs(ball.speed_x)

        if ball.rect.x < -50:
            score2 +=1
            score_text2 = font_score.render(str(score2) , True, text_color)
            ball.start()
        if ball.rect.x > WIDTH +50:
            score1 +=1
            score_text1 = font_score.render(str(score1) , True, text_color)
            ball.start()

        if score1 >= 5 or score2 >= 5:
            finish = True
            if score1 > score2:
                text = font_main.render("победа не лоха", True, (0, 255, 0))
            else:
                text = font_main.render("победа лоха", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 30))
            mw.blit(text, text_rect)
                    
            text_restart = font_small.render("Нажми R для рестарта", True, text_color)
            text_rect = text_restart.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))
            mw.blit(text_restart, text_rect)

            final_score = font_main.render(f'{score1} : {score2}', True,text_color)
            final_rect = final_score.get_rect(center=(WIDTH//2, HEIGHT//2 - 80))
            mw.blit(final_score,final_rect)
        


        
        
        #text_image_count = font_main.render(f'Счет:', True, text_color)
        mw.blit(score_text2,(WIDTH - 60, 40))
        mw.blit(score_text1,(30, 40))
            
   

            
    display.update()
    clock.tick(FPS)
quit()
