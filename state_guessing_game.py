"""
State guessing game

In this game, the user guesses a state 
based on recent weather data and state facts
"""

# Import libraries:
import requests
import json
import random

# Variables:

# List of state information containing the state, largest city (by population), latitude,
# longitude, state bird, state flower, and 2020 state population
state_locations = [
    ["Alabama","Huntsville",34.7376,-86.6266, "Yellowhammer", "Camellia", "5,024,279"],
    ["Alaska","Anchorage",61.2282,-149.9138, "Willow ptarmigan", "Forget-me-not", "733,391"],
    ["Arizona","Phoenix",33.446,-112.0743, "Cactus wren", "Saguaro cactus blossom", "7,151,502"],
    ["Arkansas","Little Rock",34.7714,-92.2961, "Northern mockingbird", "Apple blossom", "3,011,524"],
    ["California","Los Angeles",34.0511,-118.2554, "<state name> quail", "<state name> poppy", "39,538,223"],
    ["Colorado","Denver",39.7501,-104.9818, "Lark bunting", "<state name> blue columbine", "5,773,714"],
    ["Connecticut","Bridgeport",41.1761,-73.1889, "American robin", "Mountain laurel", "3,605,944"],
    ["Delaware","Wilmington",39.744,-75.5582, "<state name> Hen", "Peach blossom", "989,948"],
    ["Florida","Jacksonville",30.3736,-81.6647, "Northern mockingbird", "Orange blossom", "21,538,187"],
    ["Georgia","Atlanta",33.7697,-84.4026, "Brown thrasher", "Cherokee rose", "10,711,908"],
    ["Hawaii","Honolulu",21.3381,-157.8611, "<state name> goose", "<state name> hibiscus", "1,455,271"],
    ["Idaho","Boise",43.6217,-116.2121, "Mountain bluebird", "Syringa, mock orange", "1,839,106"],
    ["Illinois","Chicago",41.8702,-87.6372, "Northern cardinal", "Violet", "12,812,508"],
    ["Indiana","Indianapolis",39.7934,-86.1616, "Northern cardinal", "Peony", "6,785,528"],
    ["Iowa","Des Moines",41.5828,-93.6189, "Eastern goldfinch", "Wild rose", "3,190,369"],
    ["Kansas","Wichita",37.685,-97.3367, "Western meadowlark", "Sunflower", "2,937,880"],
    ["Kentucky","Louisville",38.2582,-85.7571, "Northern cardinal", "Goldenrod", "4,505,836"],
    ["Louisiana","New Orleans",29.9512,-90.0771, "Brown pelican", "Magnolia", "4,657,757"],
    ["Maine","Portland",43.6742,-70.2617, "Chickadee", "White pine cone and tassel", "1,362,359"],
    ["Maryland","Baltimore",39.291,-76.6093, "<city name> oriole", "Black-eyed susan", "6,177,224"],
    ["Massachusetts","Boston",42.3292,-71.0666, "Black-capped chickadee", "Mayflower", "7,029,917"],
    ["Michigan","Detroit",42.3311,-83.0539, "American robin", "Apple blossom", "10,077,331"],
    ["Minnesota","Minneapolis",44.9551,-93.2663, "Common loon", "Pink and white lady's slipper", "5,706,494"],
    ["Mississippi","Jackson",32.3077,-90.2144, "Northern mockingbird", "Magnolia", "2,961,279"],
    ["Missouri","Kansas City",39.098,-94.5867, "Eastern bluebird", "Hawthorn", "6,154,913"],
    ["Montana","Billings",45.7787,-108.5459, "Western meadowlark", "Bitterroot", "1,084,225"],
    ["Nebraska","Omaha",41.274,-96.0182, "Western meadowlark", "Goldenrod", "1,961,504"],
    ["Nevada","Las Vegas",36.2013,-115.2384, "Mountain bluebird", "Sagebrush", "3,104,614"],
    ["New Hampshire","Manchester",42.992,-71.4468, "Purple finch", "Purple lilac", "1,377,529"],
    ["New Jersey","Newark",40.726,-74.1745, "Eastern goldfinch", "Violet", "9,288,994"],
    ["New Mexico","Albuquerque",35.0631,-106.6519, "Greater roadrunner", "Yucca flower", "2,117,522"],
    ["New York","New York City",40.719,-73.9386, "Eastern bluebird", "Rose", "20,201,249"],
    ["North Carolina","Charlotte",35.2174,-80.8261, "Northern cardinal", "Flowering dogwood", "10,439,388"],
    ["North Dakota","Fargo",46.8654,-96.832, "Western meadowlark", "Wild prairie rose", "779,094"],
    ["Ohio","Columbus",39.9648,-82.9883, "Northern cardinal", "Scarlet carnation", "11,799,448"],
    ["Oklahoma","Oklahoma City",35.4411,-97.5151, "Scissor-tailed flycatcher", "<state name> rose", "3,959,353"],
    ["Oregon","Portland",45.552,-122.6229, "Western meadowlark", "<state name> grape", "4,237,256"],
    ["Pennsylvania","Philadelphia",39.9937,-75.1194, "None", "Mountain laurel", "13,002,700"],
    ["Rhode Island","Providence",41.8301,-71.4274, "<state name> Red", "Violet", "1,097,379"],
    ["South Carolina","Charleston",32.7838,-79.9595, "<state name> wren", "Yellow jessamine", "5,118,425"],
    ["South Dakota","Sioux Falls",43.5429,-96.7253, "Ring-necked pheasant", "Pasque flower", "886,667"],
    ["Tennessee","Nashville",36.141,-86.7552, "Northern mockingbird", "Iris", "6,910,840"],
    ["Texas","Houston",29.8017,-95.4015, "Northern mockingbird", "Bluebonnet", "29,145,505"],
    ["Utah","Salt Lake City",40.7659,-111.9274, "California gull", "Sego lily", "3,271,616"],
    ["Vermont","Burlington",44.4935,-73.2139, "Hermit thrush", "Red clover", "643,077"],
    ["Virginia","Virginia Beach",36.7878,-76.0238, "Northern cardinal", "American dogwood", "8,631,393"],
    ["Washington","Seattle",47.5895,-122.3174, "Willow goldfinch", "Coast rhododendron", "7,705,281"],
    ["West Virginia","Charleston",38.3461,-81.6429, "Northern cardinal", "Rhododendron", "1,793,716"],
    ["Wisconsin","Milwaukee",43.0435,-87.9386, "American robin", "Wood violet", "5,893,718"],
    ["Wyoming","Cheyenne",41.1537,-104.796, "Western meadowlark", "Castilleja", "576,851"],
]

