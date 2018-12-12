# This Python file uses the following encoding: utf-8
import csv

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve

class Util2:
    @staticmethod
    def read_games(file):
        """ Initializes game objects from csv """
        games = [item for item in csv.DictReader(open(file))]

        # Uncommenting these three lines will grab the latest game results for 2017, update team ratings accordingly, and make forecasts for upcoming games
        #file_2017 = file.replace(".", "_2017.")
        #urlretrieve("https://projects.fivethirtyeight.com/nfl-api/2017/nfl_games_2017.csv", file_2017)
        #games += [item for item in csv.DictReader(open(file_2017))]

        for game in games:
            if game['home_score'] == '':
                game['result1'] = None
            elif game['home_score'] > game['away_score']:
                game['result1'] = 1
            elif game['home_score'] < game['away_score']:
                game['result1'] = 0
            else: game['result1'] = 0.5

            game['year'], game['neutral'], game['tournament'] = int(game['date'][:4]), str(game['neutral']), str(
                game['tournament'])
            game['home_score'], game['away_score'] = float(game['home_score']) if game['home_score'] != '' else None, float(
                game['away_score']) if game['away_score'] != '' else None
            game['elo_prob1'], game['result1'] = float(game['elo_prob1']) if game['elo_prob1'] != '' else None, float(
                game['result1']) if game['result1'] != None else None
        return games

    @staticmethod
    def evaluate_forecasts(games):
        """ Evaluates and scores forecasts in the my_prob1 field against those in the elo_prob1 field for each game """
        my_points_by_season, elo_points_by_season, spread_point_diff_by_season, avg_spread_point_diff, = {}, {}, {}, {}

        forecasted_games = [g for g in games if g['result1'] != None]
        upcoming_games = [g for g in games if g['result1'] == None and 'my_prob1' in g]
        # Evaluate forecasts and group by season
        for game in forecasted_games:

            # Skip unplayed games and ties
            if game['result1'] == None or game['result1'] == 0.5:
                continue

            if game['year'] not in elo_points_by_season:
                elo_points_by_season[game['year']] = 0.0
                my_points_by_season[game['year']] = 0.0
                spread_point_diff_by_season[game['year']] = 0.0
                avg_spread_point_diff[game['year']] = 0.0
                i_value = 0.0


            # Calculate elo's points for game
            #rounded_elo_prob = round(game['elo_prob1'], 2)
            #elo_brier = (rounded_elo_prob - game['result1']) * (rounded_elo_prob - game['result1'])
            #elo_points = round(25 - (100 * elo_brier), 1)
            #if game['tournament'] != 'Friendly':
            #    elo_points *= 2
            #elo_points_by_season[game['year']] += elo_points

            # Calculate my points for game
            rounded_my_prob = round(game['my_prob1'], 2)
            my_brier = (rounded_my_prob - game['result1']) * (rounded_my_prob - game['result1'])
            my_points = round(25 - (100 * my_brier), 1)
            if game['tournament'] != 'Friendly':
                my_points *= 2
            my_points_by_season[game['year']] += my_points

            # Calculate spread points
            #round_point_spread = round(game['point_diff2'],2)
            #actual_point_diff = game['score1']-game['score2']
            #spread_point_diff = abs(actual_point_diff - round_point_spread)
            #spread_point_diff_by_season[game['season']] += spread_point_diff
            #i_value += 1
            #avg_spread_point_diff[game['season']] = spread_point_diff_by_season[game['season']] / i_value


         # Print individual seasons
        #for season in my_points_by_season:

        #    print("In %s, your forecasts would have gotten %s points. Elo got %s points. Spread Diff Points %s Point Diff Avg %s" % (
        #    season, round(my_points_by_season[season], 2), round(elo_points_by_season[season], 2), round(spread_point_diff_by_season[season], 2), round(avg_spread_point_diff[season],2)))

        # Show overall performance
        # my_avg = sum(my_points_by_season.values()) / len(my_points_by_season.values())
        #elo_avg = sum(elo_points_by_season.values()) / len(elo_points_by_season.values())
        #point_diff_avg = sum(spread_point_diff_by_season.values()) / len(spread_point_diff_by_season.values())
        #avg_spread_point_diff= sum(avg_spread_point_diff.values()) / len(avg_spread_point_diff.values())
        #print("\nOn average, your forecasts would have gotten %s points per season. Elo got %s points per season. Points Diff/season %s Point diff/game avg %s \n" % (
        #round(my_avg, 2), round(elo_avg, 2),round(point_diff_avg,2), round(avg_spread_point_diff,2)))


        # Print forecasts for upcoming games
        if len(upcoming_games) > 0:
            print("Forecasts for upcoming games:")
            for game in upcoming_games:
                print("%s %s vs. %s%% " % (game['date'], game['home_team'], game['away_team']),int(round(100 * game['my_prob1'])))
               #print("%s\t%s vs. %s\t\t%s%% (Elo)\t\t%s%% (You) Point Diff %s    Point Diff2 %s" % (game['date'], game['team1'], game['team2'], int(round(100 * game['elo_prob1'])),int(round(100 * game['my_prob1'])),game['point_diff'],game['point_diff2']))
