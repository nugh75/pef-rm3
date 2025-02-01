from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from sqlalchemy import or_

from config.config import config
from config.roles import *
from flask_wtf.csrf import CSRFProtect

# Inizializza l'applicazione
app = Flask(__name__)

# Configura l'applicazione
app_config = config['development']
app_config.init_app(app)

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- Modelli Database ---
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    ruolo = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RegistroPresenzeTirocinioDiretto(db.Model):
    __tablename__ = 'RegistroPresenzeTirocinioDiretto'
    id_tirocinio_diretto = db.Column(db.Integer, primary_key=True)
    id_studente = db.Column(db.Integer, db.ForeignKey('Studenti.id_studente'), nullable=False)
    id_scuola = db.Column(db.Integer, db.ForeignKey('ScuoleAccreditate.id_scuola'), nullable=False)
    tutor_esterno = db.Column(db.String(100))
    data = db.Column(db.Date, nullable=False)
    ore = db.Column(db.Float, nullable=False)
    cfu = db.Column(db.Float)
    descrizione_attivita = db.Column(db.Text)

class RegistroPresenzeTirocinioIndiretto(db.Model):
    __tablename__ = 'RegistroPresenzeTirocinioIndiretto'
    id_tirocinio_indiretto = db.Column(db.Integer, primary_key=True)
    id_studente = db.Column(db.Integer, db.ForeignKey('Studenti.id_studente'), nullable=False)
    id_tutor_coordinatore = db.Column(db.Integer, db.ForeignKey('TutorCoordinatori.id_tutor_coordinatore'))
    data = db.Column(db.Date, nullable=False)
    ore = db.Column(db.Float, nullable=False)
    cfu = db.Column(db.Float)
    descrizione_attivita = db.Column(db.Text)

class TutorCoordinatori(db.Model):
    __tablename__ = 'TutorCoordinatori'
    id_tutor_coordinatore = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    dipartimento_id = db.Column(db.Integer, db.ForeignKey('Dipartimenti.id'), nullable=True)
    dipartimento = db.relationship('Dipartimenti', backref='tutor_coordinatori', lazy=True)

class TutorCollaboratori(db.Model):
    __tablename__ = 'TutorCollaboratori'
    id_tutor_collaboratore = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    dipartimento_id = db.Column(db.Integer, db.ForeignKey('Dipartimenti.id'), nullable=False)
    dipartimento = db.relationship('Dipartimenti', backref='tutor_collaboratori', lazy=True)

class SSD(db.Model):
    __tablename__ = 'SSD'
    id_ssd = db.Column(db.Integer, primary_key=True)
    nome_ssd = db.Column(db.String(255), nullable=False)
    insegnanti = db.relationship('Insegnanti', backref='ssd', lazy=True)

class Insegnanti(db.Model):
    __tablename__ = 'Insegnanti'
    id_insegnante = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cognome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    telefono = db.Column(db.String(15))
    id_dipartimento = db.Column(db.Integer, db.ForeignKey('Dipartimenti.id'))
    id_ssd = db.Column(db.Integer, db.ForeignKey('SSD.id_ssd'))
    dipartimento = db.relationship('Dipartimenti', backref='insegnanti', lazy=True)
    lezioni = db.relationship('Lezioni', backref='insegnante', lazy=True)

class Dipartimenti(db.Model):
    __tablename__ = 'Dipartimenti'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)

class Percorsi(db.Model):
    __tablename__ = 'Percorsi'
    id_percorso = db.Column(db.Integer, primary_key=True)
    nome_percorso = db.Column(db.String(255), nullable=False)

class Lezioni(db.Model):
    __tablename__ = 'Lezioni'
    id_lezione = db.Column(db.Integer, primary_key=True)
    nome_lezione = db.Column(db.String(255), nullable=False)
    data = db.Column(db.Date, nullable=False)
    orario_inizio = db.Column(db.Time, nullable=False)
    orario_fine = db.Column(db.Time, nullable=False)
    durata = db.Column(db.Time, nullable=True)
    cfu = db.Column(db.Numeric(4,2), nullable=True)
    id_insegnante = db.Column(db.Integer, db.ForeignKey('Insegnanti.id_insegnante'), nullable=True)

    classi_concorso = db.relationship('ClassiConcorso',
                                    secondary='Lezioni_ClassiConcorso',
                                    backref=db.backref('lezioni_correlate', lazy='dynamic'))
    dipartimenti = db.relationship('Dipartimenti',
                                 secondary='Lezioni_Dipartimenti',
                                 backref=db.backref('lezioni_correlate', lazy='dynamic'))
    percorsi = db.relationship('Percorsi',
                             secondary='Lezioni_Percorsi',
                             backref=db.backref('lezioni_correlate', lazy='dynamic'))

