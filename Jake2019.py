import os
import random
import time

STARVING = 45
HUNGRY = 55
MEH_COULD_EAT = 60

def move(data):
    # Get all the data
    you = data['you']
    health = you["health"]
    mySize = you['length']
    body = [(b['x'], b['y']) for b in you['body']['data']]
    head = body[0]
    walls = (data['width'], data['height'])
    snakes = data['snakes']['data']
    size = []
    for s in snakes:
        size.append(s['length'])
    snakes = [s['body']['data'] for s in snakes]
    snakes2 = []
    heads = []
    for s1 in snakes:
        heads.append((s1[0]['x'], s1[0]['y']))
        for s2 in s1:
            snakes2.append((s2['x'], s2['y']))
    snakes = snakes2
    food = data['food']['data']
    food = [(f['x'], f['y']) for f in food]
    numFood = len(food)
    try:
        pm = get_previous_move(head, body[1])
    except:

        moves = get_restrictions(head, mySize, walls, snakes, heads, size)
        if moves == []:
            return {"move": "up"}
        else:
            return {"move": random.choice(moves)}


    try:
        move = None

        # Moving restrictions
        moves = get_restrictions(head, mySize, walls, snakes, heads, size)

        # Don't choose nothing that'll kill you next time
        if ( len(moves) > 1 ):

            movesCpy = list(moves)
            for m in movesCpy:
                nextHead = get_future_head(head, m)
                nres = get_restrictions(nextHead, mySize, walls, snakes, heads, size, op=False)
                if nres == [] and len(moves) > 1:
                    moves.remove(m)

        # Take food as first preference if health is low
        if(have_choice(move, moves) and health < STARVING):
            moves = get_food(moves, head, food, 3)

        if(have_choice(move, moves) and health < HUNGRY):
            moves = get_food(moves, head, food, 2)

        # Flee from a wall as preference
        if(have_choice(move, moves)):
            moves = flee_wall(moves, walls, head)

        # Flee others (including yourself) as preference
        if(have_choice(move, moves)):
            moves = flee_others(moves, [body[0], body[-1]], snakes, head, 1)

        # Take killing others as preference
        if(have_choice(move, moves)):
            moves = kill_others(head, mySize, heads, size, moves)

        # Take local food as preference if health could use a touchup
        if(have_choice(move, moves) and health < MEH_COULD_EAT):
            moves = get_food(moves, head, food, 1)

        # Go straight as preference
        if(pm in moves or moves == []):
            move = pm

        # Make a random choice for a move
        else:
            move = random.choice(moves)

    except Exception as e:
        raise(e)
        if moves == []:
            move = "up"
        else:
            move = random.choice(moves)

    return {
        'move': move,
        'taunt': 'Battle Jake!'
    }

def have_choice(move, moves):
    if len(moves) <= 1:
        return False
    return True


def get_future_head(head, move):

    if(move == 'left'):
        return (head[0] - 1, head[1])

    elif(move == 'right'):
        return (head[0] + 1, head[1])

    elif(move == 'up'):
        return (head[0], head[1] - 1)

    else:
        return (head[0], head[1] + 1)


def get_previous_move(head, second):

    if(head[0] == second[0]):
        if(head[1] > second[1]):
            return 'down'

        else:
            return 'up'
    else:
        if(head[0] > second[0]):
            return 'right'

        else:
            return 'left'


def flee_others(moves, delMoves, snakes, head, dist):

    prevMoves = list(moves)
    validMoves = list(moves)
    for s in snakes:
        if s not in delMoves:
            for m in moves:
                fh = get_future_head(head, m)
                xdist = s[0]-fh[0]
                ydist = s[1]-fh[1]

                # If the future head is beside a snake
                if (abs(xdist) == dist and ydist == 0) or (abs(ydist) == dist and xdist == 0):
                    validMoves.remove(m)
            moves = validMoves

    if moves == []:
        return prevMoves
    return moves


