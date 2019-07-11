"""
goals for car:

abilities:
    (1) send initial data when entering intersection
    (2) receive an acceleration value to follow until inside middle of intersection (lane/reserved location eventually)
    (3) request an acceleration value
    (4) follow requested acceleration value until reached nominal speed

Things to store:
    (1) current trajectory
    (2) requested_in trajectory
    (3) requested_out trajectory

Things I don't know:
    (1) where do i store intersection data? some needs to be sent to car


"""

import time
import cmath
import numpy as np


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


class Car:
    # car criteria
    car_max_accel = 3
    car_max_decel = -3
    car_max_speed = 50

    # Intersection Criteria
    inter_side_length = 100
    inter_max_speed = 20
    inter_tolerance_time = 0.12  # intersection_side_length/[(max_Speed + min_speed)/2] (0.12s)  ---only 1 car in an in

    # Instructions
    accel0 = 0  # original acceleration value
    accel01 = 0  # first requested acceleration value
    accel1 = 0  # outgoing requested acceleration value

    # Timeline
    enterTime0 = 0  # time entering intersection
    enterTime1 = 0  # time entering second half of intersection
    exitTime = 0  # time leaving intersection

    # Proposed Timeline
    expectedTime0 = 0  # original specs
    expectedTime01 = 0  # after first update to middle
    expectedTime1 = 0  # after seconds update to end

    # simulation specs
    max_time = 1
    resolution = max_time * 10

    def __init__(self, VIN, speed, accel, enterTime, lane):
        self.vin = VIN
        self.speed = speed
        self.accel0 = accel
        self.enter = 0  # 0 if entering intesection -- 1 if in middle --- 2 if exiting
        self.enterTime0 = enterTime
        self.expectedTime0 = time.time() + expect(-100, self.speed, self.accel0)  # not really used
        self.lane = lane

    def toString(self):
        return ("[ Vin: " + str(self.vin) + " ,speed: " + str(self.speed) + " ,accel0: " + str(
            self.accel0) + " ,Entered time: " + str(self.enterTime0) + " ,Lane #: " + str(
            self.lane) + " ,Expected time #: " + str(self.expectedTime0) + " ,first requested accel #: " + str(
            self.accel01) + "]")

    def updateAccel01(self, a):
        self.accel01 = a[0]
        self.expectedTime01 = a[1]

    def updateExpectedTime01(self, t):
        self.expectedTime01 = t

    def distanceTravelled(self):
        time = np.linspace(0, self.max_time, self.resolution)
        path=  np.piecewise(time, [time < 0, time >= 0], [0, self.trajectory01(time, 0)])
        return path
    def trajectory0(self, time, pos):
        return pos + (self.speed * time) + (0.5 * self.accel0 * (time ** 2))

    def trajectory01(self, time, pos):
        return pos + (self.speed * time) + (0.5 * self.accel01 * (time ** 2))


"""
test = Car(0, 0, 1.0, time.time(), 2)
print test.toString()
test.distanceTravelled()
"""