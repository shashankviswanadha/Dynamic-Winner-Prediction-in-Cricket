import os
import yaml
from os import listdir
from os.path import isfile, join

def yaml_loader(filepath):
    with open(filepath,'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def yaml_dump(filepath,data):
    with open(filepath,"w") as file_descriptor:
        yaml.dump(data,file_descriptor)

def sort_player(f_name):

    path = '/home/shashank/intern_17/data/player_indexes/' + f_name

    data = yaml_loader(path)
    newlist = sorted(data, key=lambda k: int(k['match number']))
    yaml_dump(path,newlist)

if __name__ == '__main__':
    mypath = '/home/shashank/intern_17/data/player_indexes/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for f in onlyfiles:
        print 'Sorting :',f
        sort_player(f)
