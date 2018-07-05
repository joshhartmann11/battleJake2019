"""
This file must be in the same folder as the BattleSnake.py file (to make things simple)
GetTrainingData gets the JSON input/output data from games played
"""

import argparse
import os
import sys
import time
from BattleSnake import *


# Parses the input arguments
def parse_arguments():
    parser = argparse.ArgumentParser("Produces the JSON files from games played")
    parser.add_argument("-o", "--output", default="output", help="The output folder of the input/output \
vectors")
    parser.add_argument("-w", "--width", default=20, type=int, help="The width of the game board")
    parser.add_argument("-t", "--height", default=20, type=int, help="The height of the game board")
    parser.add_argument("-f", "--food", default=20, type=int, help="The amount of food in the arena")
    parser.add_argument("-n", "--games", default=1, type=int, help="The number of games to play")
    args = parser.parse_args()
    args.output = os.path.abspath(args.output)
    return args


# Sets up a game with the classic boys
def setup_game(gameNumber, outputFolder, width=20, height=20, food=20):
    s = BattleSnake(food=food, dims=[width,height])
    s.add_snake(Snake("SimpleJake", color=COLORS["cyan"]), SimpleJake())
    s.add_snake(Snake("MitchellNursey", color=COLORS["yellow"]), MitchellNursey())
    s.add_snake(Snake("MimicMitchellNursey", color=COLORS["yellow"]), MimicMitchellNursey(gameNumber, outputFolder))
    s.add_snake(Snake("SajanDinsa", color=COLORS["red"]), SajanDinsa())
    s.add_snake(Snake("Jake2018", color=COLORS["blue"]), Jake2018())
    return s


# Starts the game to run as fast as possible, without throwing errors and with 
# output piped to /dev/null
def start_single_game(game):
    try:
        with open(os.devnull, 'w') as devnull:
            sys.stdout = devnull
            game.start_game(speed=100, outputBoard=False, debug=False)
        sys.stdout = sys.__stdout__
    except:
        sys.stdout = sys.__stdout__


# Starts the loop to run all the games
def start_games(args):
    t = time.time()
    for gameNumber in range(args.games):
        print("Game Number: {0} | Completed: {1:.2f}% | Time Elapsed: {2:.0f}s".format(gameNumber,
              gameNumber*100/args.games, time.time()-t), end="\r")
        game = setup_game(gameNumber, args.output, args.width, args.height, args.food)
        start_single_game(game)

# The main function of execution
def main():
    args = parse_arguments()
    os.makedirs(args.output, exist_ok=True)
    start_games(args)

if __name__ == "__main__":
    main()
