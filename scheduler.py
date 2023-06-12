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
    # this should generate a double round-robin schedule
    # without considering any of the constraints
    # placeholder for your code here
    pass

def assign_locations_to_matches(schedule, teams, locations):
    # this should go through the schedule and for each match
    # assign it to the home location of one of the teams
    # if the location is already full or not available on that day, skip that match to a later date
    # placeholder for your code here
    pass

def adjust_home_streaks(schedule):
    # this should go through the schedule and for each team
    # ensure they have no more than two consecutive home games
    # if a team has more than two consecutive home games, swap this match with another one
    # placeholder for your code here
    pass

def generate_match_dates(start_date, num_matches):
    # generates a list of dates for the matches, one per week, skipping weeks when necessary
    dates = []
    current_date = start_date
    for _ in range(num_matches):
        dates.append(current_date)
        current_date += timedelta(weeks=1)
    return dates

def main():
    data = load_data('teams.yaml')
    teams, locations = generate_teams_and_locations(data)
    schedule = generate_initial_schedule(teams)
    schedule = assign_locations_to_matches(schedule, teams, locations)
    schedule = adjust_home_streaks(schedule)

    start_date = datetime.strptime('2023-06-06', '%Y-%m-%d')  # Example start date
    match_dates = generate_match_dates(start_date, len(schedule))
    # Assign dates to matches here

main()
