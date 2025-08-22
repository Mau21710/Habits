import pandas as pd
import os

LOG_FILE = 'activity_log.csv'

def clean_activity_log():
    """
    Legge activity_log.csv, standardizza la colonna timestamp 
    al formato 'YYYY-MM-DD HH:MM:SS' e salva il file.
    """
    if not os.path.exists(LOG_FILE):
        print(f"File {LOG_FILE} non trovato. Nessuna operazione da eseguire.")
        return

    try:
        df = pd.read_csv(LOG_FILE)
        if df.empty:
            print(f"File {LOG_FILE} è vuoto. Nessuna operazione da eseguire.")
            return

        # 1. Rinomina la vecchia colonna 'date' se esiste
        if 'date' in df.columns:
            df.rename(columns={'date': 'timestamp'}, inplace=True)

        # 2. Converte la colonna timestamp in oggetti datetime
        #    'ISO8601' è robusto per gestire formati misti (date e timestamp)
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601')

        # 3. Formatta la colonna nel formato standard e leggibile
        df['timestamp'] = df.timestamp.dt.strftime('%Y-%m-%d %H:%M:%S')

        # 4. Salva il file pulito
        df.to_csv(LOG_FILE, index=False)
        print(f"File {LOG_FILE} pulito e standardizzato con successo.")

    except Exception as e:
        print(f"Si è verificato un errore durante la pulizia del file: {e}")

if __name__ == "__main__":
    clean_activity_log()
