import logging
import signal
import requests
import sys
import time
import json
from aiogram import Bot, Dispatcher, executor, types
API_TOKEN = '5605931750:AAH5I2yMkqiKIXLobMjXPD6KCRLoP09lExQ'
#API_TOKEN = '5164815705:AAHZuIrXz2CA-7dRPVfyBmX4HDK6NjjwPYA'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


signal.signal(signal.SIGINT, signal_handler)
def wait_time(g_time):
    interrupted = False
    for remaining in range(g_time, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)
        if interrupted:
            print("Gotta go")
            break

scorelist = [0]*100
prevdata = " "

@dp.message_handler(commands=['score','scor'])
async def echo(message: types.Message):

        while True:
            count = 0
            response = requests.get('https://hs-consumer-api.espncricinfo.com/v1/pages/matches/live?')
            time.sleep(1)
            data = json.loads(response.text)

            if prevdata != data:
                for liveInning in data['content']['matches']:
                    if liveInning['liveInning'] != None:
                        msg = ""
                        txt = liveInning['slug']
                        x = txt.upper()
                        msg = msg + " " + x + " " + "\n"
                        msg = msg + liveInning['state'] + "\n"
                        msg = msg + liveInning['statusText'] + "\n"
                        flag = False

                        for isLive in liveInning['teams']:

                            if isLive['isLive'] == False:
                                if isLive['score'] == None:
                                    msg = msg + "Bowling..." + "\n"
                                else:
                                    msg = msg + isLive['team']['name'] + " scored: " + isLive['score'] + "\n"
                            if isLive['isLive'] == True:
                                if scorelist[count] == 0:
                                    scorelist.insert(count, isLive['score'])
                                    flag = True
                                elif scorelist[count] != isLive['score']:
                                    flag = True
                                    scorelist[count] = isLive['score']
                                else:
                                    flag = False

                                msg = msg + isLive['team']['name'] + " current score: " + isLive['score'] + "\n"
                                msg = msg + "Score Info: " + isLive['scoreInfo'] + "\n"

                        if flag == True:
                            await message.reply(msg)
                            await bot.send_message('1778193674',msg)

                        count = count + 1

if _name_ == '_main_':
    executor.start_polling(dp,skip_updates=True)