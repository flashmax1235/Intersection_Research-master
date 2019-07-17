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
        #vaariables used..
        needNewNode = False
        left_fit = [False, 0]
        right_fit = [False, 0]
        goal = [0, 0]
        can_right = [0, 0]
        can_left = [0, 0]
        left = 0
        right = 0

        newNode = res
        if newNode.lane == 1:
            print ("lane 1")
            # must check lane 1 and lane 2
            while(newNode.set != 1): #continue looking until reservation is set and safe

                if quads[0].check_avalability_initial(newNode): #availble in q1?
                    print ("q1 open")

                    #check to see if q2 is open
                    q2_status = quads[1].check_P2_Avalibility(newNode.expectedTime2)
                    if q2_status[0]: #availble in q2?
                        print ("q2 open")
                       # insert reservation

                        # insert generic reservation, only expected time
                        simpleRes = IC.Reservation(newNode.vin, newNode.speed, newNode.accel,
                                                   newNode.enterTime, newNode.lane)
                        simpleRes.expectedTime = newNode.expectedTime2
                        simpleRes.expectedTime2 = None
                        simpleRes.requestedAccel = None
                        quads[1].insertBetween(q2_status[1], q2_status[1].nextt, simpleRes)

                        q1_status = quads[0].check_avalability_time(newNode.expectedTime)         #TODO already calculated in if statment...


                        quads[0].insertBetween(q1_status[1], q1_status[1].nextt, newNode)
                        newNode.set = 1
                    else:                                      #not available in q2, find open time in q2
                        print ("q2 not open")
                        while not (left_fit[0] or right_fit[0]):
                            print("neither option work for P1, find a greater changing option in P2")
                            # calculate accel and abilties value needed
                            left = quads[1].find_open_left_alt(newNode.expectedTime2,res.lane)  #spot in p2 that is open
                            can_left = quads[1].withinCriteriaLeftp2(newNode, left)         #accel value needed to reach opnening

                            right = quads[1].find_open_right(newNode)                           #spot in p2 that is open
                            can_right = quads[1].withinCriteriaRightp2(newNode, right)      #accel value needed to reach opnening

                            #how much energy is needed
                            goal = quads[1].calcEnergyNeeded2(newNode, left, right)         #how much time is waisted for either option

                            # calculate expeecetd time
                            # expectedtime with proposed accel value
                            test_expectedTime_left = IC.expect(-95,newNode.speed,newNode.accel + can_left[1]) + newNode.enterTime
                            test_expectedTime_right = IC.expect(-95, newNode.speed, newNode.accel + can_right[1]) + newNode.enterTime


                            #check if new expected time fits in P1
                            left_fit = quads[0].check_P2_Avalibility(test_expectedTime_left)
                            right_fit = quads[0].check_P2_Avalibility(test_expectedTime_right)


                            print("left expectTime: " + str(test_expectedTime_left))
                            print("right expectTime: " + str(test_expectedTime_right))

                            print(goal)

                        #----------------------------------

                        print("Proposed new time/accel works, adding to both P1 and P2")
                        if (goal[0] <= goal[1]) and can_left[0] and left_fit:  # less energy to get to left and witin criteria and fits in P1
                            print("case1")
                            #update fields
                            newNode.expectedTime = test_expectedTime_left
                            newNode.expectedTime2 = left.expectedTime - self.inter_tolerance_time
                            newNode.requestedAccel = can_left[1]

                            #insert reservation

                            #insert generic reservation, only expected time
                            simpleRes = IC.Reservation(newNode.vin,newNode.speed,newNode.accel,newNode.enterTime,newNode.lane)
                            simpleRes.expectedTime = newNode.expectedTime2
                            simpleRes.expectedTime2 = None
                            simpleRes.requestedAccel = None
                            quads[1].insertBetween(left.prev,left, simpleRes)

                            quads[0].insertBetween(left_fit[1],left_fit[1].nextt,newNode)
                        elif (goal[0] >= goal[1]) and can_right[0] and right_fit:  # less energy to get to right and witin criteria and fits P1
                            print("case2")
                            # update fields
                            newNode.expectedTime = test_expectedTime_right
                            newNode.expectedTime2 = right.expectedTime + self.inter_tolerance_time
                            newNode.requestedAccel = can_right[1]

                            # insert reservation

                            # insert generic reservation, only expected time
                            simpleRes = IC.Reservation(newNode.vin, newNode.speed, newNode.accel,
                                                       newNode.enterTime, newNode.lane)
                            simpleRes.expectedTime = newNode.expectedTime2
                            simpleRes.expectedTime2 = None
                            simpleRes.requestedAccel = None
                            quads[1].insertBetween(right, right.nextt, simpleRes)

                            quads[0].insertBetween(left_fit[1], left_fit[1].nextt, newNode)
                        #less eficient cases
                        elif ~can_left[0] and can_right[0]:   #
                            print("case3")
                            # update fields
                            newNode.expectedTime = test_expectedTime_right
                            newNode.expectedTime2 = right.expectedTime + self.inter_tolerance_time
                            newNode.requestedAccel = can_right[1]

                            # insert reservation

                            # insert generic reservation, only expected time
                            simpleRes = IC.Reservation(newNode.vin, newNode.speed, newNode.accel,
                                                       newNode.enterTime, newNode.lane)
                            simpleRes.expectedTime = newNode.expectedTime2
                            simpleRes.expectedTime2 = None
                            simpleRes.requestedAccel = None
                            quads[1].insertBetween(right, right.nextt, simpleRes)

                            quads[0].insertBetween(left_fit[1], left_fit[1].nextt, newNode)
                        elif can_left[0] and ~can_right[0]:
                            print("case4")
                            # update fields
                            newNode.expectedTime = test_expectedTime_left
                            newNode.expectedTime2 = left.expectedTime - self.inter_tolerance_time
                            newNode.requestedAccel = can_left[1]

                            # insert reservation

                            # insert generic reservation, only expected time
                            simpleRes = IC.Reservation(newNode.vin, newNode.speed, newNode.accel,
                                                       newNode.enterTime, newNode.lane)
                            simpleRes.expectedTime = newNode.expectedTime2
                            simpleRes.expectedTime2 = None
                            simpleRes.requestedAccel = None
                            quads[1].insertBetween(left.prev, left, simpleRes)

                            quads[0].insertBetween(left_fit[1], left_fit[1].nextt, newNode)
                        else:
                            print("shit nothing fits...")

                        newNode.set = 1 #end search

                else:
                    print("P1 does not fit")
                    # find opening to right of newNode
                    cursor = quads[0].find_open_right(newNode)  #TODO: should also look for open left *lane matters*
                    print(cursor)


                    #check if opening to the rights fits car criteria
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
fakeRes.expectedTime= tempRes.expectedTime
manager.q1.insertBetween(manager.q1.head,manager.q1.tail,fakeRes)


print(fakeRes.toString())

#fake fill for P2
fakeRes = IC.Reservation(79,10,0,T.time(),2)
fakeRes.expectedTime= tempRes.expectedTime2 - .7
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

