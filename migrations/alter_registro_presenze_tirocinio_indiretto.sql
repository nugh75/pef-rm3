-- Rimuovi i trigger esistenti se presenti
DROP TRIGGER IF EXISTS before_registro_presenze_tirocinio_indiretto_insert;
DROP TRIGGER IF EXISTS before_registro_presenze_tirocinio_indiretto_update;

-- Modifica la tabella per rimuovere la colonna generata
ALTER TABLE `RegistroPresenzeTirocinioIndiretto` 
MODIFY COLUMN `cfu` float NULL;
