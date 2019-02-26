
#from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
#from sklearn.gaussian_process import GaussianProcessClassifier
#from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
#from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.grid_search import ParameterGrid
from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegression
from data import *
import matplotlib.pyplot as plt

def yaml_dump(filepath,data):
    with open(filepath,"w") as file_descriptor:
        yaml.dump(data,file_descriptor)


classifiers = [
    KNeighborsClassifier(5),
    SVC(),
    SVC(gamma=0.2, C=1),#c=[1,5],gamma = [0.2,0.3]
    DecisionTreeClassifier(),#10,15,20
    RandomForestClassifier(),#n_estimators = 50,100,200,500
    GradientBoostingClassifier(),#learn = 0.005,0.015,0.01,n_estimators = 50,100,200,500
    LogisticRegression()
]

params = {0:{'n_neighbors':[i for i in range(2,11)]},1:{'kernel':['linear'],'C':[1,2,3,4,5]},2:{'C':[1,2,3,4,5],'gamma': [0.2,0.3]},3:{'max_depth':[i for i in range(2,21)]},4:{'n_estimators':[i for i in range(1,41)],'max_depth':[i for i in range(1,16)],'max_features':[1,2,3,4],'n_jobs':[-1]},5:{'n_estimators':[i for i in range(2,30)],'learning_rate':[0.005,0.015,0.01]},6:{'C':[1,2,3,4,5],'penalty':['l1','l2']}}

names = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree", "Random Forest", "Gradient Boost","Logistic Regression"]

def calclulate_drop(li):
    prev = li[0]
    count = 0
    for i in range(1,len(li)):
        if li[i] < prev:
            count += 1
        prev = li[i]
    #print count
    return count

train_x,train_y = get_data_for_ml(0,20)
valid_x,valid_y = get_data_for_ml(2,20)
test_20_x,test_20_y = get_data_for_ml(1,20)
min_drop = 0
best_acc = 0
best_test_score = 0
best_valid_score = 0
X = [i for i in range(21)]
dt = {}
for k in range(21):
    test_x,test_y = get_single_over_test_data(k)
    dt[k] = (test_x,test_y)
for i in range(1):
    print i
    Y = []
    clf = SVC(gamma=0.2,C=5) #RandomForestClassifier(max_depth=9,n_estimators=28,max_features=1,n_jobs=-1)#classifiers[2]
    clf.fit(train_x,train_y)
    for k in range(21):
        Y.append(clf.score(dt[k][0],dt[k][1]))

    drop = calclulate_drop(Y)
    if ((Y[len(Y)-1] == 1 and Y[0]>0.62 and drop < min_drop) or i == 0):
        min_drop = drop
        best_acc = Y
        best_test_score = clf.score(test_20_x,test_20_y)
        best_valid_score = clf.score(valid_x,valid_y)
        print i,min_drop
#te_x,te_y = get_data_for_ml(1,20)
#print names[4]
#print clf.n_features_,clf.feature_importances_
print best_valid_score
print best_test_score
print best_acc
plt.figure()
plt.plot(X,best_acc)
plt.show()



'''#parameters = {'max_depth':[i for i in range(2,16)]}#{'kernel':['rbf'], 'C':[1,2,3,4,5,6,7,8,9,10,11,12,13],'gamma':[0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.001,0.01]}
#par = {'n_estimators':[i for i in range(1,31)],'max_features':[i for i in range(1,5)],'max_depth':[i for i in range(1,11)]}
#write_data = []
for i in range(2,3):
    grid = list(ParameterGrid(params[i]))
    best_grid = best_score = 0
    for g in grid:
        print names[i],g
        clf = classifiers[i]
        clf.set_params(**g)
        clf.fit(train_x,train_y)
        if clf.score(valid_x,valid_y) > best_score :
            best_score = clf.score(valid_x,valid_y)
            best_grid = g
            print best_score
    print best_grid,best_score'''
    #write_data.append({'Classifier':names[i],'best_grid':best_grid,'best_score':best_score})

#path = '/home/shashank/intern_17/data/param_grid_results.yaml'
#yaml_dump(path,write_data)
