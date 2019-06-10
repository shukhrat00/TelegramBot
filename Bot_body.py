import requests
import json

class telegrambot():
    def __init__(self):
        with open("Bot_constants.txt", 'r') as file:
            data = json.load(file)
            Token = data['bot_constants']["token"]
            Offset = data['bot_constants']["offset"]        
        self.token = Token
        self.url = "https://api.telegram.org/bot" + self.token + '/'
        self.offset = Offset
        
    def write_offset(self, offset):
        data = json.load(open("Bot_constants.txt", 'r'))
        with open("Bot_constants.txt", 'w') as file:
            data['bot_constants']["offset"] = offset
            json.dump(data, file)    

    def get_updates_json(self, timeout = 5):
        try:
            method = 'getUpdates'
            params = {'timeout': timeout, 'offset' : self.offset}
            response = requests.get(self.url + method, params).json()
            self.offset = response['result'][-1]['update_id'] + 1
            self.write_offset(self.offset)
            return response
        except:
            print("No new messages")
    
    def send_mess(self, chat, text):  
        params = {'chat_id': chat, 'text': text}
        response = requests.post(url + 'sendMessage', data=params)
        return response    
