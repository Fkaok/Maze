from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()

        if key_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed

        if key_pressed[K_s] and self.rect.y < 450:
            self.rect.y += self.speed

        if key_pressed[K_d] and self.rect.y < 650:
            self.rect.x += self.speed

        if key_pressed[K_a] and self.rect.y > 0:
            self.rect.x -= self.speed

class Enemy(GameSprite):


    direction = 'left'

    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'

        if self.rect.x >= 645:
            self.direction = 'left'

        if self.direction == 'right':
            self.rect.x += self.speed

        else:
            self.rect.x -= self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y,  wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((self.color_1, self.color_2, self.color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('Лабиринт')

background = transform.scale(image.load('background.jpg'), (700, 500))

player = Player('hero.png', 30, 50, 4)
monster = Enemy('cyborg.png', 200, 200, 2)
final = GameSprite('treasure.png', 400, 400, 0)

w1 = Wall(0, 255, 0, 100, 20, 450, 10)
w2 = Wall(0, 255, 0, 100, 480, 370, 10)
w3 = Wall(0, 255, 0, 100, 20, 10, 390)

clock = time.Clock()
FPS = 70
game = True
finish = False

font.init()
font = font.SysFont('Arial', 70)
win = font.render('YOU WIN', True, (255, 20, 15))
lose = font.render('YOU LOSE', True, (255, 70, 28))

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

kick = mixer.Sound('kick.ogg')
money = mixer.Sound('money.ogg')

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        window.blit(background,(0,0))
        player.update()
        monster.update()
        final.update()

        player.reset()
        monster.reset()
        final.reset()
        final.reset()

        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        
        if sprite.collide_rect(player, final):
                finish = True
                window.blit(win, (200, 200))
                money.play()

        if (sprite.collide_rect(player, monster) or sprite.collide_rect(player, w1) 
        or sprite.collide_rect(player, w2) or  sprite.collide_rect(player, w3)):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

    clock.tick(FPS)
    display.update()