import pygame 
import sys
import random

Width, Height = 600, 600
Rows, Cols = 20, 20
Square_Size = Width // Cols
White, Black = (255, 255, 255), (0, 0, 0)
X_color, O_color = (255, 0, 0), (0, 0, 255)  
board = [[' ' for _ in range(Cols)] for _ in range(Rows)]
pygame.init()
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Caro Game')
def draw_board():
    for row in range(Rows):
        for col in range(Cols):
            pygame.draw.rect(screen, White, (col * Square_Size, row * Square_Size, Square_Size, Square_Size))
            pygame.draw.rect(screen, Black, (col * Square_Size, row * Square_Size, Square_Size, Square_Size), 1)
            if board[row][col] == 'X':
                pygame.draw.line(screen, X_color, (col * Square_Size + 10, row * Square_Size + 10), (col * Square_Size + Square_Size - 10, row * Square_Size + Square_Size - 10), 4)
                pygame.draw.line(screen, X_color, (col * Square_Size + Square_Size - 10, row * Square_Size + 10), (col * Square_Size + 10, row * Square_Size + Square_Size - 10), 4)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, O_color, (col * Square_Size + Square_Size // 2, row * Square_Size + Square_Size // 2), Square_Size // 2 - 10, 4)
def check_winner():
    for i in range(Rows):
        for j in range(Cols - 4):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == board[i][j + 4] and board[i][j] != ' ':
                return True
            if board[j][i] == board[j + 1][i] == board[j + 2][i] == board[j + 3][i] == board[j + 4][i] and board[j][i] != ' ':
                return True
    for i in range(Rows - 4):
        for j in range(Cols - 4):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == board[i + 4][j + 4] and board[i][j] != ' ':
                return True
    for i in range(4, Rows):
        for j in range(Cols - 4):
            if board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == board[i - 3][j + 3] == board[i - 4][j + 4] and board[i][j] != ' ':
                return True
    return False
def restart():
    global board, game_over, turn
    board = [[' ' for _ in range(Cols)] for _ in range(Rows)]
    game_over = False
    turn = 'X'
def show_winner(winner):
    popup_font = pygame.font.Font(None, 48)
    popup_text = popup_font.render(f'Player {winner} wins!', True, White)
    popup_rect = popup_text.get_rect(center=(Width // 2, Height // 2))
    pygame.draw.rect(screen, Black, (popup_rect.x - 10, popup_rect.y - 10, popup_rect.width + 20, popup_rect.height + 20))
    screen.blit(popup_text, popup_rect)
    pygame.display.flip()
    pygame.time.delay(1500)  
def print_last_move_x(row, col):
    print(f'Last move of X: ({row}, {col})')
    return row, col
def print_empty_adjacent_cells(row, col):
    blocking_cells = check_4_O() or check_4_X(row, col) or check_3_O_oth_se() or check_3_O_oth() or check_3_O() or check_3_O_oth_pro() or check_3_X_oth_se() or check_3_X_oth() or check_3_X(row, col) or check_3_X_oth_pro() or check_2_O() or check_2_X(row, col) or check_1_O()
    if blocking_cells:
        empty_cells = [(r, c) for r, c in blocking_cells if 0 <= r < Rows and 0 <= c < Cols and board[r][c] == ' ']
    else:
        adjacent_cells = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
            (row - 1, col - 1),
            (row - 1, col + 1),
            (row + 1, col - 1),
            (row + 1, col + 1)
        ]
        empty_cells = [(r, c) for r, c in adjacent_cells if 0 <= r < Rows and 0 <= c < Cols and board[r][c] == ' ']
    return empty_cells
def check_1_O():
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols):
            if board[i][j] == 'O' and board[i][j + 1] == ' ' == board[i][j - 1]:
                blocking_positions.append((i, j + 1))
                blocking_positions.append((i, j - 1))
    for i in range(Cols):
        for j in range(Rows):
            if board[j][i] == 'O' and board[j + 1][i] == ' ' == board[j - 1][i]:
                blocking_positions.append((j + 1, i))
                blocking_positions.append((j - 1, i))
    for i in range(Rows):
        for j in range(Cols):
            if board[i][j] == 'O' and board[i + 1][j + 1] == ' ' and board[i - 1][j - 1]:
                blocking_positions.append((i + 1, j + 1))
                blocking_positions.append((i - 1, j - 1))
    for i in range(0, Rows):
        for j in range(Cols):
            if board[i][j] == 'X' and board[i - 1][j + 1] == ' ' == board[i + 1][j - 1]:
                blocking_positions.append((i - 1, j + 1))
                blocking_positions.append((i + 1, j - 1))
    return blocking_positions if blocking_positions else None
def check_2_X(row, col):
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols - 1):
            if board[row][j] == board[row][j + 1] == 'X':
                if j + 2 < Cols and board[row][j + 2] == ' ':
                    blocking_positions.append((row, j + 2))
                if j - 1 >= 0 and board[row][j - 1] == ' ':
                    blocking_positions.append((row, j - 1))
            if board[j][col] == board[j + 1][col] == 'X':
                if j + 2 < Rows and board[j + 2][col] == ' ':
                    blocking_positions.append((j + 2, col))
                if j - 1 >= 0 and board[j - 1][col] == ' ':
                    blocking_positions.append((j - 1, col))
    for i in range(Rows - 1):
        for j in range(Cols - 1):
            if board[i][j] == board[i + 1][j + 1] == 'X':
                if i + 2 < Rows and j + 2 < Cols and board[i + 2][j + 2] == ' ':
                    blocking_positions.append((i + 2, j + 2))
                if i - 1 >= 0 and j - 1 >= 0 and board[i - 1][j - 1] == ' ':
                    blocking_positions.append((i - 1, j - 1))
            if board[i + 1][j] == board[i][j + 1] == 'X':
                if i - 1 >= 0 and j + 2 < Cols and board[i - 1][j + 2] == ' ':
                    blocking_positions.append((i - 1, j + 2))
                if i + 2 < Rows and j - 1 >= 0 and board[i + 2][j - 1] == ' ':
                    blocking_positions.append((i + 2, j - 1))
    return blocking_positions if blocking_positions else None
