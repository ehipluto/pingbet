from datetime import datetime
import os
from nis import match

import requests
import json
import pytz
from methods.db.db import DB
from methods.odds_matches import getOdds as odds
from . import matches_H2H as h2h


def removeMatches():
    db = DB()
    db.doLogin()
    db.removeMatches()

def update_database():
    with open('file.txt', 'w') as file:
        file.write("LOL\n")
    db = DB()
    db.doLogin()
    current_date = datetime.now().strftime("%Y-%m-%d")
    url = f"https://table-tennis.sportdevs.com/matches-by-date?date=eq.{current_date}"
    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer dsBH5k-JaEybFCGkeMY2gg'
    }
    print("Faccio fetch...")
    response = requests.request("GET", url, headers=headers, data=payload)
    list_of_dict = json.loads(response.text)
    with open('file.txt', 'a') as file:
        file.write(str(list_of_dict[0]))
        file.write("\n\n")
    print(f"Dati ottenuti\nControllo {len(list_of_dict[0])} elementi...")
    for elem in list_of_dict[0]['matches']:
        print(f"\nControllo match {elem['id']}\n{elem['tournament_name']}")
        tournament_matches = False
        tournament_name = elem['tournament_name'].upper()
        with open('file.txt', 'a') as file:
            file.write(str(elem))
        for keyword in os.getenv('tournamentsKeywords'):
            if keyword.upper() in tournament_name:
                tournament_matches = True


        if elem['status'] != "finished" and elem['status'] != 'live' and tournament_matches:
            print("Controllo Odds")
            val = odds(elem['id'])
            if val:
                print("Odds trovate!\nControllo H2H")
                homePer, awayPer = h2h.getH2H(elem['home_team_id'], elem['away_team_id'])
                elem['probability_home'] = round(homePer,2)
                elem['probability_away'] = round(awayPer,2)
                elem['start_time'] = convert_to_italian_time(elem['start_time'])
                elem['h2h_count'] = TotalMatches
                elem['odds'] = val
                with open('file.txt', 'a') as file:
                    file.write(str(elem))
                    file.write("\n")
                print("Inserisco match nel db")
                db.insertMatch(elem, os.getenv('DB_MATCHES'))
            else:
                print("Odds non trovate...")

    print("\nInserimento completato!")

def getMatches():
    print("Sono in getMatches")
    db = DB()
    db.doLogin()
    match_list = []
    print("Richiedo match")
    listMatches =db.getData(os.getenv('DB_MATCHES'))
    print("Match ottenuti")
    for elem in listMatches:
        match_data = {
            "ID": elem['id'],
            "Match": elem['name'],
            "Tournament": elem['tournament_name'],
            "Time": convert_to_italian_time(elem['start_time']),
            "Probability": f"{elem['probability_home']} - {elem['probability_away']}",
            "H2HCount": h2h_count,
            "Odds": elem['odds'],
        }
        match_list.append(match_data)

    print("Ritorno i match sistemati")
    return match_list

def convert_to_italian_time(utc_time):
    if utc_time is None:
        return None
    utc_time = utc_time.replace('+00:00', '')
    utc = pytz.UTC.localize(datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S"))
    italian_tz = pytz.timezone('Europe/Rome')
    italian_time = utc.astimezone(italian_tz)
    return italian_time
