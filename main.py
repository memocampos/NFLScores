'''
    File name: main.py
    Author: Guillermo Campos
    Date created: 10/15/2022
    Date last modified: 10/17/2022
    Python Version: 3.8
    Project description: Based on the realtime NFL scores from sportradar.com determine if there is a touchdown and trigger a Webhook to turn on a HUE or Nanoleaf scene accorting to the team color.

'''

import http.client
import json
import os
import requests
import time
import sqlite3 as sl
from dotenv import load_dotenv




load_dotenv()

WebHookID = os.getenv('IFTTTWebHook')
JSONTEMP = os.getenv('JSONTEMP')
api_key = os.getenv('api_key')

con = sl.connect('NFL.db')

PIT = 'https://maker.ifttt.com/trigger/SteelersON/json/with/key/' + WebHookID
LAR = 'https://maker.ifttt.com/trigger/Rams/json/with/key/' + WebHookID
CIN = 'https://maker.ifttt.com/trigger/Bengalies/json/with/key/' + WebHookID
GB = 'https://maker.ifttt.com/trigger/GreenBay/json/with/key/' + WebHookID
SF = 'https://maker.ifttt.com/trigger/SFO/json/with/key/' + WebHookID
LAC = 'https://maker.ifttt.com/trigger/LAC/json/with/key/' + WebHookID
LV = 'https://maker.ifttt.com/trigger/LV/json/with/key/' + WebHookID
SEA = 'https://maker.ifttt.com/trigger/SEAHAWKS/json/with/key/' + WebHookID
MIA = 'https://maker.ifttt.com/trigger/DOLPINS/json/with/key/' + WebHookID
NE = 'https://maker.ifttt.com/trigger/PATS/json/with/key/' + WebHookID
CLV = 'https://maker.ifttt.com/trigger/BROWNS/json/with/key/' + WebHookID
ARZ = 'https://maker.ifttt.com/trigger/Arizona/json/with/key/' + WebHookID
ATL = 'https://maker.ifttt.com/trigger/Atlanta/json/with/key/' + WebHookID
CHI = 'https://maker.ifttt.com/trigger/Bears/json/with/key/' + WebHookID
BUF = 'https://maker.ifttt.com/trigger/Bills/json/with/key/' + WebHookID
DEN = 'https://maker.ifttt.com/trigger/Broncos/json/with/key/' + WebHookID
CAR = 'https://maker.ifttt.com/trigger/Panthers/json/with/key/' + WebHookID
KC = 'https://maker.ifttt.com/trigger/Chiefs/json/with/key/' + WebHookID
DAL = 'https://maker.ifttt.com/trigger/Cowboys/json/with/key/' + WebHookID
NYJ = 'https://maker.ifttt.com/trigger/Jets/json/with/key/' + WebHookID
DET = 'https://maker.ifttt.com/trigger/Lions/json/with/key/' + WebHookID
NE = 'https://maker.ifttt.com/trigger/Patriots/json/with/key/' + WebHookID
BLT = 'https://maker.ifttt.com/trigger/Ravens/json/with/key/' + WebHookID
SEA = 'https://maker.ifttt.com/trigger/Seattle/json/with/key/' + WebHookID
HST = 'https://maker.ifttt.com/trigger/Houston/json/with/key/' + WebHookID


def istouchdown(feedscore, dbscore, team):
    if (feedscore - dbscore) >= 6:
        print("Touch down:", team)
        if team == 'PIT':
            teamwebhook = PIT
        elif team == 'LAR':
            teamwebhook = LAR
        elif team == 'CIN':
            teamwebhook = CIN
        elif team == 'GB':
            teamwebhook = GB
        elif team == 'SF':
            teamwebhook = SF
        elif team == 'LAC':
            teamwebhook = LAC
        elif team == 'LV':
            teamwebhook = LV
        elif team == 'MIA':
            teamwebhook = MIA
        elif team == 'NE':
            teamwebhook = NE
        elif team == 'CLV':
            teamwebhook = CLV
        elif team == 'CLE':
            # CLE AND CLV IS THE SAME
            teamwebhook = CLV
        elif team == 'ARZ':
            teamwebhook = ARZ
        elif team == 'ATL':
            teamwebhook = ATL
        elif team == 'CHI':
            teamwebhook = CHI
        elif team == 'BUF':
            teamwebhook = BUF
        elif team == 'DEN':
            teamwebhook = DEN
        elif team == 'CAR':
            teamwebhook = CAR
        elif team == 'KC':
            teamwebhook = KC
        elif team == 'DAL':
            teamwebhook = DAL
        elif team == 'NYJ':
            teamwebhook = NYJ
        elif team == 'DET':
            teamwebhook = DET
        elif team == 'NE':
            teamwebhook = NE
        elif team == 'BLT':
            teamwebhook = BLT
        elif team == 'BAL':
            teamwebhook = BLT
        elif team == 'SEA':
            teamwebhook = SEA
        elif team == 'HST':
            teamwebhook = HST
        elif team == 'HOU':
            teamwebhook = HST

        datawebhook = {'name': team + ' Touchdown', 'Channel URL': teamwebhook}
        r = requests.post(teamwebhook, data=json.dumps(datawebhook), headers={'Content-Type': 'application/json'})








