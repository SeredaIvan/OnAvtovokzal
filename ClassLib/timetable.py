import datetime

class Timetable:
    def __init__(self):
        self.id_journey = None
        self.bus_id = None
        self.city_start_id = None
        self.city_finish_id = None
        self.cost = None
        self.time_start = None
        self.time_finish = None
        self.seats_occupied=None
        self.is_active=None


    def getBusId(self):
       return self.id_journey