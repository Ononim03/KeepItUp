from random import randint

import pygame

from constant import WHITE, NOMOSS, MOSS
from load_image import load_image


class Ball(pygame.sprite.Sprite):

    image = {'<Football>': load_image('ball/ball.png'),
             '<Юля>': load_image('ball/yulya.png')}

    def __init__(self, pos: tuple, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.size = 160
        self.sound = True
        self.image = pygame.transform.scale(Ball.image['<Football>'], (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.set_coordinates(pos)
        self.v = [0, 0]
        self.multiplier = 0
        self.is_knock = 0
        self.side = 0

    def update(self, *args):
        self.rect.x += self.v[0]
        self.rect.y += self.v[1]
        self.v[1] += 1
        if self.rect.x >= 500 - self.size or self.rect.x <= 0:
            if self.sound:
                NOMOSS.play()
            self.multiplier = 0
            self.v[0] *= -1
            if self.rect.x >= 500 - self.size:
                self.rect.x -= 10
                self.side = 'right'
            else:
                self.rect.x += 10
                self.side = 'left'
            self.is_knock = 15
        self.is_knock -= 1
        self.is_knock = max(0, self.is_knock)

    def set_speed(self, speed: list):
        if self.sound:
            MOSS.play()
        self.v = speed
        self.multiplier += 1

    def set_coordinates(self, coords):
        self.rect.x = coords[0] + randint(-2, 2)
        self.rect.y = coords[1] + randint(-2, 2)

    def change_image(self, text):
        self.image = pygame.transform.scale(Ball.image[text], (self.size, self.size))

    def turn_sound(self, text):
        self.sound = True if text == '<On>' else False
