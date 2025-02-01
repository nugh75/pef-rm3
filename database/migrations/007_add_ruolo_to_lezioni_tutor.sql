-- Aggiunta campo ruolo alla tabella Lezioni_TutorCollaboratori
ALTER TABLE Lezioni_TutorCollaboratori 
ADD ruolo VARCHAR(255);

-- Aggiornamento della tabella storia per includere il ruolo
ALTER TABLE Lezioni_TutorCollaboratori_Storia 
ADD ruolo VARCHAR(255);

-- Aggiornamento dei trigger per gestire il nuovo campo
DROP TRIGGER IF EXISTS tr_lezioni_tutor_insert;
CREATE TRIGGER tr_lezioni_tutor_insert 
AFTER INSERT ON Lezioni_TutorCollaboratori
FOR EACH ROW
BEGIN
    INSERT INTO Lezioni_TutorCollaboratori_Storia 
    (id_lezione, id_tutor_collaboratore, ruolo, azione, note, modificato_da)
    VALUES 
    (NEW.id_lezione, NEW.id_tutor_collaboratore, NEW.ruolo, 'INSERT', NEW.note, CURRENT_USER());
END;

DROP TRIGGER IF EXISTS tr_lezioni_tutor_update;
CREATE TRIGGER tr_lezioni_tutor_update 
AFTER UPDATE ON Lezioni_TutorCollaboratori
FOR EACH ROW
BEGIN
    INSERT INTO Lezioni_TutorCollaboratori_Storia 
    (id_lezione, id_tutor_collaboratore, ruolo, azione, note, modificato_da)
    VALUES 
    (NEW.id_lezione, NEW.id_tutor_collaboratore, NEW.ruolo, 'UPDATE', NEW.note, CURRENT_USER());
END;

DROP TRIGGER IF EXISTS tr_lezioni_tutor_delete;
CREATE TRIGGER tr_lezioni_tutor_delete 
AFTER DELETE ON Lezioni_TutorCollaboratori
FOR EACH ROW
BEGIN
    INSERT INTO Lezioni_TutorCollaboratori_Storia 
    (id_lezione, id_tutor_collaboratore, ruolo, azione, note, modificato_da)
    VALUES 
    (OLD.id_lezione, OLD.id_tutor_collaboratore, OLD.ruolo, 'DELETE', OLD.note, CURRENT_USER());
END;