import yaml
from math import sqrt

def yaml_loader(filepath):
    with open(filepath,'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def yaml_dump(filepath,data):
    with open(filepath,"w") as file_descriptor:
        yaml.dump(data,file_descriptor)


def calculate_for_match(name,n,batting_score,batsman_count,bowling_score,bowler_count):
    path = '/home/shashank/intern_17/data/updated_player_stats/' + name
    data = yaml_loader(path)
    team_a_name = data.keys()[0]
    team_a_name = data.keys()[1]
    count = 0
    for team in data.keys():
        for pl in data[team][0]['batting averages']:
            if int(pl['Mat']) == n:
                if int(pl['Inns']) > 0:
                    if float(pl['Ave']) != 0 and float(pl['SR']) != 0:
                        batsman_count += 1
                        batting_score += round(float(pl['Ave'])*float(pl['SR'])*sqrt(float(pl['Inns'])/float(pl['Mat'])),2)
                for bl in data[team][1]['bowling averages']:
                    if bl['Player'] == pl['Player']:
                        if int(bl['Inns']) > 0:
                            if float(bl['Econ']) != 0 and float(bl['SR']) != 0:
                                print 'Bat:',pl['Player']
                                print 'Bowl:',bl['Player']
                                bowler_count += 1
                                bowling_score += round(sqrt(float(bl['Inns'])/float(bl['Mat']))/(float(bl['Econ'])*float(bl['SR'])),7)

    return (batting_score,batsman_count,bowling_score,bowler_count)

def calculate_aggregate_score(tup):
    batting_average = None
    bowling_average = None
    if tup[1] != 0:
        batting_average = tup[0]/tup[1]
    if tup[3] != 0:
        bowling_average = tup[2]/tup[3]
    return (batting_average,bowling_average)

if __name__ == '__main__':
    season_1_files = [(str(i) + '.yaml') for i in range(335982,336041)]
    season_1_files.remove(season_1_files[48])
    season_2_files = [(str(i) + '.yaml') for i in range(392181, 392240)]
    season_2_files.remove(season_2_files[6])
    season_2_files.remove(season_2_files[11])
    tup = (0,0,0,0)
    yaml_store = {}
    for i in range(1,9):
        for f in season_1_files:
            tup = calculate_for_match(f,i,tup[0],tup[1],tup[2],tup[3])
        for f in season_2_files:
            tup = calculate_for_match(f,i,tup[0],tup[1],tup[2],tup[3])
        agg = calculate_aggregate_score(tup)
        yaml_store[i] = [{'batting score':agg[0]},{'bowling score':agg[1]}]
    print yaml_store
    path = '/home/shashank/intern_17/data/debut_last_n_scores.yaml'
    yaml_dump(path,yaml_store)
