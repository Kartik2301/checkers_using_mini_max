## References :-

import pygame
from individual_checker import individual_checker
from copy import deepcopy
import math
#dimensions

m = 8
n = 8

#maintain state of the game
turnA = True
turnB = False

# maintain these :-

checkersA = 12
checkersB = 12
kingsA = 0
kingsB = 0

# A goes down, b goes up

pygame.init()

board = []
copy_board = []

inTheProcess = False


screen = pygame.display.set_mode((704,724))# 704 % 8 == 0
pygame.display.set_caption("IIT2018156")

running = True

font = pygame.font.Font('freesansbold.ttf',40)

def valid(x,y):
    return (x >= 0 and x < 8 and y >= 0 and y < 8)




















def calculate_inidivs(board):
    red = 0
    blue = 0
    king_red = 0
    king_blue = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] != None:
                if board[i][j].color == (255, 0, 0):
                    red += 1
                    if board[i][j].isKing == True:
                        king_red += 1
                if board[i][j].color == (0, 0, 255):
                    blue += 1
                    if board[i][j].isKing == True:
                        king_blue += 1
    return (red, blue, king_red, king_blue)

def check_board_for_winners(board):
    (red, blue, king_red, king_blue) = calculate_inidivs(board)
    if (red == 0) or (blue == 0):
        return True
    return False

def score(board):
    (red, blue, king_red, king_blue) = calculate_inidivs(board)
    return ((blue - red) + (king_blue - king_red))

    # 1 => MAX => blue
    # 2 => MIN => red

def get_all(board, player):
    found = []
    color = (255, 255, 255)
    if player == 2:
        color = (255, 0, 0)
    elif player == 1:
        color = (0, 0, 255)

    for i in range(8):
        for j in range(8):
            if board[i][j] != None:
                if board[i][j].color == color:
                    found.append((i, j))

    return found

def move_to_target_new(board, a, b, target_a, target_b):

    item = board[a][b]
    board[a][b] = None
    board[target_a][target_b] = item
    return True

def state_list(board, player):
    all_moves = get_all(board, player)
    all_possible_all_moves = []
    for item in all_moves:
        dict_moves = get_all_valid_move(item[0], item[1])
        for keys, toRemove in dict_moves.items():
            temp_board = deepcopy(board)
            ket = keys.split(" ")
            move_to_target_new(temp_board, item[0], item[1], int(ket[0]), int(ket[1]))
            for item in toRemove:
                temp_board[item[0]][item[1]] = None
            all_possible_all_moves.append(temp_board)

    return all_possible_all_moves


def minimax(board, h, player):
    if h == 0 or check_board_for_winners(board):
        return score(board), board

    if player == 1:
        v = -math.inf
        best_action = None
        # get all possible new states
        for s in state_list(board, player):
            v_new = minimax(board, h - 1, 2)[0]
            if v_new > v:
                best_action = s
                v = v_new
        return v, best_action
    elif player == 2:
        v = math.inf
        best_action = None
        # get all possible new states
        for s in state_list(board, player):
            v_new = minimax(board, h - 1, 1)[0]
            if v_new < v:
                best_action = s
                v = v_new
        return v, best_action













def get_all_by_jumps(killed, row, col,moves,step) :
    flag = False
    #if board[row][col] == None: return
    if(board[row][col] != None) :
        pass
        #print(copy_board[row][col].row,copy_board[row][col].col,copy_board[row][col].color)
    else:
        print("its over")
    if valid(row+step,col-1) and valid(row,col):
        if board[row+step][col-1] != None:
            if valid(row+2*step,col-2) :
                if board[row+2*step][col-2] == None and board[row+step][col-1].color != board[row][col].color:
                    flag = True
                    killed.append((row+step, col-1))
                    get_all_by_jumps(killed, row + 2*step, col - 2,moves,step)

    if valid(row+step,col+1) and valid(row,col):
        if board[row+step][col+1] != None:
            if valid(row+2*step,col+2) :
                if board[row+2*step][col+2] == None and board[row+step][col+1].color != board[row][col].color:
                    flag = True
                    killed.append((row+step, col+1))
                    get_all_by_jumps(killed, row + 2*step, col + 2,moves,step)

    if flag == False:
        moves[str(row) + " " + str(col)] = killed
        return


def valids_for_a(row,col,moves):
    # check left
    killed = []
    if (row + 1) < 8 and (col - 1) >= 0:
        if board[row+1][col-1] == None:
            target = str(row+1)  + " " + str(col-1)
            moves[target] = killed
        elif board[row+1][col-1].color == board[row][col].color:
            pass
        else :
            if valid(row + 2, col - 2) and board[row + 2][col - 2] == None:
                killed.append((row+1,col-1))
                board[row + 2][col - 2] = board[row][col]
                temp_moves = {}
                get_all_by_jumps(killed,row+2,col-2,temp_moves,+1)
                if len(temp_moves) > 0 :
                    board[row+2][col-2] = None
                moves.update(temp_moves)
    # check right

    killed = []
    if (row + 1) < 8 and (col + 1) < 8:
        if board[row+1][col+1] == None:
            target = str(row + 1) + " " + str(col + 1)
            moves[target] = killed
        elif board[row+1][col+1].color == board[row][col].color:
            pass
        else :
            if valid(row + 2, col + 2) and board[row + 2][col + 2] == None:
                killed.append((row+1,col+1))
                board[row+2][col+2] = board[row][col]
                temp_moves = {}
                get_all_by_jumps(killed,row+2,col+2,temp_moves,1)
                if len(temp_moves) > 0 :
                    board[row+2][col+2] = None
                moves.update(temp_moves)

