import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

schalterGedrueckt = False

def warteAufSchalterGedrueckt():
    global schalterGedrueckt
    while not(schalterGedrueckt):
        time.sleep(0.05)

    schalterGedrueckt = False

def schalterGedruecktEvent(pin):
    global schalterGedrueckt
    schalterGedrueckt = True

def starten():
    gpio.setup(14, gpio.IN, pull_up_down=gpio.PUD_DOWN)
    gpio.add_event_detect(14, gpio.RISING,schalterGedruecktEvent,bouncetime=500)