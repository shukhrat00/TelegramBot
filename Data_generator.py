import json
import random
import datetime

class scheduleChunk():
    def __init__(self):
        with open("Data_generator_constants.txt", 'r') as file:
            self.data = json.load(file)
        self.schedules = {}
        self.filledDates = set()

    def generate_schedule(self):
        schedule = {}
        for airport in self.data["Airports"]:
            schedule[airport[0]] = {}
            for terminal in airport[1]:
                schedule[airport[0]][terminal] = {}
                minutes = 0
                while minutes < 24 * 60:
                    minutes += random.randint(0, 100)
                    airline = airport[2][random.randint(0, len(airport[2]) - 1)]
                    schedule[airport[0]][terminal][minutes] = (self.data['Flight_samples'][airport[0]][airline][random.randint(0, len(self.data['Flight_samples'][airport[0]][airline]) - 1)], airline)
        return schedule
    
    def check_date(self, date):
        if date in self.filledDates:
            return True
        else:
            return False
            
    def fill_date(self, date):
        self.filledDates.add(date)
        self.schedules[date] = self.generate_schedule()