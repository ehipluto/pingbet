import requests, json

def getH2H(home_team_id, away_team_id):
    url = f"https://table-tennis.sportdevs.com/matches?home_team_id=in.({home_team_id},{away_team_id})&away_team_id=in.({home_team_id},{away_team_id})"
    payload={}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer dsBH5k-JaEybFCGkeMY2gg' 
    }
    home = 0
    away = 0
    response = requests.request("GET", url, headers=headers, data=payload)
    list = json.loads(response.text)
    for elem in list:
        if elem.get('home_team_score') is not None and elem.get('away_team_score') is not None:
            if 'current' in elem['home_team_score'] and 'current' in elem['away_team_score']:
                if elem['home_team_id'] == home_team_id:
                    if elem['home_team_score']['current'] > elem['away_team_score']['current']:
                        home += 1
                    else:
                        away +=1

                elif elem['away_team_id'] == home_team_id:
                    if elem['away_team_score']['current'] > elem['home_team_score']['current']:
                        home += 1
                    else:
                        away +=1



    if home == 0:
        homePer = 0
        awayPer = 100
    elif away == 0:
        homePer = 100
        awayPer = 0
    else: 
        homePer = (home/(home+away)) * 100
        awayPer = (away/(home+away)) * 100
    
    return homePer, awayPer




    

home_team_i = 150130
away_team_i = 66556

getH2H(home_team_i, away_team_i)