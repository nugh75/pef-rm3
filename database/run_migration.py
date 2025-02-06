import os
import mysql.connector
from mysql.connector import Error
import sys
from dotenv import load_dotenv

# Carica le variabili d'ambiente
load_dotenv()

def execute_migration(connection, file_path):
    try:
        with open(file_path, 'r') as file:
            # Leggi il contenuto del file
            sql_commands = file.read()
            
            # Dividi il file in comandi separati
            commands = sql_commands.split(';')
            
            cursor = connection.cursor()
            
            # Esegui ogni comando
            for command in commands:
                # Salta i comandi vuoti
                if command.strip():
                    try:
                        cursor.execute(command)
                        print(f"Comando eseguito con successo: {command[:50]}...")
                    except Error as e:
                        print(f"Errore nell'esecuzione del comando: {command[:50]}...")
                        print(f"Errore: {str(e)}")
            
            connection.commit()
            print("Migrazione completata con successo!")
            
    except Error as e:
        print(f"Errore durante l'esecuzione della migrazione: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()

def main():
    try:
        # Configura la connessione al database usando le variabili d'ambiente
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        
        if connection.is_connected():
            print("Connesso al database MySQL")
            
            # Percorso del file di migrazione
            migration_file = '007_create_dipartimenti_tutor_tables.sql'
            migration_path = os.path.join(os.path.dirname(__file__), 'migrations', migration_file)
            
            # Esegui la migrazione
            execute_migration(connection, migration_path)
            
    except Error as e:
        print(f"Errore durante la connessione al database: {str(e)}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Connessione al database chiusa")

if __name__ == "__main__":
    main()