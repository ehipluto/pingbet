import mysql.connector, sys, os
from dotenv import load_dotenv

class DB:
    _instance = None
    #controlla prima di init se esiste l'istanza della classe
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Inizializza la connessione se non è già presente
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
        cursor = self.data.cursor(dictionary = True)
        cursor.execute(f"select * from {table}")
        listMatches = cursor.fetchall()
        cursor.close()
        return listMatches


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
            'odds' : elem['odds']
        }
        columns = ", ".join(temp.keys())
        placeholders = ", ".join(["%s"] * len(temp))
        query = """
            INSERT IGNORE INTO your_table (
                id, name, status, duration, start_time,
                away_team_id, home_team_id, status_reason, tournament_id,
                away_team_name, home_team_name, tournament_name,
                away_team_hash_image, home_team_hash_image,
                tournament_importance, probability_home, probability_away
            )
            VALUES (
                %(id)s, %(name)s, %(status)s, %(duration)s, %(start_time)s,
                %(away_team_id)s, %(home_team_id)s, %(status_reason)s, %(tournament_id)s,
                %(away_team_name)s, %(home_team_name)s, %(tournament_name)s,
                %(away_team_hash_image)s, %(home_team_hash_image)s,
                %(tournament_importance)s, %(probability_home)s, %(probability_away)s
            )
        """
        sqlQuery = f"INSERT IGNORE INTO {table} ({columns}) VALUES ({placeholders})"

        cursor = self.data.cursor(dictionary = True)
        cursor.execute(sqlQuery, tuple(temp.values()))
        self.data.commit()
        print(f"Record inserito, ID: {elem['id']}")
        cursor.close()
