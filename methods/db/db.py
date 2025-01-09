from os import remove

import mysql.connector
import sys
import os
from threading import Lock
from dotenv import load_dotenv

class DB:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):

        load_dotenv()
        if not hasattr(self, 'data'):
            self.data = None

    def getInstance(self):
        if self.data is None:
            raise Exception("Devi eseguire il login prima!")
        return self.data

    def doLogin(self):
        try:
            if self.data is None:
                self.data = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    database=os.getenv('DB_NAME')
                )
        except mysql.connector.Error as err:
            print(f"Errore di connessione al database: {err}")
            sys.exit(1)
        print("Connessione effettuata al database")
        return self.data

    def getData(self, table):
        with self._lock:
            cursor = self.data.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM {table}")
            listMatches = cursor.fetchall()
            cursor.close()
            return listMatches
    def removeMatches(self):
        sqlQuery = f"DELETE FROM {os.getenv('DB_MATCHES')} WHERE start_time < NOW()"

        with self._lock:
            cursor = self.data.cursor(dictionary=True)
            cursor.execute(sqlQuery)
            self.data.commit()
            print("Eliminazione completata!")
            cursor.close()

    def insertMatch(self, elem, table):
        temp = {
            'id': elem['id'],
            'name': elem['name'],
            'status': elem['status'],
            'duration': elem['duration'],
            'start_time': elem['start_time'],
            'away_team_id': elem['away_team_id'],
            'home_team_id': elem['home_team_id'],
            'status_reason': elem['status_reason'],
            'tournament_id': elem['tournament_id'],
            'away_team_name': elem['away_team_name'],
            'home_team_name': elem['home_team_name'],
            'tournament_name': elem['tournament_name'],
            'away_team_hash_image': elem['away_team_hash_image'],
            'home_team_hash_image': elem['home_team_hash_image'],
            'tournament_importance': elem['tournament_importance'],
            'probability_home': elem['probability_home'],
            'probability_away': elem['probability_away'],
            'odds': elem['odds']
        }
        columns = ", ".join(temp.keys())
        placeholders = ", ".join(["%s"] * len(temp))
        sqlQuery = f"INSERT IGNORE INTO {table} ({columns}) VALUES ({placeholders})"

        with self._lock:
            cursor = self.data.cursor(dictionary=True)
            cursor.execute(sqlQuery, tuple(temp.values()))
            self.data.commit()
            print(f"Record inserito, ID: {elem['id']}")
            cursor.close()