import yaml
import sys
sys.path.append("/home/shashank/intern_17/scripts/")
from match_sim import *
sys.path.append("/home/shashank/intern_17/scripts/normalizing/")
from normalizing import *
from os import listdir
from os.path import isfile, join

def yaml_dump(filepath,data):
    with open(filepath,"w") as file_descriptor:
        yaml.dump(data,file_descriptor)

def get_players_in_match(matchState):
    batsman = {}
    bowlers = {}
    teams = [matchState.team_a,matchState.team_b]
    for team in teams:
        for pl in team.player_list:
            if pl.balls_played > 0 or pl.is_batting > 0:
                if pl.balls_played != 0:
                    batsman[pl.name] = pl.runs_scored * float(pl.runs_scored)/float(pl.balls_played)
                else:
                    batsman[pl.name] = 0.0

            if pl.balls_bowled > 0:
                if pl.wickets_taken == 0:
                    strike_rate = 24.0
                else:
                    strike_rate = float(pl.balls_bowled)/float(pl.wickets_taken)
                if pl.runs_conceded == 0:
                    pl.runs_conceded = 1
                i,d = divmod(pl.overs_bowled,1)
                econ = float(pl.runs_conceded)/(i + 100*d/6)
                bowlers[pl.name] = round(1/(econ*strike_rate),7)
    return (batsman,bowlers)

def get_player_career_last_n(n,p,pl_names,name,ch):
    players = {}
    last_n_path = '/home/shashank/intern_17/data/last_' + str(n) + '_scores/' + name
    career_path = '/home/shashank/intern_17/data/career_scores/' + name
    last_n_data = normalize(last_n_path,0,0)
    career_data = normalize(career_path,0,0)
    babo = ['batting scores','bowling scores']
    teams = career_data.keys()
    for team in teams:
        count = 0
        for pl in career_data[team][ch][babo[ch]]:
            score = 0
            if pl['Player'] in pl_names:
                score += p*float(pl['Score'])
                for pl1 in last_n_data[team][ch][babo[ch]]:
                    if pl1['Player'] == pl['Player']:
                        score += (1-p)*float(pl1['Score'])
                if ch == 0:
                    score = round(score,2)
                else:
                    score = round(score,7)
                players[pl['Player']] = score
            count += 1
    return players

def sort_and_compare(match_dict,last_n_dict):
    match_ranks = sorted(match_dict.items(), key=lambda x: x[1],reverse=True)
    last_n_ranks = sorted(last_n_dict.items(), key=lambda x: x[1],reverse=True)
    distance = 0
    for i in range(len(match_ranks)):
        name = match_ranks[i][0]
        for j in range(len(last_n_ranks)):
            if name == last_n_ranks[j][0]:
                distance += abs(i-j)
                break
    return distance


def n_p_experiment_for_match(name,n,p):
    ball_by_ball = load_ball_by_ball_data(name)
    matchState = initialize_match(ball_by_ball,name)
    simulate_match(ball_by_ball,matchState)

    batsmen_match,bowlers_match = get_players_in_match(matchState)


    batsman_names = []
    bowler_names = []
    for k in batsmen_match.keys():
        batsman_names.append(k)
    for k in bowlers_match.keys():
        bowler_names.append(k)

    last_n_batsmen = get_player_career_last_n(n,p,batsman_names,name,0)
    last_n_bolwler = get_player_career_last_n(n,p,bowler_names,name,1)

    batsmen_d = sort_and_compare(batsmen_match,last_n_batsmen)
    bowlers_d = sort_and_compare(bowlers_match,last_n_bolwler)

    total_d = batsmen_d + bowlers_d
    return total_d


if __name__ == '__main__':


    '''season_5_files = [(str(i) + '.yaml') for i in range(548306,548382)]
    season_5_files.remove(season_5_files[32])
    season_5_files.remove(season_5_files[33])
    season_4_files = [(str(i) + '.yaml') for i in range(501198,501272)]
    season_4_files.remove(season_4_files[19])
    season_4_files.remove(season_4_files[66])'''
    season_1_files = [(str(i) + '.yaml') for i in range(335982,336041)]
    season_1_files.remove(season_1_files[48])
    season_2_files = [(str(i) + '.yaml') for i in range(392181, 392240)]
    season_2_files.remove(season_2_files[6])
    season_2_files.remove(season_2_files[11])
    season_9_files = [(str(i) + '.yaml') for i in range(980901,981020,2)]
    season_10_files = [(str(i) + '.yaml') for i in range(1082591,1082651)]
    season_10_files.remove(season_10_files[28])

    mypath = '/home/shashank/intern_17/data/updated_player_stats/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for f in season_1_files:
        onlyfiles.remove(f)
    for f in season_2_files:
        onlyfiles.remove(f)
    for f in season_9_files:
        onlyfiles.remove(f)
    for f in season_10_files:
        onlyfiles.remove(f)

    data_dump = {3:[],4:[],5:[],6:[],7:[],8:[]}
    for n in range(4,6):
        p = 0.20
        while p < 0.85:
            distance = 0
            for f in onlyfiles:
                print n,p,f
                distance += n_p_experiment_for_match(f,n,p)
            data_dump[n].append({'p':p,'distance':distance})
            p += 0.050
            p = round(p,2)
    write_path = '/home/shashank/intern_17/data/normalized_np_exp.yaml'
    yaml_dump(write_path,data_dump)
