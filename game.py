"""
Вся игра в одном файле с работающими платформами
"""

import pygame
import sys
import math

from sprites import sprite_manager

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Цвета
BACKGROUND = (26, 26, 46)        # Темно-синий
PLAYER_CHIP = (249, 168, 38)     # Оранжевый
PLAYER_DALE = (233, 69, 96)      # Красный
PLATFORM_MAIN = (15, 52, 96)     # Синий
PLATFORM_TOP = (233, 69, 96)     # Красный
PLATFORM_TEXTURE = (22, 33, 62)  # Темно-синий
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ENEMY_GROUND = (139, 69, 19)     # Коричневый
ENEMY_FLYING = (255, 105, 180)   # Розовый
ENEMY_BOSS = (255, 0, 0)         # Красный
TEXT_COLOR = (255, 255, 255)

class Player:
    def __init__(self, start_x=50, start_y=300):
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.width = 40
        self.height = 60
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.jump_power = 12
        self.gravity = 0.5
        self.friction = 0.8
        self.is_jumping = False
        self.character = "Чип"
        self.facing_right = True
        self.projectiles = []
        self.attack_cooldown = 0
        # Добавляем rect для коллизий
        self.rect = pygame.Rect(start_x, start_y, self.width, self.height)
        self.on_ground = False

    def update(self, keys, platforms=None):
        """Обновление состояния игрока"""
        # Сохраняем предыдущую позицию
        prev_x, prev_y = self.x, self.y

        # Движение
        if keys[pygame.K_LEFT]:
            self.vx = -self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.vx = self.speed
            self.facing_right = True
        else:
            self.vx *= self.friction

        # Прыжок - только если стоит на поверхности
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vy = -self.jump_power
            self.is_jumping = True
            self.on_ground = False

        # Атака
        if keys[pygame.K_z] and self.attack_cooldown <= 0:
            self.shoot()
            self.attack_cooldown = 15

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Применяем гравитацию
        self.vy += self.gravity

        # Сохраняем позицию до движения
        old_x, old_y = self.x, self.y

        # Пробуем двигаться по X
        self.x += self.vx
        self.rect.x = int(self.x)

        # Проверяем коллизии по X
        if platforms:
            self.check_platform_collisions_x(platforms)

        # Пробуем двигаться по Y
        self.y += self.vy
        self.rect.y = int(self.y)

        # Сбрасываем флаг земли
        self.on_ground = False

        # Проверяем коллизии по Y
        if platforms:
            self.check_platform_collisions_y(platforms)

        # Границы экрана по X
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.rect.x = int(self.x)

        # Проверка на падение за экран
        if self.y > SCREEN_HEIGHT:
            self.respawn()
            return

        # Обновление снарядов
        for proj in self.projectiles[:]:
            proj['x'] += proj['speed']
            if proj['x'] > SCREEN_WIDTH or proj['x'] + proj['width'] < 0:
                self.projectiles.remove(proj)

    def check_platform_collisions_x(self, platforms):
        """Проверка горизонтальных столкновений с платформами"""
        for platform in platforms:
            x, y, width, height = platform
            platform_rect = pygame.Rect(x, y, width, height)

            if self.rect.colliderect(platform_rect):
                # Если движемся вправо
                if self.vx > 0:
                    self.x = x - self.width
                    self.rect.x = int(self.x)
                    self.vx = 0
                # Если движемся влево
                elif self.vx < 0:
                    self.x = x + width
                    self.rect.x = int(self.x)
                    self.vx = 0

    def check_platform_collisions_y(self, platforms):
        """Проверка вертикальных столкновений с платформами"""
        for platform in platforms:
            x, y, width, height = platform
            platform_rect = pygame.Rect(x, y, width, height)

            if self.rect.colliderect(platform_rect):
                # Если падаем вниз (стоим на платформе)
                if self.vy > 0:
                    self.y = y - self.height
                    self.rect.y = int(self.y)
                    self.vy = 0
                    self.is_jumping = False
                    self.on_ground = True
                # Если движемся вверх (ударились головой)
                elif self.vy < 0:
                    self.y = y + height
                    self.rect.y = int(self.y)
                    self.vy = 0

    def shoot(self):
        """Выстрел снарядом"""
        if self.facing_right:
            projectile = {
                'x': self.x + self.width,
                'y': self.y + self.height // 2 - 5,
                'width': 20,
                'height': 10,
                'speed': 8,
                'rect': pygame.Rect(self.x + self.width, self.y + self.height // 2 - 5, 20, 10)
            }
        else:
            projectile = {
                'x': self.x - 20,
                'y': self.y + self.height // 2 - 5,
                'width': 20,
                'height': 10,
                'speed': -8,
                'rect': pygame.Rect(self.x - 20, self.y + self.height // 2 - 5, 20, 10)
            }
        self.projectiles.append(projectile)

    def switch_character(self):
        """Смена персонажа"""
        self.character = "Дейл" if self.character == "Чип" else "Чип"

    def respawn(self):
        """Возрождение на стартовой позиции"""
        self.x = self.start_x
        self.y = self.start_y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.vx = 0
        self.vy = 0
        self.projectiles = []
        self.is_jumping = False
        self.on_ground = False
        self.facing_right = True

    def draw(self, screen):
        """Отрисовка игрока со спрайтом"""
        # Получаем спрайт
        sprite_name = 'chip' if self.character == 'Чип' else 'dale'
        sprite = sprite_manager.get_sprite(sprite_name)

        if sprite and sprite_manager.loaded:
            # Если спрайт загружен
            if not self.facing_right:
                # Отражаем спрайт если смотрит влево
                sprite = pygame.transform.flip(sprite, True, False)

            # Рисуем спрайт
            screen.blit(sprite, (self.x, self.y))
        else:
            # Fallback - цветной прямоугольник
            color = PLAYER_CHIP if self.character == "Чип" else PLAYER_DALE

            # Тело
            pygame.draw.rect(screen, color,
                             (self.x, self.y, self.width, self.height))

            # Глаза
            eye_x = self.x + 25 if self.facing_right else self.x + 7
            pygame.draw.rect(screen, WHITE,
                             (eye_x, self.y + 15, 8, 8))
            pygame.draw.rect(screen, BLACK,
                             (eye_x + 2, self.y + 17, 4, 4))

            # Нос
            nose_x = self.x + 20 if self.facing_right else self.x + 12
            pygame.draw.rect(screen, BLACK,
                             (nose_x, self.y + 25, 5, 5))

        # Снаряды
        for proj in self.projectiles:
            projectile_color = (0, 255, 0)  # Зеленый
            pygame.draw.rect(screen, projectile_color,
                             (proj['x'], proj['y'], proj['width'], proj['height']))

class Enemy:
    def __init__(self, x, y, enemy_type="ground", speed=2):
        self.x = x
        self.y = y
        self.type = enemy_type

        if enemy_type == "boss":
            self.width = 60
            self.height = 60
        else:
            self.width = 40
            self.height = 40

        self.speed = speed
        self.direction = 1
        self.is_alive = True
        self.animation_timer = 0
        self.rect = pygame.Rect(x, y, self.width, self.height)  # Добавляем rect

        # Цвета врагов
        if enemy_type == "ground":
            self.color = ENEMY_GROUND
        elif enemy_type == "flying":
            self.color = ENEMY_FLYING
        else:
            self.color = ENEMY_BOSS

    def update(self, player_x=400):
        """Обновление врага"""
        if not self.is_alive:
            return

        self.animation_timer += 1

        if self.type == "ground":
            # Наземный враг ходит туда-сюда
            self.x += self.speed * self.direction
            self.rect.x = int(self.x)
            if self.x <= 0 or self.x + self.width >= SCREEN_WIDTH:
                self.direction *= -1

        elif self.type == "flying":
            # Летающий враг летает волнообразно
            self.x += self.speed * self.direction
            self.y += math.sin(self.animation_timer / 30) * 2
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)
            if self.x <= 0 or self.x + self.width >= SCREEN_WIDTH:
                self.direction *= -1

        elif self.type == "boss":
            # Босс следует за игроком
            if player_x > self.x:
                self.x += self.speed
            else:
                self.x -= self.speed

            # Ограничение движения босса
            self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
            self.y = max(50, min(SCREEN_HEIGHT - 150, self.y))
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

    def draw(self, screen):
        """Отрисовка врага со спрайтом"""
        if not self.is_alive:
            return

        # Определяем имя спрайта
        if self.type == "ground":
            sprite_name = 'rat'
        elif self.type == "flying":
            sprite_name = 'bee'
        else:  # boss
            sprite_name = 'fatcat'

        # Пытаемся получить спрайт
        sprite = sprite_manager.get_sprite(sprite_name)

        if sprite and sprite_manager.loaded:
            # Масштабируем спрайт к размеру врага
            sprite = pygame.transform.scale(sprite, (self.width, self.height))

            # Рисуем спрайт
            screen.blit(sprite, (self.x, self.y))
        else:
            # Fallback - цветной прямоугольник
            # Тело
            pygame.draw.rect(screen, self.color,
                             (self.x, self.y, self.width, self.height))

            # Глаза
            eye_size = 8 if self.type != "boss" else 10
            pupil_size = 4 if self.type != "boss" else 6

            pygame.draw.rect(screen, WHITE,
                             (self.x + 5, self.y + 10, eye_size, eye_size))
            pygame.draw.rect(screen, WHITE,
                             (self.x + self.width - eye_size - 5,
                              self.y + 10, eye_size, eye_size))

            # Зрачки
            pygame.draw.rect(screen, BLACK,
                             (self.x + 7, self.y + 12, pupil_size, pupil_size))
            pygame.draw.rect(screen, BLACK,
                             (self.x + self.width - pupil_size - 7,
                              self.y + 12, pupil_size, pupil_size))

    def get_rect(self):
        """Получение прямоугольника для коллизий"""
        return self.rect

class Level:
    def __init__(self, number):
        self.number = number
        self.platforms = []
        self.enemies = []
        self.player_start = (50, 300)
        self.objective = ""

        if number == 1:
            self.load_level1()
        elif number == 2:
            self.load_level2()
        elif number == 3:
            self.load_level3()

    def load_level1(self):
        """Лесной уровень"""
        self.platforms = [
            (0, 500, 800, 100),   # Земля (нижняя платформа)
            (100, 400, 150, 20),  # Платформа 1
            (350, 350, 150, 20),  # Платформа 2
            (550, 300, 150, 20)   # Платформа 3
        ]

        # Враги стоят на платформах
        self.enemies = [
            Enemy(120, 340, "ground", 2),  # На нижней платформе
            Enemy(470, 290, "ground", 2),  # На средней платформе
            Enemy(600, 240, "flying", 3)   # Летающий
        ]

        self.player_start = (50, 440)  # Старт на земле
        self.objective = "Победите 3 врагов!"

    def load_level2(self):
        """Городской уровень"""
        self.platforms = [
            (0, 500, 800, 100),   # Земля
            (50, 400, 120, 20),   # Платформа 1
            (200, 350, 120, 20),  # Платформа 2
            (380, 300, 120, 20),  # Платформа 3
            (560, 250, 120, 20),  # Платформа 4
            (700, 200, 100, 20)   # Платформа 5
        ]

        self.enemies = [
            Enemy(80, 380, "ground", 3),   # На платформе 1
            Enemy(230, 330, "ground", 3),  # На платформе 2
            Enemy(410, 250, "flying", 4),  # Летающий
            Enemy(590, 200, "flying", 4)   # Летающий
        ]

        self.player_start = (50, 440)  # Старт на земле
        self.objective = "Победите 4 врагов!"

    def load_level3(self):
        """Лабиринт Котомрыска"""
        self.platforms = [
            (0, 500, 800, 100),   # Земля
            (100, 400, 100, 20),  # Платформа 1
            (220, 350, 100, 20),  # Платформа 2
            (340, 300, 100, 20),  # Платформа 3
            (460, 250, 100, 20),  # Платформа 4
            (580, 200, 100, 20),  # Платформа 5
            (700, 150, 100, 20)   # Платформа 6
        ]

        self.enemies = [
            Enemy(120, 380, "ground", 4),   # На платформе 1
            Enemy(240, 330, "ground", 4),   # На платформе 2
            Enemy(360, 250, "flying", 5),   # Летающий
            Enemy(480, 200, "flying", 5),   # Летающий
            Enemy(720, 90, "boss", 2)       # Босс на верхней платформе
        ]

        self.player_start = (50, 440)  # Старт на земле
        self.objective = "Победите босса Котомрыска!"

    def draw_platforms(self, screen):
        """Отрисовка платформ уровня"""
        for platform in self.platforms:
            x, y, width, height = platform

            # Основная часть платформы
            pygame.draw.rect(screen, PLATFORM_MAIN,
                            (x, y, width, height))

            # Верхняя грань (для лучшей видимости)
            pygame.draw.rect(screen, PLATFORM_TOP,
                            (x, y, width, 5))

            # Текстура платформы (точки)
            for i in range(x + 10, x + width - 10, 20):
                pygame.draw.rect(screen, PLATFORM_TEXTURE,
                                (i, y + 8, 6, 4))

class Game:
    def __init__(self):
        # Инициализация PyGame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Чип и Дейл спешат на помощь")

        # Шрифты
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)

        # Загрузка спрайтов
        sprite_manager.load_sprites()

        # Игровые данные
        self.score = 0
        self.lives = 3
        self.current_level = 1
        self.game_state = "menu"  # menu, playing, paused, game_over, level_complete
        self.level_score = 0

        # Игровые объекты
        self.player = None
        self.level = None
        self.enemies = []

        # Загрузка первого уровня
        self.load_level(self.current_level)

        # Таймер
        self.clock = pygame.time.Clock()
        self.running = True

    def load_level(self, level_number):
        """Загрузка уровня"""
        self.level = Level(level_number)
        self.player = Player(*self.level.player_start)
        self.enemies = self.level.enemies.copy()
        self.level_score = 0
        self.game_state = "playing"

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.game_state == "playing":
                    if event.key == pygame.K_x:
                        self.player.switch_character()
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "paused"

                elif self.game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        self.game_state = "playing"

                elif self.game_state == "paused":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "playing"

                elif self.game_state == "game_over":
                    if event.key == pygame.K_r:
                        self.restart_game()

                elif self.game_state == "level_complete":
                    if event.key == pygame.K_n:
                        self.next_level()

    def update(self):
        """Обновление игровой логики"""
        if self.game_state != "playing":
            return

        # Обновление игрока с передачей платформ
        keys = pygame.key.get_pressed()
        platforms = self.level.platforms if self.level else []
        self.player.update(keys, platforms)

        # Обновление врагов
        for enemy in self.enemies:
            enemy.update(self.player.x)

        # Проверка столкновений
        self.check_collisions()

        # Проверка завершения уровня
        if all(not enemy.is_alive for enemy in self.enemies):
            self.complete_level()

    def check_collisions(self):
        """Проверка всех столкновений"""
        # Игрок с врагами
        player_rect = self.player.rect

        for enemy in self.enemies:
            if not enemy.is_alive:
                continue

            enemy_rect = enemy.get_rect()

            # Столкновение игрока с врагом
            if player_rect.colliderect(enemy_rect):
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()
                else:
                    self.player.respawn()
                return

        # Снаряды с врагами
        for projectile in self.player.projectiles[:]:
            # Обновляем rect снаряда
            projectile['rect'].x = int(projectile['x'])
            projectile['rect'].y = int(projectile['y'])

            for enemy in self.enemies:
                if not enemy.is_alive:
                    continue

                enemy_rect = enemy.get_rect()

                if projectile['rect'].colliderect(enemy_rect):
                    enemy.is_alive = False
                    if projectile in self.player.projectiles:
                        self.player.projectiles.remove(projectile)
                    self.score += 100
                    self.level_score += 100
                    break

    def complete_level(self):
        """Завершение уровня"""
        # Бонус за оставшиеся жизни
        life_bonus = self.lives * 500
        self.score += life_bonus
        self.level_score += life_bonus

        self.game_state = "level_complete"
        print(f"Уровень {self.current_level} пройден! Очки: {self.level_score}")

    def next_level(self):
        """Переход на следующий уровень"""
        self.current_level += 1
        if self.current_level > 3:
            self.game_complete()
        else:
            self.load_level(self.current_level)

    def game_over(self):
        """Конец игры"""
        self.game_state = "game_over"
        print("Игра окончена!")

    def game_complete(self):
        """Завершение всей игры"""
        print(f"Поздравляем! Вы выиграли! Финальный счет: {self.score}")
        self.running = False

    def restart_game(self):
        """Перезапуск игры"""
        self.score = 0
        self.lives = 3
        self.current_level = 1
        self.load_level(self.current_level)

    def draw(self):
        """Отрисовка игры"""
        # Фон
        self.screen.fill(BACKGROUND)

        if self.game_state == "playing":
            # Отрисовка уровня
            if self.level:
                self.level.draw_platforms(self.screen)

            # Отрисовка врагов
            for enemy in self.enemies:
                enemy.draw(self.screen)

            # Отрисовка игрока
            self.player.draw(self.screen)

        # Отрисовка UI
        self.draw_ui()

    def draw_ui(self):
        """Отрисовка пользовательского интерфейса"""
        # Панель статистики
        stats_bg = pygame.Rect(0, 0, SCREEN_WIDTH, 40)
        pygame.draw.rect(self.screen, PLATFORM_MAIN, stats_bg)
        pygame.draw.rect(self.screen, PLATFORM_TOP, stats_bg, 2)

        # Тексты статистики
        score_text = self.small_font.render(f"Очки: {self.score}", True, TEXT_COLOR)
        lives_text = self.small_font.render(f"Жизни: {self.lives}", True, TEXT_COLOR)
        level_text = self.small_font.render(f"Уровень: {self.current_level}", True, TEXT_COLOR)
        char_text = self.small_font.render(f"Персонаж: {self.player.character if self.player else 'Чип'}", True, TEXT_COLOR)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (150, 10))
        self.screen.blit(level_text, (280, 10))
        self.screen.blit(char_text, (420, 10))

        # Цель уровня
        if self.level and self.game_state == "playing":
            obj_text = self.small_font.render(f"Цель: {self.level.objective}", True, TEXT_COLOR)
            self.screen.blit(obj_text, (10, SCREEN_HEIGHT - 30))

        # Подсказки управления (только во время игры)
        if self.game_state == "playing":
            controls_text = self.small_font.render("X-смена персонажа | Z-атака | ESC-пауза", True, TEXT_COLOR)
            self.screen.blit(controls_text, (SCREEN_WIDTH - controls_text.get_width() - 10, SCREEN_HEIGHT - 30))

        # Экран меню
        if self.game_state == "menu":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))

            title = self.large_font.render("Чип и Дейл спешат на помощь", True, PLAYER_CHIP)
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))

            controls = [
                "Управление:",
                "← → - Движение",
                "Пробел - Прыжок",
                "Z - Атака",
                "X - Смена персонажа",
                "ESC - Пауза/Выход",
                "",
                "Нажми ПРОБЕЛ чтобы начать"
            ]

            for i, line in enumerate(controls):
                text = self.font.render(line, True, TEXT_COLOR)
                self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 200 + i*40))

        # Экран паузы
        elif self.game_state == "paused":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            pause_text = self.large_font.render("ПАУЗА", True, TEXT_COLOR)
            self.screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, 250))

            inst_text = self.font.render("Нажми ESC чтобы продолжить", True, TEXT_COLOR)
            self.screen.blit(inst_text, (SCREEN_WIDTH//2 - inst_text.get_width()//2, 320))

        # Game Over
        elif self.game_state == "game_over":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.large_font.render("ИГРА ОКОНЧЕНА", True, (255, 0, 0))
            score_text = self.font.render(f"Ваш счет: {self.score}", True, TEXT_COLOR)
            restart_text = self.font.render("Нажми R чтобы начать заново", True, TEXT_COLOR)

            self.screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 200))
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 280))
            self.screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 340))

        # Уровень пройден
        elif self.game_state == "level_complete":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            complete_text = self.large_font.render(f"УРОВЕНЬ {self.current_level} ПРОЙДЕН!", True, (0, 255, 0))
            score_text = self.font.render(f"Очки за уровень: {self.level_score}", True, TEXT_COLOR)
            next_text = self.font.render("Нажми N для следующего уровня", True, TEXT_COLOR)

            self.screen.blit(complete_text, (SCREEN_WIDTH//2 - complete_text.get_width()//2, 200))
            self.screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 280))
            self.screen.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, 340))

    def run(self):
        """Главный игровой цикл"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()