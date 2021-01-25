<?php
    require_once "config.php";
    require_once "allgemein.php";

    function neusteDatenBekommen() {
        $luftinfos = new LuftInformationen();

        $sql = "SELECT * FROM woche ORDER BY `daten-index` DESC LIMIT 1";
        if ($statement = $GLOBALS["mysqli"]->prepare($sql)) {
            if ($statement->execute()) {
                $statement->store_result();
                $statement->bind_result($luftinfos->id, $luftinfos->zeitpunkt, $luftinfos->temperatur, $luftinfos->druck, $luftinfos->feuchtigkeit);
                $statement->fetch();
            }
        }

        return $luftinfos;
    }

    $luftinfos = neusteDatenBekommen();
    echo $luftinfos->zuJSON();
?>