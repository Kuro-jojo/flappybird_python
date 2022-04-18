import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_position, 700))
    screen.blit(floor_surface, (576+floor_x_position, 700))


def create_pipe():
    random_pipe_position = random.choice(pipe_heights)
    return (pipe_surface.get_rect(midtop=(700, random_pipe_position)),
            pipe_surface.get_rect(midbottom=(700, random_pipe_position - 200)))


def move_pipes():
    for pipe in pipe_list:
        pipe.centerx -= 5

    return [pipe for pipe in pipe_list if pipe.right > -50]


def draw_pipes():
    for pipe in pipe_list:
        # pipe is out of the screen
        if pipe.bottom >= 800:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe_surface = pygame.transform.flip(
                pipe_surface, False, True)
            screen.blit(flip_pipe_surface, pipe)


def check_collision():  # sourcery skip: extract-duplicate-method, use-next
    global can_score

    if bird_rect.top <= -10 or bird_rect.bottom >= 700:
        death_sound.play()
        can_score = True
        return False

    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
    return True


def rotate_bird():
    return pygame.transform.rotozoom(bird_surface, -bird_movement * 3, 1)


def bird_animation():
    new_bird = bird_frames[bird_frame_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))

    return new_bird, new_bird_rect


def display_score(game_state=None):
    _score(score, "Score", 90)
    if game_state == 'game_over':
        _score(high_score, "High Score", 680)


def _score(score, text, position):
    score_surface = game_font.render(
        f"{text}: {int(score)}", True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(225, position))
    screen.blit(score_surface, score_rect)


def update_high_score(high_score):
    if score > high_score:
        high_score = score
    return high_score


def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if can_score and bird_rect.centerx - 5 < pipe.centerx < bird_rect.centerx + 5:
                score += 1
                can_score = False
                score_sound.play()
            if pipe.centerx < 0:
                can_score = True


def reinit():
    global score, bird_movement

    pipe_list.clear()
    bird_rect.center = (100, 400)
    score = 0
    bird_movement = 0


if __name__ == '__main__':

    # pygame.mixer.pre_init(frequency=44100, size=8, channels=1, buffer=512)
    pygame.init()
    pygame.display.set_caption("Flappy Bird")
    favicon_surface = pygame.image.load("favicon.ico")
    pygame.display.set_icon(favicon_surface)
    screen = pygame.display.set_mode((450, 780))
    # implement the frame rate limitation
    clock = pygame.time.Clock()
    # create a font
    game_font = pygame.font.Font('04B_19.ttf', 35)

    # Game variables
    gravity = 0.15
    bird_movement = 0
    game_active = True
    score = 0
    high_score = 0
    can_score = True
    game_started = False

    # convert the image into a file format that is much easier for pygame to run
    bg_surface = pygame.image.load('assets/background-day.png').convert_alpha()
    bg_surface = pygame.transform.scale2x(bg_surface)

    floor_surface = pygame.image.load('assets/base.png').convert_alpha()
    floor_surface = pygame.transform.scale2x(floor_surface)
    floor_x_position = 0

    bird_downflap_surface = pygame.transform.scale2x(
        pygame.image.load('assets/bluebird-downflap.png')).convert_alpha()
    bird_midflap_surface = pygame.transform.scale2x(
        pygame.image.load('assets/bluebird-midflap.png')).convert_alpha()
    bird_upflap_surface = pygame.transform.scale2x(
        pygame.image.load('assets/bluebird-upflap.png')).convert_alpha()

    bird_frames = [bird_downflap_surface,
                   bird_midflap_surface, bird_upflap_surface]
    bird_frame_index = 2

    bird_surface = bird_frames[bird_frame_index]
    bird_rect = bird_surface.get_rect(center=(100, 400))

    BIRD_FLAP = pygame.USEREVENT + 1
    pygame.time.set_timer(BIRD_FLAP, 200)

    # bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
    # bird_surface = pygame.transform.scale2x(bird_surface)
    # # put a rectangle around the bird surface (where to place the rectangle)
    # bird_rect = bird_surface.get_rect(center=(100, 400))

    pipe_surface = pygame.image.load('assets/pipe-green.png').convert_alpha()
    pipe_surface = pygame.transform.scale2x(pipe_surface)
    pipe_list = []
    SPAWN_PIPE = pygame.USEREVENT  # this event is triggered by a timer
    pygame.time.set_timer(SPAWN_PIPE, 1200)
    pipe_heights = [300, 400, 500, 600]

    # Game Over
    game_over_surface = pygame.transform.scale2x(
        pygame.image.load('assets/message.png').convert_alpha())
    game_over_rect = game_over_surface.get_rect(center=(225, 385))

    # Sounds
    flap_sound = pygame.mixer.Sound('sound/wing.wav')
    death_sound = pygame.mixer.Sound('sound/hit.wav')
    score_sound = pygame.mixer.Sound('sound/point.wav')

    while True:
        # event loop
        for event in pygame.event.get():
            if not game_started:
                game_active = False
                game_started = True
                screen.blit(game_over_surface,game_over_rect)

            if event.type == pygame.QUIT:
                pygame.quit()
                # ensure that we shut down the game properly
                sys.exit()
                
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                if game_active:
                    flap_sound.play()
                    # to prevent gravity
                    bird_movement = -6
                if not game_active:
                    game_active = True
                    reinit()

            if event.type == SPAWN_PIPE:
                pipe_list.extend(create_pipe())

            if event.type == BIRD_FLAP:
                if bird_frame_index < 2:
                    bird_frame_index += 1
                else:
                    bird_frame_index = 0
                bird_surface, bird_rect = bird_animation()

        # put one (regular) surface on another
        screen.blit(bg_surface, (0, 0))

        if game_active:
            # Bird moves
            bird_movement += gravity
            rotated_bird_surface = rotate_bird()
            # apply the movement
            bird_rect.centery += bird_movement
            screen.blit(rotated_bird_surface, bird_rect)
            game_active = check_collision()

            # Pipes
            pipe_list = move_pipes()
            draw_pipes()

            # Score
            pipe_score_check()
            display_score()

        else:
            screen.blit(game_over_surface, game_over_rect)
            high_score = update_high_score(high_score)
            display_score('game_over')

        # Floor
        floor_x_position -= 1
        draw_floor()
        if floor_x_position <= -576:
            floor_x_position = 0

        pygame.display.update()
        # the game can't run faster than 120 FPS
        clock.tick(120)
