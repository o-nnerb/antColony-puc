from Ant import Ant
from random import randint, random

class AntColonySettings:
    numberOfCities = 0
    numberOfAnts = 0
    graph = [[]]
    trails = [[]]
    ants = []
    probabilities = []

    def __init__(self):
        self.numberOfCities = 0
        self.numberOfAnts = 0
        self.graph = [[]]
        self.trails = [[]]
        self.ants = []
        self.probabilities = []

    @staticmethod
    def byGraph(graph, antFactor):
        self = AntColonySettings()
        self.graph = graph
        self.numberOfCities = len(self.graph)
        self.numberOfAnts = int(self.numberOfCities * antFactor)

        self.trails = [[0.0 for j in range(0, self.numberOfCities)] for i in range(0, self.numberOfCities)]
        self.probabilities = [0.0 for i in range(0, self.numberOfCities)]

        self.ants = [Ant(self.numberOfCities) for i in range(0, self.numberOfAnts)]
        return self
    
    @staticmethod
    def default(noOfCities, antFactor):
        return AntColonySettings.byGraph(AntColonySettings.randomMatrix(noOfCities), antFactor)
    
    @staticmethod
    def testCase1(antFactor):
        graph = [
            [0, 0, 75, 0, 25, 0, 10, 0],
            [0, 0, 10, 0, 20, 0, 35, 0],
            [75, 10, 0, 0, 0, 0, 0, 90],
            [0, 0, 0, 0, 100, 5, 0, 0],
            [25, 20, 45, 100, 0, 0, 75, 15],
            [0, 0, 0, 5, 0, 0, 0, 25],
            [10, 35, 0, 0, 75, 0, 0, 60],
            [0, 0, 90, 0, 15, 25, 60, 0]
        ]

        return AntColonySettings.byGraph(graph, antFactor)

    @staticmethod
    def testCase2(antFactor):
        graph = [
            [0, 1, 10, 20, 30, 40, 50, 1],
            [1, 0, 1, 10, 20, 30, 40, 50],
            [10, 1, 0, 1, 10, 20, 30, 40],
            [20, 10, 1, 0, 1, 10, 20, 30],
            [30, 20, 10, 1, 0, 1, 10, 20],
            [40, 30, 20, 10, 1, 0, 1, 10],
            [50, 40, 30, 20, 10, 1, 0, 1],
            [1, 50, 40, 30, 20, 10, 1, 0]
        ]

        for i in range(0, len(graph)):
            for j in range(0, len(graph[i])):
                if graph[i][j] >= 10:
                    graph[i][j] *= 100

        return AntColonySettings.byGraph(graph, antFactor)

    @staticmethod
    def randomMatrix(n):
        return [[(randint(0, 100-1) + 1) for j in range(0, n)] for i in range(0, n)]

    def range(self, atNode=-1):
        if atNode == -1:
            return [self.range(i) for i in range(0, self.numberOfCities)]

        return [i for i in range(0, len(self.graph[atNode])) if self.graph[atNode][i] > 0]

    def cities(self):
        return [i for i in range(0, self.numberOfCities) if len(self.graph[i]) >= 1]

    def citiesAfter(self, city):
        cities = self.cities()
        
        return [city] + [cities[i] for i in range(0, len(cities)) if cities[i] > city]
    
    def path(self, city):
        cities = self.cities()[city]
        return [i for i in range(0, len(self.graph[cities])) if self.graph[cities][i] > 0]

    def notInPath(self, city):
        cities = self.cities()
        paths = self.path(city)

        for city in paths:
            cities[city] = -1

        return [city for city in cities if city >= 0]

