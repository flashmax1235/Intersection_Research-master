import Intersection_Class as IC
import Car_Class as CC
import time
import random
import Encode as E
import csv
import Tkinter as tk

# start intersection
intersection = IC.Intersection()
list_car_data = []

for i in range(20):
    # generate a car
    vin = i
    lane = random.randint(1, 4)
    delay = random.randrange(1, 50, 1) / 60.0
    speed = random.randrange(90, 110, 1) / 10.0
    accel = random.randrange(-5, 5, 1) / 10.0
    time.sleep(delay)
    test_car = CC.Car(vin, speed, accel, time.time(), lane)

    # generate a possible reservation
    test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane)

    # request a reservation
    test_car.updateAccel01(intersection.addReservation3(test_res))

    # copy path data to csv file
    list_car_data.append(test_car.distanceTravelled(intersection.starTime))

    print intersection.print_as_list()


with open('carData.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(list_car_data)
csvFile.close()

