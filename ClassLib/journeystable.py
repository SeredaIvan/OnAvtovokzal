class JourneysTable:
    def __init__(self):
        self.id_journey=None
        self.bus_name = None
        self.start_city = None
        self.finish_city = None
        self.time_start = None
        self.time_finish = None
        self.cost = None

    def getJourneyId(self):
        return self.id_journey