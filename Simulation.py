import Intersection_Manager_class as IMC
import Intersection_Class as IC
import Car_Class as CC
import time
import random
import csv
import numpy as np


manager = IMC.Intersection_Manager()
list_car_data = []

def findCarInfront(n):
    current = manager.quads[n-1].tail.prev
    while current.lane != n:
        current = current.prev
    return current

def getDelay(n, l2):
    car = findCarInfront(n)
    if car.length == 0:
        return 0

    dx = (car.length + l2) * 1.5
    dt =dx / car.speed
    for i in range (5):
        dt = dx / (car.speed + car.accel * dt)
    return dt*1.2



for i in range(15):
    # generate data
    vin = i
    lane = random.randint(1, 4)
    delay = random.randrange(30, 35, 1) / 60.0
    speed = random.randrange(3400, 3600, 1) / 100.00
    accel = 0#random.randrange(-1, 1, 1) / 10.0
    turn = 0 #random.randint(0, 1)
    lenth = 2.5
    width = 1.5
    #time.sleep(getDelay(lane, lenth))
    time.sleep(delay)

    # create car
    test_car = CC.Car(vin, speed, accel, time.time(), lane, turn, lenth, width)

    # generate a possible reservation
    test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn, test_car.length, test_car.width)

    # request a reservation
    test_car.updateAccel01(manager.addReservation(test_res))

    # copy path data to csv file
    list_car_data.append(test_car.distanceTravelled(manager.starTime))



#inline whith a hole
"""
start = time.time()
# generate data
vin = 1
lane = 1
delay = 0
speed = 25
accel = 0.0
turn = 0
lenth = 2.5
width = 1.5
# create car
test_car = CC.Car(vin, speed, accel, start, lane, turn, lenth, width)

# generate a possible reservation
test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn, lenth, width)

# request a reservation
test_car.updateAccel01(manager.addReservation(test_res))

# copy path data to csv file
list_car_data.append(test_car.distanceTravelled(manager.starTime))

manager.toString()

# generate data
vin = 2
lane = 1
delay = 0
speed = 25
accel = 0
turn = 0
lenth = 2.5
width = 1.5
# create car
test_car = CC.Car(vin, speed, accel, start + 0.4, lane, turn, lenth, width)

# generate a possible reservation
test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn, lenth, width)

# request a reservation
test_car.updateAccel01(manager.addReservation(test_res))

# copy path data to csv file
list_car_data.append(test_car.distanceTravelled(manager.starTime))
print "\n\n"
manager.toString()
print "\n\n"

# generate data
vin = 3
lane = 1
delay = 0
speed = 25
accel = 0
turn = 0
lenth = 2.5
width = 1.5
# create car
test_car = CC.Car(vin, speed, accel, start + 0.8, lane, turn, lenth, width)

# generate a possible reservation
test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn, lenth, width)

# request a reservation
test_car.updateAccel01(manager.addReservation(test_res))

# copy path data to csv file
list_car_data.append(test_car.distanceTravelled(manager.starTime))
print "\n\n"
manager.toString()
print "\n\n"

# generate data
vin = 4
lane = 2
delay = 0
speed = 25
accel = 0
turn = 0
lenth = 2.5
width = 1.5
# create car
test_car = CC.Car(vin, speed, accel, start + 1.5, lane, turn, lenth, width)

# generate a possible reservation
test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn, lenth, width)

# request a reservation
test_car.updateAccel01(manager.addReservation(test_res))

# copy path data to csv file
list_car_data.append(test_car.distanceTravelled(manager.starTime))
print "\n\n"
manager.toString()
print "\n\n"


# generate data
vin = 5
lane = 1
delay = 0
speed = 25
accel = 0
turn = 0
lenth = 2.5
width = 1.5
# create car
test_car = CC.Car(vin, speed, accel, start + 1.6, lane, turn, lenth, width)

# generate a possible reservation
test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn, lenth, width)

# request a reservation
test_car.updateAccel01(manager.addReservation(test_res))

# copy path data to csv file
list_car_data.append(test_car.distanceTravelled(manager.starTime))
print "\n\n"
manager.toString()
print "\n\n"
"""

with open('carData.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(list_car_data)
csvFile.close()


print(manager.toString())