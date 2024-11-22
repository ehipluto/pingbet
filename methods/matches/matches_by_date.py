import requests, json, os, time
from datetime import datetime
from . import matches_H2H as h2h
from ..odds_matches import getOdds as odds

def getMatchToday():
    call = 0
    callOdds = 0
    current_date = datetime.now().strftime("%Y-%m-%d")
    print(f"Effettuo controllo match in data {current_date}")
    url = f"https://table-tennis.sportdevs.com/matches-by-date?date=eq.{current_date}"
    tournamentsName = ["TT Star Series", "TT Elite Series", "Challenger Series TT", "WTT Feeder", "WTT Star", 
                       "TT Cup", "China Smash", "Contender", "Liga Pro China", "WTT Champions", "WTT Contender", 
                       "WTT Star Contender"]
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
        if elem['status'] != "finished" and elem['status'] != 'live' and elem['tournament_name'] in tournamentsName:
            val = odds(elem['id'])
            callOdds += 1
            if val:
                homePer, awayPer = h2h.getH2H(elem['home_team_id'], elem['away_team_id'])
                call += 1
                match_data = {
                    "ID": elem['id'],
                    "Match": elem['name'],
                    "Tournament": elem['tournament_name'],
                    "Time": elem['start_time'],
                    "Probability": f"{round(homePer, 2)} - {round(awayPer, 2)}",
                    "Odds": val
                }
                # Aggiungi i dati alla lista
                match_list.append(match_data)

    print(f"Chiamate effettuate: {call + callOdds}\nChiamate odds: {callOdds}\nChiamate h2h: {call - 1}")  

    # Restituisci la lista dei match
    return match_list

