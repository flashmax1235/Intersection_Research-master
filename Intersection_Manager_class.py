import Intersection_Class as IC
import Car_Class as CC
import time as T
import csv






"""
check lanes you bitvh!!!



"""










intersection_grid_size = 2  # square dimensions of in side intersection
quads = []  # stores all Qs


class Intersection_Manager:

    #who is going to own this stuff??
    # Intersection Criteria
    inter_side_length = 100
    inter_size = 10
    inter_max_speed = 20
    inter_tolerance_time = 0.2  # intersection_side_length/[(max_Speed + min_speed)/2] (0.12s)  ---only 1 car in an in
    p1_distance = -1 * (inter_side_length - (inter_size / 2))
    p2_distance = -1 * (inter_side_length + (inter_size / 2))
    check_resolution = inter_tolerance_time/4


    def __init__(self):
        self.q1 = IC.Intersection("q1")
        self.q2 = IC.Intersection("q2")
        self.q3 = IC.Intersection("q3")
        self.q4 = IC.Intersection("q4")
        quads.append(self.q1)
        quads.append(self.q2)
        quads.append(self.q3)
        quads.append(self.q4)

        self.starTime = T.time()


    def toString(self):
        for q in quads:
            print(q.name)
            print(q.print_as_list())

    def addReservation(self, res):
        newNode = None
        print res.toString()
        if res.lane == 1:
            if res.turn == 1:
                newNode = self.quadBooker_RightTurn(0,res.lane,res)
            else:
                newNode = self.quadBooker_straight(0, 1, res)
        elif res.lane == 2:
            newNode = self.quadBooker_straight(1, 2, res)
        elif res.lane == 3:
            newNode = self.quadBooker_straight(2, 3, res)
        elif res.lane == 4:
            newNode = self.quadBooker_straight(3, 0, res)
        else:
            print("unknown lane")
        print newNode.toString()
        return newNode.requestedAccel, newNode.expectedTime

    def quadBooker_straight(self, P1, P2, res):
        newNode = res
        # must check lane 1 and lane 2
        while (newNode.set != 1):  # continue looking until reservation is set and safe
            if quads[P1].check_avalability_initial(newNode):  # availble in q1?
                print ("P1 open")

                # check to see if q2 is open
                q2_status = quads[P2].check_P2_Avalibility(newNode.expectedTime2)
                if q2_status[0]:  # availble in q2?
                    print ("P2 open")
                    # insert reservation
                    if(newNode.vin == 3):
                        print "here"
                    # insert generic reservation, only expected time
                    simpleRes = IC.Reservation(newNode.vin, newNode.speed, newNode.accel,
                                               newNode.enterTime, newNode.lane, newNode.turn)
                    simpleRes.expectedTime = newNode.expectedTime2
                    simpleRes.expectedTime2 = None
                    simpleRes.requestedAccel = None
                    quads[P2].insertBetween(q2_status[1], q2_status[1].nextt, simpleRes)


                    #check if first node:
                    if quads[P1].head.nextt == quads[P1].tail:
                        quads[P1].insertBetween(quads[P1].head, quads[P1].head.nextt, newNode)
                        newNode.set = 1
                    else:
                        q1_status = quads[P1].find_closest(newNode)  # TODO already calculated in if statment...
                        quads[P1].insertBetween(q1_status, q1_status.nextt, newNode)
                        newNode.set = 1

                else:  # not available in q2, find open time in q2
                    print ("P2 not open")
                    # find next avalible change P1 only looking to the right todo: UNECSSARY INITIAL CHECK


                    #todo: turn into function plzz
                    # find next possible time for P1
                    GoodSpot = False
                    possibleTime = newNode.expectedTime + self.inter_tolerance_time / 2

                    while not GoodSpot:
                        #print "propsed time is: " + str(possibleTime)
                        result = quads[P1].check_avalability_time(possibleTime)
                        if not result[0]:  # not avalible, something in the way, going tolook after that thing
                            if (result[1] == quads[P1].tail):
                                possibleTime = possibleTime + self.inter_tolerance_time / 2
                            else:
                                possibleTime = result[1].expectedTime + self.inter_tolerance_time / 2
                        else:
                            GoodSpot = result[0]

                        #print (result[0], result[1].toString())

                        #T.sleep(0.5)

                    # update expected time
                    newNode.expectedTime = possibleTime

                    # calculate accel value needed for P1, update accel and requested accel
                    newNode.accel = quads[P1].getAccelValue(newNode, possibleTime, -1 * self.p1_distance)
                    newNode.requestedAccel = newNode.accel
                    newNode.expectedTime2 = IC.expect(self.p2_distance, newNode.speed, newNode.accel) + newNode.enterTime
            else:
                print("P1 does not fit")
                # find next possible time for P1
                GoodSpot = False
                possibleTime = newNode.expectedTime + self.inter_tolerance_time / 2

                while not GoodSpot:
                   # print "propsed time is: " + str(possibleTime)
                    result = quads[P1].check_avalability_time(possibleTime)
                    if not result[0]:  # not avalible, something in the way, going tolook after that thing
                        if (result[1] == quads[P1].tail):
                            possibleTime = possibleTime + self.inter_tolerance_time / 2
                        else:
                            possibleTime = result[1].expectedTime + self.inter_tolerance_time / 2
                    else:
                        GoodSpot = result[0]

                # update expected time

                newNode.expectedTime = possibleTime

                # calculate accel value needed for P1, update accel and requested accel
                newNode.accel = quads[P1].getAccelValue(newNode, possibleTime, -1 * self.p1_distance)
                newNode.requestedAccel = newNode.accel
                newNode.expectedTime2 = IC.expect(self.p2_distance, newNode.speed, newNode.accel) + newNode.enterTime
        return newNode

    def quadBooker_RightTurn(self, P1, lane, res):
        newNode = res
        # must check lane 1 and lane 2
        while (newNode.set != 1):  # continue looking until reservation is set and safe
            if quads[P1].check_avalability_initial(newNode):  # availble in q1?
                print ("P1 open")

                #set accel value
                newNode.requestedAccel = newNode.accel

                # check if first node:
                if quads[P1].head.nextt == quads[P1].tail:
                    quads[P1].insertBetween(quads[P1].head, quads[P1].head.nextt, newNode)
                    newNode.set = 1
                else:
                    q1_status = quads[P1].find_closest(newNode)  # TODO already calculated in if statment...
                    quads[P1].insertBetween(q1_status, q1_status.nextt, newNode)
                    newNode.set = 1
            else:
                print("P1 does not fit")
                # find next possible time for P1
                GoodSpot = False
                possibleTime = newNode.expectedTime + self.inter_tolerance_time / 2

                while not GoodSpot:
                    # print "propsed time is: " + str(possibleTime)
                    result = quads[P1].check_avalability_time(possibleTime)
                    if not result[0]:  # not avalible, something in the way, going tolook after that thing
                        if (result[1] == quads[P1].tail):
                            possibleTime = possibleTime + self.inter_tolerance_time / 2
                        else:
                            possibleTime = result[1].expectedTime + self.inter_tolerance_time / 2
                    else:
                        GoodSpot = result[0]

                # update expected time
                newNode.expectedTime = possibleTime

                # calculate accel value needed for P1, update accel and requested accel
                newNode.accel = quads[P1].getAccelValue(newNode, possibleTime, -1 * self.p1_distance)
                newNode.requestedAccel = newNode.accel
                newNode.expectedTime2 = IC.expect(self.p2_distance, newNode.speed, newNode.accel) + newNode.enterTime
        newNode.requestedAccel = newNode.accel
        return newNode


































