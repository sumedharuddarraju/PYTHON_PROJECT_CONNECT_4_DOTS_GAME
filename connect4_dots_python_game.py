import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255, 255, 255)

rows = 6
columns = 7

def game_grid():
    board = np.zeros((rows,columns))
    return board

def fill_piece(board, row, col, piece):
    board[row][col] = piece
          
def is_valid_location(board, col):
    return board[rows-1][col] == 0

def next_avaliable_row(board, col):
    for r in range(rows):
        if board[r][col] == 0:
            return r

def iseven(num):
    return num % 2 == 0

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for i in range(rows):
        for j in range(columns - 3):
            if board[i][j] == piece and board[i][j + 1] == piece and board[i][j + 2] == piece and board[i][j+3] == piece:
                return True

    # Check vertical locations for win
    for j in range(columns):
        for i in range(rows-3): 
            if board[i][j] == piece and board[i + 1][j] == piece and board[i + 2][j] == piece and board[i + 3][j] == piece:
                return True

    # Checking diagonally
    for j in range(columns-3):
        for i in range(rows-3):
            if board[i][j] == piece and board[i + 1][j + 1] == piece and board[i + 2][j + 2] == piece and board[i + 3][j + 3] == piece:
                return True

    for j in range(columns-3):
        for i in range(3,rows):
            if board[i][j] == piece and board[i - 1][j + 1] == piece and board[i - 2][j + 2] == piece and board[i - 3][j + 3] == piece:
                return True

#Draw condition         
def isboard_filled(board):
    count = 0
    for i in range(columns):
        if board[5][i] == 1 or board[5][i] == 2:
            count += 1
    return count == 7    

def game_board(board):
    for i in range(rows):
        for j in range(columns):
            pygame.draw.rect(screen,WHITE , (j * sq_size, (i + 1) * sq_size + sq_size, sq_size, sq_size))
            pygame.draw.circle(screen, BLUE, (int(j * sq_size + sq_size / 2), int(( i + 1) * sq_size + sq_size + sq_size / 2)), RADIUS)
            
    for j in range(columns):
        for i in range(rows):
            if board[i][j] == 1:
                pygame.draw.circle(screen, RED, (int(j * sq_size + sq_size/2), height-int(i * sq_size + sq_size/2)), RADIUS)
            elif board[i][j] == 2:
                pygame.draw.circle(screen, YELLOW, (int(j * sq_size + sq_size/2), height-int(i * sq_size + sq_size/2)), RADIUS)
                
    pygame.display.update()

board = game_grid()
print_board(board)
game = True
turn = 0
pygame.display.set_caption("Connect Four")

pygame.init()

sq_size = 85

width = columns * sq_size
height = (rows + 2) * sq_size

size = (width, height)

RADIUS = int(sq_size/2 - 5)

screen = pygame.display.set_mode(size)
game_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("serif", 50)

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, sq_size))
            posx = event.pos[0]
            
            if iseven(turn):
                pygame.draw.rect(screen, BLACK, (0,0, width, 2 * sq_size))
                pygame.draw.circle(screen, RED, (posx,sq_size + int(sq_size/2)), RADIUS)
                message = myfont.render("Player 1", 1, RED,WHITE)
                screen.blit(message, (40,10))

            else:
                pygame.draw.rect(screen, BLACK, (0,0, width, 2*sq_size))
                pygame.draw.circle(screen, YELLOW, (posx,  sq_size+int(sq_size/2)), RADIUS)
                message = myfont.render("Player 2", 1, YELLOW,RED)
                screen.blit(message, (40,10))
                
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, sq_size))
            #print(event.pos)
            # Ask for Player 1 Input
            if iseven(turn):
                posx = event.pos[0]
                col = int(math.floor(posx/sq_size))
                
                if is_valid_location(board, col):
                    row = next_avaliable_row(board, col)
                    fill_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        message = myfont.render("Player 1 wins!!", 1, RED,WHITE)
                        screen.blit(message, (40,10))
                        game = False

                else:                
                    if isboard_filled(board):
                        message = myfont.render("Draw",1,RED,WHITE)
                        screen.blit(message,(40,10))
                    else:
                        message = myfont.render("Column Filled!!", 1, RED,WHITE)
                        screen.blit(message, (40,10))

            # Ask for Player 2 Input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx/sq_size))
                
                if is_valid_location(board, col):
                    row = next_avaliable_row(board, col)
                    fill_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        message = myfont.render("Player 2 wins!!", 1, YELLOW,RED)
                        screen.blit(message, (40,10))
                        game = False
                else:
                    if isboard_filled(board):
                        message = myfont.render("Draw",1,RED,WHITE)
                        screen.blit(message,(40,10))
                    else:
                        message = myfont.render("Column Filled!!", 1, YELLOW,RED)
                        screen.blit(message, (40,10))
                        
            print_board(board)
            game_board(board)
            turn += 1

            if not game:
                pygame.time.wait(10)
