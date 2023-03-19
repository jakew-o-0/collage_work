directions = [[-1, -1], [1, 1],     # diagonal in \ direction
              [1, -1], [-1, 1],     # diagonal in / direction
              [1, 0], [-1, 0],      # virtical
              [0, 1], [0, -1]]      # horizontal

board = [[1,1,0],
         [0,1,0],
         [1,0,1]]




def calc_new_pos(pos, direction):
        new_pos = [0,0]

        new_pos[0] = pos[0] + direction[0]
        new_pos[1] = pos[1] + direction[1]

        return new_pos




def check_win_cond(board, pos, direction, player):

    # base cases
    #
    if(pos[0] >= len(board[0]) or pos[0] < 0):
        return 0

    if(pos[1] >= len(board) or pos[1] < 0):
        return 0

    if(board[pos[1]][pos[0]] != player):
        return 0

    if(direction is not None):
        new_pos = calc_new_pos(pos, direction)
        return 1 + check_win_cond(board, new_pos, direction, player)


    # recurse
    #
    count = 0                   # counts the itterations in the loop
    for i in directions:
        if(count % 2 == 0):     # resets total_corect when the direction changes (every two changes)
            total_correct = 1


        new_pos = calc_new_pos(pos, direction)      # calculatest the position in a given position
        if(total_correct + check_win_cond(board, new_pos, i, player) == 3): # checks if the given direction is equal to to the win condition
            return 1

    return 0

print(check_win_cond(board, [0,0], None, 1))