# Gestione Tutor Collaboratori nelle Lezioni

## Struttura del Database

### Tabelle

1. **Lezioni_TutorCollaboratori**
   - Tabella di associazione many-to-many tra lezioni e tutor collaboratori
   - Campi:
     * `id_lezione` (INT): Chiave esterna riferita a Lezioni
     * `id_tutor_collaboratore` (INT): Chiave esterna riferita a TutorCollaboratori
     * `ruolo` (VARCHAR): Ruolo del tutor nella lezione
     * `note` (TEXT): Note opzionali
     * `data_creazione` (TIMESTAMP): Data di creazione del record
     * `data_modifica` (TIMESTAMP): Data dell'ultima modifica

2. **Lezioni_TutorCollaboratori_Storia**
   - Tabella per il tracciamento storico delle modifiche
   - Campi:
     * `id_storia` (INT): Identificatore univoco auto-incrementante
     * `id_lezione` (INT): Riferimento alla lezione
     * `id_tutor_collaboratore` (INT): Riferimento al tutor
     * `ruolo` (VARCHAR): Ruolo del tutor
     * `note` (TEXT): Note associate
     * `azione` (ENUM): Tipo di modifica ('INSERT', 'UPDATE', 'DELETE')
     * `data_modifica` (TIMESTAMP): Data della modifica
     * `modificato_da` (VARCHAR): Utente che ha effettuato la modifica

### Indici
- `idx_lezioni_tutor_lezione`: Ottimizza le ricerche per lezione
- `idx_lezioni_tutor_collaboratore`: Ottimizza le ricerche per tutor
- `idx_storia_lezione`: Ottimizza le ricerche storiche per lezione
- `idx_storia_tutor`: Ottimizza le ricerche storiche per tutor
- `idx_storia_data`: Ottimizza le ricerche storiche per data

### Trigger
1. `tr_lezioni_tutor_insert`: Registra nuove assegnazioni
2. `tr_lezioni_tutor_update`: Registra modifiche alle assegnazioni
3. `tr_lezioni_tutor_delete`: Registra rimozioni di assegnazioni

## Implementazione

### Modelli SQLAlchemy

```python
class LezioniTutorCollaboratori(db.Model):
    __tablename__ = 'Lezioni_TutorCollaboratori'
    id_lezione = db.Column(db.Integer, db.ForeignKey('Lezioni.id_lezione'), primary_key=True)
    id_tutor_collaboratore = db.Column(db.Integer, db.ForeignKey('TutorCollaboratori.id_tutor_collaboratore'), primary_key=True)
    ruolo = db.Column(db.String(255))
    note = db.Column(db.Text)

class Lezioni(db.Model):
    # ... altri campi ...
    tutor_collaboratori = db.relationship('TutorCollaboratori',
                                      secondary='Lezioni_TutorCollaboratori',
                                      backref=db.backref('lezioni', lazy='dynamic'))
```

### Query Comuni

1. Ottenere tutti i tutor di una lezione:
```python
tutor_collaboratori = db.session.query(
    TutorCollaboratori, LezioniTutorCollaboratori
).join(
    LezioniTutorCollaboratori,
    TutorCollaboratori.id_tutor_collaboratore == LezioniTutorCollaboratori.id_tutor_collaboratore
).filter(
    LezioniTutorCollaboratori.id_lezione == id_lezione
).all()
```

2. Ottenere tutte le lezioni di un tutor:
```python
lezioni = db.session.query(
    Lezioni, LezioniTutorCollaboratori
).join(
    LezioniTutorCollaboratori,
    Lezioni.id_lezione == LezioniTutorCollaboratori.id_lezione
).filter(
    LezioniTutorCollaboratori.id_tutor_collaboratore == id_tutor
).all()
```

## Installazione

1. Eseguire la migrazione del database:
```bash
mysql -u username -p database_name < database/migrations/006_create_lezioni_tutor_tables.sql
```

2. Verificare la creazione delle tabelle:
```sql
SHOW TABLES LIKE 'Lezioni_TutorCollaboratori%';
```

3. Verificare gli indici:
```sql
SHOW INDEX FROM Lezioni_TutorCollaboratori;
SHOW INDEX FROM Lezioni_TutorCollaboratori_Storia;
```

4. Verificare i trigger:
```sql
SHOW TRIGGERS LIKE 'Lezioni_TutorCollaboratori%';
```

## Interfaccia Utente

L'interfaccia utente per la gestione dei tutor collaboratori è implementata in:
- `templates/edit_lezione.html`: Form per l'assegnazione dei tutor
- `static/js/edit_lezione.js`: Gestione dinamica dei tutor

### Funzionalità
- Aggiunta/rimozione dinamica dei tutor
- Assegnazione ruoli e note per ogni tutor
- Validazione lato client per evitare duplicati
- Feedback visuale per le azioni dell'utente

## Sicurezza e Validazione

1. **Validazione Lato Client**
   - Controllo duplicati
   - Campi obbligatori
   - Feedback immediato

2. **Validazione Lato Server**
   - Verifica permessi utente
   - Validazione dati in ingresso
   - Gestione transazioni

3. **Tracciamento Modifiche**
   - Logging automatico attraverso trigger
   - Storico completo delle modifiche
   - Identificazione dell'utente che effettua le modifiche

## Manutenzione

1. **Backup**
   - Includere entrambe le tabelle nei backup
   - Verificare l'integrità dei dati storici
   - Mantenere gli indici aggiornati

2. **Pulizia Dati**
   - Implementare policy di retention per i dati storici
   - Monitorare la crescita della tabella storia
   - Ottimizzare periodicamente gli indici

3. **Monitoraggio**
   - Verificare le performance delle query
   - Monitorare lo spazio utilizzato
   - Controllare l'integrità referenziale