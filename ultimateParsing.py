import pandas as pd
import csv
import numpy as np
import glob




def assistDetection(input_team, input_year):
	'''
	user inputs a specific team and year, then the function pulls up the names of everyone 
	on the relevant roster and searches through the 82 games of data to look for passing activity 
	between players on the team. As it iterates through the season-worth of games, it will create
	a list of list to record the interaction between the passer and the receiver. The size of the 
	list is determined by the size of the roster. If a team has 15 players, the function will generate
	a 15 by 15 list.
	'''

	player_names = "team_roster_by_season.csv"
	'''
	this file is prepared manually. In Chrome, visit www.basketball-reference.com, 
	and use a Chrome extension called "Copytables" to select and copy the column of names
	'''
	reviews = pd.read_csv(player_names)
	first_row = list(reviews.columns)
	team_year_title = input_team + " " + input_year
	team_year_titleInsideTeamRoster = input_team + " " + input_year
	for teams in range(0,len(first_row)):
		if team_year_titleInsideTeamRoster == first_row[teams]:
			desiredTeam = teams
		else:
			teams +=2

	team_roster = reviews.iloc[0:, desiredTeam]
	team_roster_list = list(team_roster)
	cleaned_team_roster = [x for x in team_roster_list if str(x) != 'nan']

	organize = team_year_title.lower() + " organize.csv"
	organize_address = input_team + "/" + team_year_title + "/" + organize

	tally = team_year_title.lower() + " tally.csv" 
	tally_address = input_team + "/" + team_year_title + "/" + tally

	game_counter = 1
	total_assist_table = [[0 for assistee in range(len(cleaned_team_roster))] for assister in range(len(cleaned_team_roster))]
	roster_size = len(cleaned_team_roster)

	file_name = glob.glob(input_team + "/" + team_year_title + "/" + "Spurs*")

	while(True):
		try:
			# iterate each game in a season
			# file_name = input_team + str(game_counter) + ".csv"
			file_address = file_name[game_counter-1]
			print file_address
			reviews = pd.read_csv(file_address)
			print reviews
			action = reviews.iloc[1:,2]
			filtered_action = action.str.contains('assists', case=False, na=False)
			assist = action[filtered_action]
			assist_list = list(assist)
			occurence = len(assist)-1
			team_dictionary = {		# dictionary
					team_roster_list[i] : i  # key : value where key = player name, value = index
					for i in range(len(team_roster_list))
				}

			assist_table = [
					[0 for assistee in range(len(team_roster_list))] # inner list
					for assister in range(len(team_roster_list))
				]
		# parsing for all assist interactions
			for counter in range(0, occurence):
				giver = assist_list[counter].split('(')[1].split(' assists')[0]
				receiver = assist_list[counter].split(' makes')[0]
				if giver in team_roster_list and receiver in team_roster_list:
					assist_table[team_dictionary[giver]][team_dictionary[receiver]]+=1
					total_assist_table[team_dictionary[giver]][team_dictionary[receiver]]+=1
				else:
					continue
			game_counter += 1
			print game_counter
			# print assist_list
		except:
			break

	for x in range(0,len(total_assist_table)):
		row_sum = sum(total_assist_table[x])
		total_assist_table[x].append(row_sum)

		# saving into csv
	with open(organize_address, "w") as f:
		writer = csv.writer(f)
		headers = tuple(team_roster_list)
		writer.writerow(headers)
		writer.writerows(total_assist_table)

	return total_assist_table, roster_size, cleaned_team_roster, tally_address


def nineByNineTable(total_assist_table, roster_size, cleaned_team_roster, tally_address):
	'''
	In order to visually standardize the graphs, this function will pick out the top 8 passers from 
	the team of a specific season, and group everyone else into 'Other'. With this design, each graph 
	will feature 9 players around the circle. This allows the viewer to focus on the most significant interactions.
	'''
	starter_list = []
	other_list = []
	updated_roster = []
	sorted_index_List = []
	numberofStarter = 8
	endofList = roster_size

	# sort entire roster numerically based on total assist contribution from that year. Descending
	for index in range(0, roster_size):
		sorted_index_List.append(total_assist_table[index][roster_size])
	sorted_index_List = np.array(sorted_index_List)
	sorted_index_List = sorted_index_List.argsort()
	sorted_index_List = sorted_index_List.tolist()
	sorted_index_List.reverse()

	# sort the 8 highest contributors into starter_list, and everyone else into 'Other'
	for passer_index in range(0,numberofStarter):
		starter_list.append(cleaned_team_roster[sorted_index_List[passer_index]])
	for receiver_index in range(numberofStarter, roster_size):
		other_list.append(cleaned_team_roster[sorted_index_List[receiver_index]])

	#  create a dictionary to map player names to their position on the total_assist_table
	team_roster_dictionary = {k: v for v, k in enumerate(cleaned_team_roster)}

	# create 9x9 table for starters and other
	starter_table = [[0 for start_passer in range(numberofStarter+1)] for start_receiver in range((numberofStarter+1))]

	# copy starter stats from total_assist_table
	for passer in range(len(starter_list)):
		for receiver in range(len(starter_list)):
			if receiver == passer:
				continue
			else:
				starter_table[passer][receiver] = total_assist_table[team_roster_dictionary[starter_list[passer]]][team_roster_dictionary[starter_list[receiver]]]

	# fill up exterior of new table with interactions involving 'Other' players
	# starter passer to 'Other' receiver
	for passer in range(numberofStarter):
		for receiver in range(len(other_list)):
			starter_table[passer][numberofStarter] += total_assist_table[team_roster_dictionary[starter_list[passer]]][team_roster_dictionary[other_list[receiver]]]
	# 'Other' passer to starter receiver
	for receiver in range(numberofStarter):
		for passer in range(len(other_list)):
			starter_table[numberofStarter][receiver] += total_assist_table[team_roster_dictionary[other_list[passer]]][team_roster_dictionary[starter_list[receiver]]]
	# 'Other' passer to other receiver
	for passer in range(len(other_list)):
		for receiver in range(len(other_list)):
			starter_table[numberofStarter][numberofStarter] += total_assist_table[team_roster_dictionary[other_list[passer]]][team_roster_dictionary[other_list[receiver]]]

	starter_list.append("Other")
	print("starter_list", starter_list)

	# reorganize data structure into 3 columns of passer, receiver, and # of assist
	for passer in range(numberofStarter+1):
		for receiver in range(numberofStarter+1):
			parsed_list = ["passer", "receiver", 1]
			parsed_list[0] = starter_list[passer]
			parsed_list[1] = starter_list[receiver]
			parsed_list[2] = starter_table[passer][receiver]
			updated_roster.append(parsed_list)

	# save into 3 column adjacency list
	column_names = ["passer", "receiver", "assist"]
	with open(tally_address, "w") as f:
		writer = csv.writer(f)
		headers = tuple(column_names)
		writer.writerow(headers)
		writer.writerows(updated_roster)



# cd Desktop/classes/NBA/webscraping/data/scrapingDone
current_team = "Spurs"
for current_year in range(2015,2015+1):
	print current_year
	total_assist_table, roster_size, cleaned_team_roster, tally_address = assistDetection(current_team, str(current_year))
	nineByNineTable(total_assist_table, roster_size, cleaned_team_roster, tally_address)