def check_2_O():
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols - 1):
            if board[i][j] == board[i][j + 1] == 'O' and board[i][j + 2] == ' ' == board[i][j - 1]:
                blocking_positions.append((i, j + 2))
                blocking_positions.append((i, j - 1))
    for i in range(Cols):
        for j in range(Rows - 1):
            if board[j][i] == board[j + 1][i] == 'O' and board[j + 2][i] == ' ' == board[j - 1][i]:
                blocking_positions.append((j + 2, i))
                blocking_positions.append((j - 1, i))
    for i in range(Rows - 1):
        for j in range(Cols - 1):
            if board[i][j] == board[i + 1][j + 1] == 'O' and board[i + 2][j + 2] == ' ' and board[i - 1][j - 1]:
                blocking_positions.append((i + 2, j + 2))
                blocking_positions.append((i - 1, j - 1))
    for i in range(1, Rows):
        for j in range(Cols - 1):
            if board[i][j] == board[i - 1][j + 1] == 'X' and board[i - 2][j + 2] == ' ' == board[i + 1][j - 1]:
                blocking_positions.append((i - 2, j + 2))
                blocking_positions.append((i + 1, j - 1))
    return blocking_positions if blocking_positions else None
def check_3_X(row, col):
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols - 2):
            if board[row][j] == board[row][j + 1] == board[row][j + 2] == 'X':
                if j + 3 < Cols and board[row][j + 3] == ' ':
                    blocking_positions.append((row, j + 3))
                if j - 1 >= 0 and board[row][j - 1] == ' ':
                    blocking_positions.append((row, j - 1))
            if board[j][col] == board[j + 1][col] == board[j + 2][col] == 'X':
                if j + 3 < Rows and board[j + 3][col] == ' ':
                    blocking_positions.append((j + 3, col))
                if j - 1 >= 0 and board[j - 1][col] == ' ':
                    blocking_positions.append((j - 1, col))
    for i in range(Rows - 2):
        for j in range(Cols - 2):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == 'X':
                if i + 3 < Rows and j + 3 < Cols and board[i + 3][j + 3] == ' ':
                    blocking_positions.append((i + 3, j + 3))
                if i - 1 >= 0 and j - 1 >= 0 and board[i - 1][j - 1] == ' ':
                    blocking_positions.append((i - 1, j - 1))
            if board[i + 2][j] == board[i + 1][j + 1] == board[i][j + 2] == 'X':
                if i - 1 >= 0 and j + 3 < Cols and board[i - 1][j + 3] == ' ':
                    blocking_positions.append((i - 1, j + 3))
                if i + 3 < Rows and j - 1 >= 0 and board[i + 3][j - 1] == ' ':
                    blocking_positions.append((i + 3, j - 1))
    return blocking_positions if blocking_positions else None
