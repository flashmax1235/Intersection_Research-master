
                # if turn
                if (abs(delta) > self.p1_distance):
                    self.posY = self.p1_distance
                    self.posX = delta + self.inter_size




#vert
            if (val < self.enterTime0) or (self.lane % 2 == 1): # car not started yet
                delta = 0.0
                countX = countX + 1
            else:  #TODO: you are going to put turning shit in here
                delta = self.trajectory01(realTime[inx - countX], 0)
                if self.lane == 2:
                    delta = delta * -1



            self.posX = self.posX_OG + delta

            #hor
            if (val < self.enterTime0) or (self.lane % 2 == 0):
                delta = 0.0
                countY = countY + 1
            else:
                delta = self.trajectory01(realTime[inx - countY], 0)
                if self.lane == 3:
                    delta = delta * -1

            self.posY = self.posY_OG + delta


            path = np.append(path, self.posX)
            path = np.append(path, self.posY)










            """
                ####
                newNode.expectedTime = possibleTime
                # calculate accel value needed for P1, update accel and requested accel
                newNode.accel = self.quads[P1].getAccelValue(newNode, possibleTime, -1 * self.p1_distance)
                newNode.requestedAccel = newNode.accel
                newNode.expectedTime2 = IC.expect(self.p2_distance, newNode.speed, newNode.accel) + newNode.enterTime
                ###

                print possibleTime
                while not GoodSpot:
                    result = self.quads[P1].simple_check_time(newNode)
                    if not result[0]:  # not avalible, something in the way, going tolook after that thing
                            possibleTime = possibleTime + self.inter_tolerance_time
                            #possibleTime = result[1].expectedTime + self.inter_tolerance_time / 2
                    else:
                        GoodSpot = result[0]
                    ##
                    newNode.expectedTime = possibleTime
                    # calculate accel value needed for P1, update accel and requested accel
                    newNode.accel = self.quads[P1].getAccelValue(newNode, possibleTime, -1 * self.p1_distance)
                    newNode.requestedAccel = newNode.accel
                    newNode.expectedTime2 = IC.expect(self.p2_distance, newNode.speed,
                                                      newNode.accel) + newNode.enterTime
                    ##

                #TODO maybe a duplicate

                # update expected time
                newNode.expectedTime = possibleTime
                # calculate accel value needed for P1, update accel and requested accel
                newNode.accel = self.quads[P1].getAccelValue(newNode, possibleTime, -1 * self.p1_distance)
                newNode.requestedAccel = newNode.accel
                newNode.expectedTime2 = IC.expect(self.p2_distance, newNode.speed, newNode.accel) + newNode.enterTime
                """