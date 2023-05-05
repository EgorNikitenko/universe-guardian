import pygame
import random

pygame.init()

w = pygame.display.set_mode((512, 512))

clock = pygame.time.Clock()

cooldown_tracker = 0



fps = 60

pygame.display.set_caption('Universe Guardian')


class Area:
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = (0, 0, 0)
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(w, self.fill_color, self.rect)


class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10, color=None):
        Area.__init__(self, x, y, width, height, color)
        self.image = pygame.image.load(filename)

        self.last = pygame.time.get_ticks()
        self.cooldown = 3000

    def draw_picture(self):
        w.blit(self.image, (self.rect.x, self.rect.y))


class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.text = text
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw_text(self, shift_x=0, shift_y=0):
        self.fill()
        w.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

#class Explosion(pygame.sprite.Sprite):
   # def __init__(self, x, y):
       # pygame.sprite.Sprite.__init__(self)
       # self.images = []
       # for num in range(1, 6):
           # img = pygame.image.load(f"imm/exp{num}.png")
           # img = pygame.transform.scale(img,(100,100))
           # self.images.append(img)
        #self.index = 0
       # self.image = self.images[self.index]
        #self.rect = self.image.get_rect()
       # self.rect.center = [x, y]
       # self.counter = 0

    #def update(self):
       # explosion_speed = 4
        #self.counter += 1

        #if self.counter >= explosion_speed and self.index < len(self.images) -1:
           # self.counter = 0
            #self.index += 1
           # self.image = self.images[self.index]
        #if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
           # self.kiil()





# спрайт
gun = Picture('gun.png', 210, 410, 80, 100)
enemy = Picture('enemy.png', 200, 5, 10, 10)
bg = Picture('space.png', 0, 0, 10, 10)
gg = Picture('gameover.png',140,100, 10, 10)
restart = Picture('restart.png',140, 250, 275,92)
quit1 = Picture('quit.png', 140, 330, 154,117)
youwin = Picture('youwin.png',140, 100,319,101)


# управление кораблём

is_right = False
is_left = False
is_up = False
is_down = False

# проджектайлы

bullets_monsters = []

bullets = []

# ряд с чуваками

bullet_speed = 5
monsters_speed = 60

monsters = []
enemies_per_row = 8
enemy_rows = 1
start_x = 5
start_y = 5

is_enemies_drawn = False

is_gg = False

is_win = False

is_paused = False


# отрисовка чуваков

def render_enemies():

    for i in range(enemy_rows):
        x = start_x + 1
        y = start_y + 70 * i

        for j in range(enemies_per_row):
            m = Picture('enemy.png',x, y, 60, 60)
            monsters.append(m)
            x += 63.5


# игровой цикл

wait = 0

while True:

    #print(clock.get_time())
    cooldown_tracker += clock.get_time()


#проигрыш


    if is_gg:


#кнопка рефреш

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if restart.rect.collidepoint(x,y):
                    is_gg = False
                if quit1.rect.collidepoint(x,y):
                    pygame.quit()



        bg.draw_picture()

        if is_win:
            youwin.draw_picture()

        else:

            gg.draw_picture()
        quit1.draw_picture()
        restart.draw_picture()

        clock.tick(fps)
        pygame.display.update()

    else:

        if not is_paused:

            bg.draw_picture()
            gun.draw_picture()


            if not is_enemies_drawn:
                render_enemies()
                is_enemies_drawn = True

            if wait == 0:
                m = random.choice(monsters)
                projectilem = Picture('projectilem.png', m.rect.x + 2, m.rect.y + 23, 10, 10)
                projectilem2 = Picture('projectilem.png', m.rect.x + 42, m.rect.y + 23, 10, 10)
                bullets_monsters.append(projectilem)
                bullets_monsters.append(projectilem2)

                wait = 60
            else:
                wait -= 1

            for i in bullets_monsters:
                i.rect.y += 3
                i.draw_picture()

                if i.rect.colliderect(gun.rect):
                    is_gg = True
                    bullets.clear()
                    monsters.clear()
                    bullets_monsters.clear()
                    gun.rect.x = 210
                    gun.rect.y = 410
                    render_enemies()

            if len(monsters) == 0:
                is_gg = True
                bullets.clear()
                monsters.clear()
                bullets_monsters.clear()
                gun.rect.x = 210
                gun.rect.y = 410
                render_enemies()
                is_win = True




            # движение чуваков

            if cooldown_tracker > monsters_speed:
                for monster in monsters:
                    monster.rect.y += 1

                    monster.draw_picture()




                cooldown_tracker = 0

            for monster in monsters:
                monster.draw_picture()

            # движение пуль

            for bullet in bullets:
                bullet.draw_picture()
                bullet.rect.y -= bullet_speed

                for monster in monsters:

                    if monster.rect.colliderect(bullet.rect):
                        monsters.remove(monster)
                        bullets.remove(bullet)

            #анимація вибуху


            # системное окно

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # управление кораблём

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        is_right = True

                    if event.key == pygame.K_a:
                        is_left = True

                    if event.key == pygame.K_w:
                        is_up = True

                    if event.key == pygame.K_s:
                        is_down = True

                    # механика стрельбы

                    if event.key == pygame.K_SPACE:
                        projectile = Picture('projectile.png', gun.rect.x + 13, gun.rect.y +23, 10, 10)
                        projectile1 = Picture('projectile.png', gun.rect.x + 57, gun.rect.y +23, 10, 10)

                        bullets.append(projectile)
                        bullets.append(projectile1)


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d:
                        is_right = False

                    if event.key == pygame.K_a:
                        is_left = False

                    if event.key == pygame.K_w:
                        is_up = False

                    if event.key == pygame.K_s:
                        is_down = False

            if is_right == True and gun.rect.x <= 422:
                gun.rect.x += 3.5

            if is_left == True and gun.rect.x >= 0:
                gun.rect.x -= 3.5

            if is_up == True and gun.rect.y >= 380:
                gun.rect.y -= 3.5

            if is_down == True and gun.rect.y <= 409:
                gun.rect.y += 3.5

            #if event.type == monsters.rect.colliderect(bullet.rect):
                #explosion = Explosion(pos[0], pos[1])
                #explotion_group.add(explosion)


            clock.tick(fps)
            pygame.display.update()
