class Reservation:

    def toString(self):
        return ("[ Vin: " + str(self.vin) + " ,speed: " + str(self.speed) + " ,accel: " + str(
            self.accel) + " ,Entered time: " + str(self.enterTime) + " ,Lane #: " + str(
            self.lane) + " ,Expected time #: " + str(self.expectedTime) + " ,requested accel #: " + str(
            self.requestedAccel) + "]")

    def __init__(self, VIN, speed, accel, enterTime, lane):
        self.vin = VIN
        self.speed = speed
        self.accel = accel
        self.enter = 0  # 0 if entering -- 1 if exiting
        self.enterTime = enterTime
        self.expectedTime = time.time() + expect(-100, self.speed, self.accel)
        self.nextt = None
        self.prev = None
        self.lane = lane
        self.proposedTime = 0
        self.requestedAccel = 0
        self.set = 0