class LezioniClassiConcorso(db.Model):
    __tablename__ = 'Lezioni_ClassiConcorso'
    id_lezione = db.Column(db.Integer, db.ForeignKey('Lezioni.id_lezione'), primary_key=True)
    id_classe = db.Column(db.Integer, db.ForeignKey('Classi di concorso.id_classe'), primary_key=True)

class LezioniDipartimenti(db.Model):
    __tablename__ = 'Lezioni_Dipartimenti'
    id_lezione = db.Column(db.Integer, db.ForeignKey('Lezioni.id_lezione'), primary_key=True)
    id_dipartimento = db.Column(db.Integer, db.ForeignKey('Dipartimenti.id'), primary_key=True)

class LezioniPercorsi(db.Model):
    __tablename__ = 'Lezioni_Percorsi'
    id_lezione = db.Column(db.Integer, db.ForeignKey('Lezioni.id_lezione'), primary_key=True)
    id_percorso = db.Column(db.Integer, db.ForeignKey('Percorsi.id_percorso'), primary_key=True)

class ClassiConcorso(db.Model):
    __tablename__ = 'Classi di concorso'
    id_classe = db.Column(db.Integer, primary_key=True)
    dipartimento = db.Column(db.Integer, db.ForeignKey('Dipartimenti.id'), nullable=False)
    nome_classe = db.Column(db.String(4), nullable=False)
    denominazione_classe = db.Column(db.String(255), nullable=False)

class ScuoleAccreditate(db.Model):
    __tablename__ = 'ScuoleAccreditate'
    id_scuola = db.Column(db.Integer, primary_key=True)
    nome_scuola = db.Column(db.String(150), nullable=False)
    indirizzo = db.Column(db.String(255))
    referente = db.Column(db.String(100))
    email_referente = db.Column(db.String(150))

class Studenti(db.Model):
    __tablename__ = 'Studenti'
    id_studente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    telefono = db.Column(db.String(15))
    classe_id = db.Column(db.Integer, db.ForeignKey('Classi di concorso.id_classe'), nullable=False)
    percorso_id = db.Column(db.Integer, db.ForeignKey('Percorsi.id_percorso'), nullable=False)
    scuola_assegnata_id = db.Column(db.Integer, db.ForeignKey('ScuoleAccreditate.id_scuola'))
    tutor_esterno = db.Column(db.String(150))

class DeleteTutorCollaboratoreForm(FlaskForm):
    pass

class LoginForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])


# --- Funzioni Utilità ---
def calcola_cfu(ore, ore_per_cfu=6):
    """Calcola i CFU in base alle ore."""
    return round(ore / ore_per_cfu, 2) if ore else 0

