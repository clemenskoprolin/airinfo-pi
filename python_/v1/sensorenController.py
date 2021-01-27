import board #Modul, zur Kennzeichnung von Pins.
import busio #Modul, zur Kommunikation über das IO.
import adafruit_bmp280 #Modul, zum Kommunizieren mit dem BMP280 Sensor.
from threading import Thread #Wird dazu verwendet, Funktionen asyncron aufzurufen.
from ledController import farbeAnzeigen #Wird für die Ansteuerung der LED gebraucht.

benutzeLED = True #Gibt an, ob die LED beim Lesen von Sensorendaten aufbliken soll.

i2c = busio.I2C(board.SCL, board.SDA) #Konfiguration des I2C Ports mit den Daten des Raspberry Pis.
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c) #Verbinden mit dem BMP280 per I2C Port.

#Für die Kalibrierung des Sensors wird der Druck auf der Seehöhe des Ortes in hPA benötigt.
#Da aber Wien nicht die Seehöhe erreicht, wurde der Wert mit https://rechneronline.de/barometer/ berrechnet.
#bmp280.sea_level_pressure = 1013.25 #Auskommentierter vorgeschlagener Wert des Moduls.
bmp280.sea_level_pressure = 1005.8

def leseDaten():
    [temperatur, druck, seehoehe] = leseBMP280()
    return [temperatur, druck, seehoehe, None]

def leseBMP280():
    if benutzeLED:
        #Die Funktion wird asyncron durch Threading aufgerufen, sodass in der Zwischenzeit gemessen werden kann.
        Thread(target=farbeAnzeigen, args=("gruen",0.1)).start()    #Zeigt mit einem grünen Blinken für eine Sekunde an, dass der BMP280 misst.
    temperatur = bmp280.temperature #Gibt die Temperatur in Grad Celcius zurück.
    druck = bmp280.pressure #Gibt den Luftdruck in hPA zurück.
    seehoehe = bmp280.altitude #Gibt die geschätze Seehöhe zurück (wird mithilfe von sea_level_pressure berechnet).

    return [temperatur, druck, seehoehe] #Gibt die ausgelesen Werte zurück.