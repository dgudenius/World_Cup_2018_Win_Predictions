# This Python file uses the following encoding: utf-8
import csv
import math
import pandas as pd

HFA = 100.0  # Home field advantage is worth Elo points
K = 27  # The speed at which Elo ratings change
Tourn = 2 # Multiplier for tournaments
Friend = 1 # Multiplier for Friendly
REVERT = 1/20.0# Between seasons, a team retains 2/3 of its previous season's rating

# REVERSIONS = {'CBD1925': 1502.032, 'RAC1926': 1403.384, 'LOU1926': 1307.201, 'CIB1927': 1362.919, 'MNN1929': 1306.702, # Some between-season reversions of unknown origin
#              'BFF1929': 1331.943, 'LAR1944': 1373.977, 'PHI1944': 1497.988, 'ARI1945': 1353.939, 'PIT1945': 1353.939, 'CLE1999': 1300.0}

class Forecast_soccer:

    @staticmethod
    def forecast(games):
        """ Generates win probabilities in the my_prob1 field for each game based on Elo model """

        # Initialize team objects to maintain ratings
        teams = {}
        for row in [item for item in csv.DictReader(open("elo_rankings_init.csv"))]:
            teams[row['country_full']] = {
                'name': row['country_full'],
                'year': None,
                'elo': float(row['elo']),
            }

        for game in games:
            home_team, away_team = teams[game['home_team']], teams[game['away_team']]

            # Revert teams at the start of seasons
            for team in [home_team, away_team]:
                if team['year'] and game['year'] != team['year']:
                    k = "%s%s" % (team['name'], game['year'])
            #        if k in REVERSIONS:
            #            team['elo'] = REVERSIONS[k]
            #        else:
                    team['elo'] = 1505.0*REVERT + team['elo']*(1-REVERT)
                    team['year'] = game['year']

            # Elo difference includes home field advantage
            #elo_diff = home_team['elo'] - away_team['elo'] + (0 if game['neutral'] == True else HFA)
            if (game['neutral']) == "True":
                neutral2 = 2
            else: neutral2 = 0
            print neutral2
            if neutral2 == 0:
                elo_diff = (home_team['elo']+HFA)-away_team['elo']
                print(elo_diff)
            else:
                elo_diff = home_team['elo'] - away_team['elo']


            # This is the most important piece, where we set my_prob1 to our forecasted probability
            if game['elo_prob1'] == None:
               game['my_prob1'] = 1.0 / (math.pow(10.0, (-elo_diff / 400.0)) + 1.0)
            else: game['my_prob1'] = game['elo_prob1']

            # If game was played, maintain team Elo ratings
            if game['home_score'] != None and game['away_score'] != None:
                # Margin of victory is used as a K multiplier
                if game['home_score']== game['away_score']:
                    game['result1']=0.5
                elif game['home_score'] >= game['away_score']:
                    game['result1']= 1.0
                else: game['result1']= 0.0

                pd = abs(game['home_score'] - game['away_score'])
                mult = math.log(max(pd, 1) + 1.0) * (2.2 / (1.0 if game['result1'] == 0.5 else ((elo_diff if game['result1'] == 1.0 else -elo_diff) * 0.001 + 2.2)))
                if game['tournament']!='Friendly':
                    mult = mult*Tourn
                else: mult = mult*Friend

                # Elo shift based on K and the margin of victory multiplier
                shift = (K * mult) * (game['result1'] - game['my_prob1'])

                # Apply shift
                home_team['elo'] += shift
                away_team['elo'] -= shift
            print(team)