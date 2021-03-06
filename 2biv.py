import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error , hamming_loss
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import zero_one_loss
from sklearn.svm import LinearSVC, SVC
from sklearn.multiclass import OneVsRestClassifier
from imblearn.over_sampling import SMOTE
from imblearn.combine import SMOTEENN, SMOTETomek
from sklearn.metrics import accuracy_score
from sklearn.metrics import hamming_loss


# dataframe = pd.read_csv("drive/app/Frogs_MFCCs.csv")
dataframe = pd.read_csv("/media/ghost/Games And Images/INF552/hw4/Anuran Calls (MFCCs)/Frogs_MFCCs.csv")

dataframe.drop('RecordID',axis=1,inplace=True)
dataframe.replace('Bufonidae',int(1),inplace=True)
dataframe.replace('Dendrobatidae',int(2),inplace=True)
dataframe.replace('Hylidae',int(3),inplace=True)
dataframe.replace('Leptodactylidae',int(4),inplace=True)

dataframe.replace('Adenomera',int(10),inplace=True)
dataframe.replace('Ameerega',int(11),inplace=True)
dataframe.replace('Dendropsophus',int(12),inplace=True)
dataframe.replace('Hypsiboas',int(13),inplace=True)
dataframe.replace('Leptodactylus',int(14),inplace=True)
dataframe.replace('Osteocephalus',int(15),inplace=True)
dataframe.replace('Rhinella',int(16),inplace=True)
dataframe.replace('Scinax',int(17),inplace=True)

dataframe.replace('AdenomeraAndre',int(100),inplace=True)
dataframe.replace('AdenomeraHylaedactylus',int(101),inplace=True)
dataframe.replace('Ameeregatrivittata',int(102),inplace=True)
dataframe.replace('HylaMinuta',int(103),inplace=True)
dataframe.replace('HypsiboasCinerascens',int(104),inplace=True)
dataframe.replace('HypsiboasCordobae',int(105),inplace=True)
dataframe.replace('LeptodactylusFuscus',int(106),inplace=True)
dataframe.replace('OsteocephalusOophagus',int(107),inplace=True)
dataframe.replace('Rhinellagranulosa',int(108),inplace=True)
dataframe.replace('ScinaxRuber',int(109),inplace=True)


dataframe.to_csv('/media/ghost/Games And Images/INF552/hw4/Frogs_MFCCs-changed.csv',index=False)
# dataframe.to_csv('drive/app/Frogs_MFCCs-changed.csv',index=False)
# print(dataframe)

dataset=dataframe.values
# print(dataset.shape)
shuf_ds = shuffle(dataset, random_state=4)

X=shuf_ds[:,:22]
Y=shuf_ds[:,22:]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30)



# family sampling
X_train_family=X_train
X_test_family=X_test

Y_train_family=Y_train[:,:1]
Y_test_family=Y_test[:,:1]

sampling=SMOTEENN(random_state=0,kind_smote='svm')
X_train_family_smote, Y_train_family_smote = sampling.fit_sample(X_train_family, Y_train_family)
X_test_family_smote, Y_test_family_smote = sampling.fit_sample(X_test_family, Y_test_family)

# genus sampling

X_train_genus=X_train
X_test_genus=X_test


Y_train_genus= Y_train[:,1:2]
Y_test_genus=Y_test[:,1:2]


sampling=SMOTEENN(random_state=0,kind_smote='svm')
X_train_genus_smote, Y_train_genus_smote = sampling.fit_sample(X_train_genus, Y_train_genus)
X_test_genus_smote, Y_test_genus_smote = sampling.fit_sample(X_test_genus, Y_test_genus)


# species sampling
X_train_species=X_train
X_test_species=X_test

Y_train_species= Y_train[:,2:]
Y_test_species=Y_test[:,2:]

sampling=SMOTEENN(random_state=0,kind_smote='svm')
X_train_species_smote, Y_train_species_smote = sampling.fit_sample(X_train_species, Y_train_species)
X_test_species_smote, Y_test_species_smote = sampling.fit_sample(X_test_species, Y_test_species)

# print(Y_test_family.shape)


# hyperparameter setup
cv = KFold(10)
# Cs = np.linspace(0.01,5,5)
cs=  np.logspace(-2.3, -1.3, 10)

gamma_range = np.logspace(-9, 3, 3)
# print(gamma_range)
# tuned_parameters = {'C': [1,10,100]}
tuned_parameters=dict(C=cs)
# estimator__clf__gamma=gamma_range
# [0.1, 1.5]
# parameters = {'estimator__kernel':('linear', 'rbf'), 'estimator__C':Cs}
# param_grid = dict(gamma=gamma_range, C=Cs)


Cs=np.linspace(0.01,60,20)
tuned_parameters = [{'C': Cs}]


