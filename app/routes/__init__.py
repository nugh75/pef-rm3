from flask import Blueprint

# Importazione dei blueprints
from .main import main_bp
from .auth import auth_bp
from .admin import admin_bp
from .student import student_bp
from .teacher import teacher_bp
from .tutor import tutor_bp
from .attendance import attendance_bp
from .school import school_bp

# DEBUG: Stampa di debug
print("\nImportazione routes completata")

__all__ = [
    'main_bp',
    'auth_bp', 
    'admin_bp',
    'student_bp',
    'teacher_bp',
    'tutor_bp',
    'attendance_bp',
    'school_bp'
] 