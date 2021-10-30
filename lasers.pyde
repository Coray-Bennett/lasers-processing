PI = 3.14159265358979
MAX_LASERS = 1000

class Wall:
    def __init__(self, x, y, theta, leng, exists=True):
        self.x = x
        self.y = y
        self.leng = leng
        self.theta = theta
        self.exists = exists
        self.x2 = leng*cos(theta) + x
        self.y2 = leng*sin(-theta) + y
        
        
    def create(self):
        if(self.exists):
            stroke(0)
            line(self.x, self.y, self.x2, self.y2)

class Laser:
    def __init__(self, x, y, theta, leng=0, exists=True, collision=False, iter=0):
        self.x = x
        self.y = y
        self.leng = leng
        self.theta = theta
        self.exists = exists
        self.collision = collision
        self.x2 = leng*cos(theta) + x
        self.y2 = leng*sin(-theta) + y
        self.iter = iter
    
    def update(self):
        if(self.exists and not self.collision):
            self.leng += 1
            self.x2 = self.leng*cos(self.theta) + self.x
            self.y2 = self.leng*sin(-self.theta) + self.y
            stroke(255, 0, 0)
            line(self.x, self.y, self.x2, self.y2)
    def forceNoCollide(self):
        if(iter < 2):
            self.collision = False
            self.iter += 1


def testCollision(laser, wall):
    #from http://jeffreythompson.org/collision-detection/line-line.php, translated to python and implemented for my program
    (x1, y1, x2, y2) = (laser.x, laser.y, laser.x2, laser.y2)
    (x3, y3, x4, y4) = (wall.x, wall.y, wall.x2, wall.y2)
    try:
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    except ZeroDivisionError:
        return False
    
    if (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1):
        intersectionX = x1 + (uA * (x2-x1))
        intersectionY = y1 + (uA * (y2-y1))
        return intersectionX, intersectionY
    return False
    
def reflectTheta(laser, wall):
    rL = normalizeAngle(laser.theta)
    rW = normalizeAngle(wall.theta)
    return normalizeAngle((2*rW - rL))

def getQuadrant(theta):
    rW = normalizeAngle(theta)
    if(0 <= rW < PI/2): 
        q = 0
    elif(PI/2 <= rW < PI): 
        q = 1
    elif(PI <= rW < 3*PI/2): 
        q = 2
    elif(3*PI/2 <= rW < 2*PI):
        q = 3
    else:
        q = 0 
    return q

def normalizeAngle(theta):
    if(0 <= theta < 2*PI):
        return theta
    elif(theta > 2*PI):
        return normalizeAngle(theta - 2*PI)
    elif(theta < 2*PI):
        return normalizeAngle(theta + 2*PI)
        


levelWalls = [Wall(250, 750, 0, 500), 
              Wall(750, 750, PI/2, 500), 
              Wall(750, 250, PI, 500),
              Wall(250, 250, 3*PI/2, 500)]

levelLasers = [Laser(300, 300, PI/5.4545)]

def setup():
    size(1000, 1000)
    background(255)
    colorMode(HSB)
    for w in levelWalls:
        w.create()
    
def draw():
    for l in levelLasers:
        l.update()
        for w in levelWalls:
            instanceCollision = testCollision(l, w)
            if(instanceCollision != False and l.collision == False):
                l.collision = True
                refT = reflectTheta(l, w)
                if(len(levelLasers) < MAX_LASERS):
                    levelLasers.append(Laser(instanceCollision[0]+cos(refT), instanceCollision[1]+sin(-refT), reflectTheta(l, w)))

        
def main():
    testCollision(levelLasers[0], levelWalls[0])
main()
    
    
    
