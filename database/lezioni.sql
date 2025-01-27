-- Tabella principale delle lezioni
CREATE TABLE `Lezioni` (
    `id_lezione` int NOT NULL AUTO_INCREMENT,
    `nome_lezione` varchar(255) NOT NULL,
    `data` date NOT NULL,
    `orario_inizio` time NOT NULL,
    `orario_fine` time NOT NULL,
    `durata` time GENERATED ALWAYS AS (timediff(orario_fine, orario_inizio)) STORED,
    `cfu` decimal(4,2) GENERATED ALWAYS AS (time_to_sec(timediff(orario_fine, orario_inizio)) / 16200) STORED,
    `id_insegnante` int NOT NULL,
    PRIMARY KEY (`id_lezione`),
    FOREIGN KEY (`id_insegnante`) REFERENCES `Insegnanti` (`id_insegnante`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabella di collegamento per le classi di concorso
CREATE TABLE `Lezioni_ClassiConcorso` (
    `id_lezione` int NOT NULL,
    `id_classe` int NOT NULL,
    PRIMARY KEY (`id_lezione`, `id_classe`),
    FOREIGN KEY (`id_lezione`) REFERENCES `Lezioni` (`id_lezione`) ON DELETE CASCADE,
    FOREIGN KEY (`id_classe`) REFERENCES `Classi di concorso` (`id_classe`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabella di collegamento per i dipartimenti
CREATE TABLE `Lezioni_Dipartimenti` (
    `id_lezione` int NOT NULL,
    `id_dipartimento` int NOT NULL,
    PRIMARY KEY (`id_lezione`, `id_dipartimento`),
    FOREIGN KEY (`id_lezione`) REFERENCES `Lezioni` (`id_lezione`) ON DELETE CASCADE,
    FOREIGN KEY (`id_dipartimento`) REFERENCES `Dipartimenti` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabella di collegamento per i percorsi
CREATE TABLE `Lezioni_Percorsi` (
    `id_lezione` int NOT NULL,
    `id_percorso` int NOT NULL,
    PRIMARY KEY (`id_lezione`, `id_percorso`),
    FOREIGN KEY (`id_lezione`) REFERENCES `Lezioni` (`id_lezione`) ON DELETE CASCADE,
    FOREIGN KEY (`id_percorso`) REFERENCES `Percorsi` (`id_percorso`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
