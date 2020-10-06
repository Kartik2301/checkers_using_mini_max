## References :-

# https://github.com/techwithtim/Python-Checkers-AI
# https://www.youtube.com/watch?v=mYbrH1Cl3nw&t=294s

import pygame
from individual_checker import individual_checker
from copy import deepcopy
import math

# dimensions
m = 8
n = 8
# maintain state of the game
turnA = True
turnB = False
# maintain these :-
checkersA = 12
checkersB = 12
kingsA = 0
kingsB = 0
board = []
copy_board = []
inTheProcess = False
running = True
# A goes down, b goes up
pygame.init()
screen = pygame.display.set_mode((704, 724))  # 704 % 8 == 0
pygame.display.set_caption("IIT2018156")
font = pygame.font.Font('freesansbold.ttf', 40)
font1 = pygame.font.Font('freesansbold.ttf', 64)
new_font = pygame.font.Font('freesansbold.ttf', 15)
# all the functions

# check for legal coordinates on the board
def valid(x, y):
    return (x >= 0 and x < 8 and y >= 0 and y < 8)

def get_all_by_jumps(killed, row, col, moves, step):
    flag = False
    # if board[row][col] == None: return
    if (board[row][col] != None):
        pass
        # print(copy_board[row][col].row,copy_board[row][col].col,copy_board[row][col].color)
    else:
        print("its over")
        return
    if valid(row + step, col - 1) and valid(row, col):
        if board[row + step][col - 1] != None:
            if valid(row + 2 * step, col - 2):
                if board[row + 2 * step][col - 2] == None and board[row + step][col - 1].color != board[row][col].color:
                    flag = True
                    killed.append((row + step, col - 1))
                    get_all_by_jumps(killed, row + 2 * step, col - 2, moves, step)

    if valid(row + step, col + 1) and valid(row, col):
        if board[row + step][col + 1] != None:
            if valid(row + 2 * step, col + 2):
                if board[row + 2 * step][col + 2] == None and board[row + step][col + 1].color != board[row][col].color:
                    flag = True
                    killed.append((row + step, col + 1))
                    get_all_by_jumps(killed, row + 2 * step, col + 2, moves, step)

    if flag == False:
        moves[str(row) + " " + str(col)] = killed
        return


def valids_for_a(row, col, moves):
    # check left
    killed = []
    if (row + 1) < 8 and (col - 1) >= 0:
        if board[row + 1][col - 1] == None:
            target = str(row + 1) + " " + str(col - 1)
            moves[target] = killed
        elif board[row + 1][col - 1].color == board[row][col].color:
            pass
        else:
            if valid(row + 2, col - 2) and board[row + 2][col - 2] == None:
                killed.append((row + 1, col - 1))
                board[row + 2][col - 2] = board[row][col]
                temp_moves = {}
                get_all_by_jumps(killed, row + 2, col - 2, temp_moves, +1)
                if len(temp_moves) > 0:
                    board[row + 2][col - 2] = None
                moves.update(temp_moves)
    # check right

    killed = []
    if (row + 1) < 8 and (col + 1) < 8:
        if board[row + 1][col + 1] == None:
            target = str(row + 1) + " " + str(col + 1)
            moves[target] = killed
        elif board[row + 1][col + 1].color == board[row][col].color:
            pass
        else:
            if valid(row + 2, col + 2) and board[row + 2][col + 2] == None:
                killed.append((row + 1, col + 1))
                board[row + 2][col + 2] = board[row][col]
                temp_moves = {}
                get_all_by_jumps(killed, row + 2, col + 2, temp_moves, 1)
                if len(temp_moves) > 0:
                    board[row + 2][col + 2] = None
                moves.update(temp_moves)


def valids_for_b(row, col, moves):
    killed = []
    if (row - 1) >= 0 and (col - 1) >= 0:
        if board[row - 1][col - 1] == None:
            target = str(row - 1) + " " + str(col - 1)
            moves[target] = killed
        elif board[row - 1][col - 1].color == board[row][col].color:
            pass
        else:
            if valid(row - 2, col - 2) and board[row - 2][col - 2] == None:
                killed.append((row - 1, col - 1))
                temp_moves = {}
                board[row - 2][col - 2] = board[row][col]
                get_all_by_jumps(killed, row - 2, col - 2, temp_moves, -1)
                if len(temp_moves) > 0:
                    board[row - 2][col - 2] = None
                moves.update(temp_moves)
    # check right
    killed = []
    if (row - 1) >= 0 and (col + 1) < 8:
        if board[row - 1][col + 1] == None:
            target = str(row - 1) + " " + str(col + 1)
            moves[target] = killed
        elif board[row - 1][col + 1].color == board[row][col].color:
            pass
        else:
            if valid(row - 2, col + 2) and board[row - 2][col + 2] == None:
                killed.append((row - 1, col + 1))
                board[row - 2][col + 2] = board[row][col]
                temp_moves = {}
                get_all_by_jumps(killed, row - 2, col + 2, temp_moves, -1)
                if len(temp_moves) > 0:
                    board[row - 2][col + 2] = None
                moves.update(temp_moves)


def get_all_valid_move(row, col):
    global board
    if board[row][col] != None:
        if board[row][col].isKing == True:
            moves = {}
            valids_for_a(row, col, moves)
            valids_for_b(row, col, moves)
            return moves
    if turnA == True:
        moves = {}
        valids_for_a(row, col, moves)
        # board = copy_board
        return moves
    else:
        if turnB == True:
            moves = {}
            valids_for_b(row, col, moves)
            # board = copy_board
            return moves

