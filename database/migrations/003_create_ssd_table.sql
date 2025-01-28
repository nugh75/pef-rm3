-- Crea la tabella SSD se non esiste
CREATE TABLE IF NOT EXISTS `SSD` (
    `id_ssd` INT AUTO_INCREMENT PRIMARY KEY,
    `codice` VARCHAR(12) NOT NULL,
    `descrizione` VARCHAR(255)
);

-- Aggiunge la chiave esterna alla tabella Insegnanti se non esiste già
ALTER TABLE `Insegnanti`
ADD CONSTRAINT `fk_insegnanti_ssd`
FOREIGN KEY (`id_ssd`) REFERENCES `SSD` (`id_ssd`)
ON DELETE SET NULL;