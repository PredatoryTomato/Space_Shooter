from pygame import *
from random import *

win_width = 1000
win_height = 600
win = display.set_mode((win_width, win_height))
display.set_caption('Пустая трата твоего времени 2')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

rocket_skin = 'rocket2.png'
score = 0
lost = 0
HP = 3



class GameSprite(sprite.Sprite):
    def __init__(self, p_image, x, y, size_x, size_y, p_speed):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (size_x, size_y))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_d] and self.rect.x < win_width - 50:
            self.rect.x += self.speed

        if keys[K_LEFT]:
            rocket_skin = 'rocket2.png'
            player = Player(rocket_skin ,470, 520, 30, 60, 15)

        if keys[K_RIGHT]:
            rocket_skin = 'новый скин ракеты.png'
            player = Player(rocket_skin ,470, 520, 30, 60, 15)

   
    def fire(self):
        keys = key.get_pressed()
        bullet_height = 40
        bullet_width = 20
        if keys[K_l]:
            bullet_height = 200
            bullet_width = 100
        if keys[K_SPACE]:
            bullet_height = 40
            bullet_width = 20
        bullet = Bullet('bulet.png', self.rect.centerx, self.rect.top, bullet_width, bullet_height, 75)
        bullets.add(bullet)

    
class Enemy(GameSprite):
    direction = 'l'
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1
        

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player(rocket_skin ,470, 520, 30, 60, 15)


monsters = sprite.Group()
for i in range(4):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 45, 30, randint(1,5))
    monsters.add(monster)


bullets = sprite.Group()

game = True
finish = False
clock = time.Clock()
FPS = 60

font.init()
font = font.SysFont('Colibri', 50)
end_win = font.render('You  [ПОТРАТИТЬ ВРЕМЯ ВПУСТУЮ] !', True, (255, 0, 0))
end_lose = font.render('You  [СЭКОНОМИТЬ ВРЕМЯ] !', True, (0, 255, 0))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')



while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE or e.key == K_l:
                fire_sound.play()
                player.fire()


    if not finish:
        win.blit(background, (0, 0))
        text_score = font.render('Score:' + str(score), 1, (39, 130, 48))
        text_lost = font.render('Lost:' + str(lost), 1, (130, 39, 39))
        text_HP = font.render('HP:' + str(HP), 1, (185, 0, 0))
        win.blit(text_score, (10, 10))
        win.blit(text_lost, (10, 50))
        win.blit(text_HP, (10, 90))



        player.update()
        player.reset()
        monsters.update()
        monsters.draw(win)
        bullets.update()
        bullets.draw(win)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 45, 30, randint(1, 5))
            
        monsters.add(monster)
        if sprite.spritecollide(player, monsters, True):
            HP -= 1
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 45, 30, randint(1, 5))
        if HP == 0 or lost >= 30:
            finish = True
            win.blit(end_lose, (250, 200))
        if score >= 100:
            finish = True
            win.blit(end_win, (150, 200))
        display.update()
    if finish:
        finish = False
        score = 0
        lost = 0
        HP += 3
        for m in monsters: 
            m.kill()
        for b in bullets:
            b.kill()

        for i in range(4):
            monster = Enemy("ufo.png", randint(80, win_width - 80), -40, 45, 30, randint(1,5))
            monsters.add(monster)
        time.delay(2000)

 
    
        
    clock.tick(FPS)



