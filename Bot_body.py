import requests

TOKEN = '819658977:AAHQ5okDtGRi1Ks8Q3GMf-XUwMVVslsX--Y'
url = "https://api.telegram.org/bot" + TOKEN + '/'

class telegrambot():
    def __init__(self):
        self.token = TOKEN
        self.url = url

    def get_updates_json(self):  
        response = requests.get(url + 'getUpdates')
        return response.json()

    def last_update(self, data):  
        results = data['result']
        total_updates = len(results) - 1
        return results[total_updates]
    
    def send_mess(self, chat, text):  
        params = {'chat_id': chat, 'text': text}
        response = requests.post(url + 'sendMessage', data=params)
        return response    
    
    def greet(self, chat):
        self.send_mess(chat, "Hello")

