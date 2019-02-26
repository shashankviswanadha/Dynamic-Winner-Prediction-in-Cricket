import match_sim
import match_state
import team
import player
import stats
import yaml
from os import listdir
from os.path import isfile, join

def adjust_batting_stats(pl):
    stat = pl.batting_stats
    stat.matches_played -= 1
    if pl.balls_played > 0:
        stat.batt_innings -= 1
    stat.not_outs -= pl.is_batting
    stat.runs_scored -= pl.runs_scored
    if stat.batt_innings-stat.not_outs !=0:
        stat.average = round(stat.runs_scored/(stat.batt_innings-stat.not_outs),2)
    else:
        stat.average = 0
    stat.balls_faced -= pl.balls_played
    if pl.runs_scored >= 100:
        stat.centuries -= 1
    if pl.runs_scored >= 50:
        stat.fifties -= 1
    stat.fours -= pl.num_fours
    stat.sixes -= pl.num_sixes
    if pl.runs_scored == 0 and pl.balls_played > 0:
        stat.zeros += 1
    if pl.runs_scored == stat.highest_score and pl.balls_played > 0:
        stat.highest_score = -1
    if stat.balls_faced > 0:
        stat.strike_rate = round((stat.runs_scored/stat.balls_faced)* 100,2)
    else:
        stat.strike_rate = 0

def adjust_bowling_stats(pl):
    stat = pl.bowling_stats
    stat.matches_played -= 1
    if pl.balls_bowled > 0:
        stat.bowl_innings -= 1
    #print pl.name,stat.balls_bowled,pl.balls_bowled
    stat.balls_bowled = int(stat.balls_bowled) - pl.balls_bowled
    #print pl.name,stat.balls_bowled,pl.balls_bowled
    stat.calculate_overs_bowled()
    #print stat.overs_bowled,stat.balls_bowled
    stat.runs_conceded -= pl.runs_conceded
    stat.wickets_taken -= pl.wickets_taken
    if stat.wickets_taken != 0:
        stat.average = round(stat.runs_conceded/stat.wickets_taken,2)
    else:
        stat.average = 0
    if stat.balls_bowled != 0:
        i,d = divmod(stat.overs_bowled,1)
        stat.economy = round(stat.runs_conceded/(i + 100*d/6),2)
    else:
        stat.economy = 0
    if pl.wickets_taken == 4:
        stat.fourwi -= 1
    if pl.wickets_taken > 4:
        stat.fivewi -= 1
    if stat.wickets_taken > 0:
        stat.strike_rate = round(stat.balls_bowled/stat.wickets_taken,2)
    else:
        stat.strike_rate = 0


def adjust_player_stats(pl):
    adjust_batting_stats(pl)
    adjust_bowling_stats(pl)

def adjust_team_stats(team):
    for pl in team.player_list:
        adjust_player_stats(pl)

def adjust_match_stats(matchState):
    adjust_team_stats(matchState.team_a)
    adjust_team_stats(matchState.team_b)

def yaml_dump(filepath,data):
    filepath = '/home/shashank/intern_17/data/updated_player_stats/' + filepath
    with open(filepath,"w") as file_descriptor:
        yaml.dump(data,file_descriptor)

def write_to_yaml(f_name,state):
    team_a_name = state.team_a.name
    team_b_name = state.team_b.name
    data_yaml = {team_a_name:[{'batting averages':[]},{'bowling averages':[]}],team_b_name:[{'batting averages':[]},{'bowling averages':[]}]}

    team_a_bat_stats = data_yaml[team_a_name][0]['batting averages']
    team_b_bat_stats = data_yaml[team_b_name][0]['batting averages']
    team_a_bowl_stats = data_yaml[team_a_name][1]['bowling averages']
    team_b_bowl_stats = data_yaml[team_b_name][1]['bowling averages']

    for pl in state.team_a.player_list:
        team_a_bat_stats.append(bat_pl_dict(pl))
        team_a_bowl_stats.append(bowl_pl_dict(pl))

    for pl in state.team_b.player_list:
        team_b_bat_stats.append(bat_pl_dict(pl))
        team_b_bowl_stats.append(bowl_pl_dict(pl))

    yaml_dump(f_name,data_yaml)


def bat_pl_dict(pl):
    pl_dict = {}
    pl_dict['100'] = str(int(pl.batting_stats.centuries))
    pl_dict['4s'] = str(int(pl.batting_stats.fours))
    pl_dict['50'] = str(int(pl.batting_stats.fifties))
    pl_dict['6s'] = str(int(pl.batting_stats.sixes))
    pl_dict['Ave'] = str(pl.batting_stats.average)
    pl_dict['BF'] = str(int(pl.batting_stats.balls_faced))
    pl_dict['Inns'] = str(int(pl.batting_stats.batt_innings))
    pl_dict['Mat'] = str(int(pl.batting_stats.matches_played))
    pl_dict['NO'] = str(int(pl.batting_stats.not_outs))
    pl_dict['Player'] = pl.name
    pl_dict['Runs'] = str(int(pl.batting_stats.runs_scored))
    pl_dict['0'] = str(int(pl.batting_stats.zeros))
    pl_dict['HS'] = str(int(pl.batting_stats.highest_score))
    pl_dict['SR'] = str(pl.batting_stats.strike_rate)
    pl_dict['Span'] = pl.batting_stats.span
    return pl_dict

def bowl_pl_dict(pl):
    pl_dict = {}
    pl_dict['4'] = str(int(pl.bowling_stats.fourwi))
    pl_dict['5'] = str(int(pl.bowling_stats.fivewi))
    pl_dict['Ave'] = str(pl.bowling_stats.average)
    pl_dict['Econ'] = str(pl.bowling_stats.economy)
    pl_dict['Mat'] = str(int(pl.bowling_stats.matches_played))
    pl_dict['Inns'] = str(int(pl.bowling_stats.bowl_innings))
    pl_dict['Overs'] = str(pl.bowling_stats.overs_bowled)
    pl_dict['Player'] = pl.name
    pl_dict['Runs'] = str(int(pl.bowling_stats.runs_conceded))
    pl_dict['Wkts'] = str(int(pl.bowling_stats.wickets_taken))
    pl_dict['SR'] = str(pl.bowling_stats.strike_rate)
    pl_dict['Span'] = str(pl.bowling_stats.span)

    return pl_dict

def update_stats(name):
    bbb = match_sim.load_ball_by_ball_data(name)
    matchState = match_sim.initialize_match(bbb,name)
    match_sim.simulate_match(bbb,matchState)
    adjust_match_stats(matchState)
    write_to_yaml(name,matchState)

if __name__ == '__main__':
    mypath = '/home/shashank/intern_17/data/player_stats/335982.yaml'
    '''onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for i in range (619,len(onlyfiles)):
        print 'Updating : ',i,onlyfiles[i]'''
    update_stats('335982.yaml'.replace('~',''))
