from __future__ import division
import yaml
import sys
sys.path.append("/home/shashank/intern_17/scripts/")
from match_sim import *
from os import listdir
from os.path import isfile, join


def yaml_loader(filepath):
    with open(filepath,'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def yaml_dump(filepath,data):
    with open(filepath,"w") as file_descriptor:
        yaml.dump(data,file_descriptor)

def normalize(filepath,data,ch):
    if ch == 0:
        data = yaml_loader(filepath)
    dummy_list = ['batting scores','bowling scores']
    for i in range(2):
        ma = 0
        for team in data.keys():
            for pl in data[team][i][dummy_list[i]]:
                if float(pl['Score']) > ma:
                    ma = float(pl['Score'])
        for team in data.keys():
            for pl in data[team][i][dummy_list[i]]:
                pl['Score'] = float(pl['Score'])/ma
    return data

def normazlize_and_caclulate_final_scores(name,n,p):
    career_path = '/home/shashank/intern_17/data/career_scores/' + name
    last_n_path = '/home/shashank/intern_17/data/last_' + str(n) + '_scores/' + name
    normalized_career = normalize(career_path,0,0)
    normalized_form = normalize(last_n_path,0,0)
    team_a_name = normalized_career.keys()[0]
    team_b_name = normalized_career.keys()[1]
    final_scores = {team_a_name:[{'batting scores':[]},{'bowling scores':[]}],team_b_name:[{'batting scores':[]},{'bowling scores':[]}]}
    dummy_list = ['batting scores','bowling scores']
    for i in range(2):
        for team in normalized_career.keys():
            for pl in normalized_career[team][i][dummy_list[i]]:
                score = p*float(pl['Score'])
                for pll in normalized_form[team][i][dummy_list[i]]:
                    if pll['Player'] == pl['Player']:
                        score += (1-p)*float(pll['Score'])
                final_scores[team][i][dummy_list[i]].append({'Player':pl['Player'],'Score':score})
    return final_scores

def calculate_team_score(scores,team,matchState,ch):
    team_batting_score = 0
    team_bowling_score = 0
    if ch == 0:
        for pl in scores[team][0]['batting scores']:
            fac = factor(team,pl,matchState,0)
            team_batting_score += fac*pl['Score']
        for pl in scores[team][1]['bowling scores']:
            team_bowling_score += pl['Score']

    else:
        for pl in scores[team][0]['batting scores']:
            team_batting_score += pl['Score']
        for pl in scores[team][1]['bowling scores']:
            fac = factor(team,pl,matchState,1)
            team_bowling_score += fac*pl['Score']

    return (team_batting_score,team_bowling_score)

def factor(team,player,matchState,batt_bowl):
    if team == matchState.team_a.name:
        t = matchState.team_a
    else:
        t = matchState.team_b
    for pl in t.player_list:
        if pl.name == player['Player']:
            p = pl
            break
    if batt_bowl == 0:
        return 1-p.has_batted
    else:
        return ((24-p.balls_bowled)/24)
def calculate_relative_score(team_a,team_b):
    return (team_a[0]/team_b[1]-team_b[0]/team_a[1])

def output_relative_score(name,n,p,team_batting_second,matchState):
    data = normazlize_and_caclulate_final_scores(path,n,p)
    data = normalize(0,data,1)
    if team_batting_second == data.keys()[0]:
        team_a_scores = calculate_team_score(data,data.keys()[0],matchState,0)
        team_b_scores = calculate_team_score(data,data.keys()[1],matchState,1)
    else:
        team_a_scores = calculate_team_score(data,data.keys()[1],matchState,0)
        team_b_scores = calculate_team_score(data,data.keys()[0],matchState,1)
    return calculate_relative_score(team_a_scores,team_b_scores)

def get_normalized_scores(name,n,p):
    data = normazlize_and_caclulate_final_scores(path,n,p)
    data = normalize(0,data,1)
    return data


if __name__ == '__main__':
    season_1_files = [(str(i) + '.yaml') for i in range(335982,336041)]
    season_1_files.remove(season_1_files[48])
    season_2_files = [(str(i) + '.yaml') for i in range(392181, 392240)]
    season_2_files.remove(season_2_files[6])
    season_2_files.remove(season_2_files[11])
    season_8_files = [(str(i) + '.yaml') for i in range(829705,829824,2)]
    season_8_files.remove(season_8_files[25])
    #print season_8_files[28]
    season_8_files.remove(season_8_files[28])
    season_9_files = [(str(i) + '.yaml') for i in range(980901,981020,2)]
    season_10_files = [(str(i) + '.yaml') for i in range(1082591,1082651)]
    season_10_files.remove(season_10_files[28])
    test_files = []
    mypath = '/home/shashank/intern_17/data/updated_player_stats/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    validation_files = []
    for f in season_1_files:
        onlyfiles.remove(f)
    for f in season_2_files:
        onlyfiles.remove(f)
    for f in season_8_files:
        #print f
        onlyfiles.remove(f)
        validation_files.append(f)
    for f in season_9_files:
        onlyfiles.remove(f)
        test_files.append(f)
    for f in season_10_files:
        onlyfiles.remove(f)
        test_files.append(f)
    test_files.remove('980943.yaml')
    test_files.remove('980989.yaml')
    test_files.remove('980997.yaml')
    test_files.remove('980999.yaml')
    test_files.remove('1082648.yaml')
    onlyfiles.remove('733993.yaml')
    onlyfiles.remove('501245.yaml')
    validation_files.remove('829807.yaml')
    validation_files.remove('829743.yaml')

    data_list = {'train_data.yaml':onlyfiles,'validation_data.yaml':validation_files,'test_data.yaml':test_files}
    for f_name,files in data_list.iteritems():
        write_data = {}
        for i in range(21):
            write_data[i] = []
        for path in files:
            print path
            f_path = '/home/shashank/intern_17/data/data_for_ml/' + f_name
            n = 4
            p = 0.8
            ball_by_ball = load_ball_by_ball_data(path)
            second = ball_by_ball['innings'][1]['2nd innings']
            matchState = initialize_match(ball_by_ball,path)
            simulate_innings(1,ball_by_ball,matchState)
            matchState.change_innings()
            balls = second['deliveries']
            if matchState.batting_first == 0:
                team_batting_first = matchState.team_a
                team_batting_second = matchState.team_b
            else:
                team_batting_first = matchState.team_b
                team_batting_second = matchState.team_a
            if matchState.toss_winner == team_batting_second:
                toss = 1
            else:
                toss = 0
            home_ad = [0,0,0]
            if matchState.home_team_name == team_batting_second.name:
                home_ad[0] = 1
            elif matchState.home_team_name == team_batting_first.name:
                home_ad[1] = 1
            elif matchState.home_team_name == 'neutral':
                home_ad[2] = 1

            if matchState.winning_team_name == team_batting_second.name:
                result_label = 1
            else:
                result_label = 0

            relative_score = output_relative_score(path,n,p,team_batting_second.name,matchState)
            #relative_batting_score = relative_score[0]
            #relative_bowling_score = relative_score[1]
            #print 0,relative_score,result_label
            target = float(team_batting_first.score + 1)
            runs_remaining = team_batting_first.score + 1
            wickets_remaining = 10
            balls_remaining = 120
            #li = [runs_remaining/target,wickets_remaining/10.0,round(balls_remaining/120.0,),toss,1,home_ad[0],home_ad[1],home_ad[2],1,1,result_label]
            #li = [runs_remaining,wickets_remaining,balls_remaining,relative_score,result_label]#,toss,home_ad[0],home_ad[1],home_ad[2],relative_score,result_label]
            #li = [0,0,target/20.0,relative_score,result_label]
            #print target
            li = [runs_remaining,wickets_remaining,balls_remaining,relative_score,result_label]
            #print 0,li
            write_data[0].append(li)
            for i in range(20):
                simulate_over(second,matchState,i)
                flag = 0
                runs_remaining =  team_batting_first.score + 1 - team_batting_second.score
                wickets_remaining = 10 - team_batting_second.wickets_lost
                balls_remaining = (19-i) * 6
                relative_score = output_relative_score(path,n,p,team_batting_second.name,matchState)
                if runs_remaining <= 0:
                    runs_remaining = 0
                    flag = 1
                if wickets_remaining == 0:
                    flag = 1
                li = [runs_remaining,wickets_remaining,balls_remaining,relative_score,result_label]
                #print i,li
                write_data[i+1].append(li)
                if flag == 1:
                    break
                if ((runs_remaining > 0 and balls_remaining == 0) and result_label == 1):
                    print path



        yaml_dump(f_path,write_data)

        '''write_data[0].append(li)
            i = 0
            for ball in balls:
                quit = 0
                for key,value in ball.iteritems():
                    if ('extras' in value and ('wides' in value['extras'] or 'noballs' in value['extras'])):
                        simulate_ball(ball,matchState)
                        quit = 1
                if quit == 0:
                    simulate_ball(ball,matchState)
                    i+=1
                    flag = 0
                    relative_score = output_relative_score(path,n,p,team_batting_second.name,matchState)
                    #relative_batting_score = relative_score[0]
                    #relative_bowling_score = relative_score[1]
                    #print i+1,relative_score
                    runs_remaining =  team_batting_first.score + 1 - team_batting_second.score
                    wickets_remaining = 10 - team_batting_second.wickets_lost
                    #print wickets_remaining
                    balls_remaining = 120-i
                    if runs_remaining <= 0:
                        runs_remaining = 0
                        flag = 1
                    if wickets_remaining == 0:
                        flag = 1
                    if i == 19:
                        run_rate = target
                    else:
                        run_rate = (runs_remaining/target)*(20.0/(19-i)) #runs_remaining/(19-i)
                    #li = [runs_remaining/target,wickets_remaining/10.0,round(balls_remaining/120.0,),toss,run_rate,home_ad[0],home_ad[1],home_ad[2],relative_score[0]/init_relative_score[0],relative_score[1]/init_relative_score[1],result_label]
                    li = [runs_remaining,wickets_remaining,balls_remaining,relative_score,result_label]
                    #li = [runs_remaining,wickets_remaining,balls_remaining,toss,home_ad[0],home_ad[1],home_ad[2],relative_score,result_label]
                    #li = [runs_remaining,wickets_remaining,balls_remaining,relative_score,result_label]
                    #li = [i+1,team_batting_second.wickets_lost,run_rate,relative_score,result_label]
                    #print i,li
                    write_data[i+1].append(li)'''
