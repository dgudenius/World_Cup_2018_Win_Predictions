# This Python file uses the following encoding: utf-8
import csv
import math
import sklearn
import numpy as np
import pandas as panda
import matplotlib.pyplot as plt

HFA = 100.0  # Home field advantage is worth Elo points
K = 27  # The speed at which Elo ratings change
Tourn = 2 # Multiplier for tournaments
Friend = 1 # Multiplier for Friendly
REVERT = 1/20.0# Between seasons, a team retains 95% of its previous season's rating
Goal_Expect = 2.7 #Expected average goals per game
Evaluations = 5000 #number of times simulated

# REVERSIONS = {'CBD1925': 1502.032, 'RAC1926': 1403.384, 'LOU1926': 1307.201, 'CIB1927': 1362.919, 'MNN1929': 1306.702, # Some between-season reversions of unknown origin
#              'BFF1929': 1331.943, 'LAR1944': 1373.977, 'PHI1944': 1497.988, 'ARI1945': 1353.939, 'PIT1945': 1353.939, 'CLE1999': 1300.0}

class Forecast_soccer_full:

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
            # print neutral2
            if neutral2 == 0:
                elo_diff = (home_team['elo']+HFA)-away_team['elo']
            #    print(elo_diff)
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
            if game['home_score'] == None and game['away_score'] == None:
                # Find team expected scores
                game['home_score_guess'] = game['my_prob1'] * Goal_Expect
                game['away_score_guess'] = Goal_Expect - game['home_score_guess']

                home_score_range = np.random.poisson(game['home_score_guess'], Evaluations)
                home_score_table = panda.DataFrame(data=home_score_range, columns=['home'])
                away_score_range = np.random.poisson(game['away_score_guess'], Evaluations)
                away_score_table = panda.DataFrame(data=away_score_range, columns=['away'])
                game_score_table = panda.concat([home_score_table, away_score_table], 1)
                #print(game_score_table)
                # game_score_range = home_score_table away_score_range)
                # print(home_score_range)
                # print(away_score_range)

                game_score_chart = panda.DataFrame(0,index=[0,1,2,3,4,5,6,7,8,9,10], columns=['0', '1', '2', '3', '4','5','6','7','8','9','10'])

                i = 0
                while i < Evaluations:
                    h = game_score_table.iloc[i, 0]
                    if h>11:
                        h=10
                    a = game_score_table.iloc[i, 1]
                    if a>10:
                        a=10
                    game_score_chart.iloc[a,h] = game_score_chart.iloc[a,h] + 1
                    i = i + 1
                    #if h>a:
                    #    print('home')
                    #if a>h:
                    #    print('away')
                    #if a==h:
                    #    print('draw')
                # print(game_score_chart)
                game_score_percent_chart = panda.DataFrame(game_score_chart)
                j = 0
                h2 = 0
                a2 = 0
                d2 = 0
                while j<10:
                    k = 0
                    while k<10:
                        game_score_percent_chart.iloc[j,k] = 100*float(game_score_percent_chart.iloc[j,k])/float(Evaluations)
                        if j > k:
                            h2 = h2 + (game_score_percent_chart.iloc[j,k])
                        if k > j:
                            a2 = a2 + (game_score_percent_chart.iloc[j,k])
                        if k == j:
                            d2 = d2 + (game_score_percent_chart.iloc[j,k])
                        k = k + 1
                    if k <= 10:
                        k = 0
                    j = j+1
                home_win_percent = h2
                away_win_percent = a2
                draw_percent = d2
                print(home_win_percent)
                print(away_win_percent)
                print(draw_percent)
                print(game_score_percent_chart)

               # print(game['home_team'])
               # print(game['away_team'])
            #print(team)