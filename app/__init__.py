from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os

# Carica le variabili d'ambiente dal file .env
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Usa la configurazione di sviluppo
    app.config.from_object('config.DevelopmentConfig')
    
    # Configurazione del database MySQL usando le variabili d'ambiente
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Upload folder
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'xlsx', 'xls'}
    
    # Inizializzazione estensioni
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Effettua il login per accedere a questa pagina.'
    login_manager.login_message_category = 'warning'
    
    # Registra i blueprints
    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.student import student_bp
    from .routes.admin import admin_bp
    from .routes.teacher import teacher_bp
    from .routes.tutor import tutor_bp
    from .routes.attendance import attendance_bp
    from .routes.school import school_bp
    from .routes.segreteria import segreteria_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(teacher_bp, url_prefix='/teacher')
    app.register_blueprint(tutor_bp, url_prefix='/tutor')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(school_bp, url_prefix='/school')
    app.register_blueprint(segreteria_bp, url_prefix='/segreteria')
    
    @login_manager.user_loader
    def load_user(id):
        from app.models.user import User
        return User.query.get(int(id))
    
    # Error handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('error/403.html'), 403
        
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error/404.html'), 404
        
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('error/500.html'), 500
    
    return app