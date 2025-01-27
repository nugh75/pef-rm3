-- Backup dei dati esistenti
CREATE TEMPORARY TABLE temp_lezioni AS SELECT * FROM Lezioni;

-- Rimuovi le vecchie foreign key
ALTER TABLE Lezioni 
DROP FOREIGN KEY Lezioni_ibfk_2;

-- Modifica la tabella Lezioni
ALTER TABLE Lezioni 
DROP COLUMN classe_id,
MODIFY COLUMN durata time GENERATED ALWAYS AS (timediff(orario_fine, orario_inizio)) STORED,
MODIFY COLUMN cfu decimal(4,2) GENERATED ALWAYS AS (time_to_sec(timediff(orario_fine, orario_inizio)) / 16200) STORED;

-- Crea le nuove tabelle per le relazioni molti-a-molti
CREATE TABLE IF NOT EXISTS Lezioni_ClassiConcorso (
    id_lezione int NOT NULL,
    id_classe int NOT NULL,
    PRIMARY KEY (id_lezione, id_classe),
    FOREIGN KEY (id_lezione) REFERENCES Lezioni (id_lezione) ON DELETE CASCADE,
    FOREIGN KEY (id_classe) REFERENCES `Classi di concorso` (id_classe) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS Lezioni_Dipartimenti (
    id_lezione int NOT NULL,
    id_dipartimento int NOT NULL,
    PRIMARY KEY (id_lezione, id_dipartimento),
    FOREIGN KEY (id_lezione) REFERENCES Lezioni (id_lezione) ON DELETE CASCADE,
    FOREIGN KEY (id_dipartimento) REFERENCES Dipartimenti (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS Lezioni_Percorsi (
    id_lezione int NOT NULL,
    id_percorso int NOT NULL,
    PRIMARY KEY (id_lezione, id_percorso),
    FOREIGN KEY (id_lezione) REFERENCES Lezioni (id_lezione) ON DELETE CASCADE,
    FOREIGN KEY (id_percorso) REFERENCES Percorsi (id_percorso) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Migra i dati esistenti nella tabella di collegamento classi
INSERT INTO Lezioni_ClassiConcorso (id_lezione, id_classe)
SELECT id_lezione, classe_id 
FROM temp_lezioni 
WHERE classe_id IS NOT NULL;

-- Pulisci
DROP TEMPORARY TABLE temp_lezioni;

-- Script di rollback in caso di problemi
/*
DROP TABLE IF EXISTS Lezioni_Percorsi;
DROP TABLE IF EXISTS Lezioni_Dipartimenti;
DROP TABLE IF EXISTS Lezioni_ClassiConcorso;

ALTER TABLE Lezioni 
ADD COLUMN classe_id int,
ADD FOREIGN KEY (classe_id) REFERENCES `Classi di concorso` (id_classe);

-- Ripristina i dati dal backup se necessario
*/
