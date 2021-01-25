var xAchseKonfiguration = [{
    type: "time",
    time: {
        parser: "YYYY-MM-DD HH:mm",
        tooltipFormat: "ll HH:mm",

        displayFormats: {
            "millisecond": "DD:mm:ss",
            "second": "  DD:mm:ss  ",
            "minute": "   HH:mm  ",
            "hour": "  DD. HH:00   ",
            "day": "  DD.MM  ",
            "week": "   DD.MM.YYYY  ",
            "month": "  DD.MM.YYYY  ",
            "quarter": "  MM.YYYY  ",
            "year": "  YYYY  ",
        }
    },
    scaleLabel: {
        display: true
    },
    ticks: {
        maxRotation: 0
    }
}]

var pluignKonfiguration = {
    zoom: {
        zoom: {
            enabled: true,
            drag: false,
            mode: "x",
            speed: 0.05
        }
    }
}

var aktuellerHintergrund = null;

function aktualisieren() {
    liveDatenBekommen();
    statusDatenBekommen();

    if (new Date().getMinutes == 0 && new Date().getSeconds < 10)
    {
        insgesamtDatenBekommen();
    }
}

async function liveDatenBekommen() {
    var response = await fetch("api/live.php")
    if (response.ok) {
        var daten = JSON.parse(await response.text());

        liveDatenAktualisieren(daten);
        wochenDiagrammeAktualisieren(daten);

        aufnahmeZeitpunkt = new Date(daten.zeitpunkt);
        naechsterAufnahmeZeitpunkt = aufnahmeZeitpunkt.setSeconds(aufnahmeZeitpunkt.getSeconds() + 10);
        differnezZeit = Math.abs(naechsterAufnahmeZeitpunkt - new Date());

        if (differnezZeit < 14000) {
            statusAktualisieren("Live");
            setTimeout(aktualisieren, differnezZeit);
        }
        else {
            statusAktualisieren("Letzte Aktualisierung: " + aufnahmeZeitpunkt.getHours() + ":" + aufnahmeZeitpunkt.getMinutes());
            setTimeout(aktualisieren, 10000);
        }
    }
}

function liveDatenAktualisieren(daten) {
    zeit = new Date();
    kommentar = "Gute Nacht!"
    if (zeit.getHours() >= 5 && zeit.getHours() < 10)  {
        kommentar = "Guten Morgen!"
    }
    if ((zeit.getHours() >= 10 && zeit.getHours() < 12) || (zeit.getHours() >= 14 && zeit.getHours() < 18))  {
        kommentar = "Guten Tag!"
    }
    if(zeit.getHours() >= 12 && zeit.getHours() < 14) {
        kommentar = "Guten Appetit!"
    }
    if (zeit.getHours() >= 18 && zeit.getHours() < 22)  {
        kommentar = "Guten Abend!"
    }

    var minuten = zeit.getMinutes().toString();
    if (minuten.length == 1)
    {
        minuten = "0" + minuten;
    }
    zeitString = zeit.getHours() + ":" + minuten + " - " + kommentar;
    document.getElementById("uhrzeit").innerHTML = zeitString;

    window.liveTemperatur = daten.temperatur;
    /*temperatur = +(Math.round(window.liveTemperatur + "e+2")  + "e-2");*/
    temperatur = window.liveTemperatur;
    temperaturString = temperatur.toString().replaceAll(".",",") + " °C";
    document.getElementById("hauptTemperatur").innerHTML = temperaturString;

    temperaturStatusText = "Normal"
    if (temperatur < 17) {
        temperaturStatusText = "Kühl"
    }
    if (temperatur > 17 && temperatur < 19) {
        temperaturStatusText = "Etwas kühler"
    }
    if (temperatur > 22 && temperatur < 23) {
        temperaturStatusText = "Etwas wärmer"
    }
    if (temperatur > 23) {
        temperaturStatusText = "Warm"
    }
    document.getElementById("temperaturStatusText").innerHTML = temperaturStatusText;

    hintergrundBildAnpassen();

    window.liveLuftdruck = daten.druck;
    luftdruck = window.liveLuftdruck.toString().replaceAll(".",",") + " hPa";
    document.getElementById("hauptLuftdruck").innerHTML = luftdruck;
}

