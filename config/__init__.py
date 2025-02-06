"""
Package di configurazione per l'applicazione PEF-RM3.
Centralizza tutte le configurazioni dell'applicazione in un unico posto.
"""

from .roles import *
from .database import Database
from .logging import configure_logging
from .base import Config, DevelopmentConfig, ProductionConfig, TestingConfig

__all__ = [
    'Config', 
    'Database', 
    'configure_logging',
    'DevelopmentConfig',
    'ProductionConfig',
    'TestingConfig'
]

# Package per la configurazione dell'applicazione