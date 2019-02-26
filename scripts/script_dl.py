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



mypath = '/home/shashank/intern_17/data/ipl/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
write_data = []
onlyfiles.remove('README.txt')
for fl in onlyfiles:
    print fl
    data = yaml_loader(mypath + fl)
    temp = data['info']['outcome']
    if 'method' in temp.keys() and temp['method'] == 'D/L':
        write_data.append({'DL':fl})

yaml_dump('/home/shashank/intern_17/data/dl_files.yaml',write_data)
