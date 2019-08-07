import time
import cmath
import Intersection_Manager_class as IMC
import numpy




# helper functions
def expect(c, b, a):
    if (a == 0):
        a = 0.0000002
    a = a / 2
    d = (b ** 2) - (4 * a * c)
    # find two solutions
    sol1 = (-b - cmath.sqrt(d)) / (2 * a)
    sol2 = (-b + cmath.sqrt(d)) / (2 * a)
    #print('The solution are {0} and {1}'.format(sol1, sol2.__abs__()))
    return sol2.__abs__()


class Reservation:

    def toString(self):
        return ("[ Vin: " + str(self.vin) + " ,speed: " + str(self.speed) + " ,accel: " + str(
            self.accel) + " ,Entered time: " + str(self.enterTime) + " ,Lane #: " + str(
            self.lane) + " ,turn #: " + str(
            self.turn) + " ,Expected time #: " + str(self.expectedTime) + " ,Expected time2 #: " + str(self.expectedTime2) + " ,requested accel #: " + str(
            self.requestedAccel) + "]")

    def __init__(self, VIN, speed, accel, enterTime, lane, t, l, w):
        self.vin = VIN
        self.speed = speed
        self.accel = accel


        self.enter = 0  # 0 if entering -- 1 if exiting

        self.enterTime = enterTime
        self.expectedTime = enterTime + expect(IMC.Intersection_Manager.p1_distance, self.speed, self.accel) # to middle of first qm  , changed to enter tom from time()
        self.expectedTime2 = enterTime + expect(IMC.Intersection_Manager.p2_distance, self.speed, self.accel)


        self.nextt = None
        self.prev = None


        self.lane = lane
        self.turn = t

        self.requestedAccel = 0
        self.set = 0

        self.length = l
        self.width = w





