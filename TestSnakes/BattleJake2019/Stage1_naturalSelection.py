import math
import random
import time
from multiprocessing.dummy import Pool
import Stage1
from NetworkController.MLP import MLP

DATA_FOLDER = Stage1.DATA_FOLDER

class StageOneNS():

    TEST_SIZE = 100

    class Creature():
        def __init__(self, layers):
            self.score = None
            self.layers = layers

        def __lt__(self, other):
            return self.score < other.score
        def __gt__(self, other):
            return self.score > other.score
        def __eq__(self, other):
            return self.score == other.score
        def __ne__(self, other):
            return not self.score == other.score

        def getMLP(self):
            return MLP(self.layers)

    def __init__(self, competitors=10, fathers=2, change=1.5, maxLay=8, minLay=2, inNum=1600, outNum=4, verbose=False):
        self.fathers = fathers
        self.change = change
        self.inputLen = 1600
        self.outputLen = 4
        self.maxLay = maxLay
        self.minLay = minLay
        self.verbose = verbose
        self.creatures = [self._get_random_creature() for i in range(competitors)]

    def _pprint(self, msg):
        if self.verbose:
            print("[{0}: StageOneNS] {1}".format(time.strftime("%Y-%m-%d %H:%M"), msg))

    def _truncated_random_normal(self, mu, sigma, min, max):
        number = round(random.gauss(mu, sigma))
        while(number < min and number > max):
            number = round(random.gauss(mu, sigma))
        return number

    #FIXME: Add next
    def _random_layers(self, mus, sigma):
        resLay = []
        previous = self.inputLen
        for mu in mus:
            previous = self._truncated_random_normal(mu, sigma, self.outputLen, previous)
            resLay.append(previous)
        return resLay

    def _get_random_creature(self):
        sigma = 2 * self.change # Double the change for the first bit
        layers_mu = (self.maxLay + self.minLay)/2
        layNum = self._truncated_random_normal(layers_mu, sigma, self.minLay, self.maxLay)
        step = int((self.inputLen-self.outputLen)/(layNum+2))
        hidden_mus = list(reversed(range(self.outputLen, self.inputLen, step)))[1:-1]
        sigma = (step/6) * sigma # step/4 withing 99.7 of previous mu for sigma 1
        layers = self._random_layers(hidden_mus, sigma)
        return self.Creature([self.inputLen, *layers, self.outputLen])

    def _random_mutation(self, creature):
        child = self.Creature(creature.layers)

        # Adding/Deleting a layer
        hiddenLayersMu = len(child.layers)-2
        sigma = self.change
        mutLayNum = self._truncated_random_normal(hiddenLayersMu, sigma, self.minLay, self.maxLay)
        layChange = mutLayNum - hiddenLayersMu

        # Inserting/Deleting layers
        if layChange > 0:
            insertLayer = random.choice(range(hiddenLayersMu))
            newLayerSize = int((child.layers[insertLayer] + child.layers[insertLayer])/2)
            child.layers = child.layers[:insertLayer] + [newLayerSize] + child.layers[insertLayer:]
        elif layChange < 0:
            delLayer = random.choice(range(hiddenLayersMu))
            child.layers = child.layers[0:delLayer] + child.layers[delLayer+1:]

        # Mutating layer size
        step = int((self.inputLen-self.outputLen)/(mutLayNum+2))
        sigma = (step/6) * sigma
        layers = self._random_layers(child.layers[1:-1], sigma)

        return self.Creature([self.inputLen, *layers, self.outputLen])

    # FIXME: Fix for non fathers !| creatures
    def _kill_and_mutate(self):
        competitors = len(self.creatures)
        self.creatures.sort()
        self._pprint("Creature Scores: " + str([cre.score for cre in self.creatures]))
        self._pprint("Best Network in Generation: " + str(self.creatures[0].layers))
        self.creatures[0:self.fathers]
        offspring = int(len(self.creatures)/self.fathers)
        newCreatures = list(self.creatures)
        for cre in self.creatures:
            cre.score = None
            for off in range(offspring):
                newCreatures.append(self._random_mutation(cre))

    def _test_session(self, nn):
        inputs = []
        outputs = []
        self._pprint("Testing Session")
        for i in range(self.TEST_SIZE):
            tmp = Stage1.StageOne(MLP([1,1]) , DATA_FOLDER, save=False)
            inp, out = tmp.get_input_output()
            inputs.append(inp)
            outputs.append(out)
        return nn.test_network(inputs, outputs)

    def _training_session(self, creature):
        nn = creature.getMLP()
        stage1 = Stage1.StageOne(nn, DATA_FOLDER, save=False)
        self._pprint("Itteration 0")
        stage1.train(0.01, 50, 1, 1.1)
        self._pprint("Itteration 1")
        stage1.train(0.005, 100, 2, 1.1)
        self._pprint("Itteration 2")
        stage1.train(0.001, 100, 4, 1.1)
        self._pprint("Itteration 3")
        stage1.train(0.0005, 250, 10, 1.1)
        self._pprint("Itteration 4")
        stage1.train(0.0001, 60, 20, 1.1)
        return(stage1.nn)

    def run_generation(self):
        self._pprint("Creatures:\n" + str("\n".join([str(c.layers) for c in self.creatures])))
        pool = Pool(3)
        self._pprint("Training Networks...")
        resultingNNs = pool.map(self._training_session, self.creatures)
        self._pprint("Getting Scores...")
        resultingScores = pool.map(self._test_session, resultingNNs)
        for cre in range(len(self.creatures)):
            self.creatures[cre].score = resultingScores[cre]
        self._kill_and_mutate()


if __name__ == "__main__":
     ns = StageOneNS(verbose=True)
     while True:
         ns.run_generation()
         print("GENERATION COMPLETE!!! HOLY CRAP!!! THIS IS NUTS!!!")
