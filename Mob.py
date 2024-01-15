import random
from init import *

current_level = 1  # Текущий уровень


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)  # Случайное изображение метеора
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.90 / 2)  # Деление на 2 - радиус

        # Случайное начальное положение и скорость
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)  # Появление за границами экрана
        self.speedy = random.randrange(5 + current_level, 9 + current_level)
        self.speedx = random.randrange(-5 - current_level, 5 + current_level)

        self.rotation = 0
        self.rotation_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()  # Отслеживание времени последнего обновления

    def rotate(self):  # Поворот метеора
        time_now = pygame.time.get_ticks()
        if time_now - self.last_update > 50:
            self.last_update = time_now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center  # Сохранение центра при повороте

    def update(self):
        self.rotate()
        self.rect.x += self.speedx  # Движение
        self.rect.y += self.speedy

        # Проверка выхода за пределы экрана
        if (self.rect.top > HEIGHT + 20) or (self.rect.left < -20) or (self.rect.right > WIDTH + 20):
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5 + current_level, 9 + current_level)
            self.speedx = random.randrange(-5 - current_level, 5 + current_level)
