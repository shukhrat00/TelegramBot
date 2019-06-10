import requests
import json

class telegrambot():
    def __init__(self):
        with open("Bot_constants.txt", 'r') as file:
            data = json.load(file)
            Token = data['bot_constants']["token"]
            Offset = data['bot_constants']["offset"]
            Commands = [i[0] for i in data['bot_commands']]
            Descriptions = data['bot_commands']
        self.token = Token
        self.url = "https://api.telegram.org/bot" + self.token + '/'
        self.offset = Offset
        self.commands = set(Commands)
        self.descriptions = Descriptions 
        
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
    
    def reply(self, mess):
        if mess["message"]["text"] == "/help":
            text =  "My commands are: \n" + "".join([i[0] + " - " + i[1] + '\n' for i in self.descriptions])
        self.send_mess(mess['message']['chat']['id'], text)
    
    def update(self):
        messages = [i for i in self.get_updates_json()['result']]
        for mess in messages:
            if mess["message"]["text"] in self.commands:
                print(mess)
                self.reply(mess)