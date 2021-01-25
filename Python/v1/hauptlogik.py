# -*- coding: utf-8 -*-
import displayController, sensorenController, ledController, schalterController, speicherung
import time, math
from apscheduler.schedulers.blocking import BlockingScheduler
from threading import Thread

versionNummer = "1.0"
displayModus = 0 #0 = Backlight aus + LED an; 1 = Backlight aus + LED aus; 2 = Backlight an + LED an; 3 = Backlight an + LED aus; 4 = Display aus + LED an; 5 = Display aus + LED aus

def start():
    ledController.starten()
    schalterController.starten()
    displayController.startAnimation(versionNummer)
    speicherung.mitMySQLVerbinden()

def aktualisieren():
   [temperatur, druck, seehoehe, feuchtigkeit] = sensorenController.leseDaten()
   displayController.datenAnzeige(round(temperatur,1), round(druck,1), round(seehoehe,1), feuchtigkeit)

   speicherung.datenBereinigen()
   speicherung.datenSpeichern(round(temperatur,3), round(druck,3), feuchtigkeit)

def schalterUeberpruefung():
    while(True):
        schalterController.warteAufSchalterGedrueckt()
        displayModusAendern()
        time.sleep(0.5)

def displayModusAendern():
    global displayModus

    if displayModus < 5:
        displayModus += 1
    else:
        displayModus = 0

    displayController.displayModusAendern(displayModus)

    if displayModus == 1 or displayModus == 3 or displayModus == 5:
        sensorenController.benutzeLED = False
        speicherung.benutzeLED = False
    else:
        sensorenController.benutzeLED = True
        speicherung.benutzeLED = True

Thread(target=schalterUeberpruefung).start() #Ruft asyncron schalterUeberpruefung auf.

#Konfiguriert das Script so, dass aktualisieren jeden vollen 10 Sekunden einer Minute aufgerufen wird.
start()
scheduler = BlockingScheduler()
scheduler.add_job(aktualisieren, trigger='cron', second='0,10,20,30,40,50')
scheduler.start()