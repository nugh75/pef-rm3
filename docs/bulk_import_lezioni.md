# Architettura Importazione Bulk Lezioni

## Panoramica
Il sistema deve supportare l'importazione di multiple lezioni tramite file Excel. Questa funzionalità permette agli utenti di caricare un file Excel contenente i dettagli di più lezioni che verranno automaticamente importate nel sistema.

## Struttura File Excel
Il file Excel deve contenere le seguenti colonne:
- Nome Lezione (obbligatorio)
- Data (obbligatorio, formato: DD/MM/YYYY)
- Orario Inizio (obbligatorio, formato: HH:MM)
- Orario Fine (obbligatorio, formato: HH:MM)
- ID Insegnante (obbligatorio, deve esistere nel sistema)
- Classi di Concorso (opzionale, IDs separati da virgola)
- Dipartimenti (opzionale, IDs separati da virgola)
- Percorsi (opzionale, IDs separati da virgola)

## Flusso dei Dati
1. L'utente accede alla pagina delle lezioni
2. Clicca sul pulsante "Importa da Excel"
3. Seleziona il file Excel da caricare
4. Il sistema:
   - Valida il formato del file
   - Legge i dati riga per riga
   - Valida ogni riga
   - Crea le lezioni nel database
   - Gestisce le relazioni (classi, dipartimenti, percorsi)
   - Fornisce feedback sui risultati

## Validazioni
- Formato file: .xlsx o .xls
- Presenza colonne obbligatorie
- Validità dei dati:
  - Date nel formato corretto
  - Orari nel formato corretto
  - ID Insegnante esistente
  - IDs di classi/dipartimenti/percorsi validi
  - Orario fine successivo a orario inizio

## Gestione Errori
Il sistema deve:
1. Validare l'intero file prima di procedere con l'importazione
2. Creare un report degli errori che includa:
   - Righe con errori
   - Tipo di errore per ogni riga
   - Suggerimenti per la correzione
3. Supportare transazioni per mantenere l'integrità dei dati
4. Permettere rollback in caso di errori

## Modifiche Necessarie

### Backend (app.py)
1. Nuove dipendenze:
   ```python
   pandas
   openpyxl
   ```

2. Nuove funzioni:
   - `validate_excel_file(file)`: Valida formato e struttura
   - `parse_excel_data(df)`: Converte dati Excel in oggetti Lezione
   - `validate_lesson_data(row)`: Valida singola riga
   - `import_lessons(lessons)`: Importa lezioni validate
   - `generate_error_report(errors)`: Crea report errori

3. Nuova route:
   ```python
   @app.route('/import_lezioni', methods=['GET', 'POST'])
   ```

### Frontend
1. Nuovo template:
   ```
   templates/lezioni/import_lezioni.html
   ```
   - Form upload file
   - Visualizzazione progressi
   - Visualizzazione errori
   - Preview dati

2. Modifiche a tab_lezioni.html:
   - Aggiunta pulsante importazione
   - Integrazione messaggi feedback

### Database
Non sono necessarie modifiche allo schema del database poiché utilizzeremo le tabelle esistenti:
- Lezioni
- Lezioni_ClassiConcorso
- Lezioni_Dipartimenti
- Lezioni_Percorsi

## Sicurezza
- Validazione MIME type dei file
- Limite dimensione file
- Sanitizzazione dati input
- Gestione permessi utente
- Protezione CSRF

## Performance
- Processamento asincrono per file grandi
- Importazione in batch per ottimizzare le query
- Caching dei dati di riferimento (insegnanti, classi, etc.)
- Indici appropriati per le query di validazione

## Testing
1. Unit test:
   - Validazione file
   - Parsing dati
   - Gestione errori

2. Integration test:
   - Flusso completo importazione
   - Rollback transazioni
   - Gestione concorrenza

3. Test casi limite:
   - File molto grandi
   - Dati malformati
   - Errori di rete

## Monitoraggio
- Logging delle importazioni
- Metriche di successo/fallimento
- Tempi di processamento
- Utilizzo memoria/CPU

## Future Espansioni
1. Template Excel scaricabile
2. Supporto altri formati (CSV, Google Sheets)
3. Importazione incrementale
4. Validazione avanzata dati
5. API per importazione programmatica