# check if some checker has become a king
def check_for_kings():
    global kingsA
    global kingsB
    for i in range(m):
        for j in range(n):
            if board[i][j] == None: continue
            if board[i][j].color == (255, 0, 0) and i == 7:
                kingsA += 1
                board[i][j].isKing = True
            if board[i][j].color == (0, 0, 255) and i == 0:
                kingsB += 1
                board[i][j].isKing = True

# if checkers of a == 0 || checkers of b == 0, then game is over
def who_won_the_game_text(winner):
    global game_over
    over_text = font.render("Game Over, " + str(winner) + " HAS WON", True, (0, 255, 0))
    screen.blit(over_text, (45, 350))
    game_over = True

# update display, by actually moving the selected checker to the destination (for the computer player)
def move_to_target(a, b, target_a, target_b):
    if (board[a][b] == None or (
            board[target_a][target_b] != None and board[target_a][target_b].color != (125, 125, 125))):
        return False

    item = board[a][b]
    board[a][b] = None
    board[target_a][target_b] = item
    return True


# initialize the board
# References :- https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/board.py
for i in range(m):
    semi = []
    if i < 3:
        if i % 2 == 0:
            for j in range(n):
                if j % 2 == 1:
                    semi.append(individual_checker(i, j, (255, 0, 0)))
                else:
                    semi.append(None)
        else:
            for j in range(n):
                if j % 2 == 0:
                    semi.append(individual_checker(i, j, (255, 0, 0)))
                else:
                    semi.append(None)
    elif i >= 5:
        if i % 2 == 0:
            for j in range(n):
                if j % 2 == 1:
                    semi.append(individual_checker(i, j, (0, 0, 255)))
                else:
                    semi.append(None)
        else:
            for j in range(n):
                if j % 2 == 0:
                    semi.append(individual_checker(i, j, (0, 0, 255)))
                else:
                    semi.append(None)
    else:
        for j in range(n):
            semi.append(None)
    board.append(semi)

# for convenience purposes, display whose turn is it
def display_whose_turn():
    if turnA == True:
        over_text = font1.render("Turn of A", True, (0, 255, 0))
    else:
        over_text = font1.render("Turn of B", True, (0, 255, 0))
    screen.blit(over_text, (200, 340))

# At each state of the board, display to the player(s) the number of checkers left
def display_rem_checkers():
    over_text = new_font.render(
        "Checkers remaing of red :- " + str(checkersA) + "         " + "Checkers remaining of blue :- " + str(
            checkersB), True, (0, 255, 0))
    screen.blit(over_text, (110, 5))

# Actually display the board to the user
# References for gui pruposes :- https://github.com/techwithtim/Python-Checkers-AI/blob/master/checkers/board.py
def draw_board():
    # make the board, without any checkers

    for i in range(m):
        if (i % 2 == 0):
            for j in range(0, n, 2):
                pygame.draw.rect(screen, (255, 255, 255), (88 * i, 20 + 88 * j, 88,
                                                           88))  # each square gets 704/8 = 88 (since, there are 704 pixels along a row, and we have 8 sqaures in any row
        else:
            for j in range(1, n, 2):
                pygame.draw.rect(screen, (255, 255, 255), (88 * i, 20 + 88 * j, 88, 88))

    # place checkers

    if board == None: return
    for i in range(m):
        for j in range(n):
            if board[i][j] == None: continue
            x_cord = 88 * j + 88 // 2
            y_cord = 20 + 88 * i + 88 // 2
            radius = 36
            pygame.draw.circle(screen, board[i][j].color, (x_cord, y_cord), radius)

# Now start the game

initial_x = -1
initial_y = -1
allMoves = {}
game_over = False

# Game loop
while running:

    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.MOUSEBUTTONDOWN):
            clicked = event.pos
            cols = clicked[0] // 88
            rows = clicked[1] // 88
            donotexec = False
            if board[rows][cols] != None and board[rows][cols].color != (125, 125, 125) and inTheProcess == False:
                allMoves = {}
                allMoves = get_all_valid_move(rows, cols)
                if len(allMoves) > 0:
                    inTheProcess = True
                check = True
                print(allMoves)
                print(inTheProcess)
                for keys in allMoves.keys():
                    s_list = str(keys).split(" ")
                    board[int(s_list[0])][int(s_list[1])] = individual_checker(int(s_list[0]), int(s_list[1]),(125, 125, 125))


                if board[rows][cols].color == (255, 0, 0):
                    if turnB == True:
                        check = False

                if board[rows][cols].color == (0, 0, 255):
                    if turnA == True:
                        check = False

                if check == True:
                    initial_x = rows
                    initial_y = cols

            elif (board[rows][cols] == None or board[rows][cols].color == (125, 125, 125)) and len(
                    allMoves) > 0 and inTheProcess == True:
                donotexec = True
                key = str(rows) + " " + str(cols)
                if key in allMoves.keys():
                    return_value = move_to_target(initial_x, initial_y, rows, cols)
                    check_mark = board[rows][cols]
                    toRemove = allMoves[key]
                    for item in toRemove:
                        board[item[0]][item[1]] = None
                    if return_value == True:
                        if turnA:
                            checkersB -= len(toRemove)
                        if turnB:
                            checkersA -= len(toRemove)

                        for keys in allMoves.keys():
                            s_list = str(keys).split(" ")
                            board[int(s_list[0])][int(s_list[1])] = None
                        board[rows][cols] = check_mark
                        turnA = not turnA
                        turnB = not turnB
                        initial_x = -1
                        initial_y = -1
                        inTheProcess = False

                print(inTheProcess)

    draw_board()
    if game_over == False:
        display_whose_turn()
    display_rem_checkers()
    check_for_kings()
    copy_board = board
    if checkersA == 0:
        who_won_the_game_text("B (blue)")
    elif checkersB == 0:
        who_won_the_game_text("A (red)")

    pygame.display.update()