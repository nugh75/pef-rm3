import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Configurazione della connessione
config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')
}

print('Tentativo di connessione al database...')

try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print('✅ Connessione al database riuscita!')
        print(f"Server: {config['host']}:{config['port']}")
        print(f"Database: {config['database']}")
except Error as err:
    print('❌ Errore di connessione:', err)
    print('Dettagli connessione:')
    print(f"Host: {config['host']}")
    print(f"Porta: {config['port']}")
    print(f"Database: {config['database']}")
    print(f"Utente: {config['user']}")
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
