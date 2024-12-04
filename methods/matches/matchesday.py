from datetime import datetime
import os
from nis import match

import requests
import json
import pytz
from methods.db.db import DB
from methods.odds_matches import getOdds as odds
from . import matches_H2H as h2h



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
    response = requests.request("GET", url, headers=headers, data=payload)
    list_of_dict = json.loads(response.text)

    for elem in list_of_dict[0]['matches']:
        tournament_matches = False
        tournament_name = elem['tournament_name'].upper()

        for keyword in os.getenv('tournamentsKeywords'):
            if keyword.upper() in tournament_name:
                tournament_matches = True
                break

        if elem['status'] != "finished" and elem['status'] != 'live' and tournament_matches:
            val = odds(elem['id'])
            if val:
                with open('file.txt', 'a') as file:
                    file.write(str(elem))
                    file.write("\n")
                homePer, awayPer = h2h.getH2H(elem['home_team_id'], elem['away_team_id'])
                elem['probability_home'] = round(homePer,2)
                elem['probability_away'] = round(awayPer,2)
                elem['start_time'] = convert_to_italian_time(elem['start_time'])
                elem['odds'] = val
                with open('file.txt', 'a') as file:
                    file.write(str(elem))
                    file.write("\n")
                db.insertMatch(elem, os.getenv('DB_MATCHES'))
    print("Inserimento completato!")

def getMatches():
    db = DB()
    db.doLogin()
    match_list = []
    listMatches =db.getData(os.getenv('DB_MATCHES'))
    for elem in listMatches:
        match_data = {
            "ID": elem['id'],
            "Match": elem['name'],
            "Tournament": elem['tournament_name'],
            "Time": elem['start_time'],
            "Probability": f"{elem['probability_home']} - {elem['probability_away']}",
            "Odds": elem['odds']
        }
        match_list.append(match_data)
    return match_list

def convert_to_italian_time(utc_time):
    if utc_time is None:
        return None
    utc_time = utc_time.replace('+00:00', '')
    utc = pytz.UTC.localize(datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S"))
    italian_tz = pytz.timezone('Europe/Rome')
    italian_time = utc.astimezone(italian_tz)
    return italian_time


#update_database()