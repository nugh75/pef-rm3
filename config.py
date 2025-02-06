class Config:
    SECRET_KEY = 'la_tua_chiave_segreta'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@192.168.129.14:3308/Daniele'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # Usa lo stesso database MySQL anche in sviluppo
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@192.168.129.14:3308/Daniele'

class ProductionConfig(Config):
    DEBUG = False
    # Usa lo stesso database MySQL in produzione
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@192.168.129.14:3308/Daniele' 