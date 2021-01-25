<?php
    require_once "config.php";
    require_once "allgemein.php";

    function referenzwerteBekommen() {
        $luftinfosArray = array();

        $referenz1 = new LuftInformationen();
        $sql = "SELECT * FROM woche ORDER BY `daten-index` DESC LIMIT 1 OFFSET 100";
        if ($statement = $GLOBALS["mysqli"]->prepare($sql)) {
            if ($statement->execute()) {
                $statement->store_result();
                $statement->bind_result($referenz1->id, $referenz1->zeitpunkt, $referenz1->temperatur, $referenz1->druck, $referenz1->feuchtigkeit);
                $statement->fetch();
            }
        }
        array_push($luftinfosArray, $referenz1);

        $referenz2 = new LuftInformationen();
        $sql = "SELECT * FROM woche ORDER BY `daten-index` DESC LIMIT 1 OFFSET 300";
        if ($statement = $GLOBALS["mysqli"]->prepare($sql)) {
            if ($statement->execute()) {
                $statement->store_result();
                $statement->bind_result($referenz2->id, $referenz2->zeitpunkt, $referenz2->temperatur, $referenz2->druck, $referenz2->feuchtigkeit);
                $statement->fetch();
            }
        }
        array_push($luftinfosArray, $referenz2);
        return $luftinfosArray;
    }

    $luftinfosArray = referenzwerteBekommen();
    $luftinfosJsonArray = array();
    foreach ($luftinfosArray as $schlüssel => $luftinfos) {
        $luftinfosJsonArray[$schlüssel] = $luftinfos->zuArray();
    }

    echo json_encode($luftinfosJsonArray);
?>