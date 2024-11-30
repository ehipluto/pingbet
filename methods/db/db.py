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
                    password=os.getenv('DB_PASSWORD'),  # Usa la password corretta per il tuo DB
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
        print(type(listMatches))
        cursor.close()
        return listMatches


    def insertMatch(self, elem, table):
        columns = ", ".join(elem.keys())
        placeholders = ", ".join(["%s"] * len(elem))
        sqlQuery = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        cursor = self.data.cursor(dictionary = True)
        cursor.execute(sqlQuery, tuple(elem.values()))
        self.data.commit()
        print(f"Record inserito, ID: {elem['id']}")
        cursor.close()