def check_3_X_oth():
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i][j + 1] == 'X' and board[i][j + 2] == ' ' and board[i][j + 3] == 'X':
                blocking_positions.append((i, j + 2))
            if board[i][j] == 'X' and board[i][j + 1] == ' ' and board[i][j + 2] == board[i][j + 3] == 'X':
                blocking_positions.append((i, j + 1))
    for i in range(Cols):
        for j in range(Rows - 3):
            if board[j][i] == board[j + 1][i] == 'X' and board[j + 2][i] == ' ' and board[j + 3][i] == 'X':
                blocking_positions.append((j + 2, i))
            if board[j][i] == 'X' and board[j + 1][i] == ' ' and board[j + 2][i] == board[j + 3][i] == 'X':
                blocking_positions.append((j + 1, i))
    for i in range(Rows - 3):
        for j in range(Cols - 3):
            if board[i][j] == board[i + 1][j + 1] == 'X' and board[i + 2][j + 2] == ' ' and board[i + 3][j + 3] == 'X':
                blocking_positions.append((i + 2, j + 2))
            if board[i][j] == 'X' and board[i + 1][j + 1] == ' ' and board[i + 2][j + 2] == board[i + 3][j + 3] == 'X':
                blocking_positions.append((i + 1, j + 1))
    for i in range(3, Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i - 1][j + 1] == 'X' and board[i - 2][j + 2] == ' ' and board[i - 3][j + 3] == 'X':
                blocking_positions.append((i - 2, j + 2))
            if board[i][j] == 'X' and board[i - 1][j + 1] == ' ' and board[i - 2][j + 2] == board[i - 3][j + 3] == 'X':
                blocking_positions.append((i - 1, j + 1))
    return blocking_positions if blocking_positions else None
def check_3_O_oth():
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i][j + 1] == 'O' and board[i][j + 2] == ' ' and board[i][j + 3] == 'O':
                blocking_positions.append((i, j + 2))
            if board[i][j] == 'O' and board[i][j + 1] == ' ' and board[i][j + 2] == board[i][j + 3] == 'O':
                blocking_positions.append((i, j + 1))
    for i in range(Cols):
        for j in range(Rows - 3):
            if board[j][i] == board[j + 1][i] == 'O' and board[j + 2][i] == ' ' and board[j + 3][i] == 'O':
                blocking_positions.append((j + 2, i))
            if board[j][i] == 'O' and board[j + 1][i] == ' ' and board[j + 2][i] == board[j + 3][i] == 'O':
                blocking_positions.append((j + 1, i))
    for i in range(Rows - 3):
        for j in range(Cols - 3):
            if board[i][j] == board[i + 1][j + 1] == 'O' and board[i + 2][j + 2] == ' ' and board[i + 3][j + 3] == 'O':
                blocking_positions.append((i + 2, j + 2))
            if board[i][j] == 'O' and board[i + 1][j + 1] == ' ' and board[i + 2][j + 2] == board[i + 3][j + 3] == 'O':
                blocking_positions.append((i + 1, j + 1))
    for i in range(3, Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i - 1][j + 1] == 'O' and board[i - 2][j + 2] == ' ' and board[i - 3][j + 3] == 'O':
                blocking_positions.append((i - 2, j + 2))
            if board[i][j] == 'O' and board[i - 1][j + 1] == ' ' and board[i - 2][j + 2] == board[i - 3][j + 3] == 'O':
                blocking_positions.append((i - 1, j + 1))
    return blocking_positions if blocking_positions else None
