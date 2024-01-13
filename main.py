from Mobs import *
from weapon import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250  # Задержка выстрелов
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()  # Время скрытия игрока
        self.power = 1
        self.power_timer = pygame.time.get_ticks()  # Время усиления оружия
        self.current_weapon = 'default'

    def update(self):
        # Проверка времени улучшения
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power = 1
            self.power_time = pygame.time.get_ticks()

        # Проверка скрытия игрока
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 30

        self.speedx = 0

        # Управление стрелками
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        elif keystate[pygame.K_RIGHT]:
            self.speedx = 5

        # Выстрел на пробел
        if keystate[pygame.K_SPACE]:
            self.shoot()

        # Проверка выхода за границы экрана
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        self.rect.x += self.speedx

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:  # Обычный выстрел
                if is_strong_gun == True:
                    bomb1 = Bomb(self.rect.left, self.rect.centery)
                    bomb2 = Bomb(self.rect.right, self.rect.centery)
                    all_sprites.add(bomb1)
                    all_sprites.add(bomb2)
                    bullets.add(bomb1)
                    bullets.add(bomb2)
                    shooting_sound.play()
                else:
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shooting_sound.play()
            if self.power >= 2:  # Выстрел с бустом
                if is_strong_gun == True:
                    bomb1 = Bomb(self.rect.left, self.rect.centery)
                    bomb2 = Bomb(self.rect.right, self.rect.centery)
                    missile1 = Missile(self.rect.centerx, self.rect.top)
                    all_sprites.add(bomb1)
                    all_sprites.add(bomb2)
                    all_sprites.add(missile1)
                    bullets.add(bomb1)
                    bullets.add(bomb2)
                    bullets.add(missile1)
                    shooting_sound.play()
                    missile_sound.play()
                else:
                    bullet1 = Bullet(self.rect.left, self.rect.centery)
                    bullet2 = Bullet(self.rect.right, self.rect.centery)
                    missile1 = Missile(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    all_sprites.add(missile1)
                    bullets.add(bullet1)
                    bullets.add(bullet2)
                    bullets.add(missile1)
                    shooting_sound.play()
                    missile_sound.play()

    def change_player_skin(player):
        global current_skin_index, player_img, player_mini_img
        current_skin_index += 1
        if current_skin_index >= 3:
            current_skin_index = 0
        player_img = pygame.image.load(path.join(img_dir, player_skins[current_skin_index])).convert()
        player_img.set_colorkey(BLACK)
        player_mini_img = pygame.transform.scale(player_img, (40, 40))
        player_mini_img.set_colorkey(BLACK)
        background_copy = background.copy()
        # Очищаем экран и отрисовываем новое изображение игрока
        screen.fill(BLACK)
        pygame.display.flip()
        screen.blit(background_copy, background_rect)
        pygame.display.flip()
        # Заменяем текстуру у текущего спрайта игрока
        player.image = player_img
        player.image = pygame.transform.scale(player_img, (50, 38))
        player.rect = player.image.get_rect()
        player.rect.centerx = WIDTH / 2
        player.rect.bottom = HEIGHT - 10

        # Обновляем экран
        pygame.display.flip()

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


# Отображение текста, здоровья и щита
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_shield_bar(surf, x, y, pct):
    pct = max(pct, 0)
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


# Начальное меню игры
def main_menu(player):
    global screen

    menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.mp3")) #Фоновая музыка
    pygame.mixer.music.play(-1)  # Проигрывается постоянно

    screen.blit(background, (0, 0))
    pygame.display.update()

    show_game_title = True

    while True:
        ev = pygame.event.poll()  # Получение события из очереди событий
        if ev.type == pygame.KEYDOWN:  # Нажата ли клавиша
            if ev.key == pygame.K_SPACE:
                break
            elif ev.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if ev.key == pygame.K_TAB:
                player.change_player_skin()
                draw_text(screen, "Current Ship Skin", 50, WIDTH / 2, HEIGHT / 2)
                screen.blit(player_mini_img, (WIDTH / 2 - 25, (HEIGHT / 4) + 40))
                show_game_title = False
                pygame.display.update()

        elif ev.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            if show_game_title:
                screen.blit(title_background, (0, 0))
                draw_text(screen, "Asteroid rain", 75, WIDTH / 2, HEIGHT / 2 - 150)
                draw_text(screen, "Press [SPACE] To Begin", 30, WIDTH / 2, HEIGHT / 2)
                draw_text(screen, "Press [ESC] To Quit", 30, WIDTH / 2, (HEIGHT / 2) + 40)
                draw_text(screen, "Press [TAB] To Change Ship Skin", 30, WIDTH / 2, (HEIGHT / 2) + 80)
                pygame.display.update()

    screen.fill(BLACK)
    draw_text(screen, "GET READY!", 40, WIDTH / 2, HEIGHT / 2)
    pygame.display.update()

    # Обратный отсчет
    for i in range(3, 0, -1):
        draw_text(screen, str(i), 100, WIDTH / 2, HEIGHT / 2 + 50)
        pygame.display.update()
        pygame.time.wait(1000)  # Ждем 1 секунду
        screen.fill(BLACK)  # Очищаем экран после отображения каждой цифры


def newmob():
    mob_element = Mob()
    all_sprites.add(mob_element)
    mobs.add(mob_element)


# Выпадение бонусов
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'strong_gun', 'laser'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy # Движение бонуса
        if self.rect.top > HEIGHT:
            self.kill() # Удаляем, если вышел за пределы экрана


class Level:
    def __init__(self, number, meteor_count, bonus_probability):
        self.number = number
        self.meteor_count = meteor_count
        self.bonus_probability = bonus_probability

# Определение уровней
LEVELS = [
    Level(number=1, meteor_count=3, bonus_probability=0),
    Level(number=2, meteor_count=4, bonus_probability=0),
    Level(number=3, meteor_count=5, bonus_probability=0),
    Level(number=4, meteor_count=6, bonus_probability=0),
    Level(number=5, meteor_count=7, bonus_probability=0),
    Level(number=6, meteor_count=8, bonus_probability=0.2),
    Level(number=7, meteor_count=9, bonus_probability=0.2),
    Level(number=8, meteor_count=10, bonus_probability=0.2),
    Level(number=9, meteor_count=12, bonus_probability=0.2),
    Level(number=10, meteor_count=15, bonus_probability=0.2),
]

current_level = 0  # Текущий уровень


def load_level(level):
    for i in range(level.meteor_count):
        if random.random() > level.bonus_probability:
            mob_element = Mob()
        else:
            mob_element = ToughMob()
        all_sprites.add(mob_element)
        mobs.add(mob_element)


def victory_screen():
    screen.fill(BLACK)
    draw_text(screen, "VICTORY!", 60, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Score: {}".format(score), 36, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press [SPACE] to play next level", 24, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting_for_key(pygame.K_SPACE)


def game_over_screen():
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 60, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Score: {}".format(score), 36, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press [SPACE] to play again", 24, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting_for_key(pygame.K_SPACE)


def waiting_for_key(key):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    waiting = False


def reset_game():
    global LEVEL, METEOR_SPEED, score
    LEVEL = 1
    METEOR_SPEED = 5
    score = 0
    player.lives = 3
    player.shield = 100
    all_sprites.empty()
    mobs.empty()
    bullets.empty()
    powerups.empty()
    player.rect.centerx = WIDTH / 2
    player.rect.bottom = HEIGHT - 10
    for i in range(8):
        newmob()
    all_sprites.add(player)


running = True
menu_display = True
new_level = False
while running:
    if menu_display:
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        main_menu(player)
        pygame.time.wait(3000)

        # Играть музыку
        pygame.mixer.music.load(path.join(sound_folder, 'game.mp3'))
        pygame.mixer.music.play(-1)  # Играет постоянно

        menu_display = False

        mobs = pygame.sprite.Group()
        for i in range(8):
            newmob()

        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()

        bombs = pygame.sprite.Group()
        meteors = pygame.sprite.Group()
        score = 0

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            all_sprites.update()
            powerups.update()
            bombs.add(bomb)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    all_sprites.update()


    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)

    for hit in hits:
        score += 50 - hit.radius
        random.choice(expl_sounds).play()

        if is_strong_gun == True:
            expl = ExplosionBomb(hit.rect.center, 'lg')
        else:
            expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    hits = pygame.sprite.spritecollide(player, mobs, True,
                                       pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        if is_strong_gun == True:
            expl = ExplosionBomb(hit.rect.center, 'sm')
        else:
            expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
        if hit.type == 'strong_gun':
            is_strong_gun = True
        if hit.type == 'laser':
            is_strong_gun = False

    for bomb in bombs:
        meteor_hit_list = pygame.sprite.spritecollide(bomb, meteors, True)
        for meteor in meteor_hit_list:
            # Применить эффект взрыва
            explosion = ExplosionBomb(meteor.rect.center, 'lg')
            all_sprites.add(explosion)
            meteor.kill()

    # Проверка, если игрок набрал достаточно очков для победы
    if score >= VICTORY_SCORE:
        current_level += 1
        if current_level < len(LEVELS):
            level = LEVELS[current_level]
            load_level(level)
            new_level = True  # Обозначаем начало нового уровня
        else:
            # Игрок прошел все уровни
            victory_screen()
            reset_game()
            new_level = False  # Сброс флага нового уровня
        victory_screen()
        is_strong_gun = False
        reset_game()

    # Проверка, если у игрока закончились жизни
    if player.lives == 0:
        game_over_screen()
        reset_game()

    if player.lives == 0 and not death_explosion.alive():
        running = False

    # Проверка, если игрок убил все метеоры, переход на следующий уровень
    # if score >= 100 and not new_level:
    #     current_level += 1
    #     if current_level < len(LEVELS):
    #         level = LEVELS[current_level]
    #         load_level(level)
    #         new_level = True  # Обозначаем начало нового уровня
    #     else:
    #         # Игрок прошел все уровни
    #         victory_screen()
    #         reset_game()
    #         new_level = False  # Сброс флага нового уровня

    if new_level:
        screen.fill(BLACK)
        draw_text(screen, f"Level {current_level + 1}", 36, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()
        pygame.time.wait(2000)  # Пауза перед началом нового уровня
        new_level = False

    screen.fill(BLACK)
    screen.blit(background, background_rect)

    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)


    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
    draw_text(screen, f"Level: {current_level + 1}", 18, WIDTH / 2, 30)

    pygame.display.flip()
# load_level(LEVELS[current_level])
pygame.quit()
