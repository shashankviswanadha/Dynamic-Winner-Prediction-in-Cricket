import yaml
import os
from os import listdir
from os.path import isfile, join


def yaml_loader(filepath):
    with open(filepath,'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def yaml_dump(filepath,data):
    with open(filepath,"w") as file_descriptor:
        yaml.dump(data,file_descriptor)


def update_index(player,file_name):
    filepath = '/home/shashank/intern_17/data/player_indexes/' + player['Player'] + '.yaml'
    matches = int(player['Mat']) + 1
    data_dump = {'match number':str(matches),'file_name':file_name,'competition' : 'ipl'}
    if os.path.exists(filepath):
        current_data = yaml_loader(filepath)
        '''last_match = int(current_data[len(current_data)-1]['aid'])
        for i in range(last_match + 1,matches):
            current_data.append({'aid' : i,'competition' : 'unknown'})'''
    else:
        file(filepath,'w+')
        current_data = []
        '''for i in range(matches):
            current_data.append({'aid' : i,'competition' : 'unknown'})'''
    flag = 0
    for match in current_data:
        if int(match['match number']) == matches:
            flag = 1
    if flag == 0:
        current_data.append(data_dump)
        yaml_dump(filepath,current_data)



def update_player_indexes(f_name):
    path = '/home/shashank/intern_17/data/updated_player_stats/' + f_name

    stat_data = yaml_loader(path)


    team_a_name = stat_data.keys()[0]
    team_b_name = stat_data.keys()[1]

    for pl in stat_data[team_a_name][0]['batting averages']:
        update_index(pl,f_name.replace('.yaml',''))
    for pl in stat_data[team_b_name][0]['batting averages']:
        update_index(pl,f_name.replace('.yaml',''))

if __name__ == '__main__':
    mypath = '/home/shashank/intern_17/data/updated_player_stats/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    files = sorted(onlyfiles)
    count = 0
    for f in files:
        print count, f
        update_player_indexes(f)
        count += 1
