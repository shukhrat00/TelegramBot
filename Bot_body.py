import requests
import json
import datetime

from Data_generator import scheduleChunk

class telegramBot():
    def __init__(self):
        with open("Bot_constants.txt", 'r') as file:
            data = json.load(file)
            Token = data['bot_constants']["token"]
            Offset = data['bot_constants']["offset"]
            Commands = [i[0] for i in data['bot_commands']]
            Descriptions = data['bot_commands']
            Greets = data["greet_patterns"]
        self.token = Token
        self.url = "https://api.telegram.org/bot" + self.token + '/'
        self.offset = Offset
        self.commands = set(Commands)
        self.descriptions = Descriptions
        self.chunk = scheduleChunk()
        self.greet_patterns = Greets
        self.client_states = {}
        
    def write_offset(self, offset):
        data = json.load(open("Bot_constants.txt", 'r'))
        with open("Bot_constants.txt", 'w') as file:
            data['bot_constants']["offset"] = offset
            json.dump(data, file)    

    def get_updates_json(self, timeout = 1):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset' : self.offset}
        response = requests.get(self.url + method, params).json()
        try:
            self.offset = response['result'][-1]['update_id'] + 1
            self.write_offset(self.offset)
        except:
            print("No new messages")
        return response       
    
    def send_mess(self, chat, text):  
        method = 'sendMessage'
        params = {'chat_id': chat, 'text': text}
        response = requests.post(self.url + method, data=params)
        return response
    
    def reply_command(self, mess):
        req = mess["message"]["text"]
        if req == "/help":
            text = "My commands are: \n" + "".join([i[0] + " - " + i[1] + '\n' for i in self.descriptions])
        elif req == "/airports":
            text = "Avaliable airports: " + ", ".join([i[0] for i in self.chunk.data["Airports"]])
        elif req == "/find":
            text = "Okay!\nFirst of all, do you want to find arrival or departure?"
            self.client_states[mess['message']['chat']['id']][0] = 1
        self.send_mess(mess['message']['chat']['id'], text)
    
    def reply_error(self, mess):
        text = "There is no such command in my command list. Check it out by typing /help"
        self.send_mess(mess['message']['chat']['id'], text)
        
    def reply_purge(self):
        text = "My commands are: \n" + "".join([i[0] + " - " + i[1] + '\n' for i in self.descriptions])
    
    def reply_greet(self, mess):
        text = "Hello there!\nStart operating by typing /help"
        self.send_mess(mess['message']['chat']['id'], text)  
    
    def reply_in_process_1(self, mess, error):
        if error:
            text = "Try again or type /purge to abort process"
        else:
            text = "Good\nNow choose your airport"
            self.client_states[mess['message']['chat']['id']][0] = 2
        self.send_mess(mess['message']['chat']['id'], text)   
        
    def reply_in_process_2(self, mess, error):
        if error:
            text = "Try again or type /purge to abort process"
        else:
            self.client_states[mess['message']['chat']['id']] = [3, 0, mess["message"]["text"]]
            text = "Finally, pick your date. It should be written in YYYY.MM.DD format"
        self.send_mess(mess['message']['chat']['id'], text)
        
    def reply_in_process_3(self, mess, date, error):
        if error:
            text = "Try again or type /purge to abort process"
        else:
            text = "Here is your flight list on " + date.strftime("%Y.%m.%d")
            if not self.chunk.check_date(date):
                self.chunk.fill_date(date)            
            for gate in self.chunk.schedules[date][self.client_states[mess['message']['chat']['id']][2]][self.client_states[mess['message']['chat']['id']][1]]:
                text = text +  "\nFor sector " + gate
                for flight in self.chunk.schedules[date][self.client_states[mess['message']['chat']['id']][2]][self.client_states[mess['message']['chat']['id']][1]][gate]:
                    country = self.chunk.schedules[date][self.client_states[mess['message']['chat']['id']][2]][self.client_states[mess['message']['chat']['id']][1]][gate][flight][0]
                    print(flight, country)
                    text = text + "\nAt " + self.minutes_to_solid(flight) + " there is a flight " + ["from", "to"][self.client_states[mess['message']['chat']['id']][1]] + " " + country
            print(text)
        self.send_mess(mess['message']['chat']['id'], text)    
        self.client_states[mess['message']['chat']['id']] = [0, 0, ""]
    
    def minutes_to_solid(self, minut):
        hours = minut // 60
        minuts = minut % 60
        minuts = '0' * (2 - len(str(minuts))) + str(minuts)
        return str(hours) + ":" + str(minuts)
    
    def update(self):
        messages = [i for i in self.get_updates_json()['result']]
        for mess in messages:
            mess["message"]["text"] = mess["message"]["text"].lower()
            
            if not self.client_states.get(mess['message']['chat']['id']):
                self.client_states[mess['message']['chat']['id']] = [0, 0, ""]
            
            elif mess["message"]["text"] == "/purge":
                self.client_states[mess['message']['chat']['id']] = [0, 0, ""]
                self.reply_purge()
            
            elif self.client_states[mess['message']['chat']['id']][0] == 0:
                if mess["message"]["text"] in self.greet_patterns:
                    self.reply_greet(mess)
                elif mess["message"]["text"] in self.commands:
                    self.reply_command(mess)
                else:
                    self.reply_error(mess)
            elif self.client_states[mess['message']['chat']['id']][0] == 1:
                error = False
                if mess["message"]["text"] == "arrival":
                    self.client_states[mess['message']['chat']['id']][1] = 0
                elif mess["message"]["text"] == "departure":
                    self.client_states[mess['message']['chat']['id']][1] = 1   
                else:
                    error = True
                self.reply_in_process_1(mess, error)
                
            elif self.client_states[mess['message']['chat']['id']][0] == 2:
                error = False
                if not mess["message"]["text"] in self.chunk.airports:
                    error = True
                self.reply_in_process_2(mess, error)
                
            elif self.client_states[mess['message']['chat']['id']][0] == 3:
                error = False
                try:
                    date = mess["message"]["text"].split('.')
                    date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
                except:
                    error = True
                self.reply_in_process_3(mess, date, error)