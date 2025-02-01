"""
Package di configurazione per l'applicazione PEF-RM3.
Centralizza tutte le configurazioni dell'applicazione in un unico posto.
"""

from .config import Config
from .roles import *
from .database import Database
from .logging import configure_logging

__all__ = ['Config', 'Database', 'configure_logging']