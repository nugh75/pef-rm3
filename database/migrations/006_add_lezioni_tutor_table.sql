-- Creazione della tabella di associazione lezioni-tutor
CREATE TABLE IF NOT EXISTS Lezioni_TutorCollaboratori (
    id_lezione INT NOT NULL,
    id_tutor_collaboratore INT NOT NULL,
    data_assegnazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_modifica TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    note TEXT,
    PRIMARY KEY (id_lezione, id_tutor_collaboratore),
    FOREIGN KEY (id_lezione) REFERENCES Lezioni(id_lezione) ON DELETE CASCADE,
    FOREIGN KEY (id_tutor_collaboratore) REFERENCES TutorCollaboratori(id_tutor_collaboratore) ON DELETE CASCADE
);

-- Indici per ottimizzare le performance
CREATE INDEX idx_lezioni_tutor_data ON Lezioni_TutorCollaboratori(data_assegnazione);
CREATE INDEX idx_lezioni_tutor_lezione ON Lezioni_TutorCollaboratori(id_lezione);
CREATE INDEX idx_lezioni_tutor_collaboratore ON Lezioni_TutorCollaboratori(id_tutor_collaboratore);

-- Creazione della tabella per lo storico delle modifiche
CREATE TABLE IF NOT EXISTS Lezioni_TutorCollaboratori_Storia (
    id_storia INT AUTO_INCREMENT PRIMARY KEY,
    id_lezione INT NOT NULL,
    id_tutor_collaboratore INT NOT NULL,
    azione ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    data_modifica TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    note TEXT,
    modificato_da VARCHAR(255),
    FOREIGN KEY (id_lezione) REFERENCES Lezioni(id_lezione) ON DELETE CASCADE,
    FOREIGN KEY (id_tutor_collaboratore) REFERENCES TutorCollaboratori(id_tutor_collaboratore) ON DELETE CASCADE
);

-- Trigger per mantenere lo storico delle modifiche
DELIMITER //

CREATE TRIGGER tr_lezioni_tutor_insert AFTER INSERT ON Lezioni_TutorCollaboratori
FOR EACH ROW
BEGIN
    INSERT INTO Lezioni_TutorCollaboratori_Storia 
    (id_lezione, id_tutor_collaboratore, azione, note, modificato_da)
    VALUES 
    (NEW.id_lezione, NEW.id_tutor_collaboratore, 'INSERT', NEW.note, CURRENT_USER());
END//

CREATE TRIGGER tr_lezioni_tutor_update AFTER UPDATE ON Lezioni_TutorCollaboratori
FOR EACH ROW
BEGIN
    INSERT INTO Lezioni_TutorCollaboratori_Storia 
    (id_lezione, id_tutor_collaboratore, azione, note, modificato_da)
    VALUES 
    (NEW.id_lezione, NEW.id_tutor_collaboratore, 'UPDATE', NEW.note, CURRENT_USER());
END//

CREATE TRIGGER tr_lezioni_tutor_delete AFTER DELETE ON Lezioni_TutorCollaboratori
FOR EACH ROW
BEGIN
    INSERT INTO Lezioni_TutorCollaboratori_Storia 
    (id_lezione, id_tutor_collaboratore, azione, note, modificato_da)
    VALUES 
    (OLD.id_lezione, OLD.id_tutor_collaboratore, 'DELETE', OLD.note, CURRENT_USER());
END//

DELIMITER ;