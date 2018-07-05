import os
import sys
import json

INPUT_FOLDER = ""
OUTPUT_FOLDER = ""


os.mkdir(OUTPUT_FOLDER)

for f in os.listdir(INPUT_FOLDER):
    
    file = OUTPUT_FOLDER + "/" + f
    
    with open(file, "r") as input:
        
        dict = json.reads(input.next())
        
        snakes = dict["snakes"]
        
        for s in snakes:
            
        
        
        
        