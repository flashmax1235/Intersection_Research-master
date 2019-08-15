import time
import cmath, math
import numpy as np
import Intersection_Class as IC


# helper functions
def expect(c, b, a):
    if (a == 0):
        a = 0.0000002
    a = a / 2
    d = (b ** 2) - (4 * a * c)
    # find two solutions
    # sol1 = (-b - cmath.sqrt(d)) / (2 * a)
    sol2 = (-b + cmath.sqrt(d)) / (2 * a)
    # print('The solution are {0} and {1}'.format(sol1, sol2.__abs__()))
    return sol2.__abs__()


class Car:
    # car criteria
    car_max_accel = 3
    car_max_decel = -3
    car_max_speed = 50

    # Intersection Criteria/specs
    inter_side_length = IC.Intersection.inter_side_length
    inter_max_speed = IC.Intersection.inter_max_speed  # TODO actually use this....
    inter_tolerance_time = IC.Intersection.inter_tolerance_time  # intersection_side_length/[(max_Speed + min_speed)/2] (0.12s)  ---only 1 car in an in
    inter_size = IC.Intersection.inter_size  # ex: 20x20m inside
    p1_distance = -1 * inter_side_length + (inter_size / 2)
    p2_distance = -1 * inter_side_length - (inter_size / 2)


    # position
    posX = 0
    posY = 0

    # Instructions
    accel0 = 0  # original acceleration value
    accel01 = 0  # first requested acceleration value
    accel1 = 0  # outgoing requested acceleration value
    turn = None  # 0: no turn  --- 1: right turn  --- 2: left turn 9: super FUN turn

    # Timeline
    enterTime0 = 0  # time entering intersection
    enterTime1 = 0  # time entering second half of intersection
    exitTime = 0  # time leaving intersection

    # Proposed Timeline
    expectedTime01 = 0  # after first update, time at P2
    t1 = 0  # after seconds update to end
    distanceAtT1 = -1

    # simulation specs
    max_time = 2000  #miliseconds
    resolution = max_time

    # sizing
    width = 0
    length = 0



    def __init__(self, VIN, speed, accel, enterTime, lane, turn, l, w):
        self.vin = VIN
        self.speed = speed
        self.accel0 = accel
        self.set = 0  # 0 if entering intesection -- 1 if in middle --- 2 if exiting
        self.enterTime0 = enterTime

        self.lane = lane
        self.posY = 0
        self.posX = 0
        self.turn = turn
        self.posX_OG = 0
        self.posY_OG = 0
        self.length = l
        self.width = w





        # position
        # Assume:  -100:100 X -100:100
        if self.lane == 1:
            self.posX_OG = self.inter_size/2
            self.posY_OG = -1 * self.inter_side_length
        elif self.lane == 2:
            self.posX_OG = self.inter_side_length
            self.posY_OG = self.inter_size/2
        elif self.lane == 3:
            self.posX_OG = -1 * self.inter_size/2
            self.posY_OG = self.inter_side_length
        elif self.lane == 4:
            self.posX_OG = -1 * self.inter_side_length
            self.posY_OG = -1 * self.inter_size/2


    def toString(self):
        return ("[ Vin: " + str(self.vin) +
                " ,speed: " + str(self.speed) +
                " ,accel0: " + str(self.accel0)  +
                " ,Entered time: " + str(self.enterTime0) +
                " ,Lane #: " + str(self.lane) +
                " turn #: " + str(self.turn) +
                " ,Expected time (P2)#: " + str(self.expectedTime0) +
                " ,first requested accel #: " + str( self.accel01) +
                "]")

    def updateAccel01(self, a):
        self.accel01 = self.accel01 + a[0]
        self.expectedTime01 = a[1]

    def updateAccel1(self, a):
        self.accel1 = a[0]
        self.t1 = a[1]
        dt = (self.t1 - self.expectedTime01)/1000.0
        self.distanceAtT1 =  abs(self.p2_distance) + (dt*self.speed)  + (0.5 * self.accel1 * (dt ** 2))   # may have some error in there (cms)

    def updateExpectedTime01(self, t):
        self.expectedTime01 = t

    def distanceTravelled(self, T):
        path = self.piec0XY(T)
        return path

