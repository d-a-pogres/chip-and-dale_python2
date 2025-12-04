"""
Система спрайтов для игры
"""

import pygame
import os

class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.loaded = False

    def load_sprites(self):
        """Загрузка всех спрайтов"""
        try:
            # Пути к спрайтам
            sprite_paths = {
                'chip': 'assets/sprites/chip.png',
                'dale': 'assets/sprites/dale.png',
                'rat': 'assets/sprites/rat.png',
                'bee': 'assets/sprites/bee.png',
                'fatcat': 'assets/sprites/fatcat.png'
            }

            # Загрузка каждого спрайта
            for name, path in sprite_paths.items():
                try:
                    if os.path.exists(path):
                        image = pygame.image.load(path)
                        # Преобразуем в правильный формат
                        if image.get_alpha() is None:
                            image = image.convert()
                        else:
                            image = image.convert_alpha()

                        # Сохраняем оригинальный размер
                        original_size = image.get_size()

                        # Масштабируем спрайты до нужного размера
                        if name in ['chip', 'dale']:
                            # Персонажи: 40x60
                            scaled_size = (40, 60)
                        elif name == 'fatcat':
                            # Босс: 60x60
                            scaled_size = (60, 60)
                        else:
                            # Обычные враги: 40x40
                            scaled_size = (40, 40)

                        # Масштабируем только если размер не совпадает
                        if original_size != scaled_size:
                            image = pygame.transform.scale(image, scaled_size)

                        self.sprites[name] = image
                        print(f"✓ Загружен спрайт: {name}")
                    else:
                        print(f"⚠ Файл не найден: {path}, использую fallback")
                        self.create_fallback_sprite(name)

                except Exception as e:
                    print(f"❌ Ошибка загрузки {name}: {e}")
                    self.create_fallback_sprite(name)

            self.loaded = True
            print("✅ Все спрайты загружены!")

        except Exception as e:
            print(f"❌ Критическая ошибка загрузки спрайтов: {e}")
            self.create_all_fallback_sprites()
            self.loaded = True

    def create_fallback_sprite(self, name):
        """Создание fallback спрайта если файл не найден"""
        print(f"Создаю fallback спрайт для {name}")

        # Размеры спрайтов
        if name in ['chip', 'dale']:
            width, height = 40, 60
        elif name == 'fatcat':
            width, height = 60, 60
        else:
            width, height = 40, 40

        # Создаем поверхность
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Цвета в зависимости от типа
        colors = {
            'chip': (249, 168, 38),    # Оранжевый
            'dale': (233, 69, 96),     # Красный
            'rat': (139, 69, 19),      # Коричневый
            'bee': (255, 215, 0),      # Золотой
            'fatcat': (255, 69, 0)     # Оранжево-красный
        }

        color = colors.get(name, (255, 255, 255))

        # Рисуем тело
        if name in ['chip', 'dale']:
            # Бурундуки
            surface.fill(color)
            # Полоски на спине
            stripe_color = (139, 69, 19) if name == 'chip' else (178, 34, 34)
            for i in range(5):
                pygame.draw.rect(surface, stripe_color,
                               (10, 20 + i * 8, 20, 3))

            # Глаза
            pygame.draw.rect(surface, (255, 255, 255), (15, 10, 8, 8))
            pygame.draw.rect(surface, (255, 255, 255), (27, 10, 8, 8))

            # Зрачки
            pygame.draw.rect(surface, (0, 0, 0), (17, 12, 4, 4))
            pygame.draw.rect(surface, (0, 0, 0), (29, 12, 4, 4))

            # Нос
            pygame.draw.rect(surface, (0, 0, 0), (22, 20, 5, 5))

        elif name == 'rat':
            # Крыса
            surface.fill(color)
            # Хвост
            pygame.draw.rect(surface, (105, 105, 105), (35, 15, 10, 5))
            # Глаза (красные)
            pygame.draw.rect(surface, (255, 0, 0), (10, 10, 6, 6))
            pygame.draw.rect(surface, (255, 0, 0), (24, 10, 6, 6))

        elif name == 'bee':
            # Пчела
            surface.fill((255, 215, 0))  # Желтый
            # Черные полосы
            pygame.draw.rect(surface, (0, 0, 0), (0, 0, 40, 5))
            pygame.draw.rect(surface, (0, 0, 0), (0, 15, 40, 5))
            pygame.draw.rect(surface, (0, 0, 0), (0, 30, 40, 5))
            # Глаза
            pygame.draw.rect(surface, (0, 0, 255), (10, 10, 6, 6))
            pygame.draw.rect(surface, (0, 0, 255), (24, 10, 6, 6))

        elif name == 'fatcat':
            # Котомрыск
            surface.fill(color)
            # Живот (светлее)
            pygame.draw.rect(surface, (255, 140, 0), (10, 20, 40, 30))
            # Глаза (желтые)
            pygame.draw.rect(surface, (255, 255, 0), (15, 15, 8, 8))
            pygame.draw.rect(surface, (255, 255, 0), (37, 15, 8, 8))
            # Зрачки (вертикальные)
            pygame.draw.rect(surface, (0, 0, 0), (17, 16, 4, 6))
            pygame.draw.rect(surface, (0, 0, 0), (39, 16, 4, 6))
            # Усы
            for i in range(3):
                pygame.draw.line(surface, (255, 255, 255),
                               (5, 25 + i*5), (15, 25 + i*5), 1)
                pygame.draw.line(surface, (255, 255, 255),
                               (55, 25 + i*5), (45, 25 + i*5), 1)

        else:
            # Простой fallback
            surface.fill(color)
            pygame.draw.rect(surface, (255, 255, 255), (10, 10, 8, 8))
            pygame.draw.rect(surface, (255, 255, 255), (22, 10, 8, 8))
            pygame.draw.rect(surface, (0, 0, 0), (12, 12, 4, 4))
            pygame.draw.rect(surface, (0, 0, 0), (24, 12, 4, 4))

        self.sprites[name] = surface

    def create_all_fallback_sprites(self):
        """Создание всех fallback спрайтов"""
        for name in ['chip', 'dale', 'rat', 'bee', 'fatcat']:
            self.create_fallback_sprite(name)

    def get_sprite(self, name):
        """Получение спрайта по имени"""
        return self.sprites.get(name)

    def get_flipped_sprite(self, name, flip_x=False, flip_y=False):
        """Получение отраженного спрайта"""
        sprite = self.get_sprite(name)
        if sprite:
            return pygame.transform.flip(sprite, flip_x, flip_y)
        return None

# Глобальный экземпляр менеджера спрайтов
sprite_manager = SpriteManager()