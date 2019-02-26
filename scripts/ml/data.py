import yaml
import numpy as np
from itertools import chain, islice
from numpy import s_

def cslice(iterable, *selectors):
    return chain(*(islice(iterable,*s) for s in selectors))

def yaml_loader(filepath):
    with open(filepath,'r') as file_descriptor:
        data = yaml.load(file_descriptor)
    return data

def get_data_for_ml(train_or_test,overs):
    if train_or_test == 0:
        path = '/home/shashank/intern_17/data/data_for_ml/train_data.yaml'
    elif train_or_test == 1:
        path = '/home/shashank/intern_17/data/data_for_ml/test_data.yaml'
    elif train_or_test == 2:
        path = '/home/shashank/intern_17/data/data_for_ml/validation_data.yaml'
    data = yaml_loader(path)
    le = 0
    for j in range(overs+1):
        le += len(data[j])
    x = np.zeros((le, 4))
    y = []
    i = 0
    for k in range(overs+1):
        for val in data[k]:
            x[i] = val[:-1]#list(cslice(val,(0,3),(7,8)))
            y.append(val[-1])
            i+=1
    return (x,y)


def get_single_over_test_data(over):
    path = '/home/shashank/intern_17/data/data_for_ml/test_data.yaml'
    data = yaml_loader(path)
    le = 0
    for j in range(over,over+1):
        le += len(data[j])
    x = np.zeros((le, 4))
    y = []
    i = 0
    for k in range(over,over+1):
        for val in data[k]:
            x[i] = val[:-1]#list(cslice(val,(0,3),(7,8)))
            y.append(val[-1])
            i+=1
    return (x,y)
def calculate_accuracy(test_y,pred):
    error = 0
    acc = 0
    for i in range(len(test_y)):
        if test_y[i] != pred[i]:
            error += 1
        if test_y[i] == pred[i]:
            acc += 1
    accper = acc/float(len(test_y)) * 100.0
    print 'Error:',error
    print 'Accuracy:',acc
    print 'Testing Length:',len(test_y)
    print 'Accuracy:',acc/float(len(test_y)) * 100.0 ,'%'
    return accper
