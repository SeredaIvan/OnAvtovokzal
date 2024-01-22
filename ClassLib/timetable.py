import datetime

class Timetable:
    def __init__(self):
        self.id_journey = 0
        self.id_bus = 0
        self.id_city_start = 0
        self.id_city_finish = 0
        self.time_ticket = datetime.datetime.now()
        self.cost = 0