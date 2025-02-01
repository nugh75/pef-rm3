"""
Definizione dei ruoli utente per l'applicazione PEF-RM3.
Centralizza tutte le definizioni dei ruoli in un unico file.
"""

# Ruoli utente
ROLE_ADMIN = 'admin'
ROLE_STUDENTE = 'studente'
ROLE_PROFESSORE = 'professore'
ROLE_SEGRETERIA = 'segreteria'
ROLE_TUTOR_COLLABORATORE = 'tutor_collaboratore'
ROLE_TUTOR_COORDINATORE = 'tutor_coordinatore'

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

def get_role_description(role):
    """Restituisce la descrizione di un ruolo."""
    return ROLE_DESCRIPTIONS.get(role, 'Ruolo sconosciuto')

def is_valid_role(role):
    """Verifica se un ruolo è valido."""
    return role in ALL_ROLES