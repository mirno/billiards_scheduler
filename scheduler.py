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
        loc_availability = location.get("availability", [])
        locations[loc_name] = {"billiards": loc_billiards, "availability": loc_availability}
        for team in location["teams"]:
            teams[team] = loc_name
    return teams, locations

def generate_initial_schedule(teams):
    """Generates a double round-robin schedule for the teams"""
    team_list = list(teams.keys())
    n = len(team_list)
    matches = []
    for i in range(n-1):
        for j in range(i+1, n):
            matches.append((team_list[i], team_list[j])) # Each team plays every other team twice
            matches.append((team_list[j], team_list[i]))
    return matches

def assign_locations_to_matches(schedule, teams, locations):
    """Assigns locations to matches based on teams' home locations"""
    for i in range(len(schedule)):
        team1, team2 = schedule[i]
        if locations[teams[team1]]["billiards"] > 0:
            schedule[i] = (team1, team2, teams[team1])
            locations[teams[team1]]["billiards"] -= 1
        elif locations[teams[team2]]["billiards"] > 0:
            schedule[i] = (team1, team2, teams[team2])
            locations[teams[team2]]["billiards"] -= 1
        else:
            schedule[i] = (team1, team2, "Unassigned")
    return schedule

def adjust_home_streaks(schedule):
    """Ensures that no team has more than two consecutive home games"""
    home_streaks = {}
    for i in range(len(schedule)):
        team1, team2, location = schedule[i]
        if location == team1:
            home_streaks[team1] = home_streaks.get(team1, 0) + 1
            home_streaks[team2] = 0
        else:
            home_streaks[team2] = home_streaks.get(team2, 0) + 1
            home_streaks[team1] = 0

        if home_streaks[team1] > 2:
            for j in range(i+1, len(schedule)):
                if schedule[j][2] == team2 and home_streaks[team2] < 2:
                    schedule[i], schedule[j] = schedule[j], schedule[i]
                    home_streaks[team1] = 1
                    break
        elif home_streaks[team2] > 2:
            for j in range(i+1, len(schedule)):
                if schedule[j][2] == team1 and home_streaks[team1] < 2:
                    schedule[i], schedule[j] = schedule[j], schedule[i]
                    home_streaks[team2] = 1
                    break
    return schedule

def generate_match_dates(start_date, num_matches):
    # generates a list of dates for the matches, one per week, skipping weeks when necessary
    dates = []
    current_date = start_date
    for _ in range(num_matches):
        dates.append(current_date)
        current_date += timedelta(weeks=1)
    return dates


data = load_data('teams.yml')
teams, locations = generate_teams_and_locations(data)
schedule = generate_initial_schedule(teams)
schedule = assign_locations_to_matches(schedule, teams, locations)
schedule = adjust_home_streaks(schedule)

start_date = datetime.strptime('2023-06-06', '%Y-%m-%d')  # Example start date
match_dates = generate_match_dates(start_date, len(schedule))
# Assign dates to matches here


