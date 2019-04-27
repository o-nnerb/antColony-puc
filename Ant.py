class Ant:
    path = []
    colony = 0

    def __init__(self, tourSize):
        self.path = []
        self.colony = 0
        
        self.isReverted = False
        self.oldPath = []

    def setColony(self, colony):
        # Here am I?
        self.colony = colony

    def move(self, toCity):
        if len(self.path) == 0:
            self.path.append((self.colony, toCity))
            return
        
        (origin, destiny) = self.path[len(self.path)-1]
        self.path.append((destiny, toCity))
    
    def visited(self, city):
        for (origin, destiny) in self.path:
            if destiny == city:
                return True
        
        return False

    def lastVisited(self):
        if len(self.path) == 0:
            return self.colony
        
        (origin, destiny) = self.path[len(self.path)-1]
        return destiny

    def lastStay(self):
        if len(self.path) == 0:
            return self.colony
        
        (origin, destiny) = self.path[len(self.path)-1]
        return origin

    def removePath(self, fromCity, toCity):
        remain = []

        for (origin, destiny) in self.path:
            remain.append((origin, destiny))
            print("remain", remain)
            if origin == fromCity:
                if toCity == toCity:
                    remain = []
            
            if destiny == fromCity:
                if origin == toCity:
                    remain = []

        self.path = remain
    def trailLength(self, graph):
        length = 0
        for (origin, destiny) in self.path:
            length += graph[origin][destiny]
        
        return length

    def clear(self, colony=0):
        self.path = []
        self.colony = colony
        self.isReverted = False
        self.oldPath = []

    isReverted = False
    oldPath = []
    def reverse(self):
        if len(self.path) == 0:
            return
        if self.isReverted:            
            (origin, destiny) = self.oldPath.pop()
            self.move(origin)
            return            

        self.oldPath = self.path
        (origin, destiny) = self.oldPath.pop()
        self.path = [(destiny, origin)]
        self.isReverted = True