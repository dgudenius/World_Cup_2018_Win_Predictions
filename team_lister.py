import csv
import math

class team_lister:

    @staticmethod
    def team_lister(games):

        teams = {}
        for row in [item for item in csv.DictReader(open("results.csv"))]:
            if games