import pygame as py
from random import randrange

py.init()

size = SCREEN_WIDTH, SCREEN_HEIGHT = 720, 720
GRID_SIZE = 40
snakeSpeed = GRID_SIZE  
text_font = py.font.SysFont('Arial', 50)

white = (255, 255, 255)
lightGreen = (144, 238, 144)
blue = (100, 149, 237)
red = (255, 0, 0)

screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
py.display.set_caption('Jogo da Cobra')

startingX, startingY = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
snakeBody = [py.Rect(startingX, startingY, GRID_SIZE, GRID_SIZE)]

fruitX, fruitY = randrange(0, SCREEN_WIDTH, GRID_SIZE), randrange(0, SCREEN_HEIGHT, GRID_SIZE)
fruit = py.Rect(fruitX, fruitY, GRID_SIZE, GRID_SIZE)

def main():
    global snakeBody, direction, fruit
    running = True
    gameOver = False
    direction = (1, 0)
    clock = py.time.Clock()

    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

        if not gameOver:
            keys = py.key.get_pressed()
            if keys[py.K_UP] and direction != (0, 1):
                direction = (0, -1)
            if keys[py.K_DOWN] and direction != (0, -1):
                direction = (0, 1)
            if keys[py.K_RIGHT] and direction != (-1, 0):
                direction = (1, 0)
            if keys[py.K_LEFT] and direction != (1, 0):
                direction = (-1, 0)

            newHead = py.Rect(snakeBody[0].x + direction[0] * snakeSpeed,
                              snakeBody[0].y + direction[1] * snakeSpeed, 
                              GRID_SIZE, GRID_SIZE)

            newHead.x = max(0, min(SCREEN_WIDTH - GRID_SIZE, newHead.x))
            newHead.y = max(0, min(SCREEN_HEIGHT - GRID_SIZE, newHead.y))

            snakeBody.insert(0, newHead)

            if snakeBody[0].colliderect(fruit):
                fruitX, fruitY = randrange(0, SCREEN_WIDTH, GRID_SIZE), randrange(0, SCREEN_HEIGHT, GRID_SIZE)
                fruit = py.Rect(fruitX, fruitY, GRID_SIZE, GRID_SIZE)
            else:
                snakeBody.pop()

            if (snakeBody[0].left < 0 or snakeBody[0].right > SCREEN_WIDTH or
                snakeBody[0].top < 0 or snakeBody[0].bottom > SCREEN_HEIGHT or
                any(segment.colliderect(snakeBody[0]) for segment in snakeBody[1:])):
                gameOver = True

        screen.fill(lightGreen)
        drawGrid()
        for segment in snakeBody:
            py.draw.rect(screen, blue, segment)
        py.draw.rect(screen, red, fruit)

        if gameOver:
            drawText('Game Over', text_font, (0, 0, 0), SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25)

        py.display.update()
        clock.tick(10)

def drawGrid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            grid = py.Rect(x, y, GRID_SIZE, GRID_SIZE)
            py.draw.rect(screen, white, grid, 1)

def drawText(text, font, text_col, x, y):
    text_surface = font.render(text, True, text_col)
    screen.blit(text_surface, (x, y))

main()
py.quit()
