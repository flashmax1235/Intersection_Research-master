import time
import cmath

import random


# helper functions
def expect(c, b, a):
    if (a == 0):
        a = 0.0000002
    a = a / 2
    d = (b ** 2) - (4 * a * c)
    # find two solutions
    sol1 = (-b - cmath.sqrt(d)) / (2 * a)
    sol2 = (-b + cmath.sqrt(d)) / (2 * a)
    # print('The solution are {0} and {1}'.format(sol1, sol2.__abs__()))
    return sol2.__abs__()


class Reservation:

    def toString(self):
        return ("[ Vin: " + str(self.vin) + " ,speed: " + str(self.speed) + " ,accel: " + str(
            self.accel) + " ,Entered time: " + str(self.enterTime) + " ,Lane #: " + str(
            self.lane) + " ,Expected time #: " + str(self.expectedTime) + " ,requested accel #: " + str(
            self.requestedAccel) + "]")

    def __init__(self, VIN, speed, accel, enterTime, lane):
        self.vin = VIN
        self.speed = speed
        self.accel = accel
        self.enter = 0  # 0 if entering -- 1 if exiting
        self.enterTime = enterTime
        self.expectedTime = time.time() + expect(-100, self.speed, self.accel)
        self.nextt = None
        self.prev = None
        self.lane = lane
        self.proposedTime = 0
        self.requestedAccel = 0
        self.set = 0


class Intersection:
    # car criteria
    car_max_accel = 3
    car_max_decel = -3
    car_max_speed = 50

    # Intersection Criteria
    inter_side_length = 100
    inter_max_speed = 20
    inter_tolerance_time = 0.5  # intersection_side_length/[(max_Speed + min_speed)/2] (0.12s)  ---only 1 car in an in

    # set up
    starTime = 0

    def __init__(self):
        self.start = 1
        self.head = Reservation(0, 0, 0, 0, 0)
        self.tail = Reservation(99, 0, 0, 0, 0)
        self.size = 0
        self.starTime = time.time()

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
            if self.head.nextt == None:
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
            print "Expected time does not fit, finding new location for: " + str(res.toString())
            cursor = self.look_right_initial(res)  # makes sure nothing in same LANE is expected after res expectedTime
            if (cursor == None):  # nothing to worry about on the right

                print "no issues regarding lane to the right \n\n"

                print "looking to the left"
                left = self.find_open_left(res)
                can_left = self.withinCriteriaLeft(res, left)
                print "looking to the right"
                right = self.find_open_right(res)
                can_right = self.withinCriteriaRight(res, right)

                if (left != None):
                    print "Option on left: " + str(left.toString())
                else:
                    print "Option on left: none"
                if right != None:
                    print "Option on right: " + str(right.toString())
                else:
                    print "Option on right: none"

                print "\n\nchecking if within car criteria:.."
                # print "left: " + str(self.withinCriteriaLeft(res,left))
                # print "right: " + str(self.withinCriteriaRight(res,right))

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
                print "same lane at end of list"
                # reservation must be at end of the list
                res.expectedTime = self.tail.prev.expectedTime + self.inter_tolerance_time  # expected for proposed??
                # within criteria?
                can_right = self.withinCriteriaRight(res, cursor)
                res.requestedAccel = can_right[1]
                self.insertBetween(self.tail.prev, self.tail, res)
            else:
                print "issues regarding lane to the right \n\n"
                print "looking to the right"
                right = self.find_open_right_fromPos(res, cursor)
                can_right = self.withinCriteriaRight(res, right)

                if right != None:
                    print "Option on right: " + str(right.toString())
                    print "Option possible? " + str(can_right)
                else:
                    print "Option on right: none"

                print "\n\nchecking if within car criteria:.."
                # print "left: " + str(self.withinCriteriaLeft(res,left))
                # print "right: " + str(self.withinCriteriaRight(res,right))

                goal = self.calcEnergyNeeded(res, right, right)  # TODO: makes this one input at a time
                if can_right[0]:
                    # send data to car for plan for acceleration
                    # adjust estimated tim
                    res.expectedTime = right.expectedTime + self.inter_tolerance_time
                    res.requestedAccel = can_right[1]
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
        eng2 = abs(option1.expectedTime + self.inter_tolerance_time - res.expectedTime)
        return eng1, eng2

    # returns tue/false,acceleration value
    # Todo: incorperate current acceleratiuon value!! you fool!!!!!!!!!!!!!
    def withinCriteriaLeft(self, res, option):  # option1 is left search, option2 is right search
        opt1_time = (option.expectedTime - self.inter_tolerance_time) - option.enterTime
        left = (2 * (self.inter_side_length - res.speed * opt1_time)) / (opt1_time ** 2)

        if (left < 0) and (left > self.car_max_decel):  # check if pos or neg, compare to mac accel/dec and update res
            # print "left deceleration approved!"
            return True, left
        elif (left > 0) and (left < self.car_max_accel):
            # print
            # "left acceleration approved!"
            return True, left
        else:
            return False, left

    # returns tue/false,acceleration value
    # Todo: incorperate current acceleratiuon value!! you fool
    def withinCriteriaRight(self, res, option):
        optionTime = (option.expectedTime + self.inter_tolerance_time) - option.enterTime
        right = (2 * (self.inter_side_length - res.speed * optionTime)) / (optionTime ** 2)
        if (right < 0) and (
                right > self.car_max_decel):  # check if pos or neg, compare to mac accel/dec and update res
            print "right deceleration approved!"
            return True, right
        elif (right > 0) and (right < self.car_max_accel):
            print
            "right acceleration approved!"
            return True, right
        else:
            return False, right

    def print_as_list(self):
        # Create empty list
        value_list = []
        if self.head != None:
            current_node = self.head.nextt
            # Start at head and check if next is not tail
            while current_node.nextt != None:
                # Add current node to list and traverse forward
                value_list.append(current_node.toString())
                print current_node.toString()
                current_node = current_node.nextt
            # rint value_list
        else:
            # print "No nodes"
            return False

    # check if lane is safe: (1)lane is empty at that time (2) does not cut the line in its lane
    def check_avalability_initial(self, res):
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
                if (abs(n.expectedTime - res.expectedTime) < self.inter_tolerance_time) or (
                        (n.expectedTime > res.expectedTime) and (
                        n.lane == res.lane)):  # (1) colision in lane  (2) line skip   TODO:specify whitch criteria it failed at
                    # print abs(n.expectedTime - res.expectedTime)
                    # print "no room"
                    return False
                n = n.nextt
            if n is self.tail:
                # print("appears to be room")
                return True

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

    # find open space to left: (1) size greater than tolerance*2 (2) no line skipping
    # returns head. if nothing found
    def find_open_right(self, res):
        current_node = self.find_closest(res)

        while (current_node.vin != 99):
            if abs(
                    current_node.expectedTime - current_node.nextt.expectedTime) > 2 * self.inter_tolerance_time:  # (1) enough space  lane
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

    def insertBetween(self, spot1, spot2, info):
        new_node = info
        new_node.nextt = spot2
        new_node.prev = spot1
        spot1.nextt = new_node
        spot2.prev = new_node
