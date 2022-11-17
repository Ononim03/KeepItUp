# Import the pygame library and initialise the game engine
import random

import pygame
import os


from ChooseButton import ChooseButton
from constant import MOSS
from load_image import load_image


def progress_bar(percent, color_current, color_bg, screen, is_red=False):
    len_ = 200
    if is_red:
        pygame.draw.rect(screen, (255, 0, 0),
                         pygame.Rect((WIDTH - len_) // 2, 107, len_, 15))
    else:
        pygame.draw.rect(screen, color_current, pygame.Rect((WIDTH - len_) // 2, 107, len_ * percent // 100, 15))
        pygame.draw.rect(screen, color_bg,
                         pygame.Rect((WIDTH - len_) // 2 + len_ * percent // 100, 107, len_ * (100 - percent) // 100,
                                     15))
    pygame.draw.rect(screen, (0, 0, 0),
                     pygame.Rect((WIDTH - len_) // 2, 107, len_, 15),
                     2)


pygame.init()
# Open a new window
WIDTH = 500
HEIGHT = 1000
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

arturik = load_image('bg/arturik.png')
arturik_screen = pygame.transform.scale(load_image('bg/arturik.png'), (WIDTH, HEIGHT))

white_screen = pygame.Surface((WIDTH, HEIGHT))
pygame.draw.rect(white_screen, 'white', (0, 0, WIDTH, HEIGHT))

moss_screen = pygame.transform.scale(load_image('bg/moss.png'), (WIDTH, HEIGHT))
dead_screen = pygame.transform.scale(load_image('bg/dead.png'), (WIDTH, HEIGHT))
gays_screen = pygame.transform.scale(load_image('bg/gays.png'), (WIDTH, HEIGHT))
god_screen = pygame.transform.scale(load_image('bg/god.png'), (WIDTH, HEIGHT))
sermoss_screen = pygame.transform.scale(load_image('bg/sermoss.png'), (WIDTH, HEIGHT))

pygame.display.set_icon(arturik)
pygame.display.set_caption("Keep it up")
from ball import Ball

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def score_value(multiplier):
    if multiplier < 3:
        return 1
    if multiplier < 3 + 5:
        return 2
    if multiplier < 3 + 5 + 5:
        return 4
    if multiplier < 3 + 5 + 5 + 10:
        return 8
    if multiplier < 3 + 5 + 5 + 10 + 20:
        return 16
    return 32


def get_percent(multiplier):
    if multiplier < 3:
        return multiplier * 100 // 3, 'yellow', 'white'
    if multiplier < 3 + 5:
        return (multiplier - 3) * 100 // 5, 'orange', 'yellow'
    if multiplier < 3 + 5 + 5:
        return (multiplier - 8) * 100 // 5, 'red', 'orange'
    if multiplier < 3 + 5 + 5 + 10:
        return (multiplier - 13) * 100 // 10, 'purple', 'red'
    if multiplier < 3 + 5 + 5 + 10 + 20:
        return (multiplier - 23) * 100 // 20, 'black', 'purple'
    return 100, 'black', 'black'


def barrier(reverse):
    transformation_surface = pygame.Surface((10, HEIGHT), pygame.SRCALPHA)
    for i in range(1, 11):
        if not reverse:
            x = 11 - i
        else:
            x = i
        pygame.draw.rect(transformation_surface, (255, 0, 0, x * 25),
                         (i - 1, 0, 1, HEIGHT))
    return transformation_surface


# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
start_x, start_y = 190, 800
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
left = barrier(reverse=False)
right = barrier(reverse=True)
ball = Ball((start_x, start_y), all_sprites)
font = pygame.font.Font(os.path.abspath('data/font.ttf'), 32)
settings_sprites = pygame.sprite.Group()
sounds_button = ChooseButton('Sound', (WIDTH // 2, HEIGHT // 2 - 70), settings_sprites,
                             args=['<On>', '<Off>'])
ball_button = ChooseButton('Ball', (WIDTH // 2, HEIGHT // 2), settings_sprites,
                           args=['<Football>', '<Юля>'])
bg_button = ChooseButton('Bg', (WIDTH // 2, HEIGHT // 2 + 70), settings_sprites,
                         args=['<White>', '<Артур>', '<Мох>', '<Dead>', '<Gays>', '<God>', '<Sermoss>'])
bg = {
    '<White>': white_screen,
    '<Артур>': arturik_screen,
    '<Мох>': moss_screen,
    '<Dead>': dead_screen,
    '<Gays>': gays_screen,
    '<God>': god_screen,
    '<Sermoss>': sermoss_screen
}
score = 0
max_score = int(open('data/max_score.txt', 'r').read())
is_start = False
is_bot = False
bottom_y = random.randint(500, 900)
while carryOn:
    for event in pygame.event.get():
        if not is_start:
            settings_sprites.update(event)
        if event.type == pygame.QUIT:
            with open('data/max_score.txt', 'w') as f:
                f.write(str(max_score))
            carryOn = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
            if is_bot:
                ball.set_coordinates((start_x, start_y))
            is_bot = not is_bot
            is_start = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and (event.pos[0] - ball.rect.x - ball.size // 2) ** 2 + (
                    event.pos[1] - ball.rect.y - ball.size // 2) ** 2 <= 100 ** 2 and not is_bot:
                is_start = True
                is_bot = False
                dx = event.pos[0] - ball.rect.x - ball.size // 2
                if abs(dx) // 5 == 0 and dx < 0:
                    ball.set_speed([-2, -25])
                elif dx // 5 == 0 and dx >= 0:
                    ball.set_speed([2, -25])
                else:
                    ball.set_speed([-dx // 5, -25])
                score += score_value(ball.multiplier)

    if ball.rect.y >= 1000:
        if score >= max_score:
            max_score = score
        is_start = False
        ball.is_knock = 0
        progress_bar(*get_percent(ball.multiplier), screen, True if ball.is_knock else False)
        pygame.display.flip()
        score = 0
        ball.multiplier = 0
        ball.set_coordinates([start_x, start_y])

    if is_bot:
        score = 0
        ball.multiplier = 0
        if ball.rect.y >= bottom_y:
            MOSS.play()
            bottom_y = random.randint(500, 800)
            ball.set_speed([random.randint(-5, 5), -25])
        all_sprites.update()

    if is_start:
        all_sprites.update()

    ball.change_image(ball_button.get_text())
    ball.turn_sound(sounds_button.get_text())

    screen.fill(WHITE)
    screen.blit(bg[bg_button.get_text()], (0, 0))
    progress_bar(*get_percent(ball.multiplier), screen, True if ball.is_knock else False)
    all_sprites.draw(screen)
    if not is_start:
        settings_sprites.draw(screen)

    text = font.render(f'Max Score: {max_score}', True, (33, 33, 33))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 0 + text.get_height() // 2))
    text = font.render(f'x{score_value(ball.multiplier)}', True, (33, 33, 33))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50 + text.get_height() // 2))
    text = font.render(f'{score}', True, (33, 33, 33))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100 + text.get_height() // 2))

    if ball.is_knock:
        if ball.side == 'left':
            screen.blit(left, (0, 0))
        else:
            screen.blit(right, (WIDTH - 10, 0))

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
