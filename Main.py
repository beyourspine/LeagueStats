import pandas as pd
import riotwatcher
from riotwatcher import LolWatcher, ApiError

i = 0

lol_watcher = LolWatcher("RGAPI-5fd178df-d0ad-4615-8314-01f864c1b729")

region = "euw1"

summoner = lol_watcher.summoner.by_name(region, "FrozenFire2018")
puuid = summoner["puuid"]

matchList = lol_watcher.match.matchlist_by_puuid(region, puuid)

print(matchList)

querySQL = """
Select kills, deaths, killingSprees, visionScore, goldEarned, neutralMinionsKilled
From output
Group By summonerName
"""

while i < 20:
    try:
        if i == 0:
            output = pd.json_normalize(lol_watcher.match.by_id(region, matchList[0])['info']['participants'])
            matchInfo = pd.json_normalize(lol_watcher.match.by_id(region, matchList[0]))
        else:
            output = pd.concat([output, pd.json_normalize(lol_watcher.match.by_id(region, matchList[i])['info']['participants'])])
            matchInfo = pd.concat([matchInfo, pd.json_normalize(lol_watcher.match.by_id(region, matchList[i]))])
    except Exception as e:
        print("Error on match " + str(i + 1))
        print(e)
    i+= 1

outputFinal = output[["kills", "deaths", "killingSprees", "visionScore", "goldEarned", "neutralMinionsKilled", "summonerName", "baitPings", "championName", "enemyMissingPings", "win", "totalMinionsKilled", "role"]]
outputFinal["CS"] = output["neutralMinionsKilled", "totalMinionsKilled"].sum
outputFinal["gameMode"] = matchInfo["info.gameMode"]
outputFinal["gameType"] = matchInfo["info.gameType"]
outputMask = outputFinal["summonerName"] == "FrozenFire2018"
outputFinal = outputFinal[outputMask]
outputFinal.to_csv("output.csv")

