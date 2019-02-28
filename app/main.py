import os
import random
import time
import bottle

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
	return {
		'color': '#EAF0EA',
		'taunt': 'Wake up Blake, you\'re a snake',
		'head_url': headUrl
	}

@bottle.post('/move')
def move(data=None):
    if not data:
        data = bottle.request.json
    # Get all the data
    you = data['you']
    health = you["health"]
    mySize = len(you['body'])
    body = [(b['x'], b['y']) for b in you['body']]
    head = body[0]
    walls = (data['board']['width'], data['board']['height'])
    snakes = data['board']['snakes']
    size = []
    for s in snakes:
        size.append(len(s['body']))
    snakes = [s['body'] for s in snakes]
    snakes2 = []
    heads = []
    tails = []
    for s1 in snakes:
        heads.append((s1[0]['x'], s1[0]['y']))
        tails.append((s1[-1]['x'], s1[-1]['y']))
        for s2 in s1:
            snakes2.append((s2['x'], s2['y']))
    snakes = snakes2
    food = data['board']['food']
    food = [(f['x'], f['y']) for f in food]
    numFood = len(food)

    debug_print("Move Number:")
    debug_print("My Size:    ", mySize)
    debug_print("My Health:  ", health)

    try:
        move = None

        # Moving restrictions
        if mySize > 2:
            moves = get_restrictions(head, [body[-1]], mySize, walls, snakes, heads, size, tails, True)
        else:
            moves = get_restrictions(head, [], mySize, walls, snakes, heads, size, tails, True)
        debug_print("Restrictions:  ", moves)

        # Don't choose nothing that'll kill you next time
        if len(moves) > 1:

            movesCpy = list(moves)
            for m in movesCpy:
                nextHead = get_future_head(head, m)
                if mySize > 2:
                    nres = get_restrictions(nextHead, tails + [body[-2]], mySize, walls, snakes, heads, size, tails, False)
                else:
                    nres = get_restrictions(nextHead, list(tails).remove(body[-1]), mySize, walls, snakes, heads, size, tails, False)
                if (nres == []) and (len(moves) > 1):
                    moves.remove(m)
                    debug_print("Restrictions2: ", moves)



        # Take food as first preference if health is low
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
            moves = kill_others(head, mySize, heads, size, moves)
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
                move = flee_heads(moves, heads, head)
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
                move = flee_heads(moves, heads, head)
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


def get_future_head(head, move):

    if move == 'left':
        return (head[0] - 1, head[1])

    elif move == 'right':
        return (head[0] + 1, head[1])

    elif move == 'up':
        return (head[0], head[1] - 1)

    else:
        return (head[0], head[1] + 1)


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
        if pm in moves:
            return pm


def flee_heads(moves, heads, head):
    minManhattan = 999
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
def kill_others(head, mySize, heads, size, moves):

    validMoves = []

    for i, h in enumerate(heads):

        if size[i] < mySize:

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


def get_restrictions(head, ignore, mySize, walls, snakes, heads, size, tails, headScare=False):

    directions = {'up':1, 'down':1, 'left':1, 'right':1}

    # Don't hit a wall
    if head[0] == walls[0]-1:
        directions['right'] = 0

    elif head[0] == 0:
        directions['left'] = 0

    if head[1] == 0:
        directions['up'] = 0

    elif head[1] == walls[1]-1:
        directions['down'] = 0

    # Don't hit other snakes (Except for exceptions (tail etc))
    for s in snakes:
        if s not in ignore:
            xdist = abs(s[0]-head[0])
            ydist = abs(s[1]-head[1])

            if xdist + ydist == 1:

                if xdist == 1:

                    if s[0] > head[0]:
                        directions['right'] = 0

                    else:
                        directions['left'] = 0

                else:

                    if s[1] > head[1]:
                        directions['down'] = 0

                    else:
                        directions['up'] = 0

    directions2 = {key: value for key, value in directions.items()}

    # Be scared of the heads of others if they're scary
    for i, h in enumerate(heads):

        if not (size[i] < mySize):
            xdist = h[0]-head[0]
            ydist = h[1]-head[1]

            if abs(xdist) == 1 and abs(ydist) == 1:

                if xdist > 0:
                    directions['right'] = 0

                elif xdist < 0:
                    directions['left'] = 0

                if ydist > 0:
                    directions['down'] = 0

                elif ydist < 0:
                    directions['up'] = 0

            elif (abs(xdist) == 2 and ydist == 0) ^ (abs(ydist) == 2 and xdist == 0):

                if xdist == 2:
                    directions['right'] = 0

                elif xdist == -2:
                    directions['left'] = 0

                elif ydist == 2:
                    directions['down'] = 0

                else:
                    directions['up'] = 0

    # If there's no other choice but to possibly collide with a head
    if 1 not in directions.values() and headScare and mySize > 2:
        move = eat_tail(head, tails)
        if move:
            directions[move] = 1
        directions = directions2

    moves = [k for k in directions.keys() if directions[k] is 1]

    return moves

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
