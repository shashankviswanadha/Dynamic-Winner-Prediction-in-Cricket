from match_sim import *
from os import listdir
from os.path import isfile, join

mypath = '/home/shashank/intern_17/data/updated_player_stats/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
c = 1
for f in onlyfiles:
    print c
    ball_by_ball = load_ball_by_ball_data(f)
    matchState = initialize_match(ball_by_ball,f)
    simulate_match(ball_by_ball,matchState)
    c+=1
