"""
Funzioni di utilità per calcoli vari nell'applicazione.
"""

from datetime import datetime, date, time

def calcola_cfu(ore, ore_per_cfu=6):
    """
    Calcola i CFU in base alle ore.
    
    Args:
        ore (float): Numero di ore
        ore_per_cfu (int, optional): Ore necessarie per 1 CFU. Default 6
        
    Returns:
        float: Numero di CFU calcolati
    """
    return round(ore / ore_per_cfu, 2) if ore else 0

def calcola_durata_e_cfu(orario_inizio, orario_fine, ore_per_cfu=4.5):
    """
    Calcola durata e CFU da orario inizio e fine.
    
    Args:
        orario_inizio (time): Orario di inizio
        orario_fine (time): Orario di fine
        ore_per_cfu (float, optional): Ore per CFU. Default 4.5
        
    Returns:
        tuple: (time, float) Durata come time e CFU come float
    """
    inizio = datetime.combine(date.today(), orario_inizio)
    fine = datetime.combine(date.today(), orario_fine)
    durata = fine - inizio
    ore = durata.total_seconds() / 3600
    cfu = calcola_cfu(ore, ore_per_cfu)
    ore_durata = int(durata.total_seconds() // 3600)
    minuti_durata = int((durata.total_seconds() % 3600) // 60)
    return time(hour=ore_durata, minute=minuti_durata), cfu

def calcola_totali_studente(id_studente):
    """
    Calcola i totali di ore e CFU per uno studente.
    
    Args:
        id_studente (int): ID dello studente
        
    Returns:
        dict: Dizionario con i totali calcolati
    """
    from app.models.student import (RegistroPresenzeTirocinioDiretto,
                                  RegistroPresenzeTirocinioIndiretto)
    
    tirocini_diretti = RegistroPresenzeTirocinioDiretto.query.filter_by(
        id_studente=id_studente).all()
    tirocini_indiretti = RegistroPresenzeTirocinioIndiretto.query.filter_by(
        id_studente=id_studente).all()
        
    return {
        'ore_tirocinio_diretto': sum(t.ore for t in tirocini_diretti),
        'ore_tirocinio_indiretto': sum(t.ore for t in tirocini_indiretti),
        'cfu_tirocinio_diretto': sum(t.cfu for t in tirocini_diretti if t.cfu),
        'cfu_tirocinio_indiretto': sum(t.cfu for t in tirocini_indiretti if t.cfu)
    }

def calcola_totali_professore(id_professore):
    """
    Calcola i totali delle lezioni per un professore.
    
    Args:
        id_professore (int): ID del professore
        
    Returns:
        dict: Dizionario con i totali calcolati
    """
    from app.models.course import Lezioni
    
    lezioni = Lezioni.query.filter_by(id_insegnante=id_professore).all()
    
    return {
        'numero_lezioni': len(lezioni),
        'ore_totali': sum(l.durata.hour + l.durata.minute/60 if l.durata else 0 
                         for l in lezioni),
        'cfu_totali': sum(float(l.cfu) if l.cfu else 0 for l in lezioni)
    }

def calcola_totali_tutor(id_tutor):
    """
    Calcola i totali per un tutor.
    
    Args:
        id_tutor (int): ID del tutor
        
    Returns:
        dict: Dizionario con i totali calcolati
    """
    from app.models.student import RegistroPresenzeTirocinioIndiretto
    
    tirocini = RegistroPresenzeTirocinioIndiretto.query.filter_by(
        id_tutor_coordinatore=id_tutor).all()
    studenti = set(t.id_studente for t in tirocini)
    
    return {
        'numero_studenti': len(studenti),
        'ore_totali': sum(t.ore for t in tirocini),
        'cfu_totali': sum(t.cfu for t in tirocini if t.cfu)
    } 