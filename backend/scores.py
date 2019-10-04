import urllib.request
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from urllib.request import Request
from urllib.request import urlopen

RATINGS_URL = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/2019/segments/0/leagues/1172646?forTeamId=1&view=mMatchup"

with urllib.request.urlopen(RATINGS_URL) as url:
    data = json.loads(url.read().decode())
    # print(data)

df = [[
    game['matchupPeriodId'],
    game['home']['teamId'], game['home']['totalPoints'],
    game['away']['teamId'], game['away']['totalPoints']
] for game in data['schedule']]

df = pd.DataFrame(df, columns=['Week', 'Team1', 'Score1', 'Team2', 'Score2'])

# print(df.loc[df['Week'] == 4])

marginDf = df.assign(Margin1 = df['Score1'] - df['Score2'],
                     Margin2 = df['Score2'] - df['Score1'])

marginDf = (marginDf[['Week', 'Team1', 'Margin1']]
            .rename(columns={'Team1': 'Team', 'Margin1': 'Margin'})
            .append(marginDf[['Week', 'Team2', 'Margin2']]
            .rename(columns={'Team2': 'Team', 'Margin2': 'Margin'})))

fig, ax = plt.subplots(1,1, figsize=(16,6))

sns.boxplot(x='Team', y='Margin',
            data=marginDf,
            palette='muted')
ax.axhline(0, ls='--')
ax.set_xlabel('')
ax.set_title('Win/Loss margins')
plt.savefig('spread.png')
