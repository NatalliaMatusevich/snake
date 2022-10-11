import pygame
import random
import time
from os import path


img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIGHT = 600
HEIGHT = 600
FPS = 5

BLOCK = 30

BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
YELLOY = (250, 255, 0)
MAROON = (255, 52, 179)
GREEN = (0, 238, 118)

x_snake = WIGHT / 2
y_snake = HEIGHT / 2
snake = [(x_snake, y_snake)]
len_snake = 1
apple = random.randrange(BLOCK, WIGHT - BLOCK, BLOCK), random.randrange(BLOCK, WIGHT - BLOCK, BLOCK)


x_change = 0
y_change = 0

vol = 0.0
score = 0

direction = 'RIGHT'
change_to = direction

pygame.mixer.pre_init(44100, -16, 1, 512)

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load(path.join(snd_dir, 'fon.mp3'))

pygame.mixer.music.play(-1)
s_eat = pygame.mixer.Sound(path.join(snd_dir, 'eat.wav'))
s_crash = pygame.mixer.Sound(path.join(snd_dir, 'crash.wav'))

screen = pygame.display.set_mode((WIGHT, HEIGHT))
pygame.display.set_caption('Змейка')
background = pygame.image.load(path.join(img_dir, 'background.png')).convert()
background_rect = background.get_rect()

clock = pygame.time.Clock()

font_score = pygame.font.SysFont('comicsansms', 20)

font_style = pygame.font.SysFont('comicsansms', 60)
def message_1(msg,color):
    '''Visualizes the message on the screen'''
    msg = font_style.render(msg, True, color)
    screen.blit(msg, [WIGHT / 6, HEIGHT / 7.5])

font_style_2 = pygame.font.SysFont('comicsansms', 80)
def message_2(msg,color):
    '''Visualizes the message on the screen
    :param msg: the message that needs to be visualized
    :type msg: pygame.Surface
    :param color: message color
    :type color: tuple

    :return: Visualizes the message on the screen
    '''
    msg = font_style_2.render(msg, True, color)
    screen.blit(msg, [WIGHT / 6, HEIGHT / 3])

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("Game over")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                vol += 0.1
                pygame.mixer.music.set_volume(vol)
                print(pygame.mixer.music.get_volume())
            elif event.key == pygame.K_F2:
                vol -= 0.1
                pygame.mixer.music.set_volume(vol)
                print(pygame.mixer.music.get_volume())

            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'

            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'

            # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
            y_change = - BLOCK
            x_change = 0
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
            y_change = BLOCK
            x_change = 0
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
            x_change = - BLOCK
            y_change = 0
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
            x_change = BLOCK
            y_change = 0

    if x_snake >= WIGHT or x_snake < 0 or y_snake >= HEIGHT or y_snake < 0 or len(snake) != len(set(snake)):
        s_crash.play()
        running = False

    x_snake += x_change
    y_snake += y_change
    snake.append((x_snake, y_snake))
    snake = snake[- len_snake:]

    if snake[-1] == apple:
        apple = random.randrange(BLOCK, WIGHT - BLOCK, BLOCK), random.randrange(BLOCK, WIGHT - BLOCK, BLOCK)
        len_snake += 1
        score += 1
        FPS += 1
        s_eat.play()


    screen.fill(BLACK)
    screen.blit(background, background_rect)

    [pygame.draw.rect(screen, GREEN, (i, j, BLOCK - 1, BLOCK - 1)) for i, j in snake]
    pygame.draw.rect(screen, RED, [*apple, BLOCK, BLOCK])

    render_score = font_score.render(f'Съеденые яблоки: {score}', 1, MAROON)
    screen.blit(render_score, (5, 5))

    pygame.display.flip()
    clock.tick(FPS)

message_1("Вы проиграли", RED)
message_2("¯\_(ツ)_/¯", YELLOY)

pygame.display.update()
time.sleep(2)
pygame.quit()