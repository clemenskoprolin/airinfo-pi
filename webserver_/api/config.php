<?php
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);

    date_default_timezone_set("Europe/Berlin");

    define("db_server", "localhost");
    define("db_name", "airinfo");
    define("db_username","airinfo");
    define("db_password","123456"); #Das sicherste Passwort der Welt

    $mysqli = new mysqli(db_server, db_username, db_password, db_name);

    if ($mysqli->connect_errno) {
        echo "FEHLER: Verbindung zur Datenbank fehlgeschlagen: ";
        echo "Errno: " . $mysqli->connect_errno . "\n";
        echo "Error: " . $mysqli->connect_error . "\n";
    }
?>