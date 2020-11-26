#coder :- Salman Faris

import sys
import time
import telepot
import RPi.GPIO as GPIO

"""
#LED
def on(pin):
        GPIO.output(pin,GPIO.HIGH)
        return
def off(pin):
        GPIO.output(pin,GPIO.LOW)
        return
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO output channel
GPIO.setup(11, GPIO.OUT)

"""
#This is a test

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command : %s' % command)

    if command == 'hi':
       bot.sendMessage(chat_id, 'Hi there, Welcome to TrackEm!')
       print("User : Msg ok!")
    elif command =='off':
       bot.sendMessage(chat_id, off(11))


#MAIN PROGRAM

bot = telepot.Bot('1465290614:AAHoRrpYRmkff6aWaUNzPvpDf0611oHYmF4')
bot.getMe()
bot.message_loop(handle)

print('I am listening...')

while 1:
    try:
        time.sleep(10)
    
    except KeyboardInterrupt:
        print('\n Program interrupted')
        GPIO.cleanup()
        exit()
    
    except:
        print('Other error or exception occured!')
        GPIO.cleanup()
