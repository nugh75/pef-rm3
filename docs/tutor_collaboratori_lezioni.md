# Architettura Relazione Tutor Collaboratori - Lezioni

## Struttura del Database

Il sistema implementa una relazione many-to-many tra tutor collaboratori e lezioni attraverso le seguenti tabelle:

### Lezioni_TutorCollaboratori
Tabella di associazione principale che collega tutor collaboratori e lezioni:
- `id_lezione` (INT): Chiave esterna riferita alla tabella Lezioni
- `id_tutor_collaboratore` (INT): Chiave esterna riferita alla tabella TutorCollaboratori
- `data_assegnazione` (TIMESTAMP): Data di assegnazione del tutor alla lezione
- `data_modifica` (TIMESTAMP): Data dell'ultima modifica
- `note` (TEXT): Note opzionali sull'assegnazione

La chiave primaria è composta da (id_lezione, id_tutor_collaboratore), garantendo che un tutor non possa essere assegnato più volte alla stessa lezione.

### Lezioni_TutorCollaboratori_Storia
Tabella che mantiene lo storico delle modifiche:
- `id_storia` (INT): Identificatore univoco auto-incrementante
- `id_lezione` (INT): Riferimento alla lezione
- `id_tutor_collaboratore` (INT): Riferimento al tutor
- `azione` (ENUM): Tipo di modifica ('INSERT', 'UPDATE', 'DELETE')
- `data_modifica` (TIMESTAMP): Data della modifica
- `note` (TEXT): Note associate alla modifica
- `modificato_da` (VARCHAR): Utente che ha effettuato la modifica

## Indici per l'Ottimizzazione

Sono stati creati i seguenti indici per ottimizzare le query più comuni:
- `idx_lezioni_tutor_data`: Indice sulla data di assegnazione
- `idx_lezioni_tutor_lezione`: Indice sull'ID della lezione
- `idx_lezioni_tutor_collaboratore`: Indice sull'ID del tutor collaboratore

## Trigger Automatici

Il sistema mantiene automaticamente lo storico delle modifiche attraverso tre trigger:
1. `tr_lezioni_tutor_insert`: Registra nuove assegnazioni
2. `tr_lezioni_tutor_update`: Registra modifiche alle assegnazioni
3. `tr_lezioni_tutor_delete`: Registra rimozioni di assegnazioni

## Utilizzo del Sistema

### Assegnazione di un Tutor a una Lezione
```sql
INSERT INTO Lezioni_TutorCollaboratori 
(id_lezione, id_tutor_collaboratore, note)
VALUES 
(id_lezione, id_tutor_collaboratore, 'Note opzionali');
```

### Modifica di un'Assegnazione
```sql
UPDATE Lezioni_TutorCollaboratori
SET note = 'Nuove note'
WHERE id_lezione = X AND id_tutor_collaboratore = Y;
```

### Rimozione di un'Assegnazione
```sql
DELETE FROM Lezioni_TutorCollaboratori
WHERE id_lezione = X AND id_tutor_collaboratore = Y;
```

### Query Comuni

1. Trovare tutti i tutor di una lezione:
```sql
SELECT tc.*
FROM TutorCollaboratori tc
JOIN Lezioni_TutorCollaboratori ltc ON tc.id_tutor_collaboratore = ltc.id_tutor_collaboratore
WHERE ltc.id_lezione = X;
```

2. Trovare tutte le lezioni di un tutor:
```sql
SELECT l.*
FROM Lezioni l
JOIN Lezioni_TutorCollaboratori ltc ON l.id_lezione = ltc.id_lezione
WHERE ltc.id_tutor_collaboratore = X;
```

3. Visualizzare lo storico delle modifiche:
```sql
SELECT *
FROM Lezioni_TutorCollaboratori_Storia
WHERE id_lezione = X OR id_tutor_collaboratore = Y
ORDER BY data_modifica DESC;
```

## Best Practices

1. Utilizzare sempre le chiavi esterne per mantenere l'integrità referenziale
2. Sfruttare gli indici nelle query per ottimizzare le performance
3. Consultare la tabella storia per tracciare le modifiche quando necessario
4. Includere note significative per documentare le ragioni delle modifiche

## Considerazioni sulla Sicurezza

1. Le foreign key con `ON DELETE CASCADE` assicurano la pulizia automatica dei dati correlati
2. Lo storico mantiene traccia di tutte le modifiche con l'utente che le ha effettuate
3. Gli indici proteggono da problemi di performance su grandi volumi di dati