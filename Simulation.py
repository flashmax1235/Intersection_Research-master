import Intersection_Manager_class as IMC
import Intersection_Class as IC
import Car_Class as CC
import time
import random
import csv
import numpy as np


manager = IMC.Intersection_Manager()
list_car_data = []
pastLane = None
startTime = 0
timeLimit = 20 #seconds
numberOfCars = 1
speedLimit = 35
maxSpeed = 40 # not used
minSpeed = 20 # not used






def clearFile():
    file = open('carData.csv', 'w')
    file.truncate()

def addLine(data):
    with open('carData.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(data)
    csvFile.close()


#clear old data
clearFile()

#generate cars
cars = []

for i in range(numberOfCars):
    # generate data
    vin = i
    lane = random.randint(1, 1)
    delay = random.randrange(500, 600, 1)
    speed = 20#random.randrange(3400, 3600, 1) / 100.00
    accel = 0.2
    turn = 0 #random.randint(0, 1)
    lenth = random.randrange(20, 30, 1) / 10.0
    width = random.randrange(10, 20, 1) / 10.0

    if pastLane == lane:
        delay = 800
    startTime = startTime + delay
    pastLane = lane

    # create car
    test_car = CC.Car(vin, speed, accel, startTime, lane, turn, lenth, width)
    cars.append(test_car)


"""
vin = 1
lane = 1
delay = 0
speed = 35
accel = 0 #random.randrange(-1, 1, 1) / 10.0
turn = 0 #random.randint(0, 1)
lenth = 2.5#random.randrange(20, 30, 1) / 10.0
width = 1.5#random.randrange(10, 20, 1) / 10.0

startTime = startTime + delay

# create car
test_car = CC.Car(vin, speed, accel, startTime, lane, turn, lenth, width)
cars.append(test_car)


vin = 2
lane = 2
delay = 900
speed = 37
accel = 0 #random.randrange(-1, 1, 1) / 10.0
turn = 0 #random.randint(0, 1)
lenth = 2.5#random.randrange(20, 30, 1) / 10.0
width = 1.5#random.randrange(10, 20, 1) / 10.0

startTime = startTime + delay

# create car
test_car = CC.Car(vin, speed, accel, startTime, lane, turn, lenth, width)
cars.append(test_car)
"""


#generate header VIN, Lane, length, width
header = []
for i in range(4):
    for C in cars:
        if i == 0:
            header.append(C.vin)
        elif i == 1:
            header.append(C.lane)
        elif i == 2:
            header.append(C.length)
        elif i == 3:
            header.append(C.width)
    addLine(header)
    header = []


#insert each car and get updated accel value
for C in cars:
    C.updateAccel01(manager.addReservation(C.generatereservation()))

#get positioning and check for needing outro
positionsX = []
positionsY = []
currentTime = 0
while (currentTime < timeLimit * 1000):
    for C in cars:
        #check if completed p2  (combine these two checks please)
        if C.expectedTime01 <= currentTime and C.set == 0:  #
            print "needs new accel value"
            C.set = 1

            C.updateAccel1(manager.bookOutro(C.generatereservationOUT()))
            print C.distanceTravelledTime(currentTime)
        #check for done with interection


        positionsX.append(C.distanceTravelledTime(currentTime)[0])
        positionsY.append(C.distanceTravelledTime(currentTime)[1])
    addLine(positionsX)
    addLine(positionsY)
    positionsX = []
    positionsY = []
    currentTime = currentTime + 1

manager.toString()
