-- Rimuovi i trigger esistenti se presenti
DROP TRIGGER IF EXISTS before_lezione_insert;
DROP TRIGGER IF EXISTS before_lezione_update;

-- Modifica la tabella per rimuovere le colonne generate
ALTER TABLE `Lezioni` 
MODIFY COLUMN `durata` time NULL,
MODIFY COLUMN `cfu` decimal(4,2) NULL;

-- Crea i trigger per il calcolo automatico
DELIMITER //

CREATE TRIGGER before_lezione_insert
BEFORE INSERT ON Lezioni
FOR EACH ROW
BEGIN
    SET NEW.durata = TIMEDIFF(NEW.orario_fine, NEW.orario_inizio);
    SET NEW.cfu = TIME_TO_SEC(TIMEDIFF(NEW.orario_fine, NEW.orario_inizio)) / 16200;
END//

CREATE TRIGGER before_lezione_update
BEFORE UPDATE ON Lezioni
FOR EACH ROW
BEGIN
    SET NEW.durata = TIMEDIFF(NEW.orario_fine, NEW.orario_inizio);
    SET NEW.cfu = TIME_TO_SEC(TIMEDIFF(NEW.orario_fine, NEW.orario_inizio)) / 16200;
END//

DELIMITER ;
