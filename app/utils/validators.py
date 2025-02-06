"""
Funzioni di validazione per i dati importati nell'applicazione.
"""

from datetime import datetime
import pandas as pd
from app.models.student import Studenti
from app.models.school import ScuoleAccreditate
from app.models.teacher import Insegnanti
from app.models.course import ClassiConcorso, Dipartimenti, Percorsi
from app.utils.calculations import calcola_cfu

def validate_excel_data(df):
    """
    Valida i dati di un file Excel per l'importazione delle lezioni.
    
    Args:
        df (pandas.DataFrame): DataFrame con i dati da validare
        
    Returns:
        tuple: (list, list) Lista delle lezioni valide e lista degli errori
    """
    errors = []
    required_columns = [
        'Nome Lezione', 'Data', 'Orario Inizio', 'Orario Fine', 'Insegnante'
    ]
    
    # Verifica colonne obbligatorie
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return [], [{'row': 0, 'message': f'Colonne mancanti: {", ".join(missing_columns)}'}]
    
    valid_lessons = []
    
    for idx, row in df.iterrows():
        row_number = idx + 2  # +2 perché Excel parte da 1 e ha l'header
        try:
            # Validazione base dei campi obbligatori
            if pd.isna(row['Nome Lezione']) or str(row['Nome Lezione']).strip() == '':
                errors.append({'row': row_number, 'message': 'Nome lezione mancante'})
                continue
                
            # Validazione data
            try:
                if isinstance(row['Data'], str):
                    data = datetime.strptime(row['Data'], '%d/%m/%Y').date()
                else:
                    data = row['Data'].date()
            except:
                errors.append({'row': row_number, 'message': 'Formato data non valido (GG/MM/AAAA)'})
                continue

            # Validazione orari
            try:
                if isinstance(row['Orario Inizio'], str):
                    orario_inizio = datetime.strptime(row['Orario Inizio'], '%H:%M').time()
                else:
                    orario_inizio = row['Orario Inizio'].time()
                    
                if isinstance(row['Orario Fine'], str):
                    orario_fine = datetime.strptime(row['Orario Fine'], '%H:%M').time()
                else:
                    orario_fine = row['Orario Fine'].time()
            except:
                errors.append({'row': row_number, 'message': 'Formato orario non valido (HH:MM)'})
                continue

            if orario_fine <= orario_inizio:
                errors.append({'row': row_number, 'message': 'Orario fine deve essere successivo a orario inizio'})
                continue

            # Validazione Insegnante
            try:
                nome_cognome = str(row['Insegnante']).strip().split(' ', 1)
                if len(nome_cognome) != 2:
                    errors.append({'row': row_number, 'message': 'Formato insegnante non valido (Nome Cognome)'})
                    continue
                nome, cognome = nome_cognome
                insegnante = Insegnanti.query.filter(
                    Insegnanti.nome.ilike(nome),
                    Insegnanti.cognome.ilike(cognome)
                ).first()
                if not insegnante:
                    errors.append({'row': row_number, 'message': f'Insegnante {nome} {cognome} non trovato'})
                    continue
                id_insegnante = insegnante.id_insegnante
            except:
                errors.append({'row': row_number, 'message': 'Errore nel formato dell\'insegnante'})
                continue

            # Validazione relazioni opzionali
            classi_ids = []
            if 'Classi di Concorso' in row and not pd.isna(row['Classi di Concorso']):
                try:
                    classi_codici = [c.strip() for c in str(row['Classi di Concorso']).split(',')]
                    for codice in classi_codici:
                        classe = ClassiConcorso.query.filter(ClassiConcorso.nome_classe == codice).first()
                        if not classe:
                            errors.append({'row': row_number, 'message': f'Classe di concorso {codice} non trovata'})
                            continue
                        classi_ids.append(classe.id_classe)
                except:
                    errors.append({'row': row_number, 'message': 'Errore nel formato delle classi di concorso'})
                    continue

            dipartimenti_ids = []
            if 'Dipartimenti' in row and not pd.isna(row['Dipartimenti']):
                try:
                    dipartimenti_nomi = [d.strip() for d in str(row['Dipartimenti']).split(',')]
                    for nome in dipartimenti_nomi:
                        dipartimento = Dipartimenti.query.filter(Dipartimenti.nome.ilike(nome)).first()
                        if not dipartimento:
                            errors.append({'row': row_number, 'message': f'Dipartimento {nome} non trovato'})
                            continue
                        dipartimenti_ids.append(dipartimento.id)
                except:
                    errors.append({'row': row_number, 'message': 'Errore nel formato dei dipartimenti'})
                    continue

            percorsi_ids = []
            if 'Percorsi' in row and not pd.isna(row['Percorsi']):
                try:
                    percorsi_nomi = [p.strip() for p in str(row['Percorsi']).split(',')]
                    for nome in percorsi_nomi:
                        percorso = Percorsi.query.filter(Percorsi.nome_percorso.ilike(nome)).first()
                        if not percorso:
                            errors.append({'row': row_number, 'message': f'Percorso {nome} non trovato'})
                            continue
                        percorsi_ids.append(percorso.id_percorso)
                except:
                    errors.append({'row': row_number, 'message': 'Errore nel formato dei percorsi'})
                    continue

            # Se arriviamo qui, la riga è valida
            valid_lessons.append({
                'nome_lezione': str(row['Nome Lezione']).strip(),
                'data': data,
                'orario_inizio': orario_inizio,
                'orario_fine': orario_fine,
                'id_insegnante': id_insegnante,
                'classi_ids': classi_ids,
                'dipartimenti_ids': dipartimenti_ids,
                'percorsi_ids': percorsi_ids
            })

        except Exception as e:
            errors.append({'row': row_number, 'message': f'Errore generico: {str(e)}'})
            continue

    return valid_lessons, errors

