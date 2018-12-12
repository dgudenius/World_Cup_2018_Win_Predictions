import csv
import math
import pandas as pd

fifa_rankings = pd.read_csv('fifa_ranking.csv')
fifa_rankings = fifa_rankings.loc[:,['rank', 'country_full', 'country_abrv', 'cur_year_avg', 'rank_date']]
fifa_rankings = fifa_rankings.replace({"IR Iran": "Iran"})
fifa_rankings['rank_date'] = pd.to_datetime(fifa_rankings['rank_date'])

matches = pd.read_csv('results.csv')
matches =  matches.replace({'Germany DR': 'Germany', 'China': 'China PR'})
matches['date'] = pd.to_datetime(matches['date'])

fifa_rankings = fifa_rankings.set_index(['rank_date'])\
            .groupby(['country_full'], group_keys=False)\
            .resample('D').first()\
            .fillna(method='ffill')\
            .reset_index()
matches = matches.merge(fifa_rankings,
                        left_on=['date', 'home_team'],
                        right_on=['rank_date', 'country_full'])
matches = matches.merge(fifa_rankings,
                        left_on=['date', 'away_team'],
                        right_on=['rank_date', 'country_full'],
                        suffixes=('_home', '_away'))
matches.to_csv('matches2.csv', index=False)

csv_fifa = pd.read_csv('fifa_ranking.csv')
csv_master = pd.read_csv('master_rankings.csv')
csv_elo = pd.read_csv('elo_rankings.csv')

csv_master = csv_master.append(csv_fifa)
csv_master = csv_master.append(csv_elo)
csv_master.to_csv('output.csv', index=False)