import Intersection_Class as IC
import Car_Class as CC
import time as T

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


        quads.append(self.q1)
        quads.append(self.q2)
        quads.append(self.q3)
        quads.append(self.q4)

    def toString(self):
        for q in quads:
            print q.name
            print(q.print_as_list())

    def addReservation(self, res):
        newNode = res
        if newNode.lane == 1:
            print "lane 1"
            # must check lane 1 and lane 2
            while(newNode.set != 1): #continue looking until reservation is set and safe

                if quads[0].check_avalability_initial(newNode): #availble in q1?
                    print "q1 open"

                    #check to see if q2 is open
                    q2_status = quads[1].check_avalability_time(newNode.expectedTime2)
                    if q2_status[0]: #availble in q2?
                        print "q2 open"
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
                    else:                                            #not available in q2, find open time in q2

                        print "q2 not open"

                        # calculate accel and abilties value needed
                        left = quads[1].find_open_left_alt(res.expectedTime2,res.lane)
                        can_left = quads[1].withinCriteriaLeft(res, left)

                        right = quads[1].find_open_right(res)
                        can_right = quads[1].withinCriteriaRight(res, right)

                        #how much energy is needed
                        goal = quads[1].calcEnergyNeeded2(res, left, right)

                        # calculate expeecetd time
                        test_expectedTime_left = IC.expect(-95,res.speed,res.accel + can_left[1]) + res.enterTime
                        test_expectedTime_right = IC.expect(-95, res.speed, res.accel + can_right[1]) + res.enterTime

                        #check if new expected time fits in P1
                        left_fit = quads[0].check_avalability_time(test_expectedTime_left)
                        right_fit = quads[0].check_avalability_time(test_expectedTime_right)

                        goal = 1,2
                        print(goal)
                        if left_fit[0] or right_fit[0]:   #new time can fit for P1

                            if (goal[0] <= goal[1]) and can_left[0] and left_fit:  # less energy to get to left and witin criteria and fits in P1
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

                            print("Proposed new time/accel works, adding to both P1 and P2")
                            newNode.set = 1 #end search

                        else: #neither propsed time can fit
                            print("neither option work for P1, find a greater changing option in P2")








        else:
            print"unknown lane"


# create intersection manager
manager = Intersection_Manager()

#geneate a car
vin = 1
speed = 10
accel = 0.0
time = T.time()
lane = 1
test_car = CC.Car(vin, speed, accel, time, lane)

# generate test reservation
tempRes = IC.Reservation(test_car.vin, test_car.speed, test_car.accel0, test_car.enterTime0, test_car.lane)


#fake fill for P2
fakeRes = IC.Reservation(69,10,0,T.time()  ,2)
fakeRes.expectedTime= tempRes.expectedTime2 - 0.1
manager.q2.insertBetween(manager.q2.head,manager.q2.tail,fakeRes)

print(tempRes.toString())

# attempt to add reservation
manager.addReservation(tempRes)

manager.toString()

