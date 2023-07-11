import pandas as pd
import numpy as np
from os import path
import riotwatcher
from riotwatcher import LolWatcher, ApiError

z = 0
i = 0
q = 0

lol_watcher = LolWatcher("RGAPI-5d6748ad-35c4-4c35-a05c-54dfbe074297")
region = "euw1"
userName = "FrozenFire2018"
summoner = lol_watcher.summoner.by_name(region, userName)
puuid = summoner["puuid"]
userList = ['FrozenFire2018', 'IkuTurso', 'snizkabiz', 'Fractal14', 'NecroAura']

if path.isfile('gameList.npy') == False:
    file = open('gameList.npy', 'x')
    file.close

if path.getsize("gameList.npy") == 0:
    previousMatchList = np.empty(0)
else:
    previousMatchList = np.load('gameList.npy')
    
matchList = np.array(lol_watcher.match.matchlist_by_puuid(region, puuid, queue = 440))
matchMask = np.isin(matchList, previousMatchList, invert = True)
matchList = matchList[matchMask]

if len(matchList) == 0:
    print("Match List Empty")
    exit()

np.save( 'gameList' ,np.concatenate((matchList, previousMatchList), axis = 0))

while i < len(matchList):
    try:
        if i == 0:
            gameInfo = pd.json_normalize(lol_watcher.match.by_id(region, matchList[0])['info']['participants'])
            matchInfo = pd.json_normalize(lol_watcher.match.by_id(region, matchList[0])['info'])
        else:
            gameInfo = pd.concat([gameInfo, pd.json_normalize(lol_watcher.match.by_id(region, matchList[i])['info']['participants'])])
            matchInfo = pd.concat([matchInfo, pd.json_normalize(lol_watcher.match.by_id(region, matchList[i])['info'])])
            
    except Exception as e:
        print("Error on match " + str(i + 1))
        print(e)
    i+= 1

temp = pd.DataFrame(np.repeat(matchInfo.values, 10, axis = 0))
temp.columns = matchInfo.columns
matchInfo = temp
matchInfo["Index"] = range(len(matchInfo))
matchInfo.set_index("Index", inplace = True)

for user in userList:   
    output = gameInfo[["kills", "deaths", "killingSprees", "visionScore", "goldEarned", "neutralMinionsKilled", "summonerName", "baitPings", "championName", "enemyMissingPings", "win", "totalMinionsKilled", "role"]].copy()
    output["Creep Score"] = gameInfo["neutralMinionsKilled"] + gameInfo["totalMinionsKilled"]
    output["Index"] = range(len(output))
    output.set_index("Index", inplace = True)
    output = pd.concat([output, matchInfo[["gameStartTimestamp", "gameMode","queueId"]]], axis = 1)
    output["gameStartTimestamp"] = pd.to_datetime(output["gameStartTimestamp"], unit = 'ms')
    output.set_index("gameStartTimestamp", inplace = True)
    outputMask = output["summonerName"] == user
    output = output[outputMask]
    
    if path.isfile(user + "output.csv") != False:
        if path.getsize(user + "output.csv") != 0:
            currentCSV = pd.read_csv(user + "output.csv")
            currentCSV["gameStartTimestamp"] = currentCSV["gameStartTimestamp"].astype("datetime64[ns]")
            currentCSV.set_index("gameStartTimestamp", inplace = True)
            output = pd.concat([output, currentCSV], join = 'inner')
            output.sort_index(ascending = False, inplace = True)

    output.to_csv(user + "output.csv")
    z+= 1