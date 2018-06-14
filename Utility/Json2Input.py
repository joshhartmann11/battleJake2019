"""
Converts JSON output from a snake (and an extra move field) into the input and output
vectors for a neural network
"""

import os
import sys
import json
import argparse
import numpy as np

# Parses the arguments
def get_input():
    parser = argparse.ArgumentParser("Converts JSON output from a snake (and an extra move field) \
into the input and output vectors for a neural network")
    parser.add_argument("-i", "--input", default=".", help="The input folder consisting of files with\
battlesnake JSON")
    parser.add_argument("-o", "--output", default="output", help="The output folder of the input/output\
vectors")
    parser.add_argument("-w", "--width", default=20, type=int, help="The width of the game board")
    parser.add_argument("-h", "--height", default=20, type=int, help="The height of the game board")

    args = parser.parse_args()
    return args

# Merges a list of lists
def merge_lists(lists):
    merged = []
    [merged.extend(k) for k in lists]
    return merged

# Encodes a list of x,y dictionaries into a vector
def encode_xy_list(xyList, x=WIDTH, y=HEIGHT, onValue=1):
    output = np.zeros(x*y)
    for xy in xyList:
        index = xy["x"] + WIDTH*xy["y"]
        output[index] = 1
    return output

# Encodes, from the JSON, the input vector
def encode_input_vector(inputDict):
    you = inputDict["you"]["body"]["data"]
    you = encode_xy_list(you)

    head = inputDict["you"]["body"]["data"][0]
    head = encode_xy_list([head])

    health = inputDict["you"]["health"]

    food = inputDict["food"]["data"]
    food = encode_xy_list(food, onValue=health/100)

    snakes = [snake["body"]["data"] for snake in inputDict["snakes"]["data"]]
    snakes = encode_xy_list(merge_lists(snakes))

    return np.concatenate((food, head, you, snakes))
    
# Encodes, from the JSON, the output vector
def encode_output_vector(inputDict):
    output = np.zeros(4)
    choices = ("up", "right", "down", "left")  
    index = choices.index(inputDict["choice"])
    output[index] = 1
    return output

# Makes a transformation on the input file name to the output file name
def output_file_name_transformation(inputFile):
    return os.path.join(OUTPUT_FOLDER, os.path.basename(inputFile))

# Transforms a file from JSON to input and output vectors
def transform_file(inFile, outFile):
    os.makedirs(os.path.dirname(outFile), exist_ok=True)

    with open(inFile, "r") as inputFile:
        inputDict = json.loads(inputFile.read())

    inputVector = encode_input_vector(inputDict)
    outputVector = encode_output_vector(inputDict)

    outputDict = {
        "input": list(inputVector),
        "output": list(outputVector)
    }

    with open(outFile, "w") as outputFile:
        outputFile.write(json.dumps(outputDict))

# The main excecution function
def main():
    print("Starting Transformation...")

    files = os.listdir(INPUT_FOLDER)
    numFiles = len(files)

    print("Finished Listing Files...")

    files = [os.path.abspath(os.path.join(INPUT_FOLDER, f)) for f in files]

    print("Finished File Path Conversions...")

    for fileNum, inFile in enumerate(files):
        try:
            print("Progress: {0}/{1}\r".format(fileNum,numFiles), end="")
            outFile = os.path.abspath(output_file_name_transformation(inFile))
            transform_file(inFile, outFile)
        except Exception as exception:
            print("\nFailed on {0}".format(inFile))
            raise exception

    print("Completed Transformation...")

if __name__ == "__main__":
    main()
            