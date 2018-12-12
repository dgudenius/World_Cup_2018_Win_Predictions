# This Python file uses the following encoding: utf-8
import csv
import math
import pandas as pd
import unicodedata

transfer_markt_rankings = pd.read_csv('fifa_values.csv')
transfer_markt_rankings = transfer_markt_rankings.replace({"IR Iran": "Iran", "Czechoslovakia": "Czech Republic", 'Germany DR': 'Germany', 'South Korea': 'Korea Republic'})
transfer_markt_rankings.to_csv('fifa_init.csv', index=False)