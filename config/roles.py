"""
Definizione dei ruoli utente per l'applicazione PEF-RM3.
Centralizza tutte le definizioni dei ruoli in un unico file.
"""

# Definizione dei ruoli dell'applicazione
ROLE_ADMIN = 'admin'
ROLE_SEGRETERIA = 'segreteria'
ROLE_PROFESSORE = 'professore'
ROLE_STUDENTE = 'studente'
ROLE_TUTOR_COORDINATORE = 'tutor_coordinatore'
ROLE_TUTOR_COLLABORATORE = 'tutor_collaboratore'

# Lista di tutti i ruoli disponibili
ALL_ROLES = [
    ROLE_ADMIN,
    ROLE_STUDENTE,
    ROLE_PROFESSORE,
    ROLE_SEGRETERIA,
    ROLE_TUTOR_COLLABORATORE,
    ROLE_TUTOR_COORDINATORE
]

# Mapping dei ruoli con le loro descrizioni
ROLE_DESCRIPTIONS = {
    ROLE_ADMIN: 'Amministratore',
    ROLE_STUDENTE: 'Studente',
    ROLE_PROFESSORE: 'Professore',
    ROLE_SEGRETERIA: 'Segreteria',
    ROLE_TUTOR_COLLABORATORE: 'Tutor Collaboratore',
    ROLE_TUTOR_COORDINATORE: 'Tutor Coordinatore'
}

# Permessi per ruolo
ROLE_PERMISSIONS = {
    ROLE_ADMIN: ['admin', 'segreteria', 'professore', 'studente', 'tutor'],
    ROLE_SEGRETERIA: ['segreteria', 'professore', 'studente', 'tutor'],
    ROLE_PROFESSORE: ['professore'],
    ROLE_STUDENTE: ['studente'],
    ROLE_TUTOR_COORDINATORE: ['tutor'],
    ROLE_TUTOR_COLLABORATORE: ['tutor']
}

def get_role_description(role):
    """Restituisce la descrizione di un ruolo."""
    return ROLE_DESCRIPTIONS.get(role, 'Ruolo sconosciuto')

def is_valid_role(role):
    """Verifica se un ruolo è valido."""
    return role in ALL_ROLES