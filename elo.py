# This Python file uses the following encoding: utf-8
import csv
import math
import pandas as pd

elo_matches = pd.read_csv('results_new.csv')
elo_matches['elo_home'] = 1500
elo_matches['elo_away'] = 1500
elo_matches['elo_prob1'] = None
elo_matches = elo_matches.replace({"IR Iran": "Iran", "Czechoslovakia": "Czech Republic",'Ireland': 'Republic of Ireland', 'Germany DR': 'Germany', 'German DR': 'Germany', 'China': 'China PR', 'Vietnam Republic': 'Vietnam', 'Kyrgyzstan': 'Kyrgyz Republic', 'North Vietnam': 'Vietnam', 'Ivory Coast': "Côte d'Ivoire", 'Yemen DPR': 'Yemen', 'Sint Maarten': 'St. Martin', 'Bosnia-Herzegovina': 'Bosnia and Herzegovina','Macedonia': 'FYR Macedonia'})

elo_matches['date'] = pd.to_datetime(elo_matches['date'])
elo_matches.to_csv('elo_matches_new.csv', index=False)

elo_rankings = pd.read_csv('elo_rankings.csv')
elo_rankings['elo'] = 1500
elo_rankings = elo_rankings.replace({"IR Iran": "Iran", "Czechoslovakia": "Czech Republic", 'Germany DR': 'Germany'})
elo_rankings.to_csv('elo_rankings_init2.csv', index=False)

