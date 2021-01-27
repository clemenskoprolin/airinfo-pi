import board #Modul, zur Kennzeichnung von Pins.
import digitalio #Modul, zur Kommunikation über einzelene Pins.
import busio #Modul, zur Kommunikation über das IO.
import adafruit_pcd8544 #Modul, zur Kontrolle des benutzten Displays.
from PIL import Image, ImageDraw, ImageFont #Module, zum Zeichen von Formen und Texten auf dem Display.
import time #Modul, zum Warten im Script.

#Gibt an, welche Information am Display gerade angezeigtr wird.
anzeigeNumber = -1 #0 = Temperatur, 1 = Druck, 2 = Luftfeutigkeit
#Gibt an, ob das Backlight und die LED verwendet werden sollen. Wird von hauplogik gesteuert.
displayModus = 0 #0 = Backlight aus + LED an; 1 = Backlight aus + LED aus; 2 = Backlight an + LED an; 3 = Backlight an + LED aus; 4 = Display aus + LED an; 5 = Display aus + LED aus
leereDisplay = False #Gibt an, ib das Display bei der nächsten Aktualisierung geleert werden soll. Wird verwendet, wenn das Display von der Benutzerin oder den Benutzer ausgeschalten wird.

spi = busio.SPI(board.SCK, MOSI=board.MOSI) #Schnittstelle des SPI (Serial Peripheral Interface)
                                            #Wird für die Steuerung des Displays benötigt.                 
dc = digitalio.DigitalInOut(board.D23)  # data/command Pin. Entspricht Pin GPIO 16 auf Raspberry Pi.
cs = digitalio.DigitalInOut(board.D8)  #chip select Pin. Wird auch chip enabled oder SCE Pin gennant. Entspricht Pin GPIO 8 auf den Raspberry Pi.
reset = digitalio.DigitalInOut(board.D24)  #reset Pin (=RST). Entspricht Pin GPIO 24 auf den Raspberry Pi.
backlight = digitalio.DigitalInOut(board.D9)  #backlight Pin. Kontrolliert durch die Stromregulierung das Backlight. Entspricht Pin GPIO 9 auf den Raspberry Pi.

display = adafruit_pcd8544.PCD8544(spi, dc, cs, reset) #Erstellt mit den voher angegeben Daten die Verbindung zum Display.
backlight.switch_to_output() #Stellt den backlight Pin auf den Ouput-Modus um.