function hintergrundBildAnpassen() {
    temperatur = window.liveTemperatur;
    hintergrundBild = document.getElementById("hintergrundBild");

    if (aktuellerHintergrund != null) {
        hintergrundBild.classList.remove("bild" + aktuellerHintergrund);
        aktuellerHintergrund = null;
    }

    if (temperatur < 17) {
        hintergrundBild.classList.add("bild1")
        aktuellerHintergrund = 1;
    }
    if (temperatur >= 17 && temperatur < 19) {
        hintergrundBild.classList.add("bild2")
        aktuellerHintergrund = 2;
    }
    if (temperatur >= 19 && temperatur < 22) {
        hintergrundBild.classList.add("bild3")
        aktuellerHintergrund = 3;
    }
    if (temperatur >= 22 && temperatur < 23) {
        hintergrundBild.classList.add("bild4")
        aktuellerHintergrund = 4;
    }
    if (temperatur >= 23) {
        hintergrundBild.classList.add("bild5")
        aktuellerHintergrund = 5;
    }
}

function statusAktualisieren(text) {
    var statusText = document.getElementById("statusText");
    var statusPunkt = document.getElementById("statusPunkt");

    var farbe = "black";
    if (text == "Live") {
        farbe = "green";
    }

    if (text.includes("Fehler")) {
        farbe = "red";
    }
    statusText.style.color = farbe;
    statusPunkt.style.backgroundColor = farbe;
    statusText.innerHTML = text;

    var neuerStatusPunkt = statusPunkt.cloneNode(true);
    statusPunkt.parentNode.replaceChild(neuerStatusPunkt, statusPunkt);
}

async function wochenDatenBekommen() {
    var response = await fetch("api/woche.php")
    if (response.ok) {
        var daten = JSON.parse(await response.text());
        daten = datenReduzieren(daten, 1000);

        window.wochenTemperaturDiagramm = temperaturDiagrammAnzeigen(daten ,document.getElementById("wochenTemperaturDiagramm").getContext("2d"), "rgba(240, 0, 0, 1)");
        window.wochenLuftdruckDiagramm = luftdruckDiagrammAnzeigen(daten, document.getElementById("wochenLuftdruckDiagramm").getContext("2d"), "rgba(0, 200, 0, 1)");
    }
}

async function insgesamtDatenBekommen() {
    var response = await fetch("api/insgesamt.php")
    if (response.ok) {
        var daten = JSON.parse(await response.text());
        window.insgesamtTemperaturDiagramm = temperaturDiagrammAnzeigen(daten, document.getElementById("insgesamtTemperaturDiagramm").getContext("2d"), "rgba(0, 148, 255, 1)");
        window.insgesamtLuftdruckDiagramm = luftdruckDiagrammAnzeigen(daten, document.getElementById("insgesamtLuftdruckDiagramm").getContext("2d"), "rgba(222, 222, 0, 1)");

        window.insgesamtTemperaturDiagramm.update();
    }
}

function datenReduzieren(daten, max) {
    console.log(daten.length);
    while (daten.length > max)
    {
        var i = daten.length;
        while (i--) {
            if ((i + 1) % 3 === 0)
            {
                daten.splice(i, 1);
            }
        }
    }

    return daten;
}

function temperaturDiagrammAnzeigen(daten, canvas, farbe)
{
    var namen = [];
    var punkte = [];

    for (var i in daten) {
        namen.push(daten[i].zeitpunkt);
        punkte.push({
            x: new Date(daten[i].zeitpunkt),
            y: parseFloat(daten[i].temperatur)
        });
    }

    var konfiguration = {
        type: "line",
        data: {
            labels: namen,
            datasets: [{
                label: "Temperatur",
                cubicInterpolationMode: "monotone",
                lineTension: 1.5,
                data: punkte,

                borderWidth: 2,
                backgroundColor: "rgba(0, 0, 0, 0.0)",
                borderColor: farbe,

                pointRadius: 0.2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: false,
            },
            legend: {
                display: false
            },
            scales: {
                xAxes: xAchseKonfiguration,
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: "Temperatur in ℃"
                    },

                    /*ticks: {
                        suggestedMin: 16,
                        suggestedMax: 25
                    }*/
                }]
            },
            plugins: pluignKonfiguration
        }
    };

    var chart = new window.Chart(canvas, konfiguration);  
    chart.update();
    return chart;
}

