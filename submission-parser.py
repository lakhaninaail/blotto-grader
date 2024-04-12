import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt

df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQjOztXo13t00zdGX2HAkJKD3yFylTy-9YlOW8vJGqh43lyybFVTLPK7vw1lxfoP1kE3_neEECs25oL/pub?gid=1427731383&single=true&output=csv")
df['Name'] = df['Name'].str.lower().str.replace(" ", "")
df = df.drop_duplicates(subset=['Name'], keep='last')
df["Wins"] = 0
df.reset_index(inplace=True)
heatmap_df = df.copy()
for player in range(35):
    heatmap_df["player{}".format(player)] = 0

# check if submission is valid
# i.e. make sure troops sum to 100
invalid_submissions = []
for i in range(len(df)):
    # if df.iloc[i][2:12].sum() != 100:
    #     print("Submission {} is invalid".format(df.iloc[i]["Name"]))
    #     df.drop(i, inplace=True)
    total = 0
    for j in range(1, 11):
        total += df.iloc[i]["Castle {}".format(j)]
    if total != 100:
        print("{}'s submission is invalid :/".format(df.loc[i, "Name"]))
        invalid_submissions.append(df.loc[i, "Name"])
    
for submission in invalid_submissions:
    df = df[df["Name"] != submission]

for hero in range(len(df)):
    wins = 0
    for villain in range(len(df)):
        if hero != villain:
            score = 0
            for castle in range(1, 11):
                hero_alloc = df.iloc[hero]["Castle {}".format(castle)]
                villain_alloc = df.iloc[villain]["Castle {}".format(castle)]
                if hero_alloc > villain_alloc:
                    score += castle
                elif hero_alloc == villain_alloc:
                    score += 0.5 * castle
            if score > 27.5:
                wins += 1
                heatmap_df.loc[hero, "player{}".format(villain)] = 1
    df.loc[hero, "Wins"] = wins

df = df.sort_values(by="Wins", ascending=False)
df.reset_index(inplace=True)
player_nums = ["player{}".format(player) for player in range(1, 35)]
heatmap_df.drop(columns=["index", "Timestamp", "Wins"], inplace=True)
heatmap_df.index = df["Name"]
heatmap_df.drop("Name", axis=1, inplace=True)
castle_cols = ["Castle {}".format(castle) for castle in range(1, 11)]
heatmap_df.drop(columns=castle_cols, inplace=True)
#print(heatmap_df)
heatmap_df.columns = list(df["Name"])
#sn.heatmap(heatmap_df)
plt.show()
df.index += 1
df.drop(columns=["level_0"], inplace=True)
df.head(10).to_csv("./results/round1-top10.csv", encoding='utf-8', index=False)
extended_results = df.copy()
extended_results.drop(columns=["Timestamp", "Name", "index"], inplace=True)
extended_results.to_csv("./results/round1-extended.csv", encoding='utf-8', index=False)