#Gibt eine Bildfäche zurück, auf der sich ein zentrierter Text befindet.
def zentrierterText(text, schriftgroesse, bild, xVersatz = 0, yVersatz = 0, fett = False):
    zeichenflaeche = ImageDraw.Draw(bild) #Erstellt auf der Bildfläche eine Zeichenfläche.
    
    #Bestimmung der richtigen Schriftarte nach dem 'fett' Argument
    schriftart = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if fett == True:
        schriftart = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    
    schrift = ImageFont.truetype(schriftart, schriftgroesse) #Schrift, die für das schreiben des Textes verwendet wird.

    (schriftBreite, schriftHoehe) = schrift.getsize(text) #Bereichnet Breite und Höhe des Textes.
    zeichenflaeche.text(
        (display.width // 2 - schriftBreite // 2 + xVersatz, display.height // 2 - schriftHoehe // 2 + yVersatz), #Zentriert den Text und gibt den Versatz dazu.
        text,
        font=schrift,
        fill=255,
    )

    return bild

def startAnimation(versionNummer):
    display.fill(0) #Leert das Display.
    backlight.value = True #Schaltet das Backlight ein.
    
    bild = Image.new("1", (display.width, display.height)) #Erstellt eine neue Bildfläche.
    bild = zentrierterText("Clemens Koprolin",8, bild, 0, -20) #Schreibt meinen Namen oben auf den oberen Rand des Bildschirms.
    bild = zentrierterText("Luftinfos",17,bild,0,-4) #Schreibt den Namen der Anwendung versetzt in die Mitte.
    bild = zentrierterText("Version " + versionNummer, 9, bild, 0, 15) #Schreibt in der unteren Gegend die aktuelle Versionsnummer.
    
    zeichenflaeche = ImageDraw.Draw(bild) #Erstellt auf der Bildfläche eine Zeichenfläche.
    zeichenflaeche.rectangle((7, 30, display.width - 7, 31), outline=255, fill=255) #Erstellt auf der Zeichenfläche ein Rechteck, das den Titel unterstreicht.
    
    display.image(bild) #Zeigt die Bildfläche an.
    display.show() #Aktualisiert den Bildschrim.
    
def temperaturAnzeige(temperatur):
    display.fill(0) #Leert das Display.
    
    bild = Image.new("1", (display.width, display.height)) #Erstellt eine neue Bildfläche.
    bild = zentrierterText("Temperatur", 9, bild, 0, -20) #Zeit "Temperatur"am oberen Rand des Displays an.
    bild = zentrierterText(str(temperatur) + u'\N{DEGREE SIGN}', 32, bild,0, -2) #Zeigt die gegebe Temperatur
    
    #Bestimmung des infoTextes je nach Temperatur
    #Daten von https://www.inventer.de/wissen/luftqualitaet-gesundheit/luftfeuchtigkeit-in-wohnraeumen/
    infoText = "Normal"
    if temperatur < 17:
        infoText = "Kühl"
    if temperatur >= 17 and temperatur < 19:
        infoText = "Etwas kühl"
    if temperatur >= 22 and temperatur < 23:
        infoText = "Etwas warm"
    if temperatur >= 23:
        infoText = "Warm"
        
    bild = zentrierterText(infoText, 9, bild, 0, 18) #Zeigt den Infotext am unteren Rand des Displays an.
    
    display.image(bild) #Zeigt die Bildfläche an.
    display.show() #Aktualisiert den Bildschrim.
    
def druckAnzeige(druck, seehoehe):
    display.fill(0) #Leert das Display.
    
    bild = Image.new("1", (display.width, display.height)) #Erstellt eine neue Bildfläche.
    bild = zentrierterText("Luftdruck", 9, bild, 0, -20) #Zeig "Druck" am oberen Rand des Displays an.
    bild = zentrierterText(str(druck) + " hPa", 13, bild,0, -2, True) #Zeigen den gegebenen Druck.
        
    bild = zentrierterText(u'\N{ALMOST EQUAL TO}' + str(seehoehe) + " m Seehöhe", 8, bild, 0, 18) #Zeigt die gesätzte Seehöhe am unteren Rand des Displays an.
    
    display.image(bild) #Zeigt die Bildfläche an.
    display.show() #Aktualisiert den Bildschrim.
    return

def feuchtigkeitAnzeige(feutigkeit):
    display.fill(0) #Leert das Display.
    
    bild = Image.new("1", (display.width, display.height)) #Erstellt eine neue Bildfläche.
    bild = zentrierterText("Luftfeutigkeit", 9, bild, 0, -20) #Zeit "Luftfeutigkeit" am oberen Rand des Displays an.
    bild = zentrierterText(str(feutigkeit) + "%", 26, bild,0, -2) #Zeigt die gegebe Luftfeutigkeit
    
    #Bestimmung des infoTextes je nach Luftfeutigkeit
    #Daten von https://www.inventer.de/wissen/luftqualitaet-gesundheit/luftfeuchtigkeit-in-wohnraeumen/
    infoText = "Normal"
    if feutigkeit < 40:
        infoText = "Trocken"
    if feutigkeit >= 40 and feutigkeit < 45:
        infoText = "Etwas trocken"
    if feutigkeit >= 60 and feutigkeit < 65:
        infoText = "Etwas feucht"
    if feutigkeit >= 65:
        infoText = "Feucht"
        
    bild = zentrierterText(infoText, 9, bild, 0, 18) #Zeigt den Infotext am unteren Rand des Displays an.
    
    display.image(bild) #Zeigt die Bildfläche an.
    display.show() #Aktualisiert den Bildschrim.

def datenAnzeige(temperatur, druck, seehoehe, feuchtigkeit):
    global anzeigeNumber, leereDisplay
    anzeigeNumber += 1 #Erhöht anzeigeNumber um 1

    #Zeigt für die jeweilige anzeigeNumber den entsprechend Wert auf dem Display an, wenn dies nicht ausgeschalten ist oder die Werte nicht vorhanden sind.
    if anzeigeNumber == 0 and temperatur != None:
        if displayModus != 4 and displayModus != 5: #Wenn der displayModus 4 oder 5 ist, ist das Display ausgeschalten.
            temperaturAnzeige(temperatur)

    elif anzeigeNumber == 1 and druck != None and seehoehe != None:
        if displayModus != 4 and displayModus != 5: #Wenn der displayModus 4 oder 5 ist, ist das Display ausgeschalten.
            druckAnzeige(druck,seehoehe)

    elif anzeigeNumber == 2 and feuchtigkeit != None:
        if displayModus != 4 and displayModus != 5: #Wenn der displayModus 4 oder 5 ist, ist das Display ausgeschalten.
            feuchtigkeitAnzeige(feuchtigkeit)
    else:
        anzeigeNumber = -1 #Setzt anzeigeNumber zurück.
        if displayModus == 0 or displayModus == 1 or displayModus == 4 or displayModus == 5: #Schaltet das Backlight aus, falls sich das Display im entsprechenden Modus befindet.
            backlight.value = False

        #Wenn leereDisplay true ist, werden alle Pixel auf den Display und leereDisplay wieder zu ihren Standartwert zurückgesetzt.
        if leereDisplay == True:
            display.fill(0)
            display.show()
            leereDisplay = False
        
        datenAnzeige(temperatur, druck, seehoehe, feuchtigkeit) #Ruft diese Funktion mit neuen Einstellungen wieder auf.

def displayModusAendern(neuerDisplayModus):
    global displayModus, leereDisplay
    displayModus = neuerDisplayModus

    backlight.value = True #Schaltet das Backlight ein.

    #Setzt backlightText und ledText zu ihren entsprechenden Werten nach dem displayModus.
    backlightText = ""
    ledText = ""
    if displayModus == 0:
        backlightText = "Backlight aus"
        ledText = "und LED an"
    if displayModus == 1:
        backlightText = "Backlight und"
        ledText = "und LED aus"
    if displayModus == 2:
        backlightText = "Backlight und"
        ledText = "LED an"
    if displayModus == 3:
        backlightText = "Backlight an"
        ledText = "und LED aus"
    if displayModus == 4:
        backlightText = "Display aus"
        ledText = "und LED an"
        leereDisplay = True
    if displayModus == 5:
        backlightText = "Display aus"
        ledText = "und LED aus"
        leereDisplay = True

    display.fill(0) #Leert das Display.
    
    bild = Image.new("1", (display.width, display.height)) #Erstellt eine neue Bildfläche.
    bild = zentrierterText(backlightText, 11, bild,0,-6) #Plaziert backlightText auf der Bildfläche.
    bild = zentrierterText(ledText, 11, bild,0,6) #Plaziert ledText auf der Bildfläche.

    display.image(bild) #Zeigt die Bildfläche an.
    display.show() #Aktualisiert den Bildschrim.