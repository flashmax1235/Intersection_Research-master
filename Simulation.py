import Intersection_Manager_class as IMC
import Intersection_Class as IC
import Car_Class as CC
import time
import random
import csv


manager = IMC.Intersection_Manager()
list_car_data = []

for i in range(10):
    # generate data
    vin = i
    lane = random.randint(1, 4)
    delay = random.randrange(30, 40, 1) / 60.0
    speed = random.randrange(90, 110, 1) / 10.0
    accel = random.randrange(-5, 5, 1) / 10.0
    turn = random.randrange(0, 1, 1)
    time.sleep(delay)
    # create car
    test_car = CC.Car(vin, speed, accel, time.time(), lane, turn)

    # generate a possible reservation
    test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn)

    # request a reservation
    test_car.updateAccel01(manager.addReservation(test_res))

    # copy path data to csv file
    list_car_data.append(test_car.distanceTravelled(manager.starTime))






with open('carData.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(list_car_data)
csvFile.close()


print(manager.toString())