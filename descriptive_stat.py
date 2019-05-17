import pandas as pd
import csv
import numpy as np
from decimal import *

total_team = ["Mavericks","Warriors","Lakers","Rockets","Heat","Celtics","Bucks","Spurs"]
input_year = 2005
out2in_list = []
updated_roster = []

for i in range(0,len(total_team)):
	print total_team[i]
	for year in range(2015, input_year-1, -1):
		team_year_title = total_team[i] + " " + str(year)
		tally = team_year_title.lower() + " tally.csv"
		tally_address = total_team[i] + "/" + team_year_title + "/" + tally
		reviews = pd.read_csv(tally_address)

		# calculate outgoing and incoming totals for 9 players
		outgoing = {}
		incoming = {}

		for row in range(0,len(reviews)):
			if reviews.iloc[row,0] not in outgoing:
				outgoing[reviews.iloc[row,0]]=0
				outgoing[reviews.iloc[row,0]] += reviews.iloc[row,2]
			else:
				outgoing[reviews.iloc[row,0]] += reviews.iloc[row,2]

			if reviews.iloc[row,1] not in incoming:
				incoming[reviews.iloc[row,1]]=0
				incoming[reviews.iloc[row,1]] += reviews.iloc[row,2]
			else:
				incoming[reviews.iloc[row,1]] += reviews.iloc[row,2]
		total_outgoing = sum(outgoing.itervalues())
		total_incoming = sum(incoming.itervalues())

		# calculate total contribution and out2in
		total_contribution = {}
		out2in ={}

		for player in range(0,len(outgoing)):
			total_contribution[outgoing.keys()[player]] = outgoing[outgoing.keys()[player]]+incoming[incoming.keys()[player]]
			# print(year, total_contribution)
			out2in[outgoing.keys()[player]] = Decimal((outgoing[outgoing.keys()[player]]-incoming[incoming.keys()[player]]))/Decimal((outgoing[outgoing.keys()[player]]+incoming[incoming.keys()[player]]))


		parsed_list = ["team","year","total contri","out2in"]
		parsed_list[0] = total_team[i]
		parsed_list[1] = year
		parsed_list[2] = np.var(list(total_contribution.values()))
		parsed_list[3] = np.var(list(out2in.values()))
		updated_roster.append(parsed_list)


	# save into 3 column adjacency list
	column_names = ["team", "year", "contri var", "out2in var"]
	with open("zdata processing/rawSummary3.csv", "w") as f:
		writer = csv.writer(f)
		headers = tuple(column_names)
		writer.writerow(headers)
		writer.writerows(updated_roster)
