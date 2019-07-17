import Intersection_Class as IC
import Car_Class as CC
import time as T
import csv

intersection_grid_size = 2  # square dimensions of in side intersection
quads = []  # stores all Qs


class Intersection_Manager:

    #who is going to own this stuff??
    # Intersection Criteria
    inter_side_length = 100
    inter_size = 10
    inter_max_speed = 20
    inter_tolerance_time = 0.2  # intersection_side_length/[(max_Speed + min_speed)/2] (0.12s)  ---only 1 car in an in



    def __init__(self):
        self.q1 = IC.Intersection("q1")
        self.q2 = IC.Intersection("q2")
        self.q3 = IC.Intersection("q3")
        self.q4 = IC.Intersection("q4")

        # used for the strange case on paper #79
        self.needNewNode = False



        quads.append(self.q1)
        quads.append(self.q2)
        quads.append(self.q3)
        quads.append(self.q4)

    def toString(self):
        for q in quads:
            print(q.name)
            print(q.print_as_list())

    def addReservation(self, res):
        newNode = res
        if newNode.lane == 1:
            print ("lane 1")
            # must check lane 1 and lane 2
            while(newNode.set != 1): #continue looking until reservation is set and safe

                #get current node opening, willuse this if need to look past this
                notThis = quads[0].find_open_right(newNode)  #retuns right side

                if quads[0].check_avalability_initial(newNode): #availble in q1?
                    print ("P1 open")

                    #check to see if q2 is open
                    q2_status = quads[1].check_P2_Avalibility(newNode.expectedTime2)
                    if q2_status[0]: #availble in q2?
                        print ("P2 open")
                       # insert reservation

                        # insert generic reservation, only expected time
                        simpleRes = IC.Reservation(newNode.vin, newNode.speed, newNode.accel,
                                                   newNode.enterTime, newNode.lane)
                        simpleRes.expectedTime = newNode.expectedTime2
                        simpleRes.expectedTime2 = None
                        simpleRes.requestedAccel = None
                        quads[1].insertBetween(q2_status[1], q2_status[1].nextt, simpleRes)



                        q1_status = quads[0].find_closest(newNode)         #TODO already calculated in if statment...



                        quads[0].insertBetween(q1_status, q1_status.nextt, newNode)
                        newNode.set = 1

                    else:                                      #not available in q2, find open time in q2
                        print ("P2 not open")
                        # find next avalible change P1 only looking to the right



                        GoodSpot = False
                        possibleTime = newNode.expectedTime + self.inter_tolerance_time

                        while not GoodSpot:
                            print "propsed time is: " + str(possibleTime)
                            result = quads[0].check_avalability_time(possibleTime)
                            if not result[0]: #not avalible, something in the way, going tolook after that thing
                                if(result[1] == quads[0].tail):
                                    possibleTime = possibleTime + self.inter_tolerance_time
                                else:
                                    possibleTime = result[1].expectedTime + self.inter_tolerance_time
                            else:
                                GoodSpot = result[0]

                            print (result[0], result[1].toString())
                            T.sleep(0.5)
                        exit()





                        # time
                        # accel value
                        # update newNode


                        newNode.set = 1


                else:
                    print("P1 does not fit")
                    # find opening to right of newNode
                    cursor = quads[0].find_open_right(newNode)  #TODO: should also look for open left *lane matters*
                    print(cursor)


                    # check if opening to the rights fits car criteria
                    abilityToTheRight = quads[0].withinCriteriaRight(newNode,cursor)
                    print(abilityToTheRight)

                    if abilityToTheRight[0]:  #if option in P1 is availible and fits criteria
                        # update newNode to match opening
                        newNode.expectedTime = cursor.expectedTime + self.inter_tolerance_time
                        newNode.requestedAccel = abilityToTheRight[1]
                        newNode.accel = newNode.requestedAccel
                        newNode.expectedTime2 = IC.expect(self.inter_side_length,newNode.speed,abilityToTheRight[1]) + newNode.enterTime
                        print("done up[dating new aption")
                        print(newNode.toString())
                    #newNode.set = 1
        elif newNode.lane == 2:
            quads[1].insertBetween(quads[1].head,quads[1].tail,newNode)
        else:
            print("unknown lane")
        return  newNode.requestedAccel, newNode.expectedTime



# create intersection manager
manager = Intersection_Manager()
list_car_data = []

#geneate a car
vin = 1
speed = 10
accel = 0.0
time = T.time()
lane = 1
test_car = CC.Car(vin, speed, accel, time, lane)

# generate test reservation
tempRes = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane)

print("These are res to consider")
print(tempRes.toString())
#fake fill for P1
fakeRes = IC.Reservation(69,10,0,T.time(),2)
fakeRes.expectedTime= tempRes.expectedTime + 0.2
manager.q1.insertBetween(manager.q1.head,manager.q1.tail,fakeRes)


print(fakeRes.toString())

#fake fill for P2
fakeRes = IC.Reservation(79,10,0,T.time(),2)
fakeRes.expectedTime= tempRes.expectedTime2
manager.q2.insertBetween(manager.q2.head,manager.q2.tail,fakeRes)

print(fakeRes.toString())

print("\n\nAdding to Manager\n")

# attempt to add real reservation
test_car.updateAccel01(manager.addReservation(tempRes))

list_car_data.append(test_car.distanceTravelled(quads[0].starTime))

with open('carData.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(list_car_data)
csvFile.close()



print("\n\nLists \n")
manager.toString()

