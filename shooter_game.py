from pygame import *
from random import randint

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound('da3.ogg')


font.init()
font1 = font.Font(None, 50) 
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)




class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.y = -5
            self.rect.x = randint(0, 630)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
            



asteroid = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()

for i in range(10):
    enemy = Enemy("ufo.png", randint(0, 630), -5, 65, 65, randint(3,5)) 
    monsters.add(enemy)


player = Player("rocket.png", 350, 400, 65, 65, 10)


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("dark waidar")

background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

clock = time.Clock()

score = 0

finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if finish != True:
        window.blit(background, (0,0))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()

        bullets.draw(window)
        bullets.update()

        sprites_list1 = sprite.groupcollide(bullets, asteroid,True, True) 
        sprites_list = sprite.groupcollide(bullets, monsters,True, True) 
        for m in sprites_list:
            enemy = Enemy("ufo.png", randint(0, 630), -5, 65, 65, randint(1,2))
            monsters.add(enemy)

            score += 1
         


        if score >= 10:
            finish = True
            win = font1.render("Ты выиграл!", 1, (0, 255, 0))
            window.blit(win, (300, 250))
        
        if lost >= 3:
            finish = True
            game_over = font1.render("Ты проиграл!", 1, (255, 0, 0))
            window.blit( game_over, (300, 250))

        score_text = font1.render("Очки:" + str(score), 1, (255,255,255))
        window.blit(score_text, (10,10))

        text_lost = font1.render("Пропущено: " + str(lost), 1, (255,255,255))
        window.blit(text_lost, (10, 40))

    clock.tick(60)
    display.update()