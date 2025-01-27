CREATE TABLE `Classi di concorso` (
  `id_classe` int NOT NULL AUTO_INCREMENT,
  `nome_classe` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `codice` varchar(10) COLLATE utf8mb4_general_ci UNIQUE,
  PRIMARY KEY (`id_classe`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