def valids_for_b(row,col,moves):
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
                get_all_by_jumps(killed, row - 2, col - 2, temp_moves,-1)
                if len(temp_moves) > 0 :
                    board[row-2][col-2] = None
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
                get_all_by_jumps(killed, row - 2, col + 2, temp_moves,-1)
                if len(temp_moves) > 0 :
                    board[row-2][col+2] = None
                moves.update(temp_moves)

def get_all_valid_move(row,col):
    global board
    if board[row][col] != None:
        if board[row][col].isKing == True:
            moves = {}
            valids_for_a(row,col,moves)
            valids_for_b(row,col,moves)
            return moves
    if turnA == True:
        moves = {}
        valids_for_a(row,col,moves)
        #board = copy_board
        return moves
    else :
        if turnB == True:
            moves = {}
            valids_for_b(row,col,moves)
            #board = copy_board
            return moves

def check_for_kings():
    global kingsA
    global kingsB
    for i in range(m):
        for j in range(n):
            if board[i][j] == None: continue
            if board[i][j].color == (255,0,0) and i == 7:
                kingsA += 1
                board[i][j].isKing = True
            if board[i][j].color == (0,0,255) and i == 0:
                kingsB += 1
                board[i][j].isKing = True

def who_won_the_game_text(winner):
    global game_over
    over_text = font.render("Game Over, " + str(winner) + " HAS WON", True, (0, 255, 0))
    screen.blit(over_text, (45, 350))
    game_over = True


def move_to_target(a, b, target_a, target_b):
    if (board[a][b] == None or (board[target_a][target_b] != None and board[target_a][target_b].color != (125,125,125))):
        return False

    item = board[a][b]
    board[a][b] = None
    board[target_a][target_b] = item
    return True

# initialize the board
for i in range(m):
    semi = []
    if i < 3:
        if i%2 == 0:
            for j in range(n):
                if j % 2 == 1:
                    semi.append(individual_checker(i,j,(255,0,0)))
                else :
                    semi.append(None)
        else :
            for j in range(n):
                if j % 2 == 0:
                    semi.append(individual_checker(i,j,(255,0,0)))
                else :
                    semi.append(None)
    elif i >= 5 :
        if i%2 == 0:
            for j in range(n):
                if j % 2 == 1:
                    semi.append(individual_checker(i,j,(0,0,255)))
                else :
                    semi.append(None)
        else :
            for j in range(n):
                if j % 2 == 0:
                    semi.append(individual_checker(i,j,(0,0,255)))
                else :
                    semi.append(None)
    else:
        for j in range(n):
            semi.append(None)
    board.append(semi)

font1 = pygame.font.Font('freesansbold.ttf',64)

def display_whose_turn():
    if turnA == True:
        over_text = font1.render("Turn of A", True, (0, 255, 0))
    else :
        over_text = font1.render("Turn of B", True, (0, 255, 0))
    screen.blit(over_text, (200, 340))

new_font = pygame.font.Font('freesansbold.ttf',15)
def display_rem_checkers():
    over_text = new_font.render("Checkers remaing of red :- " + str(checkersA) + "         " + "Checkers remaining of blue :- " + str(checkersB), True, (0,255,0))
    screen.blit(over_text,(110,5))


def draw_board():

    # make the board, without any checkers

    for i in range(m):
        if(i % 2 == 0) :
            for j in range(0,n,2):
                pygame.draw.rect(screen, (255,255,255), (88*i,20+88*j,88,88)) # each square gets 704/8 = 88 (since, there are 704 pixels along a row, and we have 8 sqaures in any row
        else :
            for j in range(1,n,2):
                pygame.draw.rect(screen, (255,255,255),(88*i,20+88*j,88,88))

    # place checkers

    for i in range(m):
        for j in range (n):
            if board[i][j] == None: continue
            x_cord =  88*j + 88//2
            y_cord =  20+88*i + 88//2
            radius = 36
            pygame.draw.circle(screen,board[i][j].color,(x_cord,y_cord),radius)


initial_x = -1
initial_y = -1
allMoves = {}
game_over = False



while running:

    screen.fill((0, 0, 0))
    if turnB == True:
        board = minimax(deepcopy(board), 4,1)[1]
        turnA = True
        turnB = False
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False
        if (event.type == pygame.MOUSEBUTTONDOWN) and (turnA == True):
            clicked = event.pos
            cols = clicked[0]//88
            rows = clicked[1]//88
            donotexec = False
            if board[rows][cols] != None and board[rows][cols].color != (125,125,125) and inTheProcess == False:
                inTheProcess = True
                check = True
                allMoves = {}
                allMoves = get_all_valid_move(rows,cols)
                print(allMoves)
                for keys in allMoves.keys():
                    s_list = str(keys).split(" ")
                    board[int(s_list[0])][int(s_list[1])] = individual_checker(int(s_list[0]), int(s_list[1]), (125,125,125))

                if 3 > 2:
                    if board[rows][cols].color == (255, 0, 0):
                        if turnB == True:
                            check = False

                    if board[rows][cols].color == (0, 0, 255):
                        if turnA == True:
                            check = False

                    if check == True:
                        initial_x = rows
                        initial_y = cols

            elif (board[rows][cols] == None or board[rows][cols].color == (125,125,125)) and len(allMoves) > 0 and inTheProcess == True:
                print(allMoves)
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