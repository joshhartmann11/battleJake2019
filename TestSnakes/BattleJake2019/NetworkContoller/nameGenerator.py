import random

animals = ['Ardvark', 'Albatros', 'Donkey', 'Baboon', 'Antelope', 'Badger', 'Beaver', 'Bison', 'Camel', 'Cheetah', 
'Chinchilla', 'Coyote', 'Dogfish', 'Dolphin', 'Elephant', 'Emu', 'Falcon', 'Fox', 'Gazelle', 'Giraffe', 'Goose', 
'Gorilla', 'Hamster', 'Hedgehog', 'Heron', 'Hippo', 'Ibex', 'Jellyfish', 'Kangaroo', 'Koala', 'Leopard', 'Lion', 
'Loris', 'Mammoth', 'Mongoose', 'Monkey', 'Moose', 'Mosquito', 'Narwal', 'Opossum', 'Octopus', 'Ostrich', 'Otter', 
'Panther', 'Penguin', 'Porpoise', 'Raccoon', 'Rabbit', 'Rhinoceros', 'Shark', 'Squirrel', 'Turkey', 'Walrus']

adjectives = ['Attractive', 'Chubby', 'Clever', 'Helpful', 'Powerful', 'Agressive', 'Ambitious', 'Brave', 'Faithful',
'Gentle', 'Happy', 'Kind', 'Polite', 'Proud', 'Witty', 'Angry', 'Grumpy', 'Lazy', 'Scary', 'Uptight', 'Skinny',
'Modern', 'Young', 'Slow', 'Bitter', 'Damp']

def generate_name():
    return(random.choice(adjectives) + " " + random.choice(animals))
