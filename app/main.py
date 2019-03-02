import os
import random
import time
import bottle
import traceback

DEBUG = True

# The higher the quicker we start searching for food
HUNGRY = 60
# Starting search radius
FOOD_MIN = 1
# When we start searching our max radius
STARVING = 15
# Max searching radius
FOOD_MAX = 10

@bottle.route('/')
def static():

	return "the server is running"

@bottle.route('/static/<path:path>')
def static(path):
	return bottle.static_file(path, root='static/')

@bottle.post('/start')
def start():
    headUrl = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    print("\n\n\n\n\n\n")

    return {
        'color': '#EADA50',
        'taunt': 'Wake up Blake, you\'re a snake',
        'head_url': headUrl
    }

@bottle.post('/move')
def move(data=None):
    if not data:
        data = bottle.request.json
    print('-'*50)
    print('-'*50)
    # Get all the data
    you = data['you']
    health = you["health"]
    body = list(set([(b['x'], b['y']) for b in you['body']]))
    mySize = len(body)
    head = (you['body'][0]['x'], you['body'][0]['y'])
    walls = (data['board']['width'], data['board']['height'])

    snakesTogether = [ list(set([ ( b['x'], b['y'] ) for b in s['body'] ])) for s in data['board']['snakes'] ]
    snakeHeads = [ (b['body'][0]['x'], b['body'][0]['y']) for b in data['board']['snakes'] ]
    tails = [ (b['body'][-1]['x'], b['body'][-1]['y']) for b in data['board']['snakes'] ]
    snakeSizes =  [ len(s['body']) for s in data['board']['snakes'] ]
    snakes = []
    [ snakes.extend(s) for s in snakesTogether ]

    food = [(f['x'], f['y']) for f in data['board']['food']]
    numFood = len(food)

    debug_print("Move Number:")
    debug_print("My Size:    ", mySize)
    debug_print("My Health:  ", health)
    debug_print("My Body:    ", body)

    try:
        move = None
        moves = ['left', 'right', 'up', 'down']


        # Moving restrictions
        if mySize > 3:
            moves = dont_hit_wall(moves, head, walls)
            moves = dont_hit_snakes(moves, head, snakes, [body[-1]])
            moves = dont_get_eaten(moves, head, mySize, snakeHeads, snakeSizes)
        else:
            moves = dont_hit_wall(moves, head, walls)
            moves = dont_hit_snakes(moves, head, snakes, [])
            moves = dont_get_eaten(moves, head, mySize, snakeHeads, snakeSizes)
        debug_print("Restrictions:  ", moves)

        # Don't choose nothing that'll kill you next time
        if len(moves) > 1:
            tmpMoves = list(moves)
            for m in moves:
                nextHead = get_space(head, m)
                nextMoves = ['left', 'right', 'up', 'down']
                nextMoves = dont_hit_wall(nextMoves, head, walls)
                nextMoves = dont_hit_snakes(moves, head, snakes, [])
                if nextMoves == []:
                    tmpMoves.remove(m)
            if tmpMoves != []:
                moves = tmpMoves
        debug_print("Restrictions2: ", moves)

        # Take food as first preference if health is low or I'm smol
        if mySize < 6:
            health = health/2


        if have_choice(move, moves) and (health < HUNGRY):
            maxFood = round( (1 - ((health-STARVING) / (HUNGRY-STARVING))) * (FOOD_MAX-FOOD_MIN) )

            for i in reversed(range(1, maxFood)):
                if have_choice(move, moves):
                    moves = get_food(moves, head, food, i)
                    debug_print("Gimme Brunch {}:".format(i), moves)

        # Take killing others as preference
        if have_choice(move, moves):
            moves = kill_others(moves, head, mySize, snakeHeads, snakeSizes)
            debug_print("Kill Others:   ", moves)

        # Flee from a wall as preference
        if have_choice(move, moves):
            moves = flee_wall(moves, walls, head)
            debug_print("Flee Wall:     ", moves)

        # Flee others (including yourself) as preference
        if have_choice(move, moves):
            moves = flee_others(moves, [body[0], body[-1]], snakes, head, 1)
            debug_print("Flee Others:   ", moves)


        if mySize < 6:
            # Move away from the heads of others
            if have_choice(move, moves):
                move = flee_heads(moves, snakeHeads, head)
                debug_print("Flee Heads:    ", move)

            # Go straight as preference
            if have_choice(move, moves):
                move = go_straight(moves, head, body)
                debug_print("Go Straight:   ", move)

        else:
            # Go straight as preference
            if have_choice(move, moves):
                move = go_straight(moves, head, body)
                debug_print("Go Straight:   ", move)

            # Move away from the heads of others
            if have_choice(move, moves):
                move = flee_heads(moves, snakeHeads, head)
                debug_print("Flee Heads:    ", move)

        # Make a random choice for a move
        if have_choice(move, moves):
            move = random.choice(moves)
            debug_print("Random Choice:", move)

        # No suggested moves
        if move == None:

            # There is only one choice
            if len(moves) == 1:
                move = moves[0]
                debug_print("Only Choice:   ", move)

            # There is no choice
            else:
                move = eat_tail(head, tails)
                debug_print("Eat Tail:      ", move)
                if move == None:
                    move = 'up'
                    debug_print("Death:        ", move)

    except Exception as e:
        debug_print("ERROR: ", str(e))
        traceback.print_tb(e.__traceback__)
        if moves == []:
            move = "up"
            debug_print("ERROR: Going up")
        else:
            move = random.choice(moves)
            debug_print("ERROR: Random choice")

    debug_print("MOVE: ", move)

    return {
        'move': move,
        'taunt': 'Battle Jake!'
    }


