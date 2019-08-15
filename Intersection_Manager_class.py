import Intersection_Class as IC
import time as T











intersection_grid_size = 2  # square dimensions of in side intersection



class Intersection_Manager:
    quads = []  # stores all Qs
    count = 0
    #who is going to own this stuff??
    # Intersection Criteria
    inter_side_length = 200
    inter_size = 20
    p1_distance = -1 * (inter_side_length - (inter_size / 2))
    p2_distance = -1 * (inter_side_length + (inter_size / 2))



    def __init__(self):
        # inner intersection
        self.q0 = IC.Intersection(0)
        self.q1 = IC.Intersection(1)
        self.q2 = IC.Intersection(2)
        self.q3 = IC.Intersection(3)
        self.quads.append(self.q0)
        self.quads.append(self.q1)
        self.quads.append(self.q2)
        self.quads.append(self.q3)

        #outer intersection
        self.q4 = IC.Intersection(4)
        self.q5 = IC.Intersection(5)
        self.q6 = IC.Intersection(6)
        self.q7 = IC.Intersection(7)
        self.quads.append(self.q4)
        self.quads.append(self.q5)
        self.quads.append(self.q6)
        self.quads.append(self.q7)

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
        return newNode.accel,  newNode.expectedTime2

    def quadBooker_straight(self, P1, P2, res):
        self.count = 0
        newNode = res
        # must check lane 1 and lane 2
        while (newNode.set != 1):  # continue looking until reservation is set and safe
            #print ("\n\n")
            if self.quads[P1].check_time_and_colision(newNode)[0]:

                #print ("P1 open")
                # check to see if q2 is open
                q2_status = self.quads[P2].simple_check_time2(newNode)
                if q2_status[0]:  # availble in q2?
                    #print ("P2 open")

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
                    #print ("P2 not open")
                    newNode = self.quads[P1].findNextBest(newNode)
            else:
                self.count = self.count + 1
                if self.count == 15:
                    #print newNode.accel
                    exit(10)
                #print("P1 does not fit")
                # find next possible time for P1
                newNode = self.quads[P1].findNextBest(newNode)
                #print "proposing accel of: " + str(newNode.accel)
        return newNode

    def quadBooker_RightTurn(self, P1, lane, res):
        self.count = 0
        newNode = res
        # must check lane 1 and lane 2
        while (newNode.set != 1):  # continue looking until reservation is set and safe
            print ("\n\n")
            if self.quads[P1].check_time_and_colision(newNode)[0]:
                #print ("P1 open")
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
                #print("P1 does not fit")
                # find next possible time for P1
                newNode = self.quads[P1].findNextBest(newNode)
                #print "proposing accel of: " + str(newNode.accel)
        return newNode

    def quadBooker_LeftTurn(self, P1, P2, P3, res):
       return "umm"

    def bookOutro(self, res):
        newNode = None
        if res.lane == 1:
            if res.turn == 1:
                newNode = self.findOutro(res, 4)
            else:
                newNode = self.findOutro(res, 5)
        elif res.lane == 2:
            if res.turn == 1:
                newNode = self.findOutro(res, 5)
            else:
                newNode = self.findOutro(res, 6)
        elif res.lane == 3:
            if res.turn == 1:
                newNode = self.findOutro(res, 6)
            else:
                newNode = self.findOutro(res, 7)
        elif res.lane == 4:
            if res.turn == 1:
                newNode = self.findOutro(res, 7)
            else:
                newNode = self.findOutro(res, 4)
        else:
            print("unknown lane")
        print newNode.toString()
        return newNode.OutAccel, newNode.t1




    def findOutro(self,res,PEND):
        newNode = res
        # find car in front
        inFront = self.quads[PEND].tail.prev

        #check if list is empty
        if inFront == self.quads[PEND].head:
            #list is empty assign max Z
            maxZ = 2500
            newNode.updateZ(maxZ)
            self.quads[PEND].insertBetween(inFront, inFront.nextt, newNode)
        else:
            #find maxZ
            maxZ = self.getZmax(newNode, inFront)
            newNode.updateZ(maxZ)
            self.quads[PEND].insertBetween(inFront, inFront.nextt, newNode)
        return newNode


    def distAtT1(self, res):
        dt = (res.t1 - res.expectedTime2) / 1000.0
        a =  abs(self.p2_distance) + (res.endSpeed * dt) + (0.5 * res.OutAccel * dt ** 2)
        return a

    def car_dist(self, res, t):

        # if in adjusting period
        if(t  <= res.t1):
            return (res.speed * (t - res.enterTime)) + (0.50 * res.accel * (t - res.enterTime) ** 2)
        else: #in main loop
            return  (35.0 * ((t - res.t1) / 1000.0)) + self.distAtT1(res)

    # calcualtes max Z value
    # Thanks Webster
    def getZmax(self,res, close):
        """
        deltaT = abs(res.enterTime - close.enterTime)
        print("deltaT: " + str(deltaT))
        deltaX = close.speed * deltaT + (0.5 * close.adjustAccel * deltaT ** 2)
        print("deltaX: " + str(deltaX))
        goal =  self.inter_tolerance_space
        frontCarV = close.speed + close.adjustAccel * deltaT
        frontCarPos = frontCarV * (close.z - deltaT)
        frontCarPos2 = 0.5 * close.adjustAccel * (close.z - deltaT) ** 2
        zmax = 2 * ((goal - deltaX - frontCarPos - frontCarPos2 + (self.inter_nom_speed * (close.z - deltaT)))/ (self.inter_nom_speed - res.speed - 0.001))

        if(zmax > 1.5):
            zmax = 1.5

        return zmax

        """
        minSperation = (res.length + close.length) * 1.2
        while self.T1Seperation(res, close) < minSperation:  #checking min distance and if in same lane
            res.updateZ(res.z * 0.95)
            if(abs(res.z) < 0.01):
                print("nahh")
                exit()
        return res.z

    def T1Seperation(self, res, close):
        print("comparing t1 distance with: " + str(close.vin))
        backCar_t1_dist = abs(self.distAtT1(res))  # distance new car (car2) travlled by proposed t1
        frontCar_t1_dist = abs(self.car_dist(close, (res.t1)))  # distance in front car (car1) travlled by the time car2 reaches t2



        #TODO:...
        #check begining??

        return frontCar_t1_dist - backCar_t1_dist



















