# This Python file uses the following encoding: utf-8
from util2 import *
from forecast_soccer_markt_value import *


# Read historical games from CSV
games = Util2.read_games("future_matches.csv")

# Forecast every game
Forecast_soccer_markt_value.forecast(games)

# Evaluate our forecasts against Elo
Util2.evaluate_forecasts(games)


