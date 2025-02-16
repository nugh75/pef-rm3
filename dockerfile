# Usa un’immagine Python ufficiale (scegli la versione che preferisci)
FROM python:3.9-slim

# Imposta la directory di lavoro nel container
WORKDIR /app

# Copia il file dei requisiti ed installa le dipendenze
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice sorgente (la cartella "venv" verrà ignorata grazie a .dockerignore)
COPY . .

# Imposta il comando di default per avviare l’applicazione (modifica "app.py" secondo le tue necessità)
CMD ["python", "app.py"]