# This Python file uses the following encoding: utf-8
from util2 import *
from forecast_soccer import *


# Read historical games from CSV
games = Util2.read_games("elo_matches_new.csv")

# Forecast every game
Forecast_soccer.forecast(games)

# Evaluate our forecasts against Elo
Util2.evaluate_forecasts(games)


