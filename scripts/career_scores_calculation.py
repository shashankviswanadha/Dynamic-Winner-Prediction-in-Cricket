import yaml
from os import listdir
from os.path import isfile, join
from math import sqrt


def yaml_loader(filepath):
    with open(filepath,'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def yaml_dump(filepath,data):
    with open(filepath,"w") as file_descriptor:
        yaml.dump(data,file_descriptor)


def calculate_batting_score(ba,agg_score):
    score = 0
    if int(ba['Mat']) == 0:
        score = round(agg_score,2)
    else:
        if int(ba['Inns']) > 0:
            if int(ba['NO']) == int(ba['Inns']):
                ba['Ave'] = ba['Runs']
            score = round(float(ba['Ave']) * float(ba['SR']) * sqrt(float(ba['Inns'])/float(ba['Mat'])),2)
    return score

def calculate_bowling_score(bo,agg_score):
    score = 0.0
    if int(bo['Mat']) == 0:
        score = round(agg_score,7)
    else:
        if int(bo['Inns']) > 0:
            if int(bo['Runs']) == 0:
                bo['Econ'] = 1
            if int(bo['Wkts']) == 0:
                bo['SR'] = float(bo['Inns'])*4.0*6

            if float(bo['Econ']) * float(bo['SR']) != 0:
                score = round(sqrt(float(bo['Inns'])/float(bo['Mat']))/(float(bo['Econ']) * float(bo['SR'])),7)
    return score

def get_last_n_agg_scores(n):
    pa = '/home/shashank/intern_17/data/debut_last_n_scores.yaml'
    da = yaml_loader(pa)
    bat = da[n][0]['batting score']
    bowl = da[n][1]['bowling score']
    return (bat,bowl)

def calculate_career_scores_for_match(name):

    path = '/home/shashank/intern_17/data/updated_player_stats/' + name
    data = yaml_loader(path)
    team_a_name = data.keys()[0]
    team_b_name = data.keys()[1]
    mypath = '/home/shashank/intern_17/data/updated_player_stats/'
    agg_scores = get_last_n_agg_scores(1)
    dump_data = {team_a_name:[{'batting scores':[]},{'bowling scores':[]}],team_b_name:[{'batting scores':[]},{'bowling scores':[]}]}
    for team in data.keys():
        for ba in data[team][0]['batting averages']:
            t = calculate_batting_score(ba,agg_scores[0])
            dump_data[team][0]['batting scores'].append({'Player':ba['Player'],'Score':t})
        for bo in data[team][1]['bowling averages']:
            t = calculate_bowling_score(bo,agg_scores[1])
            dump_data[team][1]['bowling scores'].append({'Player':bo['Player'],'Score':t})

    write_path = '/home/shashank/intern_17/data/career_scores/' + name
    yaml_dump(write_path,dump_data)


if __name__ == '__main__':
    mypath = '/home/shashank/intern_17/data/updated_player_stats/'
    season_1_files = [(str(i) + '.yaml') for i in range(335982,336041)]
    season_1_files.remove(season_1_files[48])
    season_2_files = [(str(i) + '.yaml') for i in range(392181, 392240)]
    season_2_files.remove(season_2_files[6])
    season_2_files.remove(season_2_files[11])
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for f in season_1_files:
        onlyfiles.remove(f)
    for f in season_2_files:
        onlyfiles.remove(f)
    for i in range(len(onlyfiles)):
        print i
        calculate_career_scores_for_match(onlyfiles[i])