class AntColonyOptimization:
    c = 1.0                 # Number of trails, at the start of the simulation
    #alpha = 0.0001             # Controls the pheromone importance
    #beta = 0.005              # Controls the distance priority; Beta should be greater than alpha for best results
    #evaporation = 0.5       # Shows the percent how much pheromone is evaporating in each iteration
    Q = 500.0               # Provides information about the total amount of pheromone left on the trail by each Ant
    antFactor = 10         # How many ants per city
    #randomFactor = 0.01     # Little bit of randomness in our simulations
    maxIterations = 10000

    currentCity = 0
    firstCity = 0

    bestTourOrder = []
    bestTourLength = 0
    maxPath = 0

    settings = 0

    def randomFactor(self):
        return random() / 1000.0

    def evaporation(self):
        return random()% 0.51

    def beta(self):
        return random() * 5.0
    
    def alpha(self):
        return random() * 1.0

    def __init__(self):
        self.c = 1
        #self.alpha = 0.0005
        #self.beta = 10
        #self.evaporation = 0.5
        self.Q = 500.0
        self.antFactor = 0.8
        #self.randomFactor = 0.01
        
        self.maxIterations = 1000

        self.currentCity = 0
        self.firstCity = 0

        self.bestTourOrder = []
        self.bestTourLength = 0

        self.settings = 0
    
    @staticmethod
    def default(noOfCities):
        self = AntColonyOptimization()
        self.settings = AntColonySettings.default(noOfCities, self.antFactor)
        self.currentCity = self.settings.cities()[0]
        self.firstCity = self.currentCity
        return self

    @staticmethod
    def testCase(number):
        self = AntColonyOptimization()
        if number == 1:
            self.settings = AntColonySettings.testCase1(self.antFactor)
        if number == 2:
            self.settings = AntColonySettings.testCase2(self.antFactor)
        
        self.currentCity = self.settings.cities()[0]
        self.firstCity = self.currentCity
    
        return self

    def startAntOptimization(self):
        for i in range(1, 11):
            print("Attempt #" +str(i))
            self.solve()

    def solve(self):
        self.setupAnts()
        self.clearTrails()

        for i in range(0, self.maxIterations):
            self.moveAnts()
            self.updateTrails()
            self.restartAnts()
            self.updateBest()

        print("Best tour length: " + str(self.bestTourLength))
        print("Best tour order: " + str(self.bestTourOrder))
        print("Best lenght:", str([self.settings.graph[i[0]][i[1]] for i in self.bestTourOrder]))
        #print(self.settings.graph)
        return [self.bestTourOrder[i] for i in range(0, len(self.bestTourOrder))]

    def setupAnts(self):
        for ant in self.settings.ants:
            ant.clear(colony=self.firstCity)
        
        self.currentCity = self.firstCity
    
    def moveAnts(self):        
        for ant in self.settings.ants:
            #print(ant.path)
            if ant.isReverted:
                ant.reverse()
                #print("Ant reverted")
            else:
                nextCity = self.selectNextCity(ant)
                if nextCity >= 0:
                    ant.move(nextCity)
            #print(ant.path)
    
    def selectNextCity(self, ant):
        possiblePaths = self.settings.path(ant.lastVisited())

        t = possiblePaths[randint(0, len(possiblePaths) - 1)]

        if random() < self.randomFactor():
            if not ant.visited(t):
                return t

        probabilities = self.calculateProbabilities(ant)
        r = random()
        total = 0.0

        if not len(probabilities):
            #print("Ant dying")
            #ant.clear()
            ant.reverse()
            return -1
            raise Exception("There are no other cities")

        for (city, probability) in probabilities:
            total += probability
            if total >= r:
                return city
        
        return -1

    def calculateProbabilities(self, ant):
        last = ant.lastVisited()
        pheromone = 0.0  

        for path in self.settings.path(last):
            if not ant.visited(path):
                if not (path == ant.colony and ant.lastStay() == path):
                    pheromone += (self.settings.trails[last][path] ** self.alpha()) * ((1.0/self.settings.graph[last][path]) ** self.beta())
    
        probabilities = []

        for path in self.settings.path(last):
            if not ant.visited(path) and pheromone:
                if not (path == ant.colony and ant.lastStay() == path):
                    numerator = (self.settings.trails[last][path] ** self.alpha()) * ((1.0/self.settings.graph[last][path]) ** self.beta())
                    probabilities.append((path, float(numerator) / float(pheromone)))
        
        return probabilities

    def updateTrails(self):
        cities = self.settings.cities()
        
        for city in cities:
            for path in self.settings.path(city):
                self.settings.trails[city][path] *= self.evaporation()

        for ant in self.settings.ants:
            contribution = 0
            if len(ant.path):
                if ant.trailLength(self.settings.graph) == 0:
                    print(ant.path)
                contribution = self.Q / ant.trailLength(self.settings.graph)

            for (origin, destiny) in ant.path:
                self.settings.trails[origin][destiny] += contribution

    def updateBest(self):
        for ant in self.settings.ants:
            if len(ant.path) > 0:
                (origin, destiny) = ant.path[0]
                if origin == ant.colony:
                    if not self.bestTourLength or len(ant.path) > self.maxPath:
                        self.bestTourLength = ant.trailLength(self.settings.graph)
                        self.bestTourOrder = [a for a in ant.path]
                        self.maxPath = len(ant.path)
                    elif len(ant.path) == self.maxPath and ant.trailLength(self.settings.graph) < self.bestTourLength:
                        self.bestTourLength = ant.trailLength(self.settings.graph)
                        self.bestTourOrder = [a for a in ant.path]
                        self.maxPath = len(ant.path)
        
    def clearTrails(self):
        for city in self.settings.cities():
            for path in self.settings.path(city):
                self.settings.trails[city][path] = self.c

    def restartAnts(self):
        for ant in self.settings.ants:
            if ant.lastVisited() == ant.colony:
                #print("Ant is in colony")
                ant.clear(colony=ant.colony)
            else:
                if len(ant.path) == self.settings.numberOfCities-1:
                    path = self.settings.path(ant.lastVisited())
                    for city in path:
                        if city == ant.colony:
                            ant.move(city)
                            self.updateTrails()
                        
                        

AntColonyOptimization.testCase(1).startAntOptimization()