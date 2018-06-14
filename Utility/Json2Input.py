import os
import sys
import json
import numpy as np

INPUT_FOLDER = "moveDatabase"
OUTPUT_FOLDER = "input"

WIDTH = 20
HEIGHT = 20

def merge_lists(lists):
    merged = []
    [merged.extend(k) for k in lists]
    return merged

def encode_xy_list(xyList, x=WIDTH, y=HEIGHT, onValue=1):
    output = np.zeros(x*y)
    for xy in xyList:
        index = xy["x"] + WIDTH*xy["y"]
        output[index] = 1
    return output

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
    

def encode_output_vector(inputDict):
    output = np.zeros(4)
    choices = ("up", "right", "down", "left")  
    index = choices.index(inputDict["choice"])
    output[index] = 1
    return output

def output_file_name_transformation(inputFile):
    return os.path.join(OUTPUT_FOLDER, os.path.basename(inputFile))

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
            print("\lfFailed on {0}".format(inFile))
            raise exception

    print("Completed Transformation...")

if __name__ == "__main__":
    main()
            

        
        
        
        
