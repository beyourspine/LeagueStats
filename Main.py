import pandas as pd
import numpy as np
from os import path
import riotwatcher
from riotwatcher import LolWatcher, ApiError

z = 0
i = 0
q = 0

gameInfoColumns = ["kills", "deaths", "killingSprees", "visionScore", "goldEarned", "neutralMinionsKilled", "summonerName", "baitPings", "championName", "enemyMissingPings", "win", "totalMinionsKilled"]
gamemode = 440
gamecount = 20

lol_watcher = LolWatcher("RGAPI-22a53102-9e03-494f-86ff-1fb8ede978de")
region = "euw1"
userName = "FrozenFire2018"
summoner = lol_watcher.summoner.by_name(region, userName)
puuid = summoner["puuid"]
userList = ['FrozenFire2018', 'Fractal14', 'IkuTurso', 'snizkabiz', 'NecroAura']

if path.isfile(userName + 'gameList.npy') == False:
    file = open(userName + 'gameList.npy', 'x')
    file.close

if path.getsize(userName + 'gameList.npy') == 0:
    previousMatchList = np.empty(0)
else:
    previousMatchList = np.load(userName + 'gameList.npy')

matchList = np.array(lol_watcher.match.matchlist_by_puuid(region, puuid, queue = gamemode, count = gamecount))
matchMask = np.isin(matchList, previousMatchList, invert = True)
matchList = matchList[matchMask]


if len(matchList) == 0:
    print("Match List Empty")
    exit()

np.save( userName + 'gameList' ,np.concatenate((matchList, previousMatchList), axis = 0))

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

userOutputs = [pd.DataFrame()] * len(userList)

for user in userList:   
    output = gameInfo[gameInfoColumns].copy()
    output["Creep Score"] = gameInfo["neutralMinionsKilled"] + gameInfo["totalMinionsKilled"]
    output["Game Duration"] = round(gameInfo["timePlayed"] / 60)
    output["CS per Min"] = output["Creep Score"] / output["Game Duration"]
    output["Index"] = range(len(output))
    output.set_index("Index", inplace = True)
    output = pd.concat([output, matchInfo[["gameStartTimestamp", "queueId", "gameId"]]], axis = 1)
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
    userOutputs[z] = output
    z+= 1

k = 0

for user in userOutputs:
    for d in range(len(userOutputs)):
        Mask = user["gameId"].isin(userOutputs[d]["gameId"])
        user = user[Mask]
    user.to_csv(userList[k] + "output.csv")
    k+= 1
