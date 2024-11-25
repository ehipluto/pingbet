import requests, json, os, time
import pytz
from datetime import datetime
from . import matches_H2H as h2h
from ..odds_matches import getOdds as odds


def convert_to_italian_time(utc_time):
    utc_time = utc_time.replace('+00:00', '')
    utc = pytz.UTC.localize(datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S"))
    italian_tz = pytz.timezone('Europe/Rome')
    italian_time = utc.astimezone(italian_tz)
    return italian_time.strftime("%H:%M")


def getMatchToday():
    call = 0
    callOdds = 0
    current_date = datetime.now().strftime("%Y-%m-%d")
    print(f"Effettuo controllo match in data {current_date}")
    url = f"https://table-tennis.sportdevs.com/matches-by-date?date=eq.{current_date}"

    tournamentsKeywords = ["WTT", "TT", "Feeder", "Challenger", "World Tour", "China Smash", "Contender",
                           "Liga Pro China"]

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer dsBH5k-JaEybFCGkeMY2gg'
    }

    print("Faccio fetch")
    response = requests.request("GET", url, headers=headers, data=payload)
    dicts = json.loads(response.text)
    call += 1
    print(f"Controllo: {len(dicts[0]['matches'])} match")

    # Lista per salvare i dati
    match_list = []

    for elem in dicts[0]['matches']:
        # Verifica se il torneo contiene almeno una delle parole chiave
        tournament_matches = False
        tournament_name = elem['tournament_name'].upper()

        for keyword in tournamentsKeywords:
            if keyword.upper() in tournament_name:
                tournament_matches = True
                break

        if elem['status'] != "finished" and elem['status'] != 'live' and tournament_matches:
            val = odds(elem['id'])
            callOdds += 1
            if val:
                # Ottieni le quote del primo bookmaker
                first_bookmaker_odds = val.split('|')[1].split(':')[1].strip()

                # Calcola H2H per utilizzarlo in un secondo momento
                homePer, awayPer, h2h_count = h2h.getH2H(elem['home_team_id'], elem['away_team_id'])
                call += 1

                match_data = {
                    "ID": elem['id'],
                    "Match": elem['name'],
                    "Tournament": elem['tournament_name'],
                    "Time": convert_to_italian_time(elem['start_time']),
                    "Odds": val,  # Mantieni tutte le quote per il modal
                    "FirstBookmakerOdds": first_bookmaker_odds,  # Quote del primo bookmaker
                    "H2HProbability": f"{round(homePer, 2)} - {round(awayPer, 2)}",  # Salva per il modal
                    "H2HCount": h2h_count  # Numero di match H2H
                }
                # Aggiungi i dati alla lista
                match_list.append(match_data)

    print(f"Chiamate effettuate: {call + callOdds}\nChiamate odds: {callOdds}\nChiamate h2h: {call - 1}")

    # Restituisci la lista dei match
    return match_list
