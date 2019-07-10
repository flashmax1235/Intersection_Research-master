class Car:
    #car criteria
    car_max_accel = 3
    car_max_decel = -3
    car_max_speed = 50

    # Intersection Criteria
    inter_side_length = 100
    inter_max_speed = 20
    inter_tolerance_time = 0.12  # intersection_side_length/[(max_Speed + min_speed)/2] (0.12s)  ---only 1 car in an in


    def __init__(self):
        self.enteredTime