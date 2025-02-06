"""
Package per le utility dell'applicazione.
Contiene funzioni e decoratori di utilità generale.
"""

from .decorators import role_required
from .calculations import (calcola_cfu, calcola_durata_e_cfu, 
                         calcola_totali_studente, calcola_totali_professore,
                         calcola_totali_tutor)
from .validators import validate_excel_data, validate_tirocinio_data

__all__ = [
    'role_required',
    'calcola_cfu',
    'calcola_durata_e_cfu',
    'calcola_totali_studente',
    'calcola_totali_professore',
    'calcola_totali_tutor',
    'validate_excel_data',
    'validate_tirocinio_data'
] 