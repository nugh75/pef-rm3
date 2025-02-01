-- Creazione della tabella principale per l'associazione lezioni-tutor
CREATE TABLE IF NOT EXISTS Lezioni_TutorCollaboratori (
    id_lezione INT NOT NULL,
    id_tutor_collaboratore INT NOT NULL,
    ruolo VARCHAR(255),
    note TEXT,
    data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_modifica TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id_lezione, id_tutor_collaboratore),
    FOREIGN KEY (id_lezione) REFERENCES Lezioni(id_lezione) ON DELETE CASCADE,
    FOREIGN KEY (id_tutor_collaboratore) REFERENCES TutorCollaboratori(id_tutor_collaboratore) ON DELETE CASCADE
);

-- Creazione della tabella per lo storico
CREATE TABLE IF NOT EXISTS Lezioni_TutorCollaboratori_Storia (
    id_storia INT AUTO_INCREMENT PRIMARY KEY,
    id_lezione INT NOT NULL,
    id_tutor_collaboratore INT NOT NULL,
    ruolo VARCHAR(255),
    note TEXT,
    azione ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    data_modifica TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modificato_da VARCHAR(255),
    FOREIGN KEY (id_lezione) REFERENCES Lezioni(id_lezione) ON DELETE CASCADE,
    FOREIGN KEY (id_tutor_collaboratore) REFERENCES TutorCollaboratori(id_tutor_collaboratore) ON DELETE CASCADE
);

-- Creazione degli indici per ottimizzare le performance
CREATE INDEX idx_lezioni_tutor_lezione ON Lezioni_TutorCollaboratori(id_lezione);
CREATE INDEX idx_lezioni_tutor_collaboratore ON Lezioni_TutorCollaboratori(id_tutor_collaboratore);
CREATE INDEX idx_storia_lezione ON Lezioni_TutorCollaboratori_Storia(id_lezione);
CREATE INDEX idx_storia_tutor ON Lezioni_TutorCollaboratori_Storia(id_tutor_collaboratore);
CREATE INDEX idx_storia_data ON Lezioni_TutorCollaboratori_Storia(data_modifica);

-- Creazione dei trigger per mantenere lo storico
DELIMITER //

CREATE TRIGGER tr_lezioni_tutor_insert 
AFTER INSERT ON Lezioni_TutorCollaboratori
FOR EACH ROW
BEGIN
    INSERT INTO Lezioni_TutorCollaboratori_Storia 
    (id_lezione, id_tutor_collaboratore, ruolo, note, azione, modificato_da)
    VALUES 
    (NEW.id_lezione, NEW.id_tutor_collaboratore, NEW.ruolo, NEW.note, 'INSERT', CURRENT_USER());
END//

CREATE TRIGGER tr_lezioni_tutor_update 
AFTER UPDATE ON Lezioni_TutorCollaboratori
FOR EACH ROW
BEGIN
    INSERT INTO Lezioni_TutorCollaboratori_Storia 
    (id_lezione, id_tutor_collaboratore, ruolo, note, azione, modificato_da)
    VALUES 
    (NEW.id_lezione, NEW.id_tutor_collaboratore, NEW.ruolo, NEW.note, 'UPDATE', CURRENT_USER());
END//

CREATE TRIGGER tr_lezioni_tutor_delete 
AFTER DELETE ON Lezioni_TutorCollaboratori
FOR EACH ROW
BEGIN
    INSERT INTO Lezioni_TutorCollaboratori_Storia 
    (id_lezione, id_tutor_collaboratore, ruolo, note, azione, modificato_da)
    VALUES 
    (OLD.id_lezione, OLD.id_tutor_collaboratore, OLD.ruolo, OLD.note, 'DELETE', CURRENT_USER());
END//

DELIMITER ;