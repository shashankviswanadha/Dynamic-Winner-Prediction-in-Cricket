from bs4 import BeautifulSoup
import requests
import re
import yaml


def yaml_dump(filepath,data):
    with open(filepath,"w") as file_descriptor:
        yaml.dump(data,file_descriptor)

def extract_team_stats(table,data,team,type_stat):
    schema = []
    data_player = []
    for tr in table.find_all('tr'):
        if tr == table.find_all('tr')[0]:
            for th in tr.find_all('th'):
                schema.append(str(th.text))
        else:
            for td in tr.find_all('td'):
                data_player.append(str(td.text))
            add_player_data(schema,data_player,data,team,type_stat)
            data_player = []

def add_player_data(schema,data_player,data,team,type_pl):
    data_dict = {}
    for i in range(len(schema)):
        data_dict[schema[i]] = data_player[i]
    if type_pl == 0:
        data[team][0]['batting averages'].append(data_dict)
    else:
        data[team][1]['bowling averages'].append(data_dict)

def get_team_name(table):
    li = ['batting', 'averages','Twenty20','matches','bowling']
    sentence = table.find_all('caption')[0].text
    team_name_li = filter(lambda w: w not in li, re.split(r'\W+', sentence))
    team_name = str(''.join(team_name_li))
    return team_name

def get_file_name(url):
    words = re.findall(r"\b/\w*?.html\b",url)
    n = words[0].replace('/','')
    name = n.replace('html','')
    name = '/home/shashank/intern_17/data/player_stats/' + name + 'yaml'
    return name

def pull_player_stats_to_yaml(url):
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content)#,"html_parser")

    #extract stat tables
    team_a_batting_table = soup.find_all('table')[0]
    team_a_bowling_table = soup.find_all('table')[1]
    team_b_batting_table = soup.find_all('table')[2]
    team_b_bowling_table = soup.find_all('table')[3]

    #extract team names
    team_a_name = get_team_name(team_a_batting_table)
    team_b_name = get_team_name(team_b_batting_table)

    # initialize yaml dictionary
    data_yaml = {team_a_name:[{'batting averages':[]},{'bowling averages':[]}],team_b_name:[{'batting averages':[]},{'bowling averages':[]}]}

    extract_team_stats(team_a_batting_table,data_yaml,team_a_name,0)
    extract_team_stats(team_a_bowling_table,data_yaml,team_a_name,1)
    extract_team_stats(team_b_batting_table,data_yaml,team_b_name,0)
    extract_team_stats(team_b_bowling_table,data_yaml,team_b_name,1)

    file_name = get_file_name(url)
    yaml_dump(file_name,data_yaml)

if __name__ == '__main__':
    pull_player_stats_to_yaml('http://www.espncricinfo.com/indian-premier-league-2017/engine/match/1082593.html?view=averages')