print('\n post-SMOTE')

# SVM for family label
print("\n##### Linear SVC with L1 penalty for Label:Family... \n")
clf = GridSearchCV(LinearSVC(penalty='l1', dual=False,tol=0.1), tuned_parameters, cv=cv, refit=True, n_jobs=2)

# model=OneVsRestClassifier(LinearSVC(tol=0.1,penalty='l1',dual=False))
# {"C": [0.001, 0.01, 0.1, 1.0, 10.0]}
# clf = GridSearchCV(model, param_grid=tuned_parameters, cv=cv, refit=True, n_jobs=5)




print('Fitting...')



clf.fit(X_train_family_smote, Y_train_family_smote.ravel())

scores = clf.cv_results_['mean_test_score']
scores_std = clf.cv_results_['std_test_score']

print("Best SVM-penalty parameter is ", clf.best_params_)
print("Best Score with this parameter is", clf.best_score_)
# sigma=1/(np.sqrt(2*clf.best_params_.get('estimator__gamma')))
# print("\nMargin-Width: ",sigma)

print('Predicting...')
preds = clf.predict(X_test_family_smote)
# print(preds)
test_score_family = accuracy_score(Y_test_family_smote, preds)
print("Test Score:", test_score_family)
test_error_family = 1 - test_score_family

hamming_family=hamming_loss(Y_test_family_smote, preds)
print('Hamming Loss:',hamming_family)

zero_one=zero_one_loss(Y_test_family_smote,preds)
# print('Zero-one loss:',zero_one)



# for genus


print("\n##### Linear SVC with L1 penalty for Label:Genus... \n")


clf = GridSearchCV(LinearSVC(penalty='l1', dual=False,tol=0.1), tuned_parameters, cv=cv, refit=True, n_jobs=2)
print('Fitting...')
clf.fit(X_train_genus_smote, Y_train_genus_smote.ravel())

scores = clf.cv_results_['mean_test_score']
scores_std = clf.cv_results_['std_test_score']

print("Best SVM-penalty parameter is ", clf.best_params_)
print("Best Score with this parameter is", clf.best_score_)
# sigma=1/(np.sqrt(2*clf.best_params_.get('estimator__gamma')))
# print("\nMargin-Width: ",sigma)

print('Predicting...')
preds_ge = clf.predict(X_test_genus_smote)
# print(preds)

test_score_genus = accuracy_score(Y_test_genus_smote, preds_ge.reshape(len(preds_ge),1))
print("Test Score:", test_score_genus)
test_error_genus = 1 - test_score_genus


hamming_genus=hamming_loss(Y_test_genus_smote, preds_ge)
print('Hamming Loss:',hamming_genus)
zero_one=zero_one_loss(Y_test_genus_smote,preds_ge)
# print('Zero-one loss:',zero_one)


# for species

print("\n##### Linear SVC with L1 penalty for Label:Species... \n")


clf = GridSearchCV(LinearSVC(penalty='l1', dual=False,tol=0.1), tuned_parameters, cv=cv, refit=True, n_jobs=2)
print('Fitting...')
clf.fit(X_train_species_smote, Y_train_species_smote.ravel())

scores = clf.cv_results_['mean_test_score']
scores_std = clf.cv_results_['std_test_score']

print("Best SVM-penalty parameter is ", clf.best_params_)
print("Best Score with this parameter is", clf.best_score_)

# sigma=1/(np.sqrt(2*clf.best_params_.get('estimator__gamma')))
# print("\nMargin-Width: ",sigma)

print('Predicting...')
preds_sp = clf.predict(X_test_species_smote)

# print(preds)
test_score_species = accuracy_score(Y_test_species_smote, preds_sp)
print("Test Score:", test_score_species)
test_error_species = 1 - test_score_species

hamming_species=hamming_loss(Y_test_species_smote, preds_sp)
print('Hamming Loss:',hamming_species)
zero_one=zero_one_loss(Y_test_species_smote,preds_sp)
# print('Zero-one loss:',zero_one)


print(preds.shape)
print(Y_test_genus_smote.shape)
correct_classification=0
misclassified=0
for i in range(0,len(preds)):
    if((preds[i]==Y_test_family_smote[i]) and (preds_sp[i]==Y_test_species_smote[i]) and (preds_ge[i]==Y_test_genus_smote[i])):
        correct_classification+=1
    else:
        misclassified+=1

net_zero_one=misclassified/len(preds)
arr=[]
arr.append(hamming_family)
arr.append(hamming_genus)
arr.append(hamming_species)
arr=np.array(arr)
net_hamm=np.mean(arr)
print("\nAverage Hamming Loss:",net_hamm)
print("\nAverage Zero-one Loss:",net_zero_one)