################################
    def distanceTravelledTime(self, t):
        if(t >= self.enterTime0):
            delta =  self.trajectory01((t-self.enterTime0)/ 1000.0, 0)

            if (self.lane == 1):  # vericle lanes
               # check for turn
                if abs(delta) >= abs(self.p1_distance):
                    if self.turn == 1:
                        self.posY = -1 * self.inter_size / 2
                        self.posX = self.posX_OG + (delta + self.p1_distance)
                    elif self.turn == 2 and (abs(delta) >= abs(self.p2_distance)):
                        self.posY = self.inter_size / 2
                        self.posX = self.posX_OG - (delta + self.p2_distance)
                    else:
                        self.posX = self.posX_OG
                        self.posY = self.posY_OG + delta

                else:
                    self.posX = self.posX_OG
                    self.posY = self.posY_OG + delta
            elif (self.lane == 3):
               # check for turn
                if abs(delta) >= abs(self.p1_distance):
                    if self.turn == 1:
                        self.posY = self.inter_size / 2
                        self.posX = self.posX_OG + (delta - self.p1_distance)
                    elif self.turn == 2 and (abs(delta) >= abs(self.p2_distance)):
                        self.posY = -self.inter_size / 2
                        self.posX = self.posX_OG - (delta - self.p2_distance)
                    else:
                        self.posX = self.posX_OG
                        self.posY = self.posY_OG + delta

                else:
                    self.posX = self.posX_OG
                    self.posY = self.posY_OG + delta
            elif (self.lane == 2):
                if abs(delta) >= abs(self.p1_distance):
                    if self.turn == 1:
                        self.posX = self.inter_size / 2
                        self.posY = self.posY_OG + (delta + self.p1_distance)
                    elif self.turn == 2 and (abs(delta) >= abs(self.p2_distance)):
                        self.posX = -self.inter_size / 2
                        self.posY = self.posY_OG - (delta + self.p2_distance)
                    else:
                        self.posY = self.posY_OG
                        self.posX = self.posX_OG - delta

                else:
                    self.posY = self.posY_OG
                    self.posX = self.posX_OG - delta
            elif (self.lane == 4):
                if abs(delta) >= abs(self.p1_distance):
                    if self.turn == 1:
                        self.posX = -self.inter_size / 2
                        self.posY = self.posY_OG - (delta + self.p1_distance)
                    elif self.turn == 2 and (abs(delta) >= abs(self.p2_distance)):
                        self.posX = self.inter_size / 2
                        self.posY = self.posY_OG + (delta + self.p2_distance)
                    else:
                        self.posY = self.posY_OG
                        self.posX = self.posX_OG + delta

                else:
                    self.posY = self.posY_OG
                    self.posX = self.posX_OG + delta
            return self.posX, self.posY
        else:
            return 0.0, 0.0

    def generatereservation(self):
        tempRes = IC.Reservation(self.vin, self.speed, self.accel0, self.enterTime0, self.lane, self.turn, self.length, self.width)
        return tempRes

    #updatedSpeed
    def generatereservationOUT(self):
        newSpeed = self.speed + ((self.expectedTime01 - self.enterTime0)/1000.0) * self.accel01
        tempRes = IC.Reservation(self.vin, newSpeed, self.accel0, self.enterTime0, self.lane, self.turn, self.length, self.width)
        return tempRes



    def readyForOutro(self, t):
        # change distance for left and right turn
        if self.trajectory01((t-self.enterTime0)/ 1000.0, 0) > abs(self.p2_distance):
            return True
        else:
            return False

    def checkForDone(self, t):
        # change distance for left and right turn
        if self.trajectory01((t - self.enterTime0) / 1000.0, 0) > 210:
            return True
        else:
            return False
