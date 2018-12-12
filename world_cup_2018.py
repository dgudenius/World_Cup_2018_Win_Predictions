import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from matplotlib import pyplot as plt

world_cup = pd.read_csv('World Cup 2018 Dataset.csv')
world_cup = world_cup.loc[:, ['Team', 'Group', 'First match \nagainst', 'Second match\n against', 'Third match\n against']]
world_cup = world_cup.dropna(how='all')
world_cup = world_cup.replace({"IRAN": "Iran",
                               "Costarica": "Costa Rica",
                               "Porugal": "Portugal",
                               "Columbia": "Colombia",
                               "Korea" : "Korea Republic"})
world_cup = world_cup.set_index('Team')
print(world_cup)