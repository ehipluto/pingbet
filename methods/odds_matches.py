import requests, json

match_id = 995380
freccia_destra = "→"  # Freccia destra
freccia_sinistra = "←"  # Freccia sinistra
freccia_giu = "↓"  # Freccia verso il basso
freccia_su = "↑"  # Freccia verso l'alto
freccia_doppia = "⇄"  # Freccia doppia sinistra-destra
def getOdds(match_id):
  url = f"https://table-tennis.sportdevs.com/odds/full-time-results?match_id=eq.{match_id}&is_live=eq.false"
  payload={}
  headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer dsBH5k-JaEybFCGkeMY2gg'
    }
  value = ""
  response = requests.request("GET", url, headers=headers, data=payload)
  dict = json.loads(response.text)
  if len(dict) == 0:
    return False
  for elem in dict[0]['periods'][0]['odds']:
      value += f"|{elem['bookmaker_name']}: {elem['home']}{'↑' if elem['home_movement'] == 1 else '↓' if elem['home_movement'] == -1 else '•'} - {elem['away']}{'↑' if elem['away_movement'] == 1 else '↓' if elem['away_movement'] == -1 else '•'} \n"
  
  return value

print(getOdds(match_id))
#for odds in elem['odds']:
#value += f"|{odds['bookmaker_name']} : {odds['score']}\n"