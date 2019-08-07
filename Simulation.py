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

for i in range(20):
    # generate data
    vin = i
    lane = random.randint(1, 4)
    delay = random.randrange(40, 50, 1) / 60.0
    speed = random.randrange(900, 1100, 1) / 100.00
    accel = 0#random.randrange(-1, 1, 1) / 10.0
    turn = 0 #random.randint(0, 1)
    lenth = 2.5
    width = 1.5
    #time.sleep(getDelay(lane, lenth))
    time.sleep(0.6 * 1.2 * 1.1)

    # create car
    test_car = CC.Car(vin, speed, accel, time.time(), lane, turn, lenth, width)

    # generate a possible reservation
    test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn, test_car.length, test_car.width)

    # request a reservation
    test_car.updateAccel01(manager.addReservation(test_res))

    # copy path data to csv file
    list_car_data.append(test_car.distanceTravelled(manager.starTime))



"""
start = time.time()
# generate data
vin = 1
lane = 1
delay = 0
speed = 9.72
accel = 0.06
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

print manager.toString()

# generate data
vin = 2
lane = 2
delay = 0
speed = 10.49
accel = 0
turn = 0
# create car
test_car = CC.Car(vin, speed, accel, start + 0.82, lane, turn, lenth, width)

# generate a possible reservation
test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn, lenth, width)

# request a reservation
test_car.updateAccel01(manager.addReservation(test_res))

# copy path data to csv file
list_car_data.append(test_car.distanceTravelled(manager.starTime))

"""




with open('carData.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(list_car_data)
csvFile.close()


print(manager.toString())