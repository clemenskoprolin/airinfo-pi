<?php
    class LuftInformationen {
        public $id;
        public $zeitpunkt;
        public $temperatur;
        public $druck;
        public $feuchtigkeit;

        function erstellen($id, $zeitpunkt, $temperatur, $druck, $feuchtigkeit) {
            $this->id = $id;
            $this->zeitpunkt = $zeitpunkt;
            $this->temperatur = $temperatur;
            $this->druck = $druck;
            $this->feuchtigkeit = $feuchtigkeit;
        }

        function zuArray() {
            $datenArray = array("id"=>$this->id, "zeitpunkt"=>$this->zeitpunkt, "temperatur"=>$this->temperatur, "druck"=>$this->druck, "feuchtigkeit"=>$this->feuchtigkeit);
            return $datenArray;
        }

        function zuJson() {
            $daten = array("id"=>$this->id, "zeitpunkt"=>$this->zeitpunkt, "temperatur"=>$this->temperatur, "druck"=>$this->druck, "feuchtigkeit"=>$this->feuchtigkeit);
            return json_encode($daten);
        }
    }
?>