class Intersection:


    # car criteria
    car_max_accel = 3
    car_max_decel = -3
    car_max_speed = 50

    # Intersection Criteria
    inter_side_length = 100
    inter_size = 10
    inter_max_speed = 20
    inter_tolerance_time = 0.6  # intersection_side_length/[(max_Speed + min_speed)/2] (0.12s)  ---only 1 car in an in

    # set up
    starTime = 0

    #useful for manager
    name = ""

    def __init__(self,n):
        self.start = 1
        self.head = Reservation(0, 0, 0, 0, n, 0, 0, 0)
        self.tail = Reservation(99, 0, 0, 0, n, 0, 0, 0)
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
                if (abs(n.expectedTime - t) < (abs(temp.expectedTime - t))):
                    temp = n
                n = n.nextt
            if n is self.tail:
                # print("searched all, closest is VIN: " + str(temp.vin))
                return temp

    def addReservation(self, VIN, speed, accel, enterTime, lane):
        new_node = Reservation(VIN, speed, accel, enterTime, lane)

        # check if lane is safe: (1)lane is empty at that time (2) does not cut the line in its lane
        if (self.check_avalability_initial(new_node)):
            # If no head, set new node as head
            if self.head.nextt == None:
                self.head.nextt = new_node
                self.head.nextt.nextt = self.tail
                self.tail.prev = new_node
                return
            else:
                current_node = self.head
                # if next not none (tail) continue traversing
                while current_node.nextt != self.tail:
                    current_node = current_node.nextt
                # if tail, add to end
                current_node.nextt = new_node
                # set prev pointer to current node
                new_node.prev = current_node
                # set new tail to new node
                new_node.nextt = self.tail
                self.tail.prev = current_node
            self.size = self.size = 1

    def addReservation2(self, res):
        new_node = res
        if (self.check_avalability_initial(new_node)):
            # If no head, set new node as head
            if self.head.nextt == None:
                self.head.nextt = new_node
                self.head.nextt.nextt = self.tail
                self.tail.prev = new_node
                return
            else:
                current_node = self.head
                # if next not none (tail) continue traversing
                while current_node.nextt != self.tail:
                    current_node = current_node.nextt
                # if tail, add to end
                current_node.nextt = new_node
                # set prev pointer to current node
                new_node.prev = current_node
                # set new tail to new node
                new_node.nextt = self.tail
                self.tail.prev = current_node
            self.size = self.size = 1

    def addReservation3(self, res):
        new_node = res
        if (self.check_avalability_initial(new_node)):
            # If no head, set new node as head
            if self.head.nextt == self.tail:
                self.head.nextt = new_node
                self.head.nextt.nextt = self.tail
                self.tail.prev = new_node
                new_node.prev = self.head
                # return
            else:
                # find closest and add before/after
                current_node = self.find_closest(res)
                # if res is greater or less (expected time)
                if (current_node.expectedTime < res.expectedTime):
                    # add after
                    self.insertBetween(current_node, current_node.nextt, res)
                    # print "add after closest"
                else:
                    # add before
                    self.insertBetween(current_node.prev, current_node, res)
                    # print "add before closest"
            self.size = self.size = 1
        else:
            print ("Expected time does not fit, finding new location for: " + str(res.toString()))
            cursor = self.look_right_initial(res)  # makes sure nothing in same LANE is expected after res expectedTime
            if (cursor == None):  # nothing to worry about on the right

                print ("no issues regarding lane to the right \n\n")

                print ("looking to the left")
                left = self.find_open_left(res)
                can_left = self.withinCriteriaLeft(res, left)
                print ("looking to the right")
                right = self.find_open_right(res)
                can_right = self.withinCriteriaRight(res, right)


                goal = self.calcEnergyNeeded(res, left, right)
                if (goal[0] < goal[1]) and can_left[0]:  # less energy to get to left and witin criteria
                    # send data to car for plan for acceleration
                    # adjust estimated time
                    res.expectedTime = left.expectedTime - self.inter_tolerance_time
                    res.requestedAccel = can_left[1]
                    self.insertBetween(left.prev, left, res)

                elif (goal[0] > goal[1]) and can_right[0]:  # less energy to get to right and witin criteria
                    # send data to car for plan for acceleration
                    # adjust estimated tim
                    res.expectedTime = right.expectedTime + self.inter_tolerance_time
                    res.requestedAccel = can_right[1]
                    self.insertBetween(right, right.nextt, res)
                elif ~can_left[0] and can_right[0]:
                    # send data to car for plan for acceleration
                    # adjust estimated tim
                    res.expectedTime = right.expectedTime + self.inter_tolerance_time
                    res.requestedAccel = can_right[1]
                    self.insertBetween(right, right.nextt, res)
                elif can_left[0] and ~can_right[0]:
                    # send data to car for plan for acceleration
                    # adjust estimated tim
                    res.expectedTime = left.expectedTime - self.inter_tolerance_time
                    res.requestedAccel = can_left[1]
                    self.insertBetween(left.prev, left, res)
                else:
                    print("shit nothing fits...")
            elif (cursor == self.tail.prev):  # if last enetry is same lane
                print ("same lane at end of list")
                # reservation must be at end of the list
                res.expectedTime = self.tail.prev.expectedTime + self.inter_tolerance_time  # expected for proposed??
                # within criteria?
                can_right = self.withinCriteriaRight(res, cursor)
                res.requestedAccel = can_right[1]
                self.insertBetween(self.tail.prev, self.tail, res)
            else:
                print ("issues regarding lane to the right \n\n")
                print ("looking to the right")
                right = self.find_open_right_fromPos(res, cursor)
                can_right = self.withinCriteriaRight(res, right)

                if right != None:
                    print ("Option on right: " + str(right.toString()))
                    print ("Option possible? " + str(can_right))
                else:
                    print ("Option on right: none")

                print ("\n\nchecking if within car criteria:..")
                # print "left: " + str(self.withinCriteriaLeft(res,left))
                # print "right: " + str(self.withinCriteriaRight(res,right))

                goal = self.calcEnergyNeeded(res, right, right)  # TODO: makes this one input at a time
                if can_right[0]:
                    # send data to car for plan for acceleration
                    # adjust estimated tim
                    res.expectedTime = right.expectedTime + self.inter_tolerance_time
                    res.requestedAccel = can_right[1]


                    """
                    here you check to see if next quadrent is avalible
                    if yes:
                        continue
                    else:
                        search for next opening in P1
                        repeat
                    """
                    self.insertBetween(right, right.nextt, res)
                else:
                    #  print("shit nothing fits...")
                    exit()
        return res.requestedAccel, res.expectedTime

    def find_best_option(self):
        print("neither lol")
        """
        Everything under else
        calcEnergy, within criteria, goal<>
        """

    def calcEnergyNeeded(self, res, option1, option2):  # option1 is left search, option2 is right search
        # compare required energy, return
        eng1 = abs(option1.expectedTime - self.inter_tolerance_time - res.expectedTime)
        eng2 = abs(option2.expectedTime + self.inter_tolerance_time - res.expectedTime)
        return eng1, eng2

    def calcEnergyNeeded2(self, res, option1, option2):  # option1 is left search, option2 is right search
        # compare required energy, return
        eng1 = abs(option1.expectedTime - self.inter_tolerance_time - res.expectedTime2)
        eng2 = abs(option2.expectedTime + self.inter_tolerance_time - res.expectedTime2)
        return eng1, eng2


    # returns tue/false,acceleration value p1
    # Todo: incorperate current acceleratiuon value!! you fool!!!!!!!!!!!!!
    def withinCriteriaLeft(self, res, option):  # option1 is left search, option2 is right search
        opt1_time = (option.expectedTime - self.inter_tolerance_time) - option.enterTime
        left = (2 * (self.inter_side_length - (self.inter_size/2) - res.speed * opt1_time)) / (opt1_time ** 2)

        if (left < 0) and (left > self.car_max_decel):  # check if pos or neg, compare to mac accel/dec and update res
            print ("left deceleration approved!")
            return True, left
        elif (left > 0) and (left < self.car_max_accel):
            print  ("left acceleration approved!")
            return True, left
        else:
            return False, left

    # returns tue/false,acceleration value p2
    # Todo: incorperate current acceleratiuon value!! you fool!!!!!!!!!!!!!
    def withinCriteriaLeftp2(self, res, option):  # option1 is left search, option2 is right search
        opt1_time = (option.expectedTime - self.inter_tolerance_time) - option.enterTime
        left = (2 * (self.inter_side_length + (self.inter_size / 2) - res.speed * opt1_time)) / (opt1_time ** 2)

        if (left < 0) and (left > self.car_max_decel):  # check if pos or neg, compare to mac accel/dec and update res
            print ("left deceleration approved!")
            return True, left
        elif (left > 0) and (left < self.car_max_accel):
            print ("left acceleration approved!")
            return True, left
        else:
            return False, left




    # returns tue/false,acceleration value for p1
    # Todo: incorperate current acceleratiuon value!! you fool
    def withinCriteriaRight(self, res, option):
        optionTime = (option.expectedTime + self.inter_tolerance_time) - option.enterTime
        right = (2 * (self.inter_side_length - (self.inter_size/2) - res.speed * optionTime)) / (optionTime ** 2)
        print(optionTime + option.enterTime)
        print(right)
        if (right < 0) and (
                right > self.car_max_decel):  # check if pos or neg, compare to mac accel/dec and update res
            print ("right deceleration approved!")
            return True, right
        elif (right > 0) and (right < self.car_max_accel):
            print("right acceleration approved!")
            return True, right
        else:
            return False, right

    # returns tue/false,acceleration value for p2
    # Todo: incorperate current acceleratiuon value!! you fool
    def withinCriteriaRightp2(self, res, option):
        optionTime = (option.expectedTime + self.inter_tolerance_time) - option.enterTime
        right = (2 * (self.inter_side_length + (self.inter_size / 2) - res.speed * optionTime)) / (optionTime ** 2)
        print(optionTime + option.enterTime)
        print(right)
        if (right < 0) and (
                right > self.car_max_decel):  # check if pos or neg, compare to mac accel/dec and update res
            print("right deceleration approved!")
            return True, right
        elif (right > 0) and (right < self.car_max_accel):
            print("right acceleration approved!")
            return True, right
        else:
            return False, right

    # returns tue/false,acceleration value for p1
    # takes a time to be at
    # Todo: incorperate current acceleratiuon value!! you fool
    def withinCriteriaRightTimeBsed(self, res, T):
        optionTime = (T + self.inter_tolerance_time) - res.enterTime
        right = (2 * (self.inter_side_length - (self.inter_size / 2) - res.speed * optionTime)) / (optionTime ** 2)
        if (right < 0) and (right > self.car_max_decel):  # check if pos or neg, compare to mac accel/dec and update res
            print ("right deceleration approved!")
            return True, right
        elif (right > 0) and (right < self.car_max_accel):
            print("right acceleration approved!")
            return True, right
        else:
            return False, right

    def getAccelValue(self,res, newTime, dist):
        T = newTime - res.enterTime
        return (2 * (dist - res.speed * T)) / (T ** 2)


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
                return False, place[1]
        else:
            return False, place[1]


    def findCarInfront(self):
        current = self.tail.prev
        while current.lane != self.name:
            current = current.prev
        return current


    # (1) check initial seperation
    # (2) check for min seperation during path
    def check_colision(self, res, car):

        print "using accel value: " + str(res.accel)
        tolerance =  (res.length + car.length)* 1.2 #meters #calculate tolerance based on size


        #difference in enter time
        deltaT = res.enterTime - car.enterTime

        #calculate separation at deltaT
        seperation = (car.speed * deltaT) + (0.5 * car.accel * deltaT ** 2)

        if seperation < tolerance:
            return False
            exit(9)


        # generate derivative
        time = numpy.linspace(0, 20, 15 * 50)   # substiture length to p2 and make a real resolution




        delta = []
        for val in time:
            data = (car.speed * (val + deltaT)) + (0.5 * car.accel * (val + deltaT) ** 2) - ((res.speed * val) + (0.5 * res.accel * (val) ** 2))
            delta.append(data)
        print delta
        mini = min(delta)
        if (mini < tolerance):
            print "min distance: " + str(mini)
            return False
        else:
            return True



        """
        efficient way
        derivative = []

        for val in time:
            data = (car.speed + car.accel * (val + deltaT)) - (res.speed + res.accel * val)
            print data
        """





    #checks time spot, returns left of it and boolean
    def simple_check_time(self,res):
        closest = self.find_closest_Time(res.expectedTime)
        if closest == self.tail:
            return True, self.tail.prev

        """
        if (closest.lane == self.n): #if in same lane then tolerance is length + length
            tolerance = 10
        else:                          #different lane then tolerance is length width

            tolerance = self.inter_tolerance_time  #TODO change to speed at PX
        """
        tolerance = self.calculateToleranceTime(res, closest)

        if (abs(res.expectedTime - closest.expectedTime) >= tolerance) and ((res.expectedTime - closest.prev.expectedTime) >= tolerance) and (abs(res.expectedTime - closest.nextt.expectedTime) > tolerance):
            if res.expectedTime > closest.expectedTime:
                return True, closest
            else:
                return True, closest.prev

        else:
            return False, None

    # checks time spot, returns left of it and boolean


    #time not res based
    def simple_check_timeBased(self, t):
        closest = self.find_closest_Time(t)
        #print closest.toString()
        if closest == self.tail:
            return True, self.tail.prev

        tolerance = self.calculateToleranceTime(res, closest)

        if (abs(t - closest.expectedTime) >= tolerance) and (
                (t - closest.prev.expectedTime) >= tolerance) and (
                abs(t - closest.nextt.expectedTime) > tolerance):
            if t > closest.expectedTime:
                return True, closest
            else:
                return True, closest.prev

        else:
            return False, closest




    #checks time spot, returns left of it and boolean
    #uses expected time 2
    def simple_check_time2(self, res):
        closest = self.find_closest_Time(res.expectedTime2)
        if closest == self.tail:
            return True, self.tail.prev

        tolerance = self.calculateToleranceTime(res, closest)


        if (abs(res.expectedTime2 - closest.expectedTime) > tolerance) and ((res.expectedTime2 - closest.prev.expectedTime) > tolerance) and (abs(res.expectedTime2 - closest.nextt.expectedTime) > tolerance):
            if res.expectedTime2 > closest.expectedTime:
                return True, closest
            else:
                return True, closest.prev

        else:
            return False, None



    def calculateToleranceTime(self, res, car):
        print ("I got a low tolerance to burple kush")
        # calculate min speed of res
        Rescoef = [0.5* res.accel, res.speed, (-1 * self.inter_side_length) - (2 * res.length + car.width)]
        ResPossibleMinSpeedTime = min(numpy.roots(Rescoef))
        ResPossibleMinSpeed = res.speed + (res.accel * ResPossibleMinSpeedTime )
        # TODO: look at range now!!

        # calculate min speed of car
        Carcoef = [0.5 *car.accel, car.speed, (-1 * self.inter_side_length) + (2 * car.length + res.width)]
        CarPossibleMinSpeedTime =  min(numpy.roots(Carcoef))
        CarPossibleMinSpeed = car.speed + (car.accel * CarPossibleMinSpeedTime)
        #TODO: look at range now!!

        # calculate tolerance time1
        option1 = (res.length / ResPossibleMinSpeed) + (car.width / CarPossibleMinSpeed)

        # calculate tolerance time1
        option2 = (car.length / CarPossibleMinSpeed) + (res.width / ResPossibleMinSpeed)

        # return max
        temp = max(option1, option2)

        if temp < 0:
            print temp
            print res.toString()
            print car.toString()
            print CarPossibleMinSpeed
            print ResPossibleMinSpeed
            print Rescoef
            exit(99)


        print temp
        return max(option1,option2)















    # check if lane is safe: (1)lane is empty at that time (2) does not cut the line in its lane
    # only checks P2
    def check_avalability_initial2(self, res):
        # print ("\n\n " + str(res.vin))
        # print res.toString()
        current_node = self.head

        # search all nodes TODO:only search near by nodes
        # if empty
        if self.head.nextt is None:
            # print("List is empty, adding")
            return True
        # if not empty
        else:
            n = self.head.nextt
            while n is not self.tail:  # loop until reached tail
                if (abs(n.expectedTime - res.expectedTime2) < self.inter_tolerance_time) or (
                        (n.expectedTime > res.expectedTime2) and (
                        n.lane == res.lane)):  # (1) colision in lane  (2) line skip   TODO:specify whitch criteria it failed at
                    # print abs(n.expectedTime - res.expectedTime)
                    # print "no room"
                    return False
                n = n.nextt
            if n is self.tail:
                # print("appears to be room")
                return True



    # checks if lane has opening at T for lane l
    #  (1)lane is empty at that time
    # does not need to check for line cutting, ONLY USE WHEN CHECKING SPECIFIC TIMES, NOT FOR INITIAL USE
    # returns T/F and left node of opening
    def check_avalability_time(self,T):
        current_node = self.head
        if(current_node == self.tail): #list is empty, must be true
            return True, self.head


        while (current_node.vin != 99):
            if (abs(current_node.expectedTime - current_node.nextt.expectedTime) > 2 * self.inter_tolerance_time):  # (1) enough space  lane
                if(current_node.expectedTime - T >= self.inter_tolerance_time):
                    return True, current_node  # returns right node (x)---x

            current_node = current_node.nextt

        #check if greater than tail.prev by tolerance
        if T -current_node.prev.expectedTime >= self.inter_tolerance_time:
            return True,current_node

        return False, current_node


    def check_P2_Avalibility(self, T):
        current_node = self.head
        # list is empty
        if current_node.nextt == self.tail:
            #print("case 1")
            return True, self.head

        # time is before first node
        #if current_node.nextt.expectedTime > T:
        if current_node.nextt.expectedTime - T >= self.inter_tolerance_time:
            #print("case 2")
            return True, self.head

        # traverse to an opening
        current_node = current_node.nextt
        while current_node != self.tail:
            if (abs(current_node.expectedTime - current_node.nextt.expectedTime) > 2 * self.inter_tolerance_time):  # (1) enough space  lane
                if (T - current_node.expectedTime > self.inter_tolerance_time):
                    #print("case 3")
                    return True, current_node  # returns right node x---(x)
            current_node = current_node.nextt
        #print("case 4")
        return False, None

    # find open space to left: (1) size greater than tolerance*2 (2) no line skipping
    # returns head. if nothing found
    def find_open_left(self, res):
        current_node = self.find_closest(res)

        while (current_node.prev != None):
            if (abs(current_node.expectedTime - current_node.prev.expectedTime) > 2 * self.inter_tolerance_time) and (
                    current_node.nextt.lane != res.lane):  # (1) enough space  lane  (2) line skip
                return current_node  # returns right node x---(x)
            current_node = current_node.prev
        return None



    # find open space to left of time T: (1) size greater than tolerance*2 (2) no line skipping
    # returns head. if nothing found
    def find_open_left_alt(self, t,l):
        current_node = self.find_closest_Time(t)

        while (current_node.prev != None):
            if (abs(
                    current_node.expectedTime - current_node.prev.expectedTime) > 2 * self.inter_tolerance_time) and (
                    current_node.nextt.lane != l):  # (1) enough space  lane  (2) line skip
                return current_node  # returns right node x---(x)
            current_node = current_node.prev
        return None



    # find open space to left of time T: (1) size greater than tolerance*2 (2) no line skipping
    # returns head. if nothing found
    def find_open_right_alt(self, t, l):
        current_node = self.find_closest_Time(t)

        while (current_node.vin != 99):
            if abs(
                    current_node.expectedTime - current_node.nextt.expectedTime) > 2 * self.inter_tolerance_time:  # (1) enough space  lane
                return current_node  # returns right node x---(x)
            current_node = current_node.nextt
        return current_node


    # find open space to left: (1) size greater than tolerance*2 (2) no line skipping
    # returns head. if nothing found
    def find_open_right(self, res):
        current_node = self.find_closest(res)
        while (current_node.vin != 99):
            if abs(current_node.expectedTime - current_node.nextt.expectedTime) > 2 * self.inter_tolerance_time:  # (1) enough space  lane
                #print (current_node.toString())
                return current_node  # returns right node x---(x)
            current_node = current_node.nextt
        #print (current_node.toString())
        return current_node


    def find_open_right_newSpot(self, res, notThisNode):
        # find opening with greater expected time than res
        # if opening
        current_node = self.find_closest(res)

        while (current_node.vin != 99):
            if abs(current_node.expectedTime - current_node.nextt.expectedTime) > 2 * self.inter_tolerance_time and (current_node.nextt.vin != notThisNode.vin):  # (1) enough space  lane
                #print (current_node.toString())
                return current_node  # returns right node x---(x)
            current_node = current_node.nextt

        return current_node

    # starts search from look_right_initial
    # find open space to left: (1) size greater than tolerance*2 (2) no line skipping
    # returns head. if nothing found
    def find_open_right_fromPos(self, res, pos):
        current_node = pos
        while (current_node.vin != 99):
            if abs(
                    current_node.expectedTime - current_node.nextt.expectedTime) > 2 * self.inter_tolerance_time:  # (1) enough space  lane
                return current_node  # returns right node x---(x)
            current_node = current_node.nextt
        return current_node

    # searches all reservation to the right of closest, cannon be in the same lane, must go after
    # if none found, look_open_left is correct, if same lane found, can only look to the right from that point
    def look_right_initial(self, res):
        current_node = self.find_closest(res)
        last_same_lane = None
        while current_node != self.tail:
            if (current_node.lane == res.lane):
                last_same_lane = current_node
            current_node = current_node.nextt
        return last_same_lane

    def look_right_initial2(self, res):
        current_node = self.find_closest2(res)
        last_same_lane = None
        while current_node != self.tail:
            if (current_node.lane == res.lane):
                last_same_lane = current_node
            current_node = current_node.nextt
        return last_same_lane



    def insertBetween(self, spot1, spot2, info):
        new_node = info
        new_node.nextt = spot2
        new_node.prev = spot1
        spot1.nextt = new_node
        spot2.prev = new_node
