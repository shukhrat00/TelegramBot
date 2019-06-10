import requests
import time
import json
import datetime
from Bot_body import telegramBot
        
bot = telegramBot()
bot.chunk.fill_date(datetime.datetime.today())

while 1:
    bot.update()
    time.sleep(1)