def check_3_X_oth_pro():
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i][j + 2] == 'X' and board[i][j + 1] == board[i][j + 3] == ' ' and board[i][j + 4] == 'X':
                blocking_positions.append((i, j + 1))
                blocking_positions.append((i, j + 3))
    for i in range(Cols):
        for j in range(Rows - 3):
            if board[j][i] == board[j + 2][i] == 'X' and board[j + 1][i] == board[j + 3][i] == ' ' and board[j + 4][i] == 'X':
                blocking_positions.append((j + 1, i))
                blocking_positions.append((j + 3, i))
    for i in range(Rows - 3):
        for j in range(Cols - 3):
            if board[i][j] == board[i + 2][j + 2] == 'X' and board[i + 1][j + 1] == board[i + 3][j + 3] == ' ' and board[i + 4][j + 4] == 'X':
                blocking_positions.append((i + 1, j + 1))
                blocking_positions.append((i + 3, j + 3))
    for i in range(3, Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i - 2][j + 2] == 'X' and board[i - 1][j + 1] == board[i - 3][j + 3] == ' ' and board[i - 4][j + 4] == 'X':
                blocking_positions.append((i - 1, j + 1))
                blocking_positions.append((i - 3, j + 3))
    return blocking_positions if blocking_positions else None
def check_3_O_oth_pro():
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i][j + 2] == 'O' and board[i][j + 1] == board[i][j + 3] == ' ' and board[i][j + 4] == 'O':
                blocking_positions.append((i, j + 1))
                blocking_positions.append((i, j + 3))
    for i in range(Cols):
        for j in range(Rows - 3):
            if board[j][i] == board[j + 2][i] == 'O' and board[j + 1][i] == board[j + 3][i] == ' ' and board[j + 4][i] == 'O':
                blocking_positions.append((j + 1, i))
                blocking_positions.append((j + 3, i))
    for i in range(Rows - 3):
        for j in range(Cols - 3):
            if board[i][j] == board[i + 2][j + 2] == 'O' and board[i + 1][j + 1] == board[i + 3][j + 3] == ' ' and board[i + 4][j + 4] == 'O':
                blocking_positions.append((i + 1, j + 1))
                blocking_positions.append((i + 3, j + 3))
    for i in range(3, Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i - 2][j + 2] == 'O' and board[i - 1][j + 1] == board[i - 3][j + 3] == ' ' and board[i - 4][j + 4] == 'O':
                blocking_positions.append((i - 1, j + 1))
                blocking_positions.append((i - 3, j + 3))
    return blocking_positions if blocking_positions else None
def check_3_X_oth_se():
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i][j + 1] == 'X' == board[i][j + 2] and ' ' == board[i][j + 3] == board[i][j - 1]:
                blocking_positions.append((i, j - 1))
                blocking_positions.append((i, j + 3))
    for i in range(Cols):
        for j in range(Rows - 3):
            if board[j][i] == board[j + 1][i] == 'X' == board[j + 2][i] and ' ' == board[j + 3][i] == board[j - 1][i]:
                blocking_positions.append((j - 1, i))
                blocking_positions.append((j + 3, i))
    for i in range(Rows - 3):
        for j in range(Cols - 3):
            if board[i][j] == board[i + 1][j + 1] == 'X' == board[i + 2][j + 2] and ' ' == board[i + 3][j + 3] == board[i - 1][j - 1]:
                blocking_positions.append((i - 1, j - 1))
                blocking_positions.append((i + 3, j + 3))
    for i in range(3, Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i - 1][j + 1] == 'X' == board[i - 2][j + 2] and ' ' == board[i - 3][j + 3] == board[i + 1][j - 1]:
                blocking_positions.append((i - 3, j + 3))
                blocking_positions.append((i + 1, j - 1))
    return blocking_positions if blocking_positions else None
