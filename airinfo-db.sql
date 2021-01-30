SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `airinfo`
--
CREATE DATABASE IF NOT EXISTS `airinfo` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `airinfo`;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `gesamt`
--

CREATE TABLE `gesamt` (
  `daten-index` int(11) NOT NULL,
  `zeitpunkt` datetime NOT NULL DEFAULT current_timestamp(),
  `temperatur` float DEFAULT NULL,
  `luftdruck` float DEFAULT NULL,
  `luftfeuchtigkeit` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `woche`
--

CREATE TABLE `woche` (
  `daten-index` int(11) NOT NULL,
  `zeitpunkt` datetime NOT NULL DEFAULT current_timestamp(),
  `temperatur` float DEFAULT NULL,
  `luftdruck` float DEFAULT NULL,
  `luftfeuchtigkeit` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `gesamt`
--
ALTER TABLE `gesamt`
  ADD PRIMARY KEY (`daten-index`);

--
-- Indizes für die Tabelle `woche`
--
ALTER TABLE `woche`
  ADD PRIMARY KEY (`daten-index`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `gesamt`
--
ALTER TABLE `gesamt`
  MODIFY `daten-index` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;
--
-- AUTO_INCREMENT für Tabelle `woche`
--
ALTER TABLE `woche`
  MODIFY `daten-index` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=893;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