def validate_tirocinio_data(df, tipo='diretto'):
    """
    Valida i dati di un file Excel per l'importazione dei tirocini.
    
    Args:
        df (pandas.DataFrame): DataFrame con i dati da validare
        tipo (str): Tipo di tirocinio ('diretto' o 'indiretto')
        
    Returns:
        tuple: (list, list) Lista dei tirocini validi e lista degli errori
    """
    errors = []
    
    if tipo == 'diretto':
        required_columns = [
            'Studente', 'Scuola', 'Tutor Esterno', 'Data', 'Ore', 'Descrizione Attività'
        ]
    else:  # indiretto
        required_columns = [
            'Studente', 'Tutor Coordinatore', 'Data', 'Ore', 'Descrizione Attività'
        ]
    
    # Verifica colonne obbligatorie
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        return [], [{'row': 0, 'message': f'Colonne mancanti: {", ".join(missing_columns)}'}]
    
    valid_tirocini = []
    
    for idx, row in df.iterrows():
        row_number = idx + 2
        try:
            # Validazione campi comuni
            for col in required_columns:
                if pd.isna(row[col]) or str(row[col]).strip() == '':
                    errors.append({'row': row_number, 'message': f'Campo {col} mancante'})
                    continue

            # Validazione Studente
            try:
                nome_cognome = str(row['Studente']).strip().split(' ', 1)
                if len(nome_cognome) != 2:
                    errors.append({'row': row_number, 'message': 'Formato studente non valido (Nome Cognome)'})
                    continue
                nome, cognome = nome_cognome
                studente = Studenti.query.filter(
                    Studenti.nome.ilike(nome),
                    Studenti.cognome.ilike(cognome)
                ).first()
                if not studente:
                    errors.append({'row': row_number, 'message': f'Studente {nome} {cognome} non trovato'})
                    continue
                id_studente = studente.id_studente
            except:
                errors.append({'row': row_number, 'message': 'Errore nel formato dello studente'})
                continue

            # Validazione specifica per tipo
            if tipo == 'diretto':
                try:
                    nome_scuola = str(row['Scuola']).strip()
                    scuola = ScuoleAccreditate.query.filter(
                        ScuoleAccreditate.nome_scuola.ilike(nome_scuola)
                    ).first()
                    if not scuola:
                        errors.append({'row': row_number, 'message': f'Scuola {nome_scuola} non trovata'})
                        continue
                    id_scuola = scuola.id_scuola
                except:
                    errors.append({'row': row_number, 'message': 'Errore nel formato della scuola'})
                    continue

            # Validazioni comuni
            try:
                if isinstance(row['Data'], str):
                    data = datetime.strptime(row['Data'], '%d/%m/%Y').date()
                else:
                    data = row['Data'].date()
            except:
                errors.append({'row': row_number, 'message': 'Formato data non valido (GG/MM/AAAA)'})
                continue

            try:
                ore = float(row['Ore'])
                if ore <= 0:
                    errors.append({'row': row_number, 'message': 'Le ore devono essere maggiori di 0'})
                    continue
            except:
                errors.append({'row': row_number, 'message': 'Formato ore non valido'})
                continue

            # Calcolo CFU
            cfu = calcola_cfu(ore)

            # Validazione descrizione attività
            descrizione = str(row['Descrizione Attività']).strip()
            if len(descrizione) < 10:
                errors.append({'row': row_number, 'message': 'La descrizione attività deve essere più dettagliata'})
                continue

            # Costruzione del dizionario dei dati validi
            tirocinio_data = {
                'id_studente': id_studente,
                'data': data,
                'ore': ore,
                'cfu': cfu,
                'descrizione_attivita': descrizione
            }

            if tipo == 'diretto':
                tirocinio_data.update({
                    'id_scuola': id_scuola,
                    'tutor_esterno': str(row['Tutor Esterno']).strip()
                })
            else:
                # Aggiungi dati specifici per tirocinio indiretto se necessario
                pass

            valid_tirocini.append(tirocinio_data)

        except Exception as e:
            errors.append({'row': row_number, 'message': f'Errore generico: {str(e)}'})
            continue

    return valid_tirocini, errors 