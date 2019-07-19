
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