function luftdruckDiagrammAnzeigen(daten, canvas, farbe)
{
    var namen = [];
    var punkte = [];

    for (var i in daten) {
        namen.push(daten[i].zeitpunkt);
        punkte.push({
            x: new Date(daten[i].zeitpunkt),
            y: parseFloat(daten[i].druck)
        });
    }

    var konfiguration = {
        type: "line",
        data: {
            labels: namen,
            datasets: [{
                label: "Luftdruck",
                cubicInterpolationMode: "monotone",
                lineTension: 1.5,
                data: punkte,

                borderWidth: 2,
                backgroundColor: "rgba(0, 0, 0, 0.0)",
                borderColor: farbe,

                pointRadius: 0.2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: false,
            },
            legend: {
                display: false
            },
            scales: {
                xAxes: xAchseKonfiguration,
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: "Luftdruck in hPa"
                    }
                }]
            },
            plugins: pluignKonfiguration
        }
    };

    return new window.Chart(canvas, konfiguration);  
}

function wochenDiagrammeAktualisieren(daten) {
    if (window.wochenTemperaturDiagramm.data != null)
    {
        window.wochenTemperaturDiagramm.data.labels.push(daten.zeitpunkt);
        window.wochenTemperaturDiagramm.data.datasets.forEach((dataset) => {
            dataset.data.push({
                x: new Date(daten.zeitpunkt),
                y: parseFloat(daten.temperatur)
            });
        });
        window.wochenTemperaturDiagramm.update();
    }

    if (window.wochenLuftdruckDiagramm.data != null)
    {
        window.wochenLuftdruckDiagramm.data.labels.push(daten.zeitpunkt);
        window.wochenLuftdruckDiagramm.data.datasets.forEach((dataset) => {
            dataset.data.push({
                x: new Date(daten.zeitpunkt),
                y: parseFloat(daten.druck)
            });
        });
        window.wochenLuftdruckDiagramm.update();
    }
}

async function statusDatenBekommen() {
    var response = await fetch("api/referenzwerte.php")
    if (response.ok) {
        var daten = JSON.parse(await response.text());
        statusDatenAnwenden(daten);
    }
}

function statusDatenAnwenden(daten) {
    if (window.liveTemperatur != null) {
        temperaturStatus = "&rightarrow; gleichbleibend"
        differnezTemperatur = window.liveTemperatur - daten[0].temperatur;

        if (Math.abs(differnezTemperatur) > 0.2)
        {
            if (differnezTemperatur > 0)
            {
                temperaturStatus = "&uparrow; steigend"
            }
            if (differnezTemperatur < 0)
            {
                temperaturStatus = "&downarrow; fallend"
            }
        }

        document.getElementById("temperaturDiagrammStatus").innerHTML = temperaturStatus;
    }

    if (window.liveLuftdruck != null) {
        luftdruckStatus = "&rightarrow; gleichbleibend"
        luftdruckDiagrammStatus = "&rightarrow; gleichbleibend"
        differnezLuftdruck = window.liveLuftdruck - daten[1].druck;

        if (Math.abs(differnezLuftdruck) > 0.5)
        {
            if (differnezTemperatur > 0)
            {
                luftdruckStatus = "&uparrow; Schönwetter"
                luftdruckDiagrammStatus = "&uparrow; steigend"
            }
            if (differnezTemperatur < 0)
            {
                luftdruckStatus = "&downarrow; Schlechtwetter"
                luftdruckDiagrammStatus = "&downarrow; fallend"
            }
        }

        document.getElementById("luftdruckStatusText").innerHTML = luftdruckStatus;
        document.getElementById("luftdruckDiagrammStatus").innerHTML = luftdruckDiagrammStatus;
    }
}

window.wochenTemperaturZoomReset = function() {
    window.wochenTemperaturDiagramm.resetZoom();
};

window.wochenLuftdruckZoomReset = function() {
    window.wochenLuftdruckDiagramm.resetZoom();
};

window.insgesamtTemperaturZoomReset = function() {
    window.insgesamtTemperaturDiagramm.resetZoom();
};

window.insgesamtLuftdruckZoomReset  = function() {
    window.insgesamtLuftdruckDiagramm.resetZoom();
};

window.onload = function() {
    addPopupButtonListeners();

    Chart.defaults.global.defaultFontFamily = "Century Gothic"
    wochenDatenBekommen();
    insgesamtDatenBekommen();
    aktualisieren()
};