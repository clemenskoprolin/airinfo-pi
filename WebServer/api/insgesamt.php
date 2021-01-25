<?php
    require_once "config.php";
    require_once "allgemein.php";

    function alleDatenBekommen() {
        $luftinfosArray = array();
        $luftinfos = new LuftInformationen();

        $sql = "SELECT * FROM gesamt";
        $result = $GLOBALS["mysqli"]->query($sql);
        
        if ($result->num_rows > 0) {
            while($row = $result->fetch_assoc()) {
                $luftinfos = new LuftInformationen();
                $luftinfos->erstellen($row["daten-index"], $row["zeitpunkt"], $row["temperatur"], $row["luftdruck"], $row["luftfeuchtigkeit"]);

                array_push($luftinfosArray, $luftinfos);
            }
        }

        return $luftinfosArray;
    }

    $luftinfosArray = alleDatenBekommen();
    $luftinfosJsonArray = array();
    foreach ($luftinfosArray as $schlüssel => $luftinfos) {
        $luftinfosJsonArray[$schlüssel] = $luftinfos->zuArray();
    }

    echo json_encode($luftinfosJsonArray);
?>