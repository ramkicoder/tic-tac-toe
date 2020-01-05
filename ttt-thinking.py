import random

board = ['1','2','3','4','5','6','7','8','9']
winning_combos = [[0,1,2],[3,4,5],[6,7,8],
                    [0,3,6],[1,4,7],[2,5,8],
                      [0,4,8],[2,4,6]]

debug_flag = 0

def debug_print(*args):
    '''
    if global debug_on is turned on, print the args as is
    else just return
    '''
    if debug_flag == 1:
        print(*args)
        
def check_win_possible(board,symbol):
    count = 0
    blank_count = 0
    for combo in winning_combos:
        debug_print("Checking ", combo)
        count = 0
        blank_count = 0
        for index in combo:
            if (board[index] == symbol):
                count += 1
            if (board[index] in '123456789'):
                blank_count += 1
        debug_print("{} count {} blank {}".format(symbol, count, blank_count))
        if (count == 2 and blank_count == 1):
            debug_print("Win detected for ", symbol, combo)
            #return combo
            for i in combo:
                if board[i] in '123456789':
                    debug_print("Win index ", i)
                    return (i + 1) #this is the winning index
    return (-1)

def adjacent_symbol(board,symbol,pos):
    #bug - won't work for the first entry to be put since count will be 0
    pos -= 1
    count = 0
    for combo in winning_combos:
        count = 0
        if not pos in combo:
            continue
        for i in combo:
            if (board[i] == symbol):
                count += 1
        if (count > 0):
            return (count)
    return(count)

def display_board(board):
    '''
    board is a list of 9 characters, can be X, O, or 1-9
    Initially will be 1-9
    display using dash(-) and pipe (|) chars
    9 dashes
    for each row
        for each board el
            1 pipe, space, boardchar, space 
        1 pipe at end of row
        9 dashes
    '''
    rowdashes = "- - - - - - -"
    print(rowdashes)
    for rowindex in range(0,3):
        for colindex in range(0,3):
            print("| ",end="")
            print(board[rowindex * 3 + colindex], end="")
            print(" ", end="")
        print("|")
        print(rowdashes)

def check_win(symbol):
    for combo in winning_combos:
        if (board[combo[0]] == board[combo[1]] == board[combo[2]] == symbol):
            return True
    return False
    
def board_full(board):
    '''
    check if all slots are filled with X or O
    '''
    for c in board:
        if c in '123456789':
            return False #slots available
    debug_print("Board full!")
    return True

def get_choice_player(board, symbol):
    while True:
        choice = input("Where do you want to place {}? ".format(symbol)).strip()
        if (not choice.isdigit()):
            print("Only numbers!")
            continue
        choice = int(choice)
        if (not choice in range(1,10)):
            print("Choose between 1 to 9!")
            continue
        if (board[choice - 1] == 'X' or board[choice - 1] == 'O'):
            print("Occupied square!")
            continue
        return(choice)
    
def get_choice_computer(board, symbol):

    choice = check_win_possible(board, symbol)
    if (choice != -1):
        return(choice) #win

    debug_print("Checking block!")
    choice = check_win_possible(board, 'X')
    if (choice != -1):
        return(choice) #block

    #if middle square is available grab it
    if (board[4] == '5'):
        return(5)

    #grab corner if available:
    for i in [0,2,6,8]:
        if board[i] in '123456789':
            return (i + 1)
        
    #else grab any random square    
    while True:
        choice = random.randrange(1,10)
        if (board[choice - 1] == 'X' or board[choice - 1] == 'O'):
            #print("Occupied square!")
            continue
        else:
            return(choice)
            
    return(choice)
        
def reset_board():
    global board 
    board = ['1','2','3','4','5','6','7','8','9']

def play_game(start_player):
    reset_board()
    display_board(board)
    game_on = True
    current_player = start_player #'X'

    while game_on:
        if (board_full(board)):
            break
        print("Currently playing: ", current_player)
        if (current_player == 'X'):
            choice = get_choice_player(board,current_player)
        else:
            choice = get_choice_computer(board,current_player)
            debug_print("Comp choice ", choice)
            
        board[choice - 1] = current_player
        display_board(board)
        if (check_win(current_player)):
            game_on = False
            winner = current_player
            break
        #switch player
        if (current_player == 'X'):
            current_player = 'O'
        elif (current_player == 'O'):
            current_player = 'X'
    
    if (game_on):
        print("Draw!")
        return('D')
    else:
        print("{} is the winner!".format(winner))
        return(winner)


stats = {'X':0, 'O':0, 'D':0}

start_player = 'X'

i = 1
while(True):
    resp = input("Ready to start game {}?".format(i))
    if (resp in 'nN'):
        break
    stats[play_game(start_player)] += 1
    if start_player == 'X':
        start_player = 'O'
    else:
        start_player = 'X'
    i += 1

print("X won ", stats['X'], " games")
print("O won ", stats['O'], " games")
print(stats['D'], " games drawn")
    

