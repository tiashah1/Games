import pygame

pygame.init()

# Set up the window
wn = pygame.display.set_mode((750, 500))
pygame.display.set_caption("Tennis Game")


# Paddle
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 75])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.points = 0



# Ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10])
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.speed = 5
        self.dx = 1
        self.dy = 1

# First paddle, on the left of the screen
paddle1 = Paddle()
paddle1.rect.x = 25
paddle1.rect.y = 250
paddle1.image.fill((0, 240, 240))

# Second paddle, on the right of the screen
paddle2 = Paddle()
paddle2.rect.x = 715
paddle2.rect.y = 250
paddle2.image.fill((102, 204, 0))

# The ball, this is currently in the middle of the screen
ball = Ball()
ball.rect.x = 375
ball.rect.y = 250

# Adding the sprites to a list
sprites = pygame.sprite.Group()
sprites.add(paddle1, paddle2, ball)

# Drawing the sprites onto the window
def drawing():
    wn.fill((0, 0, 0))
    # Title
    font = pygame.font.SysFont("Arial", 30)
    text = font.render("Tennis", False, (255, 255, 255))
    textR = text.get_rect()
    textR.center = (750//2, 25)
    wn.blit(text, textR)

    # Player 1 score
    p1 = font.render(str(paddle1.points), False, (0, 240, 240))
    p1R = p1.get_rect()
    p1R.center = (50, 50)
    wn.blit(p1, p1R)

    # Player 2 score
    p2 = font.render(str(paddle2.points), False, (102, 204, 0))
    p2R = p2.get_rect()
    p2R.center = (700, 50)
    wn.blit(p2, p2R)

    sprites.draw(wn)
    pygame.display.update()


# MAIN GAME LOOP
running = True
while running:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Moving the paddles using keyboard 
    key = pygame.key.get_pressed()
    # Left paddle
    if key[pygame.K_w]:
        if paddle1.rect.y > 10:
            paddle1.rect.y += -10
    if key[pygame.K_s]:
        if paddle1.rect.y < 410:
            paddle1.rect.y += 10
    # Right paddle
    if key[pygame.K_UP]:
        if paddle2.rect.y > 10:
            paddle2.rect.y += -10
    if key[pygame.K_DOWN]:
        if paddle2.rect.y < 410:
            paddle2.rect.y += 10
    
    ball.rect.x += ball.speed * ball.dx
    ball.rect.y += ball.speed * ball.dy

    if ball.rect.y > 490:
        ball.dy = -1
    if ball.rect.y < 10:
        ball.dy = 1
    if ball.rect.x > 740:
        ball.rect.x, ball.rect.y = 375, 250
        ball.dx = -1
        paddle1.points += 1
    if ball.rect.x < 10:
        ball.rect.x, ball.rect.y = 375, 250
        ball.dx = 1
        paddle2.points += 1
    
    if paddle1.rect.colliderect(ball.rect):
        ball.dx = 1
    if paddle2.rect.colliderect(ball.rect):
        ball.dx = -1 

    drawing()

pygame.quit()