-- Rimuovi la vecchia colonna classe_id dalla tabella Lezioni
ALTER TABLE `Lezioni` DROP FOREIGN KEY `Lezioni_ibfk_2`;
ALTER TABLE `Lezioni` DROP COLUMN `classe_id`;

-- Crea le nuove tabelle di relazione
CREATE TABLE `Lezioni_ClassiConcorso` (
    `id_lezione` int NOT NULL,
    `id_classe` int NOT NULL,
    PRIMARY KEY (`id_lezione`, `id_classe`),
    FOREIGN KEY (`id_lezione`) REFERENCES `Lezioni` (`id_lezione`) ON DELETE CASCADE,
    FOREIGN KEY (`id_classe`) REFERENCES `Classi di concorso` (`id_classe`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Lezioni_Dipartimenti` (
    `id_lezione` int NOT NULL,
    `id_dipartimento` int NOT NULL,
    PRIMARY KEY (`id_lezione`, `id_dipartimento`),
    FOREIGN KEY (`id_lezione`) REFERENCES `Lezioni` (`id_lezione`) ON DELETE CASCADE,
    FOREIGN KEY (`id_dipartimento`) REFERENCES `Dipartimenti` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `Lezioni_Percorsi` (
    `id_lezione` int NOT NULL,
    `id_percorso` int NOT NULL,
    PRIMARY KEY (`id_lezione`, `id_percorso`),
    FOREIGN KEY (`id_lezione`) REFERENCES `Lezioni` (`id_lezione`) ON DELETE CASCADE,
    FOREIGN KEY (`id_percorso`) REFERENCES `Percorsi` (`id_percorso`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Migra i dati esistenti dalla vecchia relazione alla nuova
INSERT INTO `Lezioni_ClassiConcorso` (`id_lezione`, `id_classe`)
SELECT `id_lezione`, `classe_id` FROM `Lezioni` WHERE `classe_id` IS NOT NULL;
