import json
import random
import datetime

class sheduleChunk():
    def __init__(self):
        with open("Data_generator_constants.txt", 'r') as file:
            data = json.load(file)
        dates = ()

        def generate_schedule(self):
            schedules = {}
            for airport in data["Airports"]:
                schedules[airport[0]] = {}
                for terminal in airport[1]:
                    schedules[airport[0]][terminal] = {}
                    minutes = 0
                    while minutes < 24 * 60:
                        minutes += random.randint(0, 100)
                        airline = airport[2][random.randint(0, len(airport[2]) - 1)]
                        schedules[airport[0]][terminal][minutes] = (data['Flight_samples'][airport[0]][airline][random.randint(0, len(data['Flight_samples'][airport[0]][airline]) - 1)], airline)
                    