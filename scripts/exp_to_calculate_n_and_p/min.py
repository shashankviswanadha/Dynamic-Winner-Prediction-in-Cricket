import yaml

def yaml_loader(filepath):
    with open(filepath,'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

path = '/home/shashank/intern_17/data/normalized_np_exp.yaml'
data = yaml_loader(path)
mi = 45122
p = 0.2
n = 3
for i in range(3,9):
    for sc in data[i]:
        if sc['distance'] < mi:
            mi = sc['distance']
            p = sc['p']
            n = i

print mi,n,p
