import Intersection_Class as IC
import Car_Class as CC
import time as T
import csv










intersection_grid_size = 2  # square dimensions of in side intersection



class Intersection_Manager:
    quads = []  # stores all Qs
    count = 0
    #who is going to own this stuff??
    # Intersection Criteria
    inter_side_length = 200
    inter_size = 20
    inter_max_speed = 20
    inter_tolerance_time = 0.1
    p1_distance = -1 * (inter_side_length - (inter_size / 2))
    p2_distance = -1 * (inter_side_length + (inter_size / 2))



    def __init__(self):
        self.q1 = IC.Intersection(0)
        self.q2 = IC.Intersection(1)
        self.q3 = IC.Intersection(2)
        self.q4 = IC.Intersection(3)
        self.quads.append(self.q1)
        self.quads.append(self.q2)
        self.quads.append(self.q3)
        self.quads.append(self.q4)

        self.starTime = T.time()


    def toString(self):
        for q in self.quads:
            print(q.name)
            print(q.print_as_list())

    def addReservation(self, res):
        newNode = None
        print res.toString()
        if res.lane == 1:
            if res.turn == 1:
                newNode = self.quadBooker_RightTurn(0, res.lane, res)
            else:
                newNode = self.quadBooker_straight(0, 1, res)
        elif res.lane == 2:
            if res.turn == 1:
                newNode = self.quadBooker_RightTurn(0, res.lane, res)
            else:
                newNode = self.quadBooker_straight(1, 2, res)
        elif res.lane == 3:
            if res.turn == 1:
                newNode = self.quadBooker_RightTurn(0, res.lane, res)
            else:
                newNode = self.quadBooker_straight(2, 3, res)
        elif res.lane == 4:
            if res.turn == 1:
                newNode = self.quadBooker_RightTurn(0, res.lane, res)
            else:
                newNode = self.quadBooker_straight(3, 0, res)
        else:
            print("unknown lane")
        print newNode.toString()
        return newNode.requestedAccel, 2, newNode.expectedTime

    def quadBooker_straight(self, P1, P2, res):
        self.count = 0
        newNode = res
        # must check lane 1 and lane 2
        while (newNode.set != 1):  # continue looking until reservation is set and safe
            print ("\n\n")
            if self.quads[P1].check_time_and_colision(newNode)[0]:

                print ("P1 open")
                # check to see if q2 is open
                q2_status = self.quads[P2].simple_check_time2(newNode)
                if q2_status[0]:  # availble in q2?
                    print ("P2 open")

                    # insert reservation
                    # insert generic reservation, only expected time
                    simpleRes = IC.Reservation(newNode.vin, newNode.speed, newNode.accel,
                                               newNode.enterTime, newNode.lane, newNode.turn, newNode.length, newNode.width)
                    simpleRes.expectedTime = newNode.expectedTime2
                    simpleRes.expectedTime2 = None
                    simpleRes.requestedAccel = None
                    self.quads[P2].insertBetween(q2_status[1], q2_status[1].nextt, simpleRes)


                    #check if first node:
                    if self.quads[P1].head.nextt == self.quads[P1].tail:
                        self.quads[P1].insertBetween(self.quads[P1].head, self.quads[P1].head.nextt, newNode)
                        newNode.set = 1
                    else:
                        q1_status = self.quads[P1].simple_check_time(newNode)[1]  # TODO already calculated in if statment...
                        self.quads[P1].insertBetween(q1_status, q1_status.nextt, newNode)
                        newNode.set = 1
                else:  # not available in q2, find open time in q2
                    print ("P2 not open")
                    newNode = self.quads[P1].findNextBest(newNode)
            else:
                self.count = self.count + 1
                if self.count == 15:
                    print newNode.accel
                    exit(10)
                print("P1 does not fit")
                # find next possible time for P1
                newNode = self.quads[P1].findNextBest(newNode)
                print "proposing accel of: " + str(newNode.accel)
        return newNode

    def quadBooker_RightTurn(self, P1, lane, res):
        self.count = 0
        newNode = res
        # must check lane 1 and lane 2
        while (newNode.set != 1):  # continue looking until reservation is set and safe
            print ("\n\n")
            if self.quads[P1].check_time_and_colision(newNode)[0]:
                print ("P1 open")
                # check if first node:
                if self.quads[P1].head.nextt == self.quads[P1].tail:
                    self.quads[P1].insertBetween(self.quads[P1].head, self.quads[P1].head.nextt, newNode)
                    newNode.set = 1
                else:
                    q1_status = self.quads[P1].simple_check_time(newNode)[1]
                    self.quads[P1].insertBetween(q1_status, q1_status.nextt, newNode)
                    newNode.set = 1
            else:
                self.count = self.count + 1
                if self.count == 15:
                    print newNode.accel
                    exit(10)
                print("P1 does not fit")
                # find next possible time for P1
                newNode = self.quads[P1].findNextBest(newNode)
                print "proposing accel of: " + str(newNode.accel)
        return newNode

































