import time
import cmath
import Intersection_Manager_class as IMC

import numpy




# helper functions
def expect(c, b, a):
    if (a == 0):
        a = 0.0000002
    a = a / 2.0
    d = (b ** 2) - (4.0 * a * c)
    # find two solutions
    sol1 = (-b - cmath.sqrt(d)) / (2.0 * a)
    sol2 = round(abs(((-b + cmath.sqrt(d)) / (2.0 * a))), 3)
    #print('The solution are {0} and {1}'.format(sol1, sol2.__abs__()))
    return sol2.__abs__()


class Reservation:

    def __init__(self, VIN, speed, accel, enterTime, lane, t, l, w):
        self.vin = VIN
        self.speed = speed
        self.accel = accel

        # used for search
        self.originalAccel = accel

        self.OriginalExpectedTime = int(enterTime + expect(IMC.Intersection_Manager.p1_distance, self.speed, self.originalAccel) * 1000)  # to middle of first qm  , changed to enter tom from time()
        self.OriginalExpectedTime2 = int(enterTime + expect(IMC.Intersection_Manager.p2_distance, self.speed, self.originalAccel) * 1000)
        self.edgeOfSearch = 0.0




        self.enter = 0  # 0 if entering -- 1 if exiting

        self.enterTime = enterTime
        self.expectedTime = int(enterTime + expect(IMC.Intersection_Manager.p1_distance, self.speed, self.accel) * 1000)  # to middle of first qm  , changed to enter tom from time()
        self.expectedTime2 = int(enterTime + expect(IMC.Intersection_Manager.p2_distance, self.speed, self.accel) * 1000)


        self.nextt = None
        self.prev = None


        self.lane = lane
        self.turn = t

        self.requestedAccel = 0
        self.set = 0

        self.length = l
        self.width = w


        #outro data
        self.endSpeed = 0.0
        self.z = 2500
        self.zMax = 25000
        self.t1 = self.enterTime + self.z
        self.OutAccel = 0.0

    def updateZ(self,zed):
        self.updateSpeed()
        self.z = zed
        self.t1 = self.expectedTime2 + self.z
        a3 = ((35.0 - self.endSpeed) / (self.z / 1000.0))
        self.OutAccel = a3 - self.accel

    def updateSpeed(self):
        dt = (self.expectedTime2 - self.enterTime) / 1000.0
        self.endSpeed = self.speed + (self.accel * dt)

    def toString(self):
        t = self.expectedTime - self.enterTime
        if self.expectedTime2 != None:
            t2 = self.expectedTime2 - self.enterTime
        else:
            t2 = "na"
        return ("[ Vin: " + str(self.vin) + " ,speed: " + str(self.speed) + " ,accel: " + str(
            self.accel) + " ,Entered time: " + str(self.enterTime) + " ,Lane #: " + str(
            self.lane) + " ,turn #: " + str(
            self.turn) + " ,Expected time #: " + str(self.expectedTime) + " ,Expected time2 #: " + str(self.expectedTime2) + " ,requested accel #: " + str(
            self.requestedAccel) + "time to P1: " + str(t) + "time to P2: " + str(t2)  +"]")

