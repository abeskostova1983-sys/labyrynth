#создай игру "Лабиринт"!
import  pygame 
pygame.init()
pygame.font.init()
pygame.mixer.init()
win_w = 700
win_h = 500
window = pygame.display.set_mode((win_w, win_h))
pygame.display.set_caption("Maze")
backgreound = pygame.transform.scale(
    pygame.image.load('background.jpg'), (win_w, win_h)
)
clock = pygame.time.Clock()
FPS = 144
pygame.mixer.music.load('jungles.ogg')
pygame.mixer.music.play(-1)
money = pygame.mixer.Sound('money.ogg')
kick = pygame.mixer.Sound('kick.ogg')
font_obj = pygame.font.Font(None, 70)
win_text = font_obj.render('YOU WIN!', True, (255, 215, 0))
lose_text = font_obj.render('YOU LOSE!', True, (255, 0, 0))
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < win_w - 70:
            self.rect.x += self.speed
        if keys[pygame.K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < win_h - 70:
            self.rect.y += self.speed
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed, start_limit, end_limit):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.start_limit = start_limit
        self.end_limit = end_limit
        self.direction = "left"
    def update(self):
        if self.rect.x <= self.start_limit:
            self.direction = "right"
        elif self.rect.x >= self.end_limit:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Wall(pygame.sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color = (color_1, color_2, color_3)
        self.width = wall_width
        self.height = wall_height
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
packman = Player("hero.png", 50, 400, 4)
monster = Enemy("cyborg.png", 500, 280, 2, 400, 600)
final = GameSprite("treasure.png", 580, 400, 0)
w1 = Wall(154, 205, 50, 100, 20, 10, 360)
w2 = Wall(154, 205, 50, 100, 370, 350, 10)
w3 = Wall(154, 205, 50, 250, 100, 10, 270)
game = True
finish = False
while game:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            game = False
    if finish != True:
        window.blit(backgreound, (0,0))
        packman.update()
        monster.update()
        packman.reset()
        monster.reset()
        final.reset()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        if pygame.sprite.collide_rect(packman, final):
            finish = True
            window.blit(win_text,(200, 200))
            money.play()
        if (pygame.sprite.collide_rect(packman, monster) or
            pygame.sprite.collide_rect(packman, w1) or
            pygame.sprite.collide_rect(packman, w2) or
            pygame.sprite.collide_rect(packman, w3)):
            finish = True
            window.blit(lose_text, (200, 200))
            kick.play()
    pygame.display.update()
    clock.tick(FPS)