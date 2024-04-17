import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt

ROUND_1_SUBMISSION_LINK = "REDACTED"
df = pd.read_csv(ROUND_1_SUBMISSION_LINK)
df['Name'] = df['Name'].str.lower().str.replace(" ", "")
df['kerb (without @mit.edu)'] = df['kerb (without @mit.edu)'].str.lower()
df = df.drop_duplicates(subset=['Name'], keep='last')
df["Wins"] = 0
df.reset_index(inplace=True)

# check if submission is valid
# i.e. make sure troops sum to 100
invalid_submissions = []
for i in range(len(df)):
    total = 0
    for j in range(1, 11):
        total += df.iloc[i]["Castle {}".format(j)]
    if total != 100:
        print("{}'s submission is invalid :/".format(df.loc[i, "Name"]))
        invalid_submissions.append(df.loc[i, "Name"])
    
for submission in invalid_submissions:
    print(submission)
    df = df[df["Name"] != submission]

df = df.reset_index(drop=True)

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
    df.loc[hero, "Wins"] = wins

df = df.sort_values(by="Wins", ascending=False)
df.drop(columns=["Timestamp", "index"], inplace=True)
df.head(10).to_csv("./results/round1/top10.csv", encoding='utf-8', index=False)
extended_results = df.copy()
extended_results.drop(columns=["Name", "kerb (without @mit.edu)"], inplace=True)
extended_results.to_csv("./results/round1/extended.csv", encoding='utf-8', index=False)