class Intersection:


    # car criteria
    car_max_accel = 8

    car_max_speed = 125

    # Intersection Criteria
    inter_side_length = 200
    inter_size = 20
    inter_max_speed = 20
    inter_tolerance_time = 0.6  # intersection_side_length/[(max_Speed + min_speed)/2] (0.12s)  ---only 1 car in an in
    p1 = inter_side_length - (inter_size / 2)
    p2 = inter_side_length + (inter_size / 2)
   # PEND = inter_size * 2
    # set up
    starTime = 0

    #useful for manager
    name = ""

    #colision detection
    timeLength = 7

    def __init__(self,n):
        self.start = 1
        self.head = Reservation(0, 0, 0, 0, n, 0, 0, 0)
        self.tail = Reservation(99, 0, 0, 0, n, 0, 0, 0)
        self.tail.expectedTime = 2 ** 20
        self.head.expectedTime = 0
        self.size = 0
        self.starTime = time.time()
        self.name = n

        self.head.nextt = self.tail
        self.tail.prev = self.head

    def find_closest(self, res):
        if self.head.nextt is None:
            # ("List is empty, returning head")
            return self.head
        else:
            temp = self.head.nextt  # closest
            n = self.head.nextt
            while n is not self.tail:  # loop until reached tail
                if (abs(n.expectedTime - res.expectedTime) < (abs(temp.expectedTime - res.expectedTime))):
                    temp = n
                n = n.nextt
            if n is self.tail:
                # print("searched all, closest is VIN: " + str(temp.vin))
                return temp

    def find_closest2(self, res):
        if self.head.nextt is None:
            # ("List is empty, returning head")
            return self.head
        else:
            temp = self.head.nextt  # closest
            n = self.head.nextt
            while n is not self.tail:  # loop until reached tail
                if (abs(n.expectedTime - res.expectedTime2) < (abs(temp.expectedTime - res.expectedTime2))):
                    temp = n
                n = n.nextt
            if n is self.tail:
                # print("searched all, closest is VIN: " + str(temp.vin))
                return temp

    def find_closest_Time(self,t):
        if self.head.nextt is None:
            # ("List is empty, returning head")
            return self.head
        else:
            temp = self.head.nextt  # closest
            n = self.head.nextt
            while n is not self.tail:  # loop until reached tail
                if (abs(n.expectedTime - t) <= (abs(temp.expectedTime - t))):
                    temp = n
                n = n.nextt
            if n is self.tail:
                # print("searched all, closest is VIN: " + str(temp.vin))
                return temp

    def print_as_list(self):
        # Create empty list
        value_list = []
        if self.head.nextt != self.tail:
            current_node = self.head.nextt
            # Start at head and check if next is not tail
            while current_node.nextt != None:
                # Add current node to list and traverse forward
                value_list.append(current_node.toString())
                print (current_node.toString())
                current_node = current_node.nextt
            # rint value_list
        else:
            #print "No nodes"
            return False

    # check if lane is safe: (1)lane is empty at that time (2) does not cut the line in its lane
    # only checks P1
    def check_avalability_initial(self, res):
        # print ("\n\n " + str(res.vin))
        # print res.toString()
        current_node = self.head

        # search all nodes TODO:only search near by nodes
        # if empty
        if self.head.nextt is self.tail:
            # print("List is empty, adding")
            return True
        # if not empty
        else:
            n = self.head.nextt
            while n is not self.tail:  # loop until reached tail
                if (abs(n.expectedTime - res.expectedTime) < self.inter_tolerance_time) or ((n.expectedTime > res.expectedTime) and (n.lane == res.lane)):  # (1) colision in lane  (2) line skip   TODO:specify whitch criteria it failed at
                    # print "no room"
                    return False
                if(res.turn == 0): # going straight must check in front P2 and check ot to compare with cross fire
                    if(n.expectedTime2 != None):
                        if (abs(n.expectedTime2 - res.expectedTime2) < self.inter_tolerance_time) or (n.expectedTime2 > res.expectedTime2):
                                return False
                n = n.nextt
            if n is self.tail:
                # print("appears to be room")
                return True
        s = time.time()


    # checks if open timespot in P1 (using @ P1 speed for tolerance time)
    # finds car in front
    # determines case #
    # checks accordingly (for colision
    def check_time_and_colision(self, res):


        place = self.simple_check_time(res)

        if place[0]: # check time slot for P1
            car_infront = self.findCarInfront()
            if car_infront == self.head:
                return True, place[1]
            if self.check_colision(res, car_infront):
                print "safe"
                return True, place[1]
            else:
                return False, place[1], " inline colision"
        else:
            return False, place[1], "cross colision"


    def findCarInfront(self):
        current = self.tail.prev

        if current == self.head: #nothing in the way
            return current

        while current.lane -1 != self.name:
            current = current.prev
            #exception at end of list
            if current == self.head:
                return self.head

        return current


    # (1) check initial seperation
    # (2) check for min seperation during path
    def check_colision(self, res, car):

        print "using accel value: " + str(res.accel)
        tolerance =  (res.length + car.length) * 1.1 #meters #calculate tolerance based on size


        #difference in enter time
        deltaT = (res.enterTime - car.enterTime) / 1000.0

        #calculate separation at deltaT
        seperation = (car.speed * deltaT) + (0.5 * car.accel * deltaT ** 2)

        if seperation < tolerance:
            return False
            exit(9)


        # generate derivative
        time = numpy.linspace(0, self.timeLength, self.timeLength * 1000)   # substiture length to p2 and make a real resolution




        delta = []
        for val in time:
            data = (car.speed * (val + deltaT)) + (0.5 * car.accel * (val + deltaT) ** 2) - ((res.speed * val) + (0.5 * res.accel * (val) ** 2))
            delta.append(data)
        #print delta
        mini = min(delta)
        if (mini < tolerance):
            #print "min distance: " + str(mini)
            return False
        else:
            return True





    #checks time spot, returns left of it and boolean
    def simple_check_time(self,res):
        closest = self.find_closest_Time(res.expectedTime)
        if closest == self.tail:
            return True, self.tail.prev



        if closest.lane == res.lane:
            if res.expectedTime > closest.expectedTime:
                return True, closest
            else:
                return True, closest.prev
        else:
            tolerance = self.calculateToleranceTime(res, closest)
            #print (abs(res.expectedTime - closest.expectedTime))

            #TODO: need differerent tolerance times
            if (abs(res.expectedTime - closest.expectedTime) >= (tolerance / 1)) and ((res.expectedTime - closest.prev.expectedTime) >= (tolerance / 1)) and (abs(res.expectedTime - closest.nextt.expectedTime) > (tolerance / 1)):
                if res.expectedTime > closest.expectedTime:
                    return True, closest
                else:
                    return True, closest.prev

            else:
                return False, None


    #checks time spot, returns left of it and boolean
    #uses expected time 2
    def simple_check_time2(self, res):
        closest = self.find_closest_Time(res.expectedTime2)
        if closest == self.tail:
            return True, self.tail.prev



        tolerance = self.calculateToleranceTime2(res, closest)
        if (abs(res.expectedTime2 - closest.expectedTime) < (tolerance / 1.1)):
            return False, None

        try:
            t0 = self.calculateToleranceTime(res, closest.prev)
            if  (res.expectedTime2 - closest.prev.expectedTime) < (t0/1.1):
                return False, None

        except:
            print ""


        try:
            t2 = self.calculateToleranceTime2(res, closest.nextt)
            if abs(res.expectedTime2 - closest.nextt.expectedTime) < (t2/1.1):
                return False, None

        except:
            print ""




        if res.expectedTime2 > closest.expectedTime:
            return True, closest
        else:
            return True, closest.prev


    # different becasue look at reseravtions P2 time
    def calculateToleranceTime2(self, res, car):

        # calculate min speed of res
        Rescoef = [0.5* res.accel, res.speed, (-1 * (self.p2 + (res.length + car.width)))]
        ResPossibleMinSpeedTime = min(abs(numpy.roots(Rescoef)))
        ResPossibleMinSpeed = res.speed + (res.accel * ResPossibleMinSpeedTime )                   #speed that it is going to point of possible contact


        # calculate min speed of car
        #check if past P1
        if car.expectedTime2 == None:
            Carcoef = [0.5 * car.accel, car.speed, -1 * (self.p2 + (car.length + res.width))]
        else:
            Carcoef = [0.5 *car.accel, car.speed, -1 * (self.p1 + (car.length + res.width))]

        CarPossibleMinSpeedTime =  min(abs(numpy.roots(Carcoef)))
        CarPossibleMinSpeed = car.speed + (car.accel * CarPossibleMinSpeedTime)


        # calculate tolerance time1
        option1 = (2.0 * res.width + 2.0 * car.length) / CarPossibleMinSpeed

        # calculate tolerance time1
        option2 = (2.0 * car.width + 2.0 * res.length) / ResPossibleMinSpeed

        # return max
        temp = (max(option1, option2) * 1.1) * 1000







        return temp


    def calculateToleranceTime(self, res, car):

        # calculate min speed of res
        Rescoef = [0.5* res.accel, res.speed, (-1 * (self.p1 + (res.length + car.width)))]   # after
        Rescoef2 = [0.5* res.accel, res.speed, (-1 * (self.p1 - (res.length + car.width)))]  # before

        ResPossibleMinSpeedTime = min(abs(numpy.roots(Rescoef)))
        ResPossibleMinSpeed = res.speed + (res.accel * ResPossibleMinSpeedTime)                   #speed that it is going to point of possible contact

        ResPossibleMinSpeedTime2 = min(abs(numpy.roots(Rescoef2)))
        ResPossibleMinSpeed2 = res.speed + (res.accel * ResPossibleMinSpeedTime2)

        realResMinSpeed = min(ResPossibleMinSpeed, ResPossibleMinSpeed2)

        # calculate min speed of car
        #check if past P1
        if car.expectedTime2 == None:
            Carcoef = [0.5 * car.accel, car.speed,  (-1 * (self.p2 + (car.length + res.width)))] # before
            Carcoef2 = [0.5 * car.accel, car.speed, (-1 * (self.p2 - (car.length + res.width)))] # after
        else:
            Carcoef = [0.5 *car.accel, car.speed, (-1 * (self.p1 + (car.length + res.width)))]
            Carcoef2 = [0.5 * car.accel, car.speed, (-1 * (self.p1 - (car.length + res.width)))]

        CarPossibleMinSpeedTime =  min(abs(numpy.roots(Carcoef)))
        CarPossibleMinSpeed = car.speed + (car.accel * CarPossibleMinSpeedTime)


        CarPossibleMinSpeedTime2 = min(abs(numpy.roots(Carcoef2)))
        CarPossibleMinSpeed2 = car.speed + (car.accel * CarPossibleMinSpeedTime2)

        realCarMinSpeed = min(CarPossibleMinSpeed, CarPossibleMinSpeed2)

        # calculate tolerance time1
        option1 = (2.0 * res.width + 2.0 * car.length) / realResMinSpeed

        # calculate tolerance time1
        option2 = (2.0 * car.width + 2.0 * res.length) /  realCarMinSpeed

        # return max
        temp = (max(option1, option2) * 1.2) * 1000

        if temp < 0:
            print temp
            print res.toString()
            print car.toString()
            print CarPossibleMinSpeed
            print ResPossibleMinSpeed
            print Rescoef
            exit(99)




        return temp


    # find open space to left: (1) size greater than tolerances (2) no line skipping  (3) must be further than last search
    # returns x..(x)
    # returns head. if nothing found
    def find_open_left(self, res):
        current_node = self.find_closest(res)

        #check if near edge of list
        #if current_node.prev == self.head:
        #    return current_node


        while (current_node.prev != self.head):
            t1 = self.calculateToleranceTime(res, current_node)
            t2 = self.calculateToleranceTime(res, current_node.prev)

            #check for line skipping
            if current_node.lane == res.lane: # no line skipping
                return None, False

            if(current_node.expectedTime - res.expectedTime >= t1) and (res.expectedTime - current_node.prev.expectedTime >= t2) and (abs(current_node.expectedTime -t1 - res.OriginalExpectedTime) > res.edgeOfSearch):
                    return current_node.expectedTime - self.calculateToleranceTime(current_node, res), True
            else:
                current_node = current_node.prev

        #search found nothing, generate a res -0.1 seconds to the left of head.next and tolerance  (res.esedgeOfSearch - self.calculateToleranceTime(self.head.nextt, res))
        t = self.calculateToleranceTime(self.head.nextt, res)
        tolerance = max(res.edgeOfSearch + 0.1, abs(self.head.nextt.expectedTime - t - res.OriginalExpectedTime ))   #whats bigger? edge OR neccisary border between head.next and res
        expected = res.expectedTime - tolerance
        return expected, True


    # find open space to right: (1) size greater than tolerances (2) must be further than last search
    # returns (x)..x
    # returns tail. if nothing found
    def find_open_right(self, res):
        current_node = self.find_closest(res)

        #check if by edge of list
        #if current_node.nextt == self.tail:
        #    return current_node.expectedTime + self.calculateToleranceTime(current_node, res) - res.enterTime


        while (current_node.nextt != self.tail):
            t1 = self.calculateToleranceTime(res, current_node)
            t2 = self.calculateToleranceTime(res, current_node.nextt)

            if (current_node.expectedTime - res.expectedTime >= t1) and (abs(res.expectedTime - current_node.prev.expectedTime) >= t2) and ((abs(current_node.expectedTime + t1 - res.OriginalExpectedTime) > res.edgeOfSearch)):
                return current_node.expectedTime + self.calculateToleranceTime(current_node, res) - res.enterTime
            else:
                current_node = current_node.nextt

        # search found nothing, generate a res -0.1 seconds to the left of head.next and tolerance  (res.esedgeOfSearch - self.calculateToleranceTime(self.head.nextt, res))
        t = self.calculateToleranceTime(self.tail.prev, res)
        tolerance = max(res.edgeOfSearch + 0.1, abs(res.OriginalExpectedTime - self.tail.prev.expectedTime - t ))  # whats bigger? edge OR neccisary border between head.next and res
        expected = res.expectedTime + tolerance
        return expected



    def calcEnergyNeeded(self, res, lt, rt):  # option1 is left search, option2 is right search
        # compare required energy, return
        if lt != None:
            left = ((res.expectedTime - res.enterTime - abs(lt))/1000.0)
            leftAccel = ((self.p1 - res.speed * left))/(0.5 * left ** 2)
            if abs(leftAccel) > self.car_max_accel:
                leftAccel = None
        else:
            left = None
            leftAccel = None #TODO: change to none

        right = ((res.expectedTime + rt - res.enterTime)/1000.0)
        rightAccel = ((self.p1 - res.speed * right)) / (0.5 * right ** 2)
        if abs(rightAccel) > self.car_max_accel:
            rightAccel = None

        return leftAccel, rightAccel, left, right


    def findNextBest(self, res):
        node = res

        #find opening to the left
        #print "looking left"
        left = self.find_open_left(node)  # [1] is false: no data, True: real option
        if left[1]:
            leftTime = left[0] - node.expectedTime
        else:
            leftTime = None


        #find opening to the right
        #print "looking right"
        rightTime = self.find_open_right(node)- node.expectedTime


        #calculate options
        goal = self.calcEnergyNeeded(res, leftTime, rightTime)  #return : left accel , right accel, left T, right T

        #compare and add
        if goal[0] == None: #left does not exist
            node.accel = goal[1]
            node.requestedAccel = goal[1]
            node.expectedTime = goal[3] + node.enterTime
            node.expectedTime2 = expect(-1 *self.p2, node.speed, node.accel) * 1000 + node.enterTime
            node.edgeOfSearch = abs(node.expectedTime - node.OriginalExpectedTime)
        elif goal[1] == None: #right does not exist
            node.accel = goal[0]
            node.requestedAccel = goal[0]
            node.expectedTime = goal[2] + node.enterTime
            node.expectedTime2 = expect(-1 * self.p2, node.speed, node.accel) * 1000 + node.enterTime
            node.edgeOfSearch = abs(node.expectedTime - node.OriginalExpectedTime)
        elif goal[0] > abs(goal[1]) and goal[0] != 0: #right is better
            node.accel = goal[1]
            node.requestedAccel = goal[1]
            node.expectedTime = goal[3] + node.enterTime
            node.expectedTime2 = expect(-1 * self.p2, node.speed, node.accel)* 1000 + node.enterTime
            node.edgeOfSearch = abs(node.expectedTime - node.OriginalExpectedTime)
        elif goal[0] < abs(goal[1]) and goal[1] != 0: #left is better
            node.accel = goal[0]
            node.requestedAccel = goal[0]
            node.expectedTime = goal[2] + node.enterTime
            node.expectedTime2 = expect(-1 * self.p2, node.speed, node.accel) * 1000 + node.enterTime
            node.edgeOfSearch = abs(node.expectedTime - node.OriginalExpectedTime)
        else:
            print "Shit"
            exit("bad goals")

        return node

    def insertBetween(self, spot1, spot2, info):
        new_node = info
        new_node.nextt = spot2
        new_node.prev = spot1
        spot1.nextt = new_node
        spot2.prev = new_node
