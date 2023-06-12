import yaml
from datetime import datetime, timedelta

def load_data(file_name):
    with open(file_name, 'r') as stream:
        data = yaml.safe_load(stream)
    return data

def generate_teams_and_locations(data):
    teams = {}
    locations = {}
    for location in data:
        loc_name = location["location"]
        loc_billiards = location["numberOfBiljarts"]
        loc_unavailableDates = [datetime.strptime(date, '%Y-%m-%d') for date in location.get("unavailableDates", [])]
        locations[loc_name] = {"billiards": loc_billiards, "unavailableDates": loc_unavailableDates}
        for team in location["teams"]:
            teams[team] = loc_name
    return teams, locations

def generate_initial_schedule(teams):
    team_list = list(teams.keys())
    n = len(team_list)
    matches = []
    for i in range(n-1):
        for j in range(i+1, n):
            matches.append((team_list[i], team_list[j])) # Each team plays every other team twice
            matches.append((team_list[j], team_list[i]))
    return matches

def adjust_home_streaks(schedule):
    home_streaks = {}
    for i in range(len(schedule)):
        match, _ = schedule[i]
        team1, team2, location = match
        if location == team1:
            home_streaks[team1] = home_streaks.get(team1, 0) + 1
            home_streaks[team2] = 0
        else:
            home_streaks[team2] = home_streaks.get(team2, 0) + 1
            home_streaks[team1] = 0
        if home_streaks[team1] > 2:
            for j in range(i+1, len(schedule)):
                future_match, _ = schedule[j]
                if future_match[2] == team2 and home_streaks[team2] < 2:
                    schedule[i], schedule[j] = schedule[j], schedule[i]
                    home_streaks[team1] = 1
                    break
        elif home_streaks[team2] > 2:
            for j in range(i+1, len(schedule)):
                future_match, _ = schedule[j]
                if future_match[2] == team1 and home_streaks[team1] < 2:
                    schedule[i], schedule[j] = schedule[j], schedule[i]
                    home_streaks[team2] = 1
                    break
    return schedule

def generate_match_dates(start_date, num_matches):
    match_dates = []
    current_date = start_date
    for _ in range(num_matches):
        match_dates.append(current_date)
        current_date += timedelta(weeks=1)
    return match_dates

def assign_location_to_match(match, teams, locations, current_date):
    team1, team2 = match
    if locations[teams[team1]]["billiards"] > 0 and current_date not in locations[teams[team1]]["unavailableDates"]:
        locations[teams[team1]]["billiards"] -= 1
        return (team1, team2, teams[team1])
    elif locations[teams[team2]]["billiards"] > 0 and current_date not in locations[teams[team2]]["unavailableDates"]:
        locations[teams[team2]]["billiards"] -= 1
        return (team1, team2, teams[team2])
    return None

def schedule_matches(start_date, data):
    teams, locations = generate_teams_and_locations(data)
    matches = generate_initial_schedule(teams)

    current_date = start_date
    schedule = []
    for match in matches:
        # If all locations are unavailable on the current date, move to the next week
        while all(current_date in loc_data["unavailableDates"] for loc_data in locations.values()):
            current_date += timedelta(weeks=1)

        assigned = assign_location_to_match(match, teams, locations, current_date)
        if assigned is None:
            current_date += timedelta(weeks=1)
            continue

        schedule.append((assigned, current_date))
        current_date += timedelta(weeks=1)

    schedule = adjust_home_streaks(schedule)
    return schedule


# Usage
data = load_data('teams.yml')
start_date = datetime.strptime('2023-06-06', '%Y-%m-%d')
schedule = schedule_matches(start_date, data)

'''
data = load_data('teams.yml')
teams, locations = generate_teams_and_locations(data)
schedule = generate_initial_schedule(teams)
schedule = assign_locations_to_matches(schedule, teams, locations)
schedule = adjust_home_streaks(schedule)

start_date = datetime.strptime('2023-06-06', '%Y-%m-%d')  # Example start date
match_dates = generate_match_dates(start_date, len(schedule))
# Assign dates to matches here
'''