def calcola_durata_e_cfu(orario_inizio, orario_fine):
    """Calcola durata e CFU da orario inizio e fine"""
    inizio = datetime.combine(date.today(), orario_inizio)
    fine = datetime.combine(date.today(), orario_fine)
    durata = fine - inizio
    ore = durata.total_seconds() / 3600
    cfu = calcola_cfu(ore, ore_per_cfu=4.5) # CFU per lezione
    ore_durata = int(durata.total_seconds() // 3600)
    minuti_durata = int((durata.total_seconds() % 3600) // 60)
    durata_time = time(hour=ore_durata, minute=minuti_durata)
    return durata_time, cfu

def calcola_totali_studente(id_studente):
    tirocini_diretti = RegistroPresenzeTirocinioDiretto.query.filter_by(id_studente=id_studente).all()
    tirocini_indiretti = RegistroPresenzeTirocinioIndiretto.query.filter_by(id_studente=id_studente).all()
    ore_dirette = sum(t.ore for t in tirocini_diretti)
    ore_indirette = sum(t.ore for t in tirocini_indiretti)
    cfu_diretti = sum(t.cfu for t in tirocini_diretti)
    cfu_indiretti = sum(t.cfu for t in tirocini_indiretti)
    return {
        'ore_tirocinio_diretto': ore_dirette,
        'ore_tirocinio_indiretto': ore_indirette,
        'cfu_tirocinio_diretto': cfu_diretti,
        'cfu_tirocinio_indiretto': cfu_indiretti
    }

def calcola_totali_professore(id_professore):
    lezioni = Lezioni.query.filter_by(id_insegnante=id_professore).all()
    numero_lezioni = len(lezioni)
    ore_totali = sum(l.durata.hour + l.durata.minute/60 if l.durata else 0 for l in lezioni)
    cfu_totali = sum(float(l.cfu) if l.cfu else 0 for l in lezioni)
    return {
        'numero_lezioni': numero_lezioni,
        'ore_totali': ore_totali,
        'cfu_totali': cfu_totali
    }

def calcola_totali_tutor(id_tutor):
    tirocini = RegistroPresenzeTirocinioIndiretto.query.filter_by(id_tutor_coordinatore=id_tutor).all()
    studenti = set(t.id_studente for t in tirocini)
    ore_totali = sum(t.ore for t in tirocini)
    cfu_totali = sum(t.cfu for t in tirocini)
    return {
        'numero_studenti': len(studenti),
        'ore_totali': ore_totali,
        'cfu_totali': cfu_totali
    }

# --- Flask-Login ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.ruolo not in roles:
                flash('Non hai i permessi necessari per accedere a questa pagina.', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# --- Route ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user)
            flash('Login effettuato con successo!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Email o password non validi.', 'error')
    return render_template('main/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Logout effettuato con successo', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_ADMIN)
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        nome = request.form['nome']
        cognome = request.form['cognome']
        ruolo = request.form['ruolo']
        if User.query.filter_by(email=email).first():
            flash('Email già registrata.', 'error')
            return redirect(url_for('register'))
        user = User(email=email, nome=nome, cognome=cognome, ruolo=ruolo, is_active=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Utente registrato con successo!', 'success')
        return redirect(url_for('admin_users'))
    return render_template('register.html')

@app.route('/admin/users')
@login_required
@role_required(ROLE_ADMIN)
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/activate/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN)
def activate_user(id):
    user = User.query.get_or_404(id)
    user.is_active = True
    db.session.commit()
    flash('Utente attivato con successo!', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/deactivate/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN)
def deactivate_user(id):
    user = User.query.get_or_404(id)
    if user.id != current_user.id:
        user.is_active = False
        db.session.commit()
        flash('Utente disattivato con successo!', 'success')
    else:
        flash('Non puoi disattivare il tuo account!', 'error')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/delete/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN)
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id != current_user.id:
        db.session.delete(user)
        db.session.commit()
        flash('Utente eliminato con successo!', 'success')
    else:
        flash('Non puoi eliminare il tuo account!', 'error')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_ADMIN)
def edit_user(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        if user.id == current_user.id and request.form['is_active'] == '0':
            flash('Non puoi disattivare il tuo account!', 'error')
            return redirect(url_for('edit_user', id=id))
        user.email = request.form['email']
        user.nome = request.form['nome']
        user.cognome = request.form['cognome']
        user.ruolo = request.form['ruolo']
        user.is_active = bool(int(request.form['is_active']))
        if request.form['password']:
            user.set_password(request.form['password'])
        db.session.commit()
        flash('Utente aggiornato con successo!', 'success')
        return redirect(url_for('admin_users'))
    return render_template('edit_user.html', user=user)

@app.route('/segreteria')
@login_required
@role_required(ROLE_SEGRETERIA)
def segreteria():
    return render_template('main/segreterie.html')

@app.route('/insegnanti')
@login_required
@role_required(ROLE_SEGRETERIA)
def insegnanti():
    insegnanti_list = Insegnanti.query.options(db.joinedload(Insegnanti.dipartimento), db.joinedload(Insegnanti.ssd)).all()
    return render_template('tab_insegnanti.html', insegnanti=insegnanti_list)

@app.route('/add_insegnante', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def add_insegnante():
    dipartimenti = Dipartimenti.query.all()
    ssd_list = SSD.query.all()
    if request.method == 'POST':
        nuovo_insegnante = Insegnanti(nome=request.form['nome'], cognome=request.form['cognome'], email=request.form['email'], telefono=request.form['telefono'], id_dipartimento=request.form['dipartimento'], id_ssd=request.form['ssd'])
        db.session.add(nuovo_insegnante)
        db.session.commit()
        flash('Insegnante aggiunto con successo!', 'success')
        return redirect(url_for('insegnanti'))
    return render_template('add_insegnante.html', dipartimenti=dipartimenti, ssd_list=ssd_list)

@app.route('/edit_insegnante/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def edit_insegnante(id):
    insegnante = Insegnanti.query.get_or_404(id)
    dipartimenti = Dipartimenti.query.all()
    ssd_list = SSD.query.all()
    if request.method == 'POST':
        insegnante.nome = request.form['nome']
        insegnante.cognome = request.form['cognome']
        insegnante.email = request.form['email']
        insegnante.telefono = request.form['telefono']
        insegnante.id_dipartimento = request.form['dipartimento']
        insegnante.id_ssd = request.form['ssd']
        db.session.commit()
        flash('Insegnante aggiornato con successo!', 'success')
        return redirect(url_for('insegnanti'))
    return render_template('edit_insegnante.html', insegnante=insegnante, dipartimenti=dipartimenti, ssd_list=ssd_list)

@app.route('/delete_insegnante/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def delete_insegnante(id):
    insegnante = Insegnanti.query.get_or_404(id)
    db.session.delete(insegnante)
    db.session.commit()
    flash('Insegnante eliminato con successo!', 'success')
    return redirect(url_for('insegnanti'))

# @app.route('/scuole_accreditate')
# @login_required
# @role_required(ROLE_SEGRETERIA)
# def scuole_accreditate():
#     scuole = ScuoleAccreditate.query.all()
#     return render_template('tab_scuole.html', scuole=scuole)

@app.route('/scuole_accreditate/add', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def add_scuola_accreditata():
    if request.method == 'POST':
        nuova_scuola = ScuoleAccreditate(nome_scuola=request.form['nome_scuola'], indirizzo=request.form['indirizzo'], referente=request.form['referente'], email_referente=request.form['email_referente'])
        db.session.add(nuova_scuola)
        db.session.commit()
        flash('Scuola accreditata aggiunta con successo!', 'success')
        return redirect(url_for('scuole_accreditate'))
    return render_template('add_scuola.html')

@app.route('/scuole_accreditate')
@login_required
@role_required(ROLE_SEGRETERIA)
def scuole_accreditate():
    scuole = ScuoleAccreditate.query.all()
    print(f"DEBUG: scuole list: {scuole}") # Print the entire list
    if scuole:
        print(f"DEBUG: Type of first item in scuole list: {type(scuole[0])}") # Print type of first item
    else:
        print("DEBUG: scuole list is EMPTY") # Indicate if list is empty
    return render_template('tab_scuole.html', scuole=scuole)

@app.route('/scuole_accreditate/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def edit_scuola_accreditata(id):
    scuola = ScuoleAccreditate.query.get_or_404(id)
    if request.method == 'POST':
        scuola.nome_scuola = request.form['nome_scuola']
        scuola.indirizzo = request.form['indirizzo']
        scuola.referente = request.form['referente']
        scuola.email_referente = request.form['email_referente']
        db.session.commit()
        flash('Scuola aggiornata con successo!', 'success')
        return redirect(url_for('scuole_accreditate'))
    return render_template('edit_scuola.html', scuola=scuola)

@app.route('/scuole_accreditate/delete/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def delete_scuola_accreditata(id):
    scuola = ScuoleAccreditate.query.get_or_404(id)
    db.session.delete(scuola)
    db.session.commit()
    flash('Scuola accreditata eliminata con successo!', 'success')
    return redirect(url_for('scuole_accreditate'))

@app.route('/tutor_coordinatori')
@login_required
@role_required(ROLE_SEGRETERIA)
def tutor_coordinatori():
    tutor = TutorCoordinatori.query.options(db.joinedload(TutorCoordinatori.dipartimento)).all()
    return render_template('tutor_coordinatori/tab_tutor_coordinatori.html', tutor=tutor)

@app.route('/tutor_coordinatori/add', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def add_tutor():
    dipartimenti = Dipartimenti.query.all()
    if request.method == 'POST':
        nuovo_tutor = TutorCoordinatori(nome=request.form['nome'], cognome=request.form['cognome'], email=request.form['email'], telefono=request.form['telefono'], dipartimento_id=request.form['dipartimento'])
        db.session.add(nuovo_tutor)
        db.session.commit()
        flash('Tutor coordinatore aggiunto con successo!', 'success')
        return redirect(url_for('tutor_coordinatori'))
    return render_template('add_tutor.html', dipartimenti=dipartimenti)

@app.route('/tutor_coordinatori/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def edit_tutor_coordinatore(id):
    tutor = TutorCoordinatori.query.get_or_404(id)
    dipartimenti = Dipartimenti.query.all()
    if request.method == 'POST':
        tutor.nome = request.form['nome']
        tutor.cognome = request.form['cognome']
        tutor.email = request.form['email']
        tutor.telefono = request.form['telefono']
        tutor.dipartimento_id = request.form['dipartimento']
        db.session.commit()
        flash('Tutor coordinatore aggiornato con successo!', 'success')
        return redirect(url_for('tutor_coordinatori'))
    return render_template('tutor_coordinatori/edit_tutor_coordinatore.html', tutor=tutor, dipartimenti=dipartimenti)

@app.route('/tutor_coordinatori/delete/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def delete_tutor_coordinatore(id):
    tutor = TutorCoordinatori.query.get_or_404(id)
    db.session.delete(tutor)
    db.session.commit()
    flash('Tutor coordinatore eliminato con successo!', 'success')
    return redirect(url_for('tutor_coordinatori'))

@app.route('/tutor_collaboratori')
@login_required
@role_required(ROLE_SEGRETERIA)
def tutor_collaboratori():
    tutor = TutorCollaboratori.query.options(db.joinedload(TutorCollaboratori.dipartimento)).all()
    delete_form = DeleteTutorCollaboratoreForm()
    return render_template('tutor_collaboratori/tab_tutor_collaboratori.html', tutor=tutor, form=delete_form)

@app.route('/tutor_collaboratori/add', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def add_tutor_collaboratore():
    dipartimenti = Dipartimenti.query.all()
    if request.method == 'POST':
        nuovo_tutor = TutorCollaboratori(nome=request.form['nome'], cognome=request.form['cognome'], email=request.form['email'], telefono=request.form['telefono'], dipartimento_id=request.form['dipartimento'])
        db.session.add(nuovo_tutor)
        db.session.commit()
        flash('Tutor collaboratore aggiunto con successo!', 'success')
        return redirect(url_for('tutor_collaboratori'))
    return render_template('tutor_collaboratori/add_tutor_collaboratore.html', dipartimenti=dipartimenti)

@app.route('/tutor_collaboratori/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def edit_tutor_collaboratore(id):
    tutor = TutorCollaboratori.query.get_or_404(id)
    dipartimenti = Dipartimenti.query.all()
    if request.method == 'POST':
        tutor.nome = request.form['nome']
        tutor.cognome = request.form['cognome']
        tutor.email = request.form['email']
        tutor.telefono = request.form['telefono']
        tutor.dipartimento_id = request.form['dipartimento']
        db.session.commit()
        flash('Tutor collaboratore aggiornato con successo!', 'success')
        return redirect(url_for('tutor_collaboratori'))
    return render_template('tutor_collaboratori/edit_tutor_collaboratore.html', tutor=tutor, dipartimenti=dipartimenti)

@app.route('/tutor_collaboratori/delete/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def delete_tutor_collaboratore(id):
    tutor = TutorCollaboratori.query.get_or_404(id)
    db.session.delete(tutor)
    db.session.commit()
    flash('Tutor collaboratore eliminato con successo!', 'success')
    return redirect(url_for('tutor_collaboratori'))

@app.route('/registro_tirocinio_indiretto')
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_STUDENTE)
def registro_tirocinio_indiretto():
    query = db.session.query(
        RegistroPresenzeTirocinioIndiretto,
        Studenti.nome.label('studente_nome'),
        Studenti.cognome.label('studente_cognome'),
        TutorCoordinatori.nome.label('tutor_nome'),
        TutorCoordinatori.cognome.label('tutor_cognome')
    ).join(Studenti, RegistroPresenzeTirocinioIndiretto.id_studente == Studenti.id_studente) \
     .outerjoin(TutorCoordinatori, RegistroPresenzeTirocinioIndiretto.id_tutor_coordinatore == TutorCoordinatori.id_tutor_coordinatore)

    studente = request.args.get('studente', '').strip()
    tutor = request.args.get('tutor', '').strip()

    if studente:
        for parte in studente.split():
            query = query.filter(or_(
                Studenti.nome.ilike(f'%{parte}%'),
                Studenti.cognome.ilike(f'%{parte}%')
            ))

    if tutor:
        for parte in tutor.split():
            query = query.filter(or_(
                TutorCoordinatori.nome.ilike(f'%{parte}%'),
                TutorCoordinatori.cognome.ilike(f'%{parte}%')
            ))
    tirocini = query.all()
    cfu_sum = sum(t[0].cfu for t in tirocini if t[0].cfu)
    return render_template('tab_tirocinio_indiretto.html', tirocini=tirocini, studente=studente, tutor=tutor, cfu_sum=cfu_sum)

@app.route('/registro_tirocinio_indiretto/add', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_STUDENTE)
def add_tirocinio_indiretto():
    studenti = Studenti.query.all()
    tutor_coordinatori = TutorCoordinatori.query.all()
    if request.method == 'POST':
        ore = float(request.form['ore'])
        cfu = calcola_cfu(ore)
        nuovo_tirocinio = RegistroPresenzeTirocinioIndiretto(id_studente=request.form['id_studente'], id_tutor_coordinatore=request.form['id_tutor_coordinatore'], data=datetime.strptime(request.form['data'], '%Y-%m-%d').date(), ore=ore, cfu=cfu, descrizione_attivita=request.form['descrizione_attivita'])
        db.session.add(nuovo_tirocinio)
        db.session.commit()
        flash('Tirocinio indiretto aggiunto con successo!', 'success')
        return redirect(url_for('registro_tirocinio_indiretto'))
    return render_template('add_tirocinio_indiretto.html', studenti=studenti, tutor_coordinatori=tutor_coordinatori)

@app.route('/registro_tirocinio_indiretto/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_STUDENTE)
def edit_tirocinio_indiretto(id):
    tirocinio = RegistroPresenzeTirocinioIndiretto.query.get_or_404(id)
    studenti = Studenti.query.all()
    tutor_coordinatori = TutorCoordinatori.query.all()
    if request.method == 'POST':
        tirocinio.id_studente = request.form['id_studente']
        tirocinio.id_tutor_coordinatore = request.form['id_tutor_coordinatore']
        tirocinio.data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        tirocinio.ore = float(request.form['ore'])
        tirocinio.cfu = calcola_cfu(tirocinio.ore)
        tirocinio.descrizione_attivita = request.form['descrizione_attivita']
        db.session.commit()
        flash('Tirocinio indiretto aggiornato con successo!', 'success')
        return redirect(url_for('registro_tirocinio_indiretto'))
    return render_template('edit_tirocinio_indiretto.html', tirocinio=tirocinio, studenti=studenti, tutor_coordinatori=tutor_coordinatori)

@app.route('/registro_tirocinio_indiretto/delete/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def delete_tirocinio_indiretto(id):
    tirocinio = RegistroPresenzeTirocinioIndiretto.query.get_or_404(id)
    db.session.delete(tirocinio)
    db.session.commit()
    flash('Tirocinio indiretto eliminato con successo!', 'success')
    return redirect(url_for('registro_tirocinio_indiretto'))

@app.route('/registro_tirocinio_diretto')
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_STUDENTE)
def registro_tirocinio_diretto():
    query = db.session.query(
        RegistroPresenzeTirocinioDiretto,
        Studenti.nome.label('studente_nome'),
        Studenti.cognome.label('studente_cognome'),
        ScuoleAccreditate.nome_scuola.label('scuola_nome')
    ).join(Studenti, RegistroPresenzeTirocinioDiretto.id_studente == Studenti.id_studente) \
     .join(ScuoleAccreditate, RegistroPresenzeTirocinioDiretto.id_scuola == ScuoleAccreditate.id_scuola)

    studente = request.args.get('studente', '').strip()
    scuola = request.args.get('scuola', '').strip()

    if studente:
        for parte in studente.split():
            query = query.filter(or_(
                Studenti.nome.ilike(f'%{parte}%'),
                Studenti.cognome.ilike(f'%{parte}%')
            ))

    if scuola:
        for parte in scuola.split():
            query = query.filter(or_(
                ScuoleAccreditate.nome_scuola.ilike(f'%{parte}%')
            ))

    tirocini = query.all()
    cfu_sum = sum(t[0].cfu for t in tirocini if t[0].cfu)
    return render_template('tab_tirocinio_diretto.html', tirocini=tirocini, studente=studente, scuola=scuola, cfu_sum=cfu_sum)

@app.route('/registro_tirocinio_diretto/add', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_STUDENTE)
def add_tirocinio_diretto():
    studenti = Studenti.query.order_by(Studenti.cognome).all()
    scuole = ScuoleAccreditate.query.order_by(ScuoleAccreditate.nome_scuola).all()
    if request.method == 'POST':
        try:
            ore = float(request.form['ore'])
            cfu = calcola_cfu(ore)
            nuovo_tirocinio = RegistroPresenzeTirocinioDiretto(id_studente=request.form['id_studente'], id_scuola=request.form['id_scuola'], tutor_esterno=request.form.get('tutor_esterno', ''), data=datetime.strptime(request.form['data'], '%Y-%m-%d').date(), ore=ore, cfu=cfu, descrizione_attivita=request.form['descrizione_attivita'])
            db.session.add(nuovo_tirocinio)
            db.session.commit()
            flash('Tirocinio diretto aggiunto con successo!', 'success')
            return redirect(url_for('registro_tirocinio_diretto'))
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiunta del tirocinio diretto: {str(e)}', 'error')
    return render_template('add_tirocinio_diretto.html', studenti=studenti, scuole=scuole)

@app.route('/registro_tirocinio_diretto/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_STUDENTE)
def edit_tirocinio_diretto(id):
    tirocinio = RegistroPresenzeTirocinioDiretto.query.get_or_404(id)
    studenti = Studenti.query.all()
    scuole = ScuoleAccreditate.query.all()
    if request.method == 'POST':
        tirocinio.id_studente = request.form['id_studente']
        tirocinio.id_scuola = request.form['id_scuola']
        tirocinio.tutor_esterno = request.form['tutor_esterno']
        tirocinio.data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
        tirocinio.ore = float(request.form['ore'])
        tirocinio.cfu = calcola_cfu(tirocinio.ore)
        tirocinio.descrizione_attivita = request.form['descrizione_attivita']
        db.session.commit()
        flash('Tirocinio diretto aggiornato con successo!', 'success')
        return redirect(url_for('registro_tirocinio_diretto'))
    return render_template('edit_tirocinio_diretto.html', tirocinio=tirocinio, studenti=studenti, scuole=scuole)

@app.route('/registro_tirocinio_diretto/delete/<int:id>', methods=['POST'])
@login_required
@role_required(ROLE_SEGRETERIA)
def delete_tirocinio_diretto(id):
    tirocinio = RegistroPresenzeTirocinioDiretto.query.get_or_404(id)
    db.session.delete(tirocinio)
    db.session.commit()
    flash('Tirocinio diretto eliminato con successo!', 'success')
    return redirect(url_for('registro_tirocinio_diretto'))

@app.route('/lezioni')
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_PROFESSORE)
def lezioni():
    try:
        query = Lezioni.query.join(Lezioni.insegnante)
        if request.args.get('nome'):
            query = query.filter(Lezioni.nome_lezione.ilike(f"%{request.args.get('nome')}%"))
        if request.args.get('insegnante'):
            query = query.filter(Lezioni.id_insegnante == request.args.get('insegnante'))
        if request.args.get('data'):
            query = query.filter(Lezioni.data == datetime.strptime(request.args.get('data'), '%Y-%m-%d').date())
        if request.args.get('orario'):
            query = query.filter(Lezioni.orario_inizio >= datetime.strptime(request.args.get('orario'), '%H:%M').time())
        if request.args.getlist('classe'):
            query = query.join(Lezioni.classi_concorso).filter(ClassiConcorso.id_classe.in_(request.args.getlist('classe')))
        if request.args.getlist('dipartimento'):
            query = query.join(Lezioni.dipartimenti).filter(Dipartimenti.id.in_(request.args.getlist('dipartimento')))
        if request.args.getlist('percorso'):
            query = query.join(Lezioni.percorsi).filter(Percorsi.id_percorso.in_(request.args.getlist('percorso')))
        query = query.distinct()
        lezioni_list = query.all()
        cfu_sum = sum(float(l.cfu) if l.cfu else 0 for l in lezioni_list)
        tutti_insegnanti = Insegnanti.query.order_by(Insegnanti.cognome).all()
        tutte_classi = ClassiConcorso.query.order_by(ClassiConcorso.nome_classe).all()
        dipartimenti = Dipartimenti.query.order_by(Dipartimenti.nome).all()
        percorsi = Percorsi.query.order_by(Percorsi.nome_percorso).all()
        return render_template('tab_lezioni.html', lezioni=lezioni_list, tutti_insegnanti=tutti_insegnanti, tutte_classi=tutte_classi, dipartimenti=dipartimenti, percorsi=percorsi, cfu_sum=cfu_sum)
    except Exception as e:
        app.logger.error(f'Errore nella route lezioni: {str(e)}')
        flash(f'Si è verificato un errore nel caricamento delle lezioni: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/add_lezione', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_PROFESSORE)
def add_lezione():
    try:
        if current_user.ruolo == ROLE_PROFESSORE:
            id_insegnante = current_user.id
        else:
            primo_insegnante = Insegnanti.query.first()
            id_insegnante = primo_insegnante.id_insegnante if primo_insegnante else None
        orario_inizio = datetime.strptime('09:00', '%H:%M').time()
        orario_fine = datetime.strptime('11:00', '%H:%M').time()
        durata, cfu = calcola_durata_e_cfu(orario_inizio, orario_fine)
        nuova_lezione = Lezioni(nome_lezione="Nuova Lezione", data=datetime.now().date(), orario_inizio=orario_inizio, orario_fine=orario_fine, durata=durata, cfu=cfu, id_insegnante=id_insegnante)
        db.session.add(nuova_lezione)
        db.session.commit()
        flash('Nuova lezione creata! Modifica i dettagli.', 'success')
        return redirect(url_for('edit_lezione', id=nuova_lezione.id_lezione))
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Errore durante la creazione della lezione: {str(e)}')
        flash(f'Errore durante la creazione della lezione: {str(e)}', 'error')
        return redirect(url_for('lezioni'))

@app.route('/edit_lezione/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_PROFESSORE)
def edit_lezione(id):
    lezione = Lezioni.query.get_or_404(id)
    insegnanti = Insegnanti.query.all()
    classi = ClassiConcorso.query.all()
    dipartimenti = Dipartimenti.query.all()
    percorsi = Percorsi.query.all()
    if request.method == 'POST':
        try:
            inizio = datetime.strptime(request.form['orario_inizio'], '%H:%M').time()
            fine = datetime.strptime(request.form['orario_fine'], '%H:%M').time()
            durata, cfu = calcola_durata_e_cfu(inizio, fine)
            lezione.nome_lezione = request.form['nome_lezione']
            lezione.data = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
            lezione.orario_inizio = inizio
            lezione.orario_fine = fine
            lezione.durata = durata
            lezione.cfu = cfu
            lezione.id_insegnante = request.form['id_insegnante']
            classi_ids = request.form.getlist('classi_concorso')
            dipartimenti_ids = request.form.getlist('dipartimenti')
            percorsi_ids = request.form.getlist('percorsi')
            lezione.classi_concorso = ClassiConcorso.query.filter(ClassiConcorso.id_classe.in_(classi_ids)).all()
            lezione.dipartimenti = Dipartimenti.query.filter(Dipartimenti.id.in_(dipartimenti_ids)).all()
            lezione.percorsi = Percorsi.query.filter(Percorsi.id_percorso.in_(percorsi_ids)).all()
            db.session.commit()
            flash('Lezione aggiornata con successo!', 'success')
            return redirect(url_for('lezioni'))
        except Exception as e:
            db.session.rollback()
            flash(f'Errore durante l\'aggiornamento della lezione: {str(e)}', 'error')
    return render_template('edit_lezione.html', lezione=lezione, insegnanti=insegnanti, classi=classi, dipartimenti=dipartimenti, percorsi=percorsi)

@app.route('/delete_lezione/<int:id>')
@login_required
@role_required(ROLE_SEGRETERIA, ROLE_PROFESSORE)
def delete_lezione(id):
    lezione = Lezioni.query.get_or_404(id)
    db.session.delete(lezione)
    db.session.commit()
    flash('Lezione eliminata con successo!', 'success')
    return redirect(url_for('lezioni'))

@app.route('/')
@login_required
def index():
    if current_user.ruolo == ROLE_SEGRETERIA:
        return redirect(url_for('segreteria'))
    elif current_user.ruolo == ROLE_STUDENTE:
        return redirect(url_for('area_studente'))
    elif current_user.ruolo == ROLE_PROFESSORE:
        return redirect(url_for('area_professore'))
    elif current_user.ruolo == ROLE_TUTOR_COLLABORATORE:
        return redirect(url_for('area_tutor_collaboratore'))
    elif current_user.ruolo == ROLE_TUTOR_COORDINATORE:
        return redirect(url_for('area_tutor_coordinatore'))
    elif current_user.ruolo == ROLE_ADMIN:
        return redirect(url_for('admin_users'))
    return render_template('main/index.html')

@app.route('/area_studente')
@login_required
@role_required(ROLE_STUDENTE)
def area_studente():
    totali = calcola_totali_studente(current_user.id)
    totale_cfu = totali['cfu_tirocinio_diretto'] + totali['cfu_tirocinio_indiretto']
    return render_template('area_studente.html', totale_cfu=totale_cfu, **totali)

@app.route('/area_professore')
@login_required
@role_required(ROLE_PROFESSORE)
def area_professore():
    lezioni = Lezioni.query.filter_by(id_insegnante=current_user.id).all()
    totali = calcola_totali_professore(current_user.id)
    return render_template('area_professore.html', lezioni=lezioni, **totali)

@app.route('/area_tutor_coordinatore')
@login_required
@role_required(ROLE_TUTOR_COORDINATORE)
def area_tutor_coordinatore():
    tirocini = RegistroPresenzeTirocinioIndiretto.query.filter_by(id_tutor_coordinatore=current_user.id).all()
    studenti_ids = set(t.id_studente for t in tirocini)
    studenti = User.query.filter(User.id.in_(studenti_ids)).all()
    for studente in studenti:
        totali = calcola_totali_studente(studente.id)
        studente.ore_totali = totali['ore_tirocinio_indiretto']
        studente.cfu_totali = totali['cfu_tirocinio_indiretto']
    totali = calcola_totali_tutor(current_user.id)
    return render_template('tutor_coordinatori/area_tutor_coordinatore.html', studenti=studenti, **totali)

@app.route('/get_tutor_esterno/<int:id_studente>')
@login_required
def get_tutor_esterno(id_studente):
    studente = Studenti.query.get_or_404(id_studente)
    return {'tutor_esterno': studente.tutor_esterno if studente.tutor_esterno else ''}

@app.route('/force-logout')
def force_logout():
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error/500.html'), 500

@app.cli.command('create-tables')
def create_tables():
    """Crea tutte le tabelle nel database"""
    try:
        db.create_all()
        print('Tabelle create con successo!')
    except Exception as e:
        print(f'Errore durante la creazione delle tabelle: {e}')

@app.cli.command('create-admin')
def create_admin():
    """Crea il primo utente amministratore"""
    email = input('Email amministratore: ')
    password = input('Password: ')
    nome = input('Nome: ')
    cognome = input('Cognome: ')
    if User.query.filter_by(email=email).first():
        print('Email già registrata')
        return
    admin = User(email=email, nome=nome, cognome=cognome, ruolo=ROLE_ADMIN, is_active=True)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print('Amministratore creato con successo!')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)