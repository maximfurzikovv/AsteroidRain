import pygame
from os import path

img_dir = path.join(path.dirname(__file__), 'assets')  # Путь к текстурам
sound_folder = path.join(path.dirname(__file__), 'sounds')  # Путь к звукам

WIDTH = 480  # Ширина окна
HEIGHT = 600  # Высота окна
FPS = 60
POWERUP_TIME = 5000  # Время действия бонуса
BAR_LENGTH = 100  # Длина bar
BAR_HEIGHT = 10  # Высота bar

# Базовые цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

is_strong_gun = False

# Инициализация pygame и создание окна
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создание окна
pygame.display.set_caption("Asteroid Rain")
clock = pygame.time.Clock()   # Синхронизация FPS

font_name = pygame.font.match_font('arial')

VICTORY_SCORE = 1000

player_skins = [
    'playerShip1_gray.png',
    'playerShip2_blue.png',
    'playerShip3_red.png',
]
current_skin_index = 0  # Индекс текущей текстуры корабля
player_img = pygame.image.load(path.join(img_dir, player_skins[current_skin_index])).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)  # Черный цвет становится прозрачным

# Загрузка текстур
background = pygame.image.load(path.join(img_dir, 'starfield.png')).convert()
background_rect = background.get_rect()
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()
missile_img = pygame.image.load(path.join(img_dir, 'missile.png')).convert()
meteor_images = []
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png',
    'meteorBrown_med1.png',
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png'
]

for image in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, image)).convert())

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert()
powerup_images['strong_gun'] = pygame.image.load(path.join(img_dir, 'strong_gun.png')).convert()

powerup_images['laser'] = pygame.image.load(path.join(img_dir, 'laser.png')).convert()
powerup_images['laser'] = pygame.transform.scale(powerup_images['laser'], (40, 40))
width_of_shield_and_bolt, height_of_shield_and_bolt = powerup_images['shield'].get_size()

strong_gun_img = pygame.image.load(path.join(img_dir, 'strong_gun.png')).convert()
strong_gun_img = pygame.transform.scale(
    strong_gun_img, (width_of_shield_and_bolt, height_of_shield_and_bolt)
)
powerup_images['strong_gun'] = strong_gun_img

# Взрыв метеора
explosion_anim = {}
explosion_anim['lg'] = []  # Большой метеор
explosion_anim['sm'] = []  # Маленький метеор
explosion_anim['player'] = []  # Игрок
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)

    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

# Загрузка звуков
shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_folder, 'rocket.ogg'))
expl_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder, sound)))

pygame.mixer.music.set_volume(0.7)  # Устанавливаем громкость
player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))

# Группы спрайтов (контейнеры графических объектов)
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
powerups = pygame.sprite.Group()
bombs = pygame.sprite.Group()
meteors = pygame.sprite.Group()