def check_3_O_oth_se():
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i][j + 1] == 'O' == board[i][j + 2] and ' ' == board[i][j + 3] == board[i][j - 1]:
                blocking_positions.append((i, j - 1))
                blocking_positions.append((i, j + 3))
    for i in range(Cols):
        for j in range(Rows - 3):
            if board[j][i] == board[j + 1][i] == 'O' == board[j + 2][i] and ' ' == board[j + 3][i] == board[j - 1][i]:
                blocking_positions.append((j - 1, i))
                blocking_positions.append((j + 3, i))
    for i in range(Rows - 3):
        for j in range(Cols - 3):
            if board[i][j] == board[i + 1][j + 1] == 'O' == board[i + 2][j + 2] and ' ' == board[i + 3][j + 3] == board[i - 1][j - 1]:
                blocking_positions.append((i - 1, j - 1))
                blocking_positions.append((i + 3, j + 3))
    for i in range(3, Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i - 1][j + 1] == 'O' == board[i - 2][j + 2] and ' ' == board[i - 3][j + 3] == board[i + 1][j - 1]:
                blocking_positions.append((i - 3, j + 3))
                blocking_positions.append((i + 1, j - 1))
    return blocking_positions if blocking_positions else None
def check_4_X(row, col):
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols - 3):
            if board[row][j] == board[row][j + 1] == board[row][j + 2] == board[row][j + 3] == 'X':
                if j + 4 < Cols and board[row][j + 4] == ' ':
                    blocking_positions.append((row, j + 4))
                if j - 1 >= 0 and board[row][j - 1] == ' ':
                    blocking_positions.append((row, j - 1))
            if board[j][col] == board[j + 1][col] == board[j + 2][col] == board[j + 3][col] == 'X':
                if j + 4 < Rows and board[j + 4][col] == ' ':
                    blocking_positions.append((j + 4, col))
                if j - 1 >= 0 and board[j - 1][col] == ' ':
                    blocking_positions.append((j - 1, col))
    for i in range(Rows - 3):
        for j in range(Cols - 3):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == 'X':
                if i + 4 < Rows and j + 4 < Cols and board[i + 4][j + 4] == ' ':
                    blocking_positions.append((i + 4, j + 4))
                if i - 1 >= 0 and j - 1 >= 0 and board[i - 1][j - 1] == ' ':
                    blocking_positions.append((i - 1, j - 1))
            if board[i + 3][j] == board[i + 2][j + 1] == board[i + 1][j + 2] == board[i][j + 3] == 'X':
                if i - 1 >= 0 and j + 4 < Cols and board[i - 1][j + 4] == ' ':
                    blocking_positions.append((i - 1, j + 4))
                if i + 4 < Rows and j - 1 >= 0 and board[i + 4][j - 1] == ' ':
                    blocking_positions.append((i + 4, j - 1))
    return blocking_positions if blocking_positions else None