# Game variables
round_over = False
playing_game = True
ask_new = True
is_a_state = True

guess = ""

just_states = []

state_number = 0
state_info = []
state_weather = ""
state_name = ""
state_city = ""
state_bird = ""
state_flower = ""
state_pop = ""

# Functions:

# Get weather data at a latitude and longitude
def request_weather(latitude, longitude):
    grid_info = requests.get("https://api.weather.gov/points/" \
    + str(latitude) + "," + str(longitude))
    grid_prop = grid_info.json()["properties"]
    grid_ID = str(grid_prop["gridId"])
    grid_X = str(grid_prop["gridX"])
    grid_Y = str(grid_prop["gridY"])
    forecast_report = requests.get("https://api.weather.gov/gridpoints/" \
    + grid_ID + "/" + grid_X + "," + grid_Y \
    + "/" + "forecast")
    forecast_one = forecast_report.json()["properties"]["periods"][0]
    forecast = forecast_one["detailedForecast"]
    return forecast

# Other data preparations:

# Create a list of state names
for k in state_locations:
    just_states.append(k[0])

# Gameplay:

# Introduction and instructions
print("\nHi, welcome to the state guessing game")
print("You'll be given the weather conditions at the largest city in a US state")
print("Guess the state by typing in state names")
print("\nType these commands to see more information:")
print("info - display the weather conditions again")
print("list - shows a list of every state")
print("hint1 - see the state's state bird")
print("hint2 - see the state's state flower")
print("hint3 - see the state's 2020 population")
print("answer - see the answer and end the game")

# Gameplay loop
while round_over == False:
    guess = ""
    
    state_number = random.randrange(0, 49)
    state_info = state_locations[state_number]
    state_name = state_info[0]
    state_city = state_info[1]
    state_bird = state_info[4]
    state_flower = state_info[5]
    state_pop = state_info[6]
    state_weather = request_weather(state_info[2],state_info[3])

    print("\nThe most recent weather forcast at the mystery location:")
    print(state_weather + "\n")
    
    while playing_game == True:
        guess = input("Type here: ")
        
        for n in just_states:
            if guess.lower() == n.lower():
                is_a_state = True
                break
            else:
                is_a_state = False
                continue

        if guess.lower() == state_name.lower():
            print("That is correct!")
            playing_game = False
        elif is_a_state == True:
            print("That is not correct. Try again!")
            is_a_state = True
        elif guess.lower() == "info":
            print(state_weather)
        elif guess.lower() == "list":
            for j in just_states:
                print(j)
        elif guess.lower() == "hint1":
            print(state_bird)
        elif guess.lower() == "hint2":
            print(state_flower)
        elif guess.lower() == "hint3":
            print(state_pop)
        elif guess.lower() == "answer":
            print(state_city + ", " + state_name)
            playing_game = False
        else:
            print("I don't recognize that")

        is_a_state = True

    while ask_new == True:
        new_round = input("Play a new round? (Y/N): ")
        if new_round.lower() == "y":
            round_over = False
            ask_new = False
            playing_game = True
        elif new_round.lower() == "n":
            print("Thanks for playing")
            round_over = True
            ask_new = False
        else:
            print("I don't recognize that")
            ask_new = True
            continue

    ask_new = True
    playing_game = True
    is_a_state = True
