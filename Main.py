import pandas as pd
import riotwatcher
from riotwatcher import LolWatcher, ApiError

i = 0

lol_watcher = LolWatcher("RGAPI-5fd178df-d0ad-4615-8314-01f864c1b729")

region = "euw1"
userName = "FrozenFire2018"
summoner = lol_watcher.summoner.by_name(region, userName)
puuid = summoner["puuid"]

matchList = lol_watcher.match.matchlist_by_puuid(region, puuid)

print(matchList)

querySQL = """
Select kills, deaths, killingSprees, visionScore, goldEarned, neutralMinionsKilled
From output
Group By summonerName
"""

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



output = gameInfo[["kills", "deaths", "killingSprees", "visionScore", "goldEarned", "neutralMinionsKilled", "summonerName", "baitPings", "championName", "enemyMissingPings", "win", "totalMinionsKilled", "role"]].copy()
output["Creep Score"] = gameInfo["neutralMinionsKilled"] + gameInfo["totalMinionsKilled"]
outputMask = output["summonerName"] == userName
output = output[outputMask]
matchInfo["Index"] = range(20)
matchInfo.set_index("Index", inplace = True)
output["Index"] = range(20)
output.set_index("Index", inplace = True)
output = pd.concat([output, matchInfo[["gameStartTimestamp", "gameMode",]]], axis = 1)
output["gameStartTimestamp"] = pd.to_datetime(output["gameStartTimestamp"], unit = 'ms')
output.set_index("gameStartTimestamp", inplace = True)

output.to_csv("output.csv")


