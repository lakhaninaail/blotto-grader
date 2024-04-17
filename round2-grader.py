import pandas as pd

ROUND_2_SUBMISSION_LINK = "REDACTED"
KERB = "kerb (without @mit.edu)"


df = pd.read_csv(ROUND_2_SUBMISSION_LINK)
df[KERB] = df[KERB].str.lower()
df['Name'] = df['Name'].str.lower().str.replace(" ", "")
df = df.drop_duplicates(subset=[KERB], keep='last')
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
        print("{}'s submission is invalid :/".format(df.loc[i, KERB]))
        invalid_submissions.append(df.loc[i, KERB])
    
for submission in invalid_submissions:
    print(submission)
    df = df[df[KERB] != submission]

df = df.reset_index(drop=True)

for hero in range(len(df)):
    wins = 0
    for villain in range(len(df)):
        if hero != villain:
            hero_score, villain_score = 0, 0
            for castle in range(1, 11):
                hero_alloc = df.iloc[hero]["Castle {}".format(castle)]
                villain_alloc = df.iloc[villain]["Castle {}".format(castle)]
                if hero_alloc >= villain_alloc + castle:
                    hero_score += castle
                elif villain_alloc >= hero_alloc + castle:
                    villain_score += castle
            if hero_score > villain_score:
                wins += 1
    df.loc[hero, "Wins"] = wins

df = df.sort_values(by="Wins", ascending=False)
df.drop(columns=["Timestamp", "index"], inplace=True)
df.head(10).to_csv("./results/round2/top10.csv", encoding='utf-8', index=False)
extended_results = df.copy()
extended_results.drop(columns=["Name", KERB], inplace=True)
extended_results.to_csv("./results/round2/extended.csv", encoding='utf-8', index=False)
