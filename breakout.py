import pygame
from pygame.locals import *

#Initialise pygame
pygame.init()

#Define the game window and create the screen
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

#Font
font = pygame.font.SysFont("Constantia", 30)

#Defining the colours
background = (0, 0, 0)
redBrick = (255, 0, 0)
greenBrick = (0, 255, 0)
blueBrick = (0, 0, 255)
batColor = (255, 255, 255)
batOutline = (222,222,222)
textColor = (0, 255, 255)

#Game variables
rows = 6
columns = 6
clock = pygame.time.Clock()
fps = 60
ballMoving = False
gameOver = 0

#Function for outputting text onto the screen
def drawText(text, font, textColor, x, y):
    img = font.render(text, True, textColor)
    screen.blit(img, (x, y))
    
#Brick wall class
class wall():
    def __init__(self):
        self.width = screen_width // columns
        self.height = 50

    def createWall(self):
        self.bricks = []
        #define empty list for individual block
        brick = []
        for row in range(rows):
            #reset the block row list
            brick_row = []
            #iterate through each column
            for col in range(columns):
                #generate x and y positions for each brick
                brick_x = col * self.width
                brick_y = row * self.height
                #create a rectangle for each brick
                rectangle = pygame.Rect(brick_x, brick_y, self.width, self.height)

                #assign values to determine the colour of brick
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1

                #create a list to store rectangle and colour
                brick = [rectangle, strength]
                #append to block row
                brick_row.append(brick)

            #append row to full list of blocks
            self.bricks.append(brick_row)

    def drawWall(self):
        for row in self.bricks:
            for brick in row:
                #assign colour based on value
                if brick[1] == 3:
                    brick_col = blueBrick
                elif brick[1] == 2:
                    brick_col = greenBrick
                elif brick[1] == 1:
                    brick_col = redBrick
                #drawing each rectangle and also a border around each to seperate them
                pygame.draw.rect(screen, brick_col, brick[0])
                pygame.draw.rect(screen, background, (brick[0]), 2)

#Bat class
class bat():
    def __init__(self):
        self.reset()

    def move(self):
        #reset the direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        elif key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, batColor, self.rect)
        pygame.draw.rect(screen, batOutline, self.rect, 3)

    def reset(self):
        #paddle variables
        self.height = 20
        self.width = int(screen_width / columns)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

#Ball class
class ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def draw(self):
        pygame.draw.circle(screen, batColor, (self.rect.x + self.ballRadius, self.rect.y + self.ballRadius), self.ballRadius)
        pygame.draw.circle(screen, batOutline, (self.rect.x + self.ballRadius, self.rect.y + self.ballRadius), self.ballRadius, 3)

    def move(self):
        collisionThreshold = 5

        wallDestroyed = True
        rowCount = 0
        for row in wall.bricks:
            itemCount = 0
            for item in row:
                #check collisions
                if (self.rect.colliderect(item[0])):
                    #check if collision was from above
                    if abs(self.rect.bottom - item[0].top) < collisionThreshold and self.speedY > 0:
                        self.speedY *= -1
                    #check if collision was from bottom
                    if abs(self.rect.top - item[0].bottom) < collisionThreshold and self.speedY < 0:
                        self.speedY *= -1
                    #check if collision was from left
                    if abs(self.rect.right - item[0].left) < collisionThreshold and self.speedX > 0:
                        self.speedX *= -1
                    #check if collision was from right
                    if abs(self.rect.left - item[0].right) < collisionThreshold and self.speedX < 0:
                        self.speedX *= -1

                    #reduce the strength
                    if wall.bricks[rowCount][itemCount][1] > 1:
                        wall.bricks[rowCount][itemCount][1] -= 1
                    else:
                        wall.bricks[rowCount][itemCount][0] = (0, 0, 0, 0)

                if wall.bricks[rowCount][itemCount][0] != (0, 0, 0, 0):
                    wallDestroyed = False
                itemCount += 1
            rowCount += 1

    
        #check if the wall is destroyed
        if wallDestroyed == True:
            self.gameOver = 1


                    
        #check for collision with walls
        if (self.rect.left < 0 or self.rect.right > screen_width):
            self.speedX *= -1

        #check for collision with top and bottom of the screen
        if (self.rect.top < 0):
            self.speedY *= -1
        if (self.rect.bottom > screen_height):
            self.gameOver = -1

        #check for collision with paddle
        if (self.rect.colliderect(player_bat)):
            #check for collisions with top
            if abs(self.rect.bottom - player_bat.rect.top) < collisionThreshold and self.speedY > 0:
                self.speedY *= -1
                self.speedX += player_bat.direction
                if (self.speedX > self.speedMax):
                    self.speedX = self.speedMax
                elif(self.speedX < 0 and self.speedX < -self.speedMax):
                    self.speedX = -self.speedMax
            else:
                self.speedX *= -1
                

        
        self.rect.x += self.speedX
        self.rect.y += self.speedY

        return self.gameOver

    def reset(self, x, y):
        self.ballRadius = 10
        self.x = x - self.ballRadius
        self.y = y
        self.rect = Rect(self.x, self.y, self.ballRadius * 2, self.ballRadius * 2)
        self.speedX = 4
        self.speedY = -4
        self.speedMax = 5
        self.gameOver = 0



#create a wall
wall = wall()
wall.createWall()

#creating the bat
player_bat = bat()

#creating the ball
ball = ball(player_bat.x + (player_bat.width // 2), player_bat.y - player_bat.height)

#The Game Loop
playing = True
while playing:

    clock.tick(fps)
    
    #Display the background
    screen.fill(background)
    
    #draw the parts of the game
    wall.drawWall()
    player_bat.draw()
    ball.draw()

    if ballMoving:
        player_bat.move()
        gameOver = ball.move()
        if gameOver != 0:
            ballMoving = False

    #print player instructions
    if not ballMoving:
        if gameOver == 0:
            drawText("Click the screen to start", font, textColor, 145, screen_height // 2 + 100)
        elif gameOver == 1:
            drawText("You won!", font, textColor, 240, screen_height // 2 + 50)
            drawText("Click the screen to start", font, textColor, 145, screen_height // 2 + 100)
        elif gameOver == -1:
            drawText("You lose!", font, textColor, 240, screen_height // 2 + 50)
            drawText("Click the screen to start", font, textColor, 145, screen_height // 2 + 100)



    #allow the game to end when the user exits
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.MOUSEBUTTONDOWN and ballMoving == False:
            ballMoving = True
            ball.reset(player_bat.x + (player_bat.width // 2), player_bat.y - player_bat.height)
            player_bat.reset()
            wall.createWall()
            
    #update the screen so the user can see the changes made
    pygame.display.update()

#end game
pygame.quit()
