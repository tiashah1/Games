import pygame as pg

# Screen size and colours 
WIDTH = 550
background_colour = (38, 38, 38)
grid_colour = (255, 255, 255)
highlight_colour = (255, 0, 0)

# The grid that the user will fill in
grid = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1], 
    [6, 8, 0, 0, 7, 0, 0, 9, 0], 
    [1, 9, 0, 0, 0, 4, 5, 0, 0], 
    [8, 2, 0, 1, 0, 0, 0, 4, 0], 
    [0, 0, 4, 6, 0, 2, 9, 0, 0], 
    [0, 5, 0, 0, 0, 3, 0, 2, 8], 
    [0, 0, 9, 3, 0, 0, 0, 7, 4], 
    [0, 4, 0, 0, 5, 0, 0, 3, 6], 
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]

# Finished grid
answer = [
    [4, 3, 5, 2, 6, 9, 7, 8, 1], 
    [6, 8, 2, 5, 7, 1, 4, 9, 3], 
    [1, 9, 7, 8, 3, 4, 5, 6, 2], 
    [8, 2, 6, 1, 9, 5, 3, 4, 7], 
    [3, 7, 4, 6, 8, 2, 9, 1, 5], 
    [9, 5, 1, 7, 4, 3, 6, 2, 8], 
    [5, 1, 9, 3, 2, 6, 8, 7, 4], 
    [2, 4, 8, 9, 5, 7, 1, 3, 6], 
    [7, 6, 3, 4, 1, 8, 2, 5, 9]
]

# Draws the grid lines 
def drawGrid(screen):
    myFont = pg.font.SysFont("comicsans", 35)
    for i in range (0, 10):
        if (i % 3 == 0):
            # Thicker around the small squares 
            pg.draw.line(screen, grid_colour, (50 + 50*i, 50), (50 + 50*i, 500), 5)
            pg.draw.line(screen, grid_colour, (50, 50+ 50*i), (500, 50 + 50*i), 5)
        else:
            # Thinner between each individual box
            pg.draw.line(screen, grid_colour, (50 + 50*i, 50), (50 + 50*i, 500), 1)
            pg.draw.line(screen, grid_colour, (50, 50+ 50*i), (500, 50 + 50*i), 1)
    pg.display.update()


def addNumbers(screen):
    myFont = pg.font.SysFont("comicsans", 35)
    # If there is a non-0 number this is entered into the grid
    for i in range(len(grid[0])):
        for j in range (len(grid[1])):
            if (grid[i][j] != 0):
                value = myFont.render(str(grid[i][j]), True, grid_colour)
            else:
                # If there is a 0, it will print nothing
                value = myFont.render(str(""), True, grid_colour)
            screen.blit(value, ((j+1)*50 + 15, (i+1)*50))
    pg.display.update()


def InputNum(x, y, screen):
    # Draw a box around the highlighted cell
    draw_box(x, y, screen)
    myFont = pg.font.SysFont("comicsans", 35)
    num = int(input("Enter a number: "))

    screen.fill([0,0,0])
    drawGrid(screen)
    addNumbers(screen)
    
    # If the user clicks on a valid position and the input is correct
    if (int(grid[y-1][x-1]) == 0 and num < 10 and num > 0):
        if (num == answer[y-1][x-1]):
            # Update the unfinished grid to include this input
            grid[y-1][x-1] = num
            for i in range(len(grid[0])):
                for j in range (len(grid[1])):
                    if (i == y-1 and j == x-1):
                        # Display the new integer in the correct position
                        value = myFont.render(str(answer[i][j]), True, grid_colour)
                    else:
                        # Display nothing on the grid position
                        value = myFont.render(str(""), True, grid_colour)
                    screen.blit(value, ((j+1)*50 + 15, (i+1)*50))
            pg.display.update()
        else:
            # Inform user that their guess is wrong
            print("Incorrect guess, try again")

# Drawing a box around the selected cell
def draw_box(x, y, screen):
    for i in range(2):
        # A thicker red square is drawn to highlight 
        pg.draw.line(screen, (255, 0, 0), (x * 50-3, (y + i)*50), (x * 50 + 50 + 3, (y + i)*50), 5)
        pg.draw.line(screen, (255, 0, 0), ( (x + i)* 50, y * 50 ), ((x + i) * 50, y * 50 + 50), 5) 
    pg.display.update()

# Main game loop
def main():
    # initialise pygame and set up the screen 
    pg.init()
    wn = pg.display.set_mode((WIDTH,WIDTH))
    wn.fill(background_colour)
    drawGrid(wn)
    addNumbers(wn)
    
    print("Welcome to the sudoku game, click on a cell and input a number \n")

    while True:
        for event in pg.event.get():
            # Allows the game to close when the user quits the game
            if event.type == pg.QUIT:
                pg.quit()

            # Use the mouse event handler to get the position
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                # Get x and y coordinates of the selected cell
                posX, posY = pg.mouse.get_pos()
                # Convert this to correspond to the cell chosen
                cellX = posX // 50
                cellY = posY // 50            
            
                InputNum(cellX, cellY, wn)
main()