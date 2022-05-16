# game imports
import pygame, sys, random, time

check_errors = pygame.init()
if check_errors[1] > 0:
    print(f"pygame has {check_errors[1]} initialization errors, exiting...")
    sys.exit(-1)
else:
    print("pygame successfully initialized")

# Play surface
play_surface = pygame.display.set_mode((720, 460))
pygame.display.set_caption("Snake Game!")

# Colors
red = pygame.Color(255, 0, 0)  # game over
green = pygame.Color(0, 255, 0)  # snake
black = pygame.Color(0, 0, 0)  # score
white = pygame.Color(255, 255, 255)  # background
brown = pygame.Color(165, 42, 42)  # food

# FPS controller
fpsController = pygame.time.Clock()

# Important variables
snake_pos = [100, 50]  # [0,0] is in the top left corner
snake_body = [snake_pos, [snake_pos[0] - 10, snake_pos[1]], [snake_pos[0] - 20, snake_pos[1]]]  # values will be updated
food_pos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
direction = 'RIGHT'  # default moving direction
score = 0


# Game Over function
def game_over():
    game_over_font = pygame.font.SysFont('monaco', 72)
    game_over_surface = game_over_font.render('Game Over!', True, red)
    game_over_rectangle = game_over_surface.get_rect()
    game_over_rectangle.midtop = (360, 20)
    play_surface.blit(game_over_surface, game_over_rectangle)
    pygame.draw.rect(play_surface, red, pygame.Rect(snake_body[0][0], snake_body[0][1], 10, 10))
    show_score(False)
    pygame.display.flip()  # update play_surface, can use .update() as well
    time.sleep(3)
    pygame.quit()  # pygame exit
    sys.exit()  # console exit


# Show Score function
def show_score(live=True):
    if live:
        score_font = pygame.font.SysFont('monaco', 26)
        score_surface = score_font.render(f"Score: {score}", True, black)
        score_rectangle = score_surface.get_rect()
        score_rectangle.midtop = (80, 10)
    else:  # show_score() should be called after game_over()
        score_font = pygame.font.SysFont('monaco', 34)
        score_surface = score_font.render(f"Score: {score}", True, black)
        score_rectangle = score_surface.get_rect()
        score_rectangle.midtop = (360, 120)
    play_surface.blit(score_surface, score_rectangle)  # pygame.display.flip() is not needed, as it's in the main code


# Game Main Logic
while True:
    # Snake Body Mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 10
        while food_pos in snake_body:
            food_pos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
    else:
        snake_body.pop()

    # Drawing
    play_surface.fill(white)
    for pos in snake_body:
        pygame.draw.rect(play_surface, black, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(play_surface, green, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Update Snake Position [x,y]
    if direction == 'RIGHT':
        snake_pos[0] += 10
    elif direction == 'LEFT':
        snake_pos[0] -= 10
    elif direction == 'UP':
        snake_pos[1] -= 10
    elif direction == 'DOWN':
        snake_pos[1] += 10

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT or event.key == ord('d')) and not direction == 'LEFT':  # using ASCII value
                direction = 'RIGHT'
            elif (event.key == pygame.K_LEFT or event.key == ord('a')) and not direction == 'RIGHT':
                direction = 'LEFT'
            elif (event.key == pygame.K_UP or event.key == ord('w')) and not direction == 'DOWN':
                direction = 'UP'
            elif (event.key == pygame.K_DOWN or event.key == ord('s')) and not direction == 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))  # create QUIT event

    # Game Over Conditions
    if snake_pos[0] < 0 or snake_pos[0] >= 720 or snake_pos[1] < 0 or snake_pos[1] >= 460:
        game_over()

    for block in snake_body:
        if snake_body.count(block) > 1:
            game_over()

    # Common Stuff
    show_score()
    fpsController.tick(22)
    pygame.display.flip()

    # Further Updates
    # Add Sound to Game Over
    # Update Game icon
    # Add Menu for restart and other options
    # Add Game Level by configuring fpsController
    # Create executable file using cmd -> pyinstaller --onefile <file_name>.py
