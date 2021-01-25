import RPi.GPIO as gpio #Modul, dass zum Ansteuern der Pins benötigt wird.
import time #Modul, zum zum Warten im Code benötigt wird.

farbPinbelegungen = [["rot",5],["gruen",13],["blau",6]] #Beinhaltet alle Farben, die von der LED angzeigt werden könne mit dem zuständigen Pin, der dazu angesprochen werden muss.

#Richtet alle Pins für das Anteuern der LED an.
def starten():
    for i in range(len(farbPinbelegungen)):
        gpio.setup(farbPinbelegungen[i][1], gpio.OUT, initial=gpio.LOW)

#Schaltet alle Pins auf LOW, sodass die LED keine Farbe anzeigt.
def ausschalten():
    for i in range (len(farbPinbelegungen)):
        gpio.output(farbPinbelegungen[i][1],gpio.LOW)

#Zeigt eine gegebene Farbe aus farbPinbelegungen für die gegeben Sekunden an.
def farbeAnzeigen(farbe, dauer):
    for i in range (len(farbPinbelegungen)):
        if (farbPinbelegungen[i][0] == farbe):
            gpio.output(farbPinbelegungen[i][1], gpio.HIGH)
        else:
            gpio.output(farbPinbelegungen[i][1], gpio.LOW)
        
    time.sleep(dauer)
    ausschalten()