def check_3_O():
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols - 2):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == 'O':
                if j + 3 < Cols and board[i][j + 3] == ' ':
                    blocking_positions.append((i, j + 3))
                if j - 1 >= 0 and board[i][j - 1] == ' ':
                    blocking_positions.append((i, j - 1))
    for i in range(Cols):
        for j in range(Rows - 2):
            if board[j][i] == board[j + 1][i] == board[j + 2][i] == 'O':
                if j + 3 < Rows and board[j + 3][i] == ' ':
                    blocking_positions.append((j + 3, i))
                if j - 1 >= 0 and board[j - 1][i] == ' ':
                    blocking_positions.append((j - 1, i))
    for i in range(Rows - 2):
        for j in range(Cols - 2):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == 'O':
                if i + 3 < Rows and j + 3 < Cols and board[i + 3][j + 3] == ' ':
                    blocking_positions.append((i + 3, j + 3))
                if i - 1 >= 0 and j - 1 >= 0 and board[i - 1][j - 1] == ' ':
                    blocking_positions.append((i - 1, j - 1))
    for i in range(2, Rows):
        for j in range(Cols - 2):
            if board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == 'O':
                if i - 3 >= 0 and j + 3 < Cols and board[i - 3][j + 3] == ' ':
                    blocking_positions.append((i - 3, j + 3))
                if i + 1 < Rows and j - 1 >= 0 and board[i + 1][j - 1] == ' ':
                    blocking_positions.append((i + 1, j - 1))
    return blocking_positions if blocking_positions else None
def check_4_O():
    blocking_positions = []
    for i in range(Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == 'O':
                if j + 4 < Cols and board[i][j + 4] == ' ':
                    blocking_positions.append((i, j + 4))
                if j - 1 >= 0 and board[i][j - 1] == ' ':
                    blocking_positions.append((i, j - 1))
    for i in range(Cols):
        for j in range(Rows - 3):
            if board[j][i] == board[j + 1][i] == board[j + 2][i] == board[j + 3][i] == 'O':
                if j + 4 < Rows and board[j + 4][i] == ' ':
                    blocking_positions.append((j + 4, i))
                if j - 1 >= 0 and board[j - 1][i] == ' ':
                    blocking_positions.append((j - 1, i))
    for i in range(Rows - 3):
        for j in range(Cols - 3):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == 'O':
                if i + 4 < Rows and j + 4 < Cols and board[i + 4][j + 4] == ' ':
                    blocking_positions.append((i + 4, j + 4))
                if i - 1 >= 0 and j - 1 >= 0 and board[i - 1][j - 1] == ' ':
                    blocking_positions.append((i - 1, j - 1))
    for i in range(3, Rows):
        for j in range(Cols - 3):
            if board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == board[i - 3][j + 3] == 'O':
                if i - 4 >= 0 and j + 4 < Cols and board[i - 4][j + 4] == ' ':
                    blocking_positions.append((i - 4, j + 4))
                if i + 1 < Rows and j - 1 >= 0 and board[i + 1][j - 1] == ' ':
                    blocking_positions.append((i + 1, j - 1))
    
    return blocking_positions if blocking_positions else None

def ai_move(row_, col_):
    empty_cells = print_empty_adjacent_cells(row_, col_)
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 'O'
        if check_winner():
            print('Player O wins!')
            show_winner('O')
            global game_over
            game_over = True
turn = 'X'
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // Square_Size
            clicked_col = mouseX // Square_Size
            if board[clicked_row][clicked_col] == ' ':
                board[clicked_row][clicked_col] = turn
                if check_winner():
                    print(f'Player {turn} wins!')
                    show_winner(turn)
                    game_over = True
                else:
                    turn = 'O' if turn == 'X' else 'X'
                    if turn == 'O' and not game_over:
                        ai_move(clicked_row, clicked_col)
                        turn = 'X'
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouseX, mouseY = event.pos
            if Width // 2 - 75 <= mouseX <= Width // 2 + 75 and Height // 2 + 50 <= mouseY <= Height // 2 + 100:
                restart()
    screen.fill(White)
    draw_board()
    if game_over:
        pygame.draw.rect(screen, Black, (Width // 2 - 75, Height // 2 + 50, 150, 50))
        restart_font = pygame.font.Font(None, 36)   
        restart_text = restart_font.render('Play Again', True, White)
        restart_rect = restart_text.get_rect(center=(Width // 2, Height // 2 + 75))
        screen.blit(restart_text, restart_rect)
    pygame.display.flip()