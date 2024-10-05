import pygame
import sys
import numpy as np

pygame.init()

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Sizes
WIDTH = 300
HEIGHT = 400  
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_X = (WIDTH - BUTTON_WIDTH) // 2
BUTTON_Y = 350  

# Game Variables
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe with AI and Play Again')


font = pygame.font.Font(None, 36)

board = np.zeros((BOARD_ROWS, BOARD_COLS))

def draw_lines(color=WHITE):
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, HEIGHT - 100), LINE_WIDTH)

def draw_figures(color=WHITE):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                # X diagonal 1
                pygame.draw.line(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 6, row * SQUARE_SIZE + SQUARE_SIZE // 6),
                                 (col * SQUARE_SIZE + 5 * SQUARE_SIZE // 6, row * SQUARE_SIZE + 5 * SQUARE_SIZE // 6),
                                 CROSS_WIDTH)
                # X diagonal 2
                pygame.draw.line(screen, color,
                                 (col * SQUARE_SIZE + SQUARE_SIZE // 6, row * SQUARE_SIZE + 5 * SQUARE_SIZE // 6),
                                 (col * SQUARE_SIZE + 5 * SQUARE_SIZE // 6, row * SQUARE_SIZE + SQUARE_SIZE // 6),
                                 CROSS_WIDTH)

def draw_button():
    pygame.draw.rect(screen, BLUE, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    text = font.render("Play Again", True, WHITE)
    screen.blit(text, (BUTTON_X + 35, BUTTON_Y + 10))

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True

def check_win(player):
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        return True

    return False

def restart_game():
    screen.fill(BLACK)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

def minimax(minimax_board, depth, is_maximizing):
    if check_win(2):
        return 1
    elif check_win(1):
        return -1
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -float('inf')
    move = (-1, -1)
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = 2
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)

# Initialize game
draw_lines()
player = 1
game_over = False
show_button = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            if not game_over:
                clicked_col = mouseX // SQUARE_SIZE
                clicked_row = mouseY // SQUARE_SIZE

                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_win(player):
                        game_over = True
                        show_button = True
                    player = player % 2 + 1

                    if not game_over and player == 2:
                        best_move()
                        if check_win(2):
                            game_over = True
                            show_button = True
                        player = player % 2 + 1

                    if is_board_full() and not check_win(1) and not check_win(2):
                        game_over = True
                        show_button = True
            else:
                # Checking if Play Again Is Pressed
                if BUTTON_X <= mouseX <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= mouseY <= BUTTON_Y + BUTTON_HEIGHT:
                    restart_game()
                    game_over = False
                    show_button = False
                    player = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                show_button = False
                player = 1

    # Drawing board and figures
    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(GREEN)
        elif check_win(2):
            draw_figures(RED)
        else:
            draw_figures(GRAY)

        if show_button:
            draw_button()

    pygame.display.update()
