import mysql.connector #Modul, dass es ermöglicht mit MySQL-Servern zu kommunizieren.
import time #Modul, zum warten im Programmcode und abrufen der aktuellen Systemzeit.
from threading import Thread #Wird dazu verwendet, Funktionen asyncron aufzurufen.
from ledController import farbeAnzeigen #Wird für die Ansteuerung der LED gebraucht.

benutzeLED = True #Gibt an, ob die LED beim Speicherb von Daten aufbliken soll.

mydb = None #Beinhaltet die Verbindung zum lokalen MySQL-Server.

#Stellt eine Verbindung zu den lokalen MySQL-Server her.
def mitMySQLVerbinden():
    global mydb

    mydb = mysql.connector.connect(
        host="localhost",
        user="airinfo",
        password="123456", #Hier natürlich wieder ein sehr sicheres Passwort.
        database="airinfo"
    )

#Speichert die von den Sonsoren empfangenen Daten auf den MySQL-Server in den richtigen Tabellen ab.
def datenSpeichern(temperatur, luftdruck, feuchtigkeit):
    #Speicherung der Daten in "woche".
    zeiger = mydb.cursor()
    sql = "INSERT INTO woche (temperatur, luftdruck) VALUES (%s, %s)"
    daten = (temperatur, luftdruck)
    zeiger.execute(sql, daten)
    mydb.commit()

    if benutzeLED:
        #Die Funktion wird asyncron durch Threading aufgerufen, sodass in der Zwischenzeit gemessen werden kann.
        Thread(target=farbeAnzeigen, args=("blau",0.1)).start()    #Zeigt mit einen blauen LED für eine Sekunde an, dass der gerade Daten abgespeichert werden.

    akuelleZeit = time.localtime()
    if time.strftime("%M", akuelleZeit) == "00" and time.strftime("%S", akuelleZeit) == "00": #Überprüft, ob es gerade eine volle Stunde ists
        #Falls ja, werden die Sensordaten auch in "insgesamt" gespeichert.
        zeiger = mydb.cursor()
        sql = "INSERT INTO gesamt (temperatur, luftdruck) VALUES (%s, %s)"
        daten = (temperatur, luftdruck)
        zeiger.execute(sql, daten)
        mydb.commit()

        if benutzeLED:
            #Die Funktion wird asyncron durch Threading aufgerufen, sodass in der Zwischenzeit gemessen werden kann.
            Thread(target=farbeAnzeigen, args=("blau",0.1)).start()    #Zeigt mit einen blauen LED für eine Sekunde an, dass der gerade Daten abgespeichert werden.

#Enfernt Daten, die älter sind als 7 Tage aus "woche"
def datenBereinigen():
    zeiger = mydb.cursor()
    sql = "DELETE FROM woche WHERE `zeitpunkt` < DATE_ADD(CURDATE(), INTERVAL -7 DAY)"

    zeiger.execute(sql)
    mydb.commit()