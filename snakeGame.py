# game imports
import pygame, sys, random, time

check_errors = pygame.init()
if check_errors[1] > 0:
    print(f"pygame has {check_errors[1]} initialization errors, exiting...")
    sys.exit(-1)
else:
    print("pygame successfully initialized")

# Play surface
playSurface = pygame.display.set_mode((720, 460))
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
snakePos = [100, 50]  # [0,0] is in the top left corner
snakeBody = [snakePos, [snakePos[0] - 10, snakePos[1]], [snakePos[0] - 20, snakePos[1]]]
foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
direction = 'RIGHT'  # current moving direction
score = 0


# Game Over function
def gameOver():
    GOFont = pygame.font.SysFont('monaco', 72)
    GOSurface = GOFont.render('Game Over!', True, red)
    GORectangle = GOSurface.get_rect()
    GORectangle.midtop = (360, 20)
    playSurface.blit(GOSurface, GORectangle)
    pygame.draw.rect(playSurface, red, pygame.Rect(snakeBody[0][0], snakeBody[0][1], 10, 10))
    showScore(False)
    pygame.display.flip()  # update playSurface, can use .update() as well
    time.sleep(3)
    pygame.quit()  # pygame exit
    sys.exit()  # console exit


# Show Score function
def showScore(live=True):
    if live:
        score_font = pygame.font.SysFont('monaco', 26)
        score_surface = score_font.render(f"Score: {score}", True, black)
        score_rectangle = score_surface.get_rect()
        score_rectangle.midtop = (80, 10)
    else:  # showScore() should be called after gameOver()
        score_font = pygame.font.SysFont('monaco', 34)
        score_surface = score_font.render(f"Score: {score}", True, black)
        score_rectangle = score_surface.get_rect()
        score_rectangle.midtop = (360, 120)
    playSurface.blit(score_surface, score_rectangle)  # pygame.display.flip() is not needed, as it's in the main code


# Game Main Logic
while True:
    # Snake Body Mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos == foodPos:
        score += 10
        while foodPos in snakeBody:
            foodPos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
    else:
        snakeBody.pop()

    # Drawing
    playSurface.fill(white)
    for pos in snakeBody:
        pygame.draw.rect(playSurface, black, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(playSurface, green, pygame.Rect(foodPos[0], foodPos[1], 10, 10))

    # Update Snake Position [x,y]
    if direction == 'RIGHT':
        snakePos[0] += 10
    elif direction == 'LEFT':
        snakePos[0] -= 10
    elif direction == 'UP':
        snakePos[1] -= 10
    elif direction == 'DOWN':
        snakePos[1] += 10

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
    if snakePos[0] < 0 or snakePos[0] >= 720 or snakePos[1] < 0 or snakePos[1] >= 460:
        gameOver()

    for block in snakeBody:
        if snakeBody.count(block) > 1:
            gameOver()

    # Common Stuff
    showScore()
    fpsController.tick(22)
    pygame.display.flip()

    # Further Updates
    # Add Sound to Game Over
    # Update Game icon
    # Add Menu for restart and other options
    # Add Game Level by configuring fpsController
    # Create executable file using cmd -> pyinstaller --onefile <file_name>.py
