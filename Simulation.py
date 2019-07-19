import Intersection_Manager_class as IMC
import Intersection_Class as IC
import Car_Class as CC
import time
import random
import csv


manager = IMC.Intersection_Manager()
list_car_data = []

for i in range(1):
    # generate data
    vin = i
    lane = random.randint(1, 1)
    delay = random.randrange(30, 40, 1) / 60.0
    speed = random.randrange(90, 110, 1) / 10.0
    accel = random.randrange(-2, 2, 1) / 10.0
    turn = 2 #random.randint(0, 1)
    time.sleep(delay)
    # create car
    test_car = CC.Car(vin, speed, accel, time.time(), lane, turn)

    # generate a possible reservation
    test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn)

    # request a reservation
    test_car.updateAccel01(manager.addReservation(test_res))

    # copy path data to csv file
    list_car_data.append(test_car.distanceTravelled(manager.starTime))

"""
# generate data
vin = 1
lane = 1
delay = 0
speed = 10
accel = 0
turn = 0

# create car
test_car = CC.Car(vin, speed, accel, time.time(), lane, turn)

# generate a possible reservation
test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn)

# request a reservation
test_car.updateAccel01(manager.addReservation(test_res))

# copy path data to csv file
list_car_data.append(test_car.distanceTravelled(manager.starTime))

# generate data
vin = 2
lane = 1
delay = 0
speed = 10.5
accel = 2
turn = 0

# create car
test_car = CC.Car(vin, speed, accel, time.time() + 0.25, lane, turn)

# generate a possible reservation
test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn)

# request a reservation
test_car.updateAccel01(manager.addReservation(test_res))

# copy path data to csv file
list_car_data.append(test_car.distanceTravelled(manager.starTime))

# generate data
vin = 3
lane = 1
delay = 0
speed = 11
accel = 1.0
turn = 0

# create car
test_car = CC.Car(vin, speed, accel, time.time() + 0.45, lane, turn)

# generate a possible reservation
test_res = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane, turn)

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