def flee_wall(moves, walls, head):

    # Flee the wall if I'm against it
    if(head[0] >= walls[0]-1):
        if 'left' in moves:
            return ['left']

    elif(head[0] <= 0):
        if 'right' in moves:
            return ['right']

    if(head[1] <= 0):
        if 'down' in moves:
            return ['down']

    elif(head[1] >= walls[1]-1):
        if 'up' in moves:
            return ['up']

    validMoves = list(moves)

    # Keep 1 space buffer between you and the wall
    if(head[0] >= walls[0]-2):
        if 'right' in moves:
            validMoves.remove('right')

    elif(head[0] <= 1):
        if 'left' in moves:
            validMoves.remove('left')

    if len(moves) > 1:

        if(head[1] <= 1):
            if 'up' in moves:
                validMoves.remove('up')

        elif(head[1] >= walls[1]-2):
            if 'down' in moves:
                validMoves.remove('down')


    if validMoves == []:
        return moves
    return validMoves


# If you're bigger than other snake, kill them
def kill_others(head, mySize, heads, size, moves):

    validMoves = []

    for i, h in enumerate(heads):

        if(size[i] < mySize):

            xdist = h[0]-head[0]
            ydist = h[1]-head[1]

            if(abs(xdist) == 1 and abs(ydist) == 1):

                if(xdist > 0 and 'right' in moves):
                    validMoves.append('right')

                elif(xdist < 0 and 'left' in moves):
                    validMoves.append('left')

                if(ydist > 0 and 'down' in moves):
                    validMoves.append('down')

                elif(ydist < 0 and 'up' in moves):
                    validMoves.append('up')

            elif((abs(xdist) == 2 and ydist == 0) ^ (abs(ydist) == 2 and xdist == 0)):

                if(xdist == 2 and 'right' in moves):
                    validMoves.append('right')

                elif(xdist == -2 and 'left' in moves):
                    validMoves.append('left')

                elif(ydist == 2 and 'down' in moves):
                    validMoves.append('down')

                elif('up' in moves):
                    validMoves.append('up')

    if validMoves == []:
        return moves
    return validMoves


def get_food(moves, head, food, dist):

    validMoves = []

    for f in food:
        xdist = f[0]-head[0]
        ydist = f[1]-head[1]

        if((abs(xdist) == dist and ydist == 0) ^ (abs(ydist) == dist and xdist == 0)):

            if(xdist == dist and 'right' in moves):
                validMoves.append('right')

            elif(xdist == -dist and 'left' in moves):
                validMoves.append('left')

            elif(ydist == dist and 'down' in moves):
                validMoves.append('down')

            elif(ydist == -dist and 'up' in moves):
                validMoves.append('up')

    if validMoves == []:
        return moves
    return validMoves


def get_restrictions(head, mySize, walls, snakes, heads, size, op=True):

    directions = {'up':1, 'down':1, 'left':1, 'right':1}

    # Don't hit a wall
    if(head[0] == walls[0]-1):
        directions['right'] = 0

    elif(head[0] == 0):
        directions['left'] = 0

    if(head[1] == 0):
        directions['up'] = 0

    elif(head[1] == walls[1]-1):
        directions['down'] = 0

    # Don't hit other snakes
    for s in snakes:
        xdist = abs(s[0]-head[0])
        ydist = abs(s[1]-head[1])

        if(xdist + ydist == 1):

            if(xdist == 1):

                if(s[0] > head[0]):
                    directions['right'] = 0

                else:
                    directions['left'] = 0

            else:

                if(s[1] > head[1]):
                    directions['down'] = 0

                else:
                    directions['up'] = 0

    directions2 = {key: value for key, value in directions.items()}

    # Be scared of the heads of others if they're scary
    for i, h in enumerate(heads):

        if(not (size[i] < mySize)):
            xdist = h[0]-head[0]
            ydist = h[1]-head[1]

            if(abs(xdist) == 1 and abs(ydist) == 1):

                if(xdist > 0):
                    directions['right'] = 0

                elif(xdist < 0):
                    directions['left'] = 0

                if(ydist > 0):
                    directions['down'] = 0

                elif(ydist < 0):
                    directions['up'] = 0

            elif((abs(xdist) == 2 and ydist == 0) ^ (abs(ydist) == 2 and xdist == 0)):

                if(xdist == 2):
                    directions['right'] = 0

                elif(xdist == -2):
                    directions['left'] = 0

                elif(ydist == 2):
                    directions['down'] = 0

                else:
                    directions['up'] = 0

    # If there's no other choice but to possibly collide with a head
    if(1 not in directions.values() and op):
        directions = directions2

    if not op:
        directions = directions2

    moves = [k for k in directions.keys() if directions[k] is 1]

    return moves