def debug_print(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def have_choice(move, moves):
    if move != None:
        return False
    if len(moves) <= 1:
        return False
    return True


def get_space(space, move):

    if move == 'left':
        return (space[0] - 1, space[1])

    elif move == 'right':
        return (space[0] + 1, space[1])

    elif move == 'up':
        return (space[0], space[1] - 1)

    else:
        return (space[0], space[1] + 1)


def get_previous_move(head, second):

    if head[0] == second[0]:
        if head[1] > second[1]:
            return 'down'

        else:
            return 'up'
    else:
        if head[0] > second[0]:
            return 'right'

        else:
            return 'left'


def eat_tail(head, tails):
    for tail in tails:
        xdist = head[0] - tail[0]
        ydist = head[1] - tail[1]
        if abs(xdist) == 1 and ydist == 0:
            if xdist > 0:
                return 'left'
            else:
                return 'right'

        if abs(ydist) == 1 and xdist == 0:
            if ydist > 0:
                return 'up'
            else:
                return 'down'


def go_straight(moves, head, body):
    if len(body) > 1:
        pm = get_previous_move(head, body[1])
        print("Previous move", pm)
        if pm in moves:
            return pm


def flee_heads(moves, heads, head):
    minManhattan = 999
    heads.remove(head)
    for h in heads:
        xdist = h[0]-head[0]
        ydist = h[1]-head[1]

        manhattan = abs(xdist) + abs(ydist)
        if manhattan < minManhattan:
            minManhattan = manhattan
            if (abs(xdist) < abs(ydist)):
                if ('left' in moves) and (xdist > 0):
                    return 'left'

                if ('right' in moves) and (xdist < 0):
                    return 'right'
            else:
                if ('down' in moves) and (ydist < 0):
                    return 'down'

                if ('up' in moves) and (ydist > 0):
                    return 'up'


def flee_others(moves, delMoves, snakes, head, dist):

    prevMoves = list(moves)
    validMoves = list(moves)
    for s in snakes:
        if s not in delMoves:
            for m in moves:
                fh = get_space(head, m)
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
    if head[0] >= walls[0]-1:
        if 'left' in moves:
            return ['left']

    elif head[0] <= 0:
        if 'right' in moves:
            return ['right']

    if head[1] <= 0:
        if 'down' in moves:
            return ['down']

    elif head[1] >= walls[1]-1:
        if 'up' in moves:
            return ['up']

    validMoves = list(moves)

    # Keep 1 space buffer between you and the wall
    if head[0] >= walls[0]-2:
        if 'right' in moves:
            validMoves.remove('right')

    elif head[0] <= 1:
        if 'left' in moves:
            validMoves.remove('left')

    if len(moves) > 1:

        if head[1] <= 1:
            if 'up' in moves:
                validMoves.remove('up')

        elif head[1] >= walls[1]-2:
            if 'down' in moves:
                validMoves.remove('down')


    if validMoves == []:
        return moves
    return validMoves


# If you're bigger than other snake, kill them
def kill_others(moves, head, mySize, snakeHeads, snakeSizes):
    validMoves = []
    for i, h in enumerate(snakeHeads):

        if snakeSizes[i] < mySize:
            xdist = h[0]-head[0]
            ydist = h[1]-head[1]

            if (abs(xdist) == 1) and (abs(ydist) == 1):
                if xdist > 0 and 'right' in moves:
                    validMoves.append('right')

                elif xdist < 0 and 'left' in moves:
                    validMoves.append('left')

                if ydist > 0 and 'down' in moves:
                    validMoves.append('down')

                elif ydist < 0 and 'up' in moves:
                    validMoves.append('up')

            elif (abs(xdist) == 2 and ydist == 0) or (abs(ydist) == 2 and xdist == 0):
                if xdist == 2 and 'right' in moves:
                    validMoves.append('right')

                elif xdist == -2 and 'left' in moves:
                    validMoves.append('left')

                elif ydist == 2 and 'down' in moves:
                    validMoves.append('down')

                elif 'up' in moves:
                    validMoves.append('up')

    if validMoves == []:
        return moves
    return list(set(validMoves))


def get_food(moves, head, food, dist):
    validMoves = []
    for f in food:
        xdist = f[0]-head[0]
        ydist = f[1]-head[1]

        if (abs(xdist) + abs(ydist)) <= dist:

            if xdist > 0 and 'right' in moves:
                validMoves.append('right')

            elif xdist < 0 and 'left' in moves:
                validMoves.append('left')

            elif ydist > 0 and 'down' in moves:
                validMoves.append('down')

            elif ydist < 0 and 'up' in moves:
                validMoves.append('up')

    if validMoves == []:
        return moves
    return list(set(validMoves))


def dont_hit_wall(moves, head, walls):
    if head[0] == walls[0]-1 and 'right' in moves:
        moves.remove('right')

    elif head[0] == 0 and 'left' in moves:
        moves.remove('left')

    if head[1] == 0 and 'up' in moves:
        moves.remove('up')

    elif head[1] == walls[1]-1 and 'down' in moves:
        moves.remove('down')

    return moves


def dont_hit_snakes(moves, head, snakes, ignore):
    if get_space(head, 'left') in snakes and 'left' in moves:
        moves.remove('left')

    if get_space(head, 'right') in snakes and 'right' in moves:
        moves.remove('right')

    if get_space(head, 'up') in snakes and 'up' in moves:
        moves.remove('up')

    if get_space(head, 'down') in snakes and 'down' in moves:
        moves.remove('down')

    return moves


def dont_get_eaten(moves, head, mySize, snakeHeads, snakeSizes):

    prevMoves = list(moves)

    for i, h in enumerate(snakeHeads):
        if (snakeSizes[i] >= mySize):
            xdist = h[0]-head[0]
            ydist = h[1]-head[1]

            if abs(xdist) == 1 and abs(ydist) == 1:

                if xdist > 0:
                    moves.remove('right')

                elif xdist < 0:
                    moves.remove('left')

                if ydist > 0:
                    moves.remove('down')

                elif ydist < 0:
                    moves.remove('up')

            elif (abs(xdist) == 2 and ydist == 0) ^ (abs(ydist) == 2 and xdist == 0):

                if xdist == 2:
                    moves.remove('right')

                elif xdist == -2:
                    moves.remove('left')

                elif ydist == 2:
                    moves.remove('down')

                else:
                    moves.remove('up')

        if moves == []:
            moves = prevMoves
        return moves


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
