import customtkinter as tk
from PIL import Image

gameInfoColumns = ["kills", "deaths", "killingSprees", "visionScore", "goldEarned", "neutralMinionsKilled", "summonerName", "baitPings", "championName", "enemyMissingPings", "win", "totalMinionsKilled"]
gamemodeList = ["Normal Draft", "Ranked Solo", "Ranked Flex", "Normal Blind", "ARAM"]
userList = ['FrozenFire2018', 'Fractal14', 'IkuTurso', 'snizkabiz', 'NecroAura']

tk.set_appearance_mode("Dark")

main = tk.CTk()
main.minsize(0,600)
main.title('League of Plebs')

title = tk.CTkFrame(main)
title.grid(row = 0)
titleImage = tk.CTkImage(Image.open("Title.png"), size = (790,76))
titleLabel = tk.CTkLabel(title, image = titleImage, text = "", fg_color = "transparent")
titleLabel.pack()


gamemode = tk.CTkFrame(main)
gamemodeButtons = tk.CTkSegmentedButton(gamemode, values = gamemodeList)
gamemodeButtons.pack()
gamemodeButtons.set("Ranked Flex")
gamemode.grid(row = 1, padx = 50, pady = 30, sticky = 'NS')

gameInfoData = tk.CTkFrame(main)
gameInfoData.grid(row = 3, padx = 50, pady = 0, sticky = 'NS')
gameInfoData1 = tk.CTkFrame(main)
gameInfoData1.grid(row = 4, padx = 50, pady = 15, sticky = 'NS')

i = 0
for x in gameInfoColumns:
    if i < 7:
        x = tk.CTkCheckBox(gameInfoData, text = x, )
        x.pack(side = 'left')
    else:
        x = tk.CTkCheckBox(gameInfoData1, text = x)
        x.pack(side = 'left')
    i+= 1

gameInfoTop = tk.CTkFrame(main)
gameInfoTop.grid(row = 2, pady = 7.5, sticky = "NS")

selectAllInfo = tk.CTkCheckBox(gameInfoTop, text = 'Select All Stats')
selectAllInfo.pack(side = 'left')

users = tk.CTkFrame(main)
users.grid(row = 6, padx = 20, sticky = "NS")

for x in userList:
    x = tk.CTkCheckBox(users, text = x)
    x.pack(side = 'left')

usersTop = tk.CTkFrame(main)
usersTop.grid(row = 5, pady = 7.5, sticky = "NS")

selectAllUsers = tk.CTkCheckBox(usersTop, text = 'Select All Users')
selectAllUsers.pack(side = 'left')



main.mainloop()