#################################


    def piec0XY(self, T):


        # add in car data
        path = self.vin
        path = np.append(path, self.lane)

        # add in car dimention
        if (self.lane % 2 == 1):
            path = np.append(path, self.length)
            path = np.append(path, self.width)
        else:
            path = np.append(path, self.width)
            path = np.append(path, self.length)


        # timelines
        time = np.linspace(T, T + self.max_time, self.resolution)
        print time.size
        realTime = np.linspace(0, T + self.max_time - self.enterTime0, self.resolution)

        # place holders
        countX = 0
        countY = 0
        delta = 0


        for inx, val in enumerate(time):
           #vert
            if (val < self.enterTime0): # car not started yet
                countX = countX + 1
            else:
                if (self.lane == 1):   # vericle lanes
                    # get distance travelled
                    delta = self.trajectory01((realTime[inx - countX]) / 100, 0)

                    #check for turn
                    if abs(delta) >= abs(self.p1_distance):
                        if self.turn == 1:
                            self.posY = -1 * self.inter_size/2
                            self.posX = self.posX_OG + (delta + self.p1_distance)
                        elif self.turn == 2 and (abs(delta) >= abs(self.p2_distance)):
                            self.posY =  self.inter_size / 2
                            self.posX = self.posX_OG - (delta + self.p2_distance)
                        else:
                            self.posX = self.posX_OG
                            self.posY = self.posY_OG + delta

                    else:
                        self.posX = self.posX_OG
                        self.posY = self.posY_OG + delta

                elif(self.lane == 3):
                    # get distance travelled
                    delta = self.trajectory01(realTime[inx - countX] / 100, 0) * -1

                    # check for turn
                    if abs(delta) >= abs(self.p1_distance):
                        if self.turn == 1:
                            self.posY = self.inter_size / 2
                            self.posX = self.posX_OG + (delta - self.p1_distance)
                        elif self.turn == 2 and (abs(delta) >= abs(self.p2_distance)):
                            self.posY = -self.inter_size / 2
                            self.posX = self.posX_OG - (delta - self.p2_distance)
                        else:
                            self.posX = self.posX_OG
                            self.posY = self.posY_OG + delta

                    else:
                        self.posX = self.posX_OG
                        self.posY = self.posY_OG + delta


                elif(self.lane == 2):
                    # get distance travelled
                    delta = self.trajectory01(realTime[inx - countX] / 100, 0)

                    if abs(delta) >= abs(self.p1_distance):
                        if self.turn == 1:
                            self.posX = self.inter_size / 2
                            self.posY = self.posY_OG + (delta + self.p1_distance)
                        elif self.turn == 2 and (abs(delta) >= abs(self.p2_distance)):
                            self.posX = -self.inter_size / 2
                            self.posY = self.posY_OG - (delta + self.p2_distance)
                        else:
                            self.posY = self.posY_OG
                            self.posX = self.posX_OG - delta

                    else:
                        self.posY = self.posY_OG
                        self.posX = self.posX_OG - delta

                elif (self.lane == 4):
                    # get distance travelled
                    delta = self.trajectory01(realTime[inx - countX] / 100 , 0)

                    if abs(delta) >= abs(self.p1_distance):
                        if self.turn == 1:
                            self.posX = -self.inter_size / 2
                            self.posY = self.posY_OG - (delta + self.p1_distance)
                        elif self.turn == 2 and (abs(delta) >= abs(self.p2_distance)):
                            self.posX = self.inter_size / 2
                            self.posY = self.posY_OG + (delta + self.p2_distance)
                        else:
                            self.posY = self.posY_OG
                            self.posX = self.posX_OG + delta

                    else:
                        self.posY = self.posY_OG
                        self.posX = self.posX_OG + delta
                else:
                    print"horizontal"

            path = np.append(path, self.posX)
            path = np.append(path, self.posY)

        return path



    def trajectory0(self, time, pos):
        return pos + (self.speed * time) + (0.5 * self.accel0 * (time ** 2))

    def trajectory01(self, time, pos):
        if(time >= (self.t1/1000.0)):
            return self.distanceAtT1 + (35.0 * ((time - self.t1) / 1000.0))
        else:
            return pos + (self.speed * time) + (0.5 * self.accel01 * (time ** 2))

    def trajectory01_turn(self,time, pos, right):
        print "turn"


"""
test = Car(0, 0, 1.0, time.time(), 2)
print test.toString()
test.distanceTravelled()
"""
