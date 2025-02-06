-- Creazione tabella Dipartimenti
DROP TABLE IF EXISTS `Dipartimenti`;
CREATE TABLE `Dipartimenti` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `nome` VARCHAR(100) NOT NULL UNIQUE,
    `descrizione` TEXT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Creazione tabella TutorCoordinatori
DROP TABLE IF EXISTS `TutorCoordinatori`;
CREATE TABLE `TutorCoordinatori` (
    `id_tutor_coordinatore` INT AUTO_INCREMENT PRIMARY KEY,
    `nome` VARCHAR(50) NOT NULL,
    `cognome` VARCHAR(50) NOT NULL,
    `email` VARCHAR(120) NOT NULL UNIQUE,
    `telefono` VARCHAR(20),
    `dipartimento_id` INT,
    `data_creazione` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `data_modifica` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `attivo` BOOLEAN DEFAULT TRUE,
    `ore_disponibili` INT DEFAULT 0,
    `specializzazione` VARCHAR(100),
    FOREIGN KEY (`dipartimento_id`) REFERENCES `Dipartimenti`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Creazione tabella TutorCollaboratori
DROP TABLE IF EXISTS `TutorCollaboratori`;
CREATE TABLE `TutorCollaboratori` (
    `id_tutor_collaboratore` INT AUTO_INCREMENT PRIMARY KEY,
    `nome` VARCHAR(50) NOT NULL,
    `cognome` VARCHAR(50) NOT NULL,
    `email` VARCHAR(120) NOT NULL UNIQUE,
    `telefono` VARCHAR(20),
    `dipartimento_id` INT,
    `data_creazione` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `data_modifica` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `attivo` BOOLEAN DEFAULT TRUE,
    `area_competenza` VARCHAR(100),
    `disponibilita_settimanale` INT DEFAULT 0,
    FOREIGN KEY (`dipartimento_id`) REFERENCES `Dipartimenti`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inserimento di alcuni dipartimenti di base
INSERT INTO `Dipartimenti` (`nome`, `descrizione`)
SELECT 'Scienze della Formazione', 'Dipartimento di Scienze della Formazione'
WHERE NOT EXISTS (
    SELECT 1 FROM `Dipartimenti` WHERE `nome` = 'Scienze della Formazione'
);

INSERT INTO `Dipartimenti` (`nome`, `descrizione`)
SELECT 'Scienze dell''Educazione', 'Dipartimento di Scienze dell''Educazione'
WHERE NOT EXISTS (
    SELECT 1 FROM `Dipartimenti` WHERE `nome` = 'Scienze dell''Educazione'
);

INSERT INTO `Dipartimenti` (`nome`, `descrizione`)
SELECT 'Scienze Umane', 'Dipartimento di Scienze Umane'
WHERE NOT EXISTS (
    SELECT 1 FROM `Dipartimenti` WHERE `nome` = 'Scienze Umane'
);