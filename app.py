import os
from flask import Flask, render_template, send_from_directory, redirect, url_for, request
from methods.matches import matchesday as test
import threading
import time
from datetime import datetime, timedelta

app = Flask(__name__)

# Variabili globali per il thread
db_thread = None
thread_running = False

def calculate_sleep_duration():
    """Calcola il tempo da dormire fino al prossimo intervallo di 3 ore."""
    now = datetime.now()
    next_hour = (now.hour // 3 + 1) * 3
    if next_hour == 24:
        next_hour = 0
        next_day = now + timedelta(days=1)
        next_time = next_day.replace(hour=next_hour, minute=0, second=0, microsecond=0)
    else:
        next_time = now.replace(hour=next_hour, minute=0, second=0, microsecond=0)
    sleep_duration = (next_time - now).total_seconds()
    return 1

def tes():
    while thread_running:
        print("CIAO")

def database_update_thread():
    """Thread demone per aggiornare il database ogni 3 ore."""
    global thread_running
    while thread_running:
        print(f"Thread: Attendo fino al prossimo intervallo di 3 ore...")
        time_to_sleep = calculate_sleep_duration()
        time.sleep(time_to_sleep)
        if not thread_running:
            break
        try:
            print("Thread: Eseguo l'aggiornamento del database...")
            test.update_database()  # Metodo di aggiornamento
            print("Thread: Aggiornamento completato.")
        except Exception as e:
            print(f"Thread: Errore durante l'aggiornamento del database: {e}")

@app.route('/')
def hello_world():
    # Mostra la pagina principale con le partite e lo stato del thread
    listMatches = test.getMatches()
    return render_template('matches.html', matches=listMatches, thread_running=thread_running)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/start-thread', methods=['POST'])
def start_thread():
    """Avvia il thread demone."""
    global db_thread, thread_running
    if not thread_running:
        thread_running = True
        db_thread = threading.Thread(target=database_update_thread(), daemon=True)
        db_thread.start()
    return redirect(url_for('hello_world'))

@app.route('/stop-thread', methods=['POST'])
def stop_thread():
    """Ferma il thread demone."""
    global thread_running
    thread_running = False
    return redirect(url_for('hello_world'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
