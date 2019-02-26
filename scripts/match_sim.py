from player import player
from match_state import match_state
from team import team
from stats import batting_stats
from stats import bowling_stats
import yaml
from itertools import izip

def yaml_loader(filepath):
    with open(filepath,'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def load_ball_by_ball_data(f_name):
    file_path = '/home/shashank/intern_17/data/ipl/' + f_name
    return yaml_loader(file_path)

def refine_stats_data(stats):
    for key,value in stats.iteritems():
        if value == '-':
            stats[key] = '0'
            value = '0'
        value = value.replace('*','')
        stats[key] = value
        if key != 'Player' and key != 'Span' and key!= 'BBI':
            stats[key] = float(value)
    return stats

def create_players(team_name,team_batt_stats,team_bowl_stats):
    players = []
    for bat,bowl in izip(team_batt_stats,team_bowl_stats):
        refined_bat = refine_stats_data(bat)
        refined_bowl = refine_stats_data(bowl)

        #create stats
        bat_stats = batting_stats(refined_bat['Mat'],refined_bat['Inns'],refined_bat['NO'],refined_bat['Runs'],refined_bat['Ave'],refined_bat['BF'],refined_bat['100'],refined_bat['50'],refined_bat['4s'],refined_bat['6s'],refined_bat['0'],refined_bat['HS'],refined_bat['SR'],refined_bat['Span'])
        bowl_stats = bowling_stats(refined_bowl['Mat'],refined_bowl['Inns'],refined_bowl['Overs'],refined_bowl['Runs'],refined_bowl['Wkts'],refined_bowl['Ave'],refined_bowl['Econ'],refined_bowl['4'],refined_bowl['5'],refined_bowl['SR'],refined_bowl['Span'])

        #create player
        pl = player(refined_bat['Player'],team_name,bat_stats,bowl_stats)

        players.append(pl)
    return players

def initialize_match(ball_by_ball,f_name):

    team_a_name = ball_by_ball['info']['teams'][0]
    team_b_name = ball_by_ball['info']['teams'][1]

    toss_data = ball_by_ball['info']['toss']
    toss_win = toss_data['winner']
    if ((toss_data['winner'] == team_a_name and toss_data['decision'] == 'bat') or (toss_data['winner'] == team_b_name and toss_data['decision'] == 'field')):
            toss = 0
    else:
        toss = 1


    file_path = '/home/shashank/intern_17/data/player_stats/' + f_name
    player_stats_data = yaml_loader(file_path)
    team_a_batt_stats = player_stats_data[team_a_name.replace(' ','')][0]['batting averages']
    team_a_bowl_stats = player_stats_data[team_a_name.replace(' ','')][1]['bowling averages']
    team_b_batt_stats = player_stats_data[team_b_name.replace(' ','')][0]['batting averages']
    team_b_bowl_stats = player_stats_data[team_b_name.replace(' ','')][1]['bowling averages']

    #create players
    team_a_players = create_players(team_a_name,team_a_batt_stats,team_a_bowl_stats)
    team_b_players = create_players(team_b_name,team_b_batt_stats,team_b_bowl_stats)

    #create teams
    team_a = team(team_a_name,team_a_players)
    team_b = team(team_b_name,team_b_players)


    #check winner
    if 'winner' not in ball_by_ball['info']['outcome'].keys():
        win = 0
    else:
        win = ball_by_ball['info']['outcome']['winner']

    venues = yaml_loader('/home/shashank/intern_17/data/home_venues.yaml')
    home_team = 'neutral'
    if 'city' in ball_by_ball['info'] and 'neutral_venue' not in ball_by_ball['info']:
        for hteam in venues[ball_by_ball['info']['city']]:
            if hteam == team_a_name :
                home_team = team_a_name
                break
            if hteam == team_b_name:
                home_team = team_b_name
                break

    #create match
    state = match_state(team_a,team_b,toss,ball_by_ball['info']['match_type'],ball_by_ball['info']['venue'],win,toss_win,home_team)

    return state

def simulate_ball(ball,matchState):
    if matchState.batting_first ==  matchState.current_innings:
        #team a is batting
        team_A = matchState.team_a
        team_B = matchState.team_b
    else:
        team_A = matchState.team_b
        team_B = matchState.team_a

    for key,value in ball.iteritems():

        batsman = team_A.get_player_by_name(value['batsman'])
        bowler = team_B.get_player_by_name(value['bowler'])
        non_striker = team_A.get_player_by_name(value['non_striker'])

        batsman.is_batting = 1
        non_striker.is_batting = 1

        team_A.balls_completed += 1
        team_A.score += value['runs']['total']
        batsman.balls_played += 1
        batsman.runs_scored += value['runs']['batsman']

        bowler.balls_bowled +=1
        bowler.runs_conceded += value['runs']['total']

        if 'extras' in value:
            if 'wides' in value['extras']:
                batsman.balls_played -= 1
                team_A.balls_completed -= 1
                bowler.balls_bowled -= 1
            if 'noballs' in value['extras']:
                team_A.balls_completed -= 1
                bowler.balls_bowled -= 1
            if 'byes' in value['extras']:
                bowler.runs_conceded -= value['extras']['byes']
                if value['runs']['extras'] == value['runs']['total']:
                    bowler.dot_balls_bowled += 1
            if 'legbyes' in value['extras']:
                bowler.runs_conceded -= value['extras']['legbyes']
                if value['runs']['extras'] == value['runs']['total']:
                    bowler.dot_balls_bowled += 1


        if value['runs']['batsman'] == 4:
            batsman.num_fours += 1
        if value['runs']['batsman'] == 6:
            batsman.num_sixes += 1

        if value['runs']['total'] == 0:
            bowler.dot_balls_bowled += 1

        if 'wicket' in value and value['wicket']['kind'] != 'run out':
            team_A.wickets_lost += 1
            bowler.wickets_taken += 1
            batsman.is_batting = 0
            batsman.has_batted = 1
        if 'wicket' in value and value['wicket']['kind'] == 'run out':
            if batsman.name == value['wicket']['player_out']:
                batsman.is_batting = 0
                batsman.has_batted = 1
            else:
                non_striker.is_batting = 0
                non_striker.has_batted = 1

        team_A.calculate_overs_completed()
        batsman.calculate_overs_played()
        bowler.calculate_overs_bowled()

        matchState.normalize_career_scores()
        team_A.calculate_team_career_score()
        team_B.calculate_team_career_score()

def simulate_over(innings,matchState,over_offset):
    balls = innings['deliveries']
    ball_offset = 0
    i = 0
    while i < ((over_offset)*6) + ball_offset:
        if i < len(balls):
            for key,value in balls[i].iteritems():
                if ('extras' in value and ('wides' in value['extras'] or 'noballs' in value['extras'])):
                    ball_offset += 1
            i+=1
        else:
            break
    offset = ((over_offset)*6) + ball_offset
    c = 6
    k = offset
    while k < offset + c:
        if k < len(balls):
            simulate_ball(balls[k],matchState)
            for key,value in balls[k].iteritems():
                if ('extras' in value and ('wides' in value['extras'] or 'noballs' in value['extras'])):
                    c += 1
            k+=1
        else:
            break

def simulate_n_overs(innings,matchState,n):
    for i in range(n):
        simulate_over(innings,matchState,i)

def simulate_innings(innings,ball_by_ball,matchState):
    if innings == 1:
        first = ball_by_ball['innings'][0]['1st innings']
        simulate_n_overs(first,matchState,20)
    if innings == 2:
        second = ball_by_ball['innings'][1]['2nd innings']
        simulate_n_overs(second,matchState,20)

def simulate_match(ball_by_ball,matchState):
    simulate_innings(1,ball_by_ball,matchState)
    matchState.change_innings()
    simulate_innings(2,ball_by_ball,matchState)


if __name__ == '__main__':
    ball_by_ball = load_ball_by_ball_data('335993.yaml')
    matchState = initialize_match(ball_by_ball,'335993.yaml')
    simulate_match(ball_by_ball,matchState)
    #print matchState.toss_winner,matchState.home_team_name
    for pl in matchState.team_b.player_list:
        print pl.name,pl.has_batted
    for pl in matchState.team_a.player_list:
        print pl.name,pl.has_batted


    #player_names_kxip = ['PP Chawla','P Dharmani','K Goel','JR Hopes','SM Katich','B Lee','WA Mota','IK Pathan','KC Sangakkara','S Sreesanth','Yuvraj Singh']
    #player_names_csk = ['P Amarnath','S Badrinath','MS Dhoni','MS Gony','ML Hayden','MEK Hussey','Joginder Sharma','M Muralitharan','JDP Oram','PA Patel','SK Raina']
    #player_names_rcb = ['B Akhil','MV Boucher','R Dravid','W Jaffer','SB Joshi','JH Kallis','Z Khan','V Kohli','P Kumar','AA Noffke','CL White']
    #player_names_kkr = ['AB Agarkar','AB Dinda','SC Ganguly','DJ Hussey','M Kartik','BB McCullum','Mohammad Hafeez','RT Ponting','WP Saha','I Sharma','LR Shukla']
