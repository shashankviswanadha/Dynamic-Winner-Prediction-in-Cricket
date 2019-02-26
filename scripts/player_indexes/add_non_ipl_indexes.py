import os
import yaml
from os import listdir
from os.path import isfile, join
import sort

def yaml_loader(filepath):
    with open(filepath,'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def yaml_dump(filepath,data):
    with open(filepath,"w") as file_descriptor:
        yaml.dump(data,file_descriptor)
def add_indexes(f_name):

    path = '/home/shashank/intern_17/data/player_indexes/' + f_name

    data = yaml_loader(path)
    current_number = int(data[0]['match number'])
    for i in range(1,current_number):
        data.append({'match number':str(i),'competition':'unknown'})
    for i in range(1,len(data)):
        if current_number +1 != int(data[i]['match number']):
            for j in range(current_number +1,int(data[i]['match number'])):
                data.append({'match number':str(j),'competition':'unknown'})
        current_number =  int(data[i]['match number'])

    yaml_dump(path,data)

if __name__=='__main__':
    mypath = '/home/shashank/intern_17/data/player_indexes/'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for f in onlyfiles:
        print 'Adding indexes :',f
        add_indexes(f)
        print 'Sorting :',f
        sort.sort_player(f)