timeloop = 1
while timeloop < 400 :
    conn = http.client.HTTPSConnection("api.sportradar.com")
    payload = ''
    headers = {}
    conn.request("GET", "/americanfootball/trial/v2/en/schedules/live/summaries.json?api_key=" + api_key , payload, headers)
    res = conn.getresponse()
    data = res.read()
    #y = json.loads(JSONTEMP)
    y = json.loads(data)
    print(y)

    timestamp = y["generated_at"]

    #VALIDAR SI EL JSON TIENE CONTENIDO DE JUEGOS
    if len(y["summaries"]) > 0:
        #OBTENER TODOS LOS JUEGOS ACTUALES
        for i in y["summaries"]:
            if i["sport_event"]["sport_event_context"]["competition"]["name"] == 'NFL':
                #OBTIENE LOS DATOS DEL PARTIDO
                teamhome = i["sport_event"]["competitors"][0]["name"]

                teamhomeabbreviation = i["sport_event"]["competitors"][0]["abbreviation"]
                teamhomescore = i["sport_event_status"]["home_score"]
                teamaway = i["sport_event"]["competitors"][1]["name"]
                teamawayabbreviation = i["sport_event"]["competitors"][1]["abbreviation"]
                teamawayscore = i["sport_event_status"]["away_score"]
                status = i["sport_event_status"]["status"]
                matchstatus = i["sport_event_status"]["match_status"]
                venuename = i["sport_event"]["venue"]["name"]
                venuecityname = i["sport_event"]["venue"]["city_name"]
                #IMPRIME LOS VALORES DEL PARTIDO
                #print(timestamp, teamhome, teamhomeabbreviation, teamhomescore, teamaway, teamawayabbreviation, teamawayscore, status,matchstatus, venuename, venuecityname)

                #1. VALIDAR EN BASE DE DATOS SI EXISTE EL REGISTRO
                query = "SELECT * FROM scores WHERE team_home = '" + teamhome + "' AND team_away = '" + teamaway + "'"

                with con:
                   data = con.execute(query)

                   count = data.fetchone()
                   if count == None:
                        # 2. SI NO EXISTE EL REGISTRO INSERTALO EN LA BD
                        query_insert = "insert into scores( time_stamp, team_home, team_home_abbreviation, team_home_score, team_away, team_away_abbreviation, team_away_score, status, match_status, venue_name, venue_city_name) values('" + timestamp + "','" + teamhome + "','" + teamhomeabbreviation + "'," + str(teamhomescore) + ",'" + teamaway + "','" + teamawayabbreviation + "'," + str(teamawayscore) + ",'" + status + "','" + matchstatus + "','" + venuename + "','" + venuecityname + "');"
                        #print(query_insert)
                        with con:
                            con.execute(query_insert)
                            print("Added new record for game " + teamhomeabbreviation + "-" + str(teamhomescore) + " VS. " + teamawayabbreviation + "-" + str(teamawayscore))
                   else:
                        # 3. SI YA ESXISTE EL REGISTRO COMPARA EL MARCADOR
                        # obtiene el ultimo marcador de la DB
                        query_scores = "SELECT team_home_score, team_away_score  FROM scores WHERE team_home = '" + teamhome + "' AND  team_away = '" + teamaway + "' order BY ID DESC limit 1"
                        with con:
                            result = con.execute(query_scores)
                            for row in result:
                                DBhomescore = row[0]
                                DBawayscore = row[1]
                        # Valida marcador de BD con el feed
                        # 4. SI EL MARCADOR ES DIFERENTE ENTONCES INSERTA REGISTRO EN LA BD Y DISPARA EVENTO
                        if (teamhomescore > DBhomescore) or (teamawayscore > DBawayscore):
                            print("New score on the game of "+ teamhomeabbreviation + " Vs. " + teamawayabbreviation)
                            query_insert = "insert into scores( time_stamp, team_home, team_home_abbreviation, team_home_score, team_away, team_away_abbreviation, team_away_score, status, match_status, venue_name, venue_city_name) values('" + timestamp + "','" + teamhome + "','" + teamhomeabbreviation + "'," + str(teamhomescore) + ",'" + teamaway + "','" + teamawayabbreviation + "'," + str(teamawayscore) + ",'" + status + "','" + matchstatus + "','" + venuename + "','" + venuecityname + "');"
                            # print(query_insert)
                            with con:
                                con.execute(query_insert)
                                print("updated score for game " + teamhomeabbreviation + "-" + str(teamhomescore) + " VS. " + teamawayabbreviation + "-" + str(teamawayscore))
                            istouchdown(teamhomescore,DBhomescore,teamhomeabbreviation)
                            istouchdown(teamawayscore, DBawayscore,teamawayabbreviation)




                        else:
                            # 5. SI EL MARCADOR ES IGUAL - ENTONCES TERMINA
                            print("No change: " + teamhomeabbreviation + "-" + str(teamhomescore)  + " " + str(teamawayscore) + "-" + teamawayabbreviation )

    else:
        print("No games at this time")
    time.sleep(30)