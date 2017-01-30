#!/usr/bin/python

import sys
import pickle
import matplotlib.pyplot as plt
import numpy as np
sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier

###################################################################
### Task 1: Select what features you'll use.
###################################################################
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','salary', 'total_payments', 'total_stock_value',
'exercised_stock_options', 'expenses', 'restricted_stock',
'shared_receipt_with_poi'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

### 1.1. List all the features existed in the dataset
features_total = []
for ppl in data_dict.keys():
    for feature in data_dict[ppl].keys():
        if feature not in features_total:
            features_total.append(feature)

### 1.2. How many ppl are POI and Non-POI?
number_of_POI = 0
number_of_Non_POI = 0
for ppl in data_dict.keys():
    if data_dict[ppl]["poi"] == 1:
        number_of_POI  += 1
    else:
        number_of_Non_POI += 1

print("POI in the dataset: ", number_of_POI)
print ("Non-POI in the dataset: ", number_of_Non_POI)


### 1.3. Pick the features
# Count the number of NaN for each feature in POI and non-POI
POI_number = {}
Non_POI_number = {}

for feature in features_total:
    POI_number[feature] = 0
    Non_POI_number[feature] = 0

for ppl in data_dict.keys():
    if data_dict[ppl]["poi"] == 1:
        for feature in features_total:
            if data_dict[ppl][feature] != 'NaN':
                POI_number[feature] = POI_number[feature] + 1
    else:
        for feature in features_total:
            if data_dict[ppl][feature] != 'NaN':
                Non_POI_number[feature] = Non_POI_number[feature] + 1

# Or use the following fuction to print the pretty results
def pretty_print(d, indent=0):
   for key, value in d.iteritems():
      print '\t' * indent + str(key)
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print '\t' * (indent+1) + str(value)

print POI_number
# pretty_print(POI_number)
print Non_POI_number
# pretty_print(Non_POI_number)

###################################################################
### Task 2: Remove outliers
###################################################################

### Remove the "TOTAL" dataset
del data_dict["TOTAL"]


### Histogram showing the distrbution of financial features
def his_plot (f, f_name = "feature 1"):
    POI_data = []
    NPOI_data = []

    for ppl in data_dict.keys():
        if data_dict[ppl]["poi"] == 1 and data_dict[ppl][f]!='NaN':
            POI_data.append(data_dict[ppl][f])

        elif data_dict[ppl]["poi"] == 0 and data_dict[ppl][f]!='NaN':
            NPOI_data.append(data_dict[ppl][f])


    plt.hist(POI_data, alpha = 0.5, label = 'POI')
    plt.hist(NPOI_data, alpha = 0.5, label = 'non-POI')
    plt.legend(loc = 'upper right')
    plt.title(f_name)
    #plt.savefig(name)

financial_features_list = ['salary', 'total_payments', 'total_stock_value',
'exercised_stock_options', 'expenses', 'restricted_stock']

plt.figure(figsize=(12, 8))
for i, f in enumerate(financial_features_list):
    plt.subplot(2,3, i+1)
    his_plot(f, f)

plt.savefig('financial_features.png')
plt.show()


email_features_list = ['to_messages', 'shared_receipt_with_poi',
'from_messages', 'from_poi_to_this_person', 'from_this_person_to_poi']

plt.figure(figsize=(12, 8))
for i, f in enumerate(email_features_list):
    plt.subplot(2,3, i+1)
    his_plot(f, f)

plt.savefig('email_features.png')
plt.show()

# Outliers will be removed again after creating new features
###################################################################
### Task 3: Create new feature(s)
###################################################################

### Store to my_dataset for easy export below.
my_dataset = data_dict

# Create new email percentage features

for ppl in my_dataset.keys():
    if my_dataset[ppl]['to_messages'] != 'NaN' and \
    my_dataset[ppl]['from_messages'] != 'NaN' and \
    my_dataset[ppl]['from_poi_to_this_person'] != 'NaN' and \
    my_dataset[ppl]['from_this_person_to_poi'] != 'NaN':
        my_dataset[ppl]['from_poi_frequency'] = \
        float(my_dataset[ppl]['from_poi_to_this_person']) / \
        float(my_dataset[ppl]['from_messages'])
        my_dataset[ppl]['to_poi_frequency'] = \
        float(my_dataset[ppl]['from_this_person_to_poi']) / \
        float(my_dataset[ppl]['to_messages'])
    else:
            my_dataset[ppl]['from_poi_frequency'] = 'NaN'
            my_dataset[ppl]['to_poi_frequency'] = 'NaN'


# Create new financial feature: Total income
for ppl in my_dataset.keys():
    if my_dataset[ppl]['salary'] != 'NaN' and \
    my_dataset[ppl]['total_stock_value'] != 'NaN' and \
    my_dataset[ppl]['bonus'] != 'NaN':
        my_dataset[ppl]['Total_income'] = my_dataset[ppl]['salary'] + \
        my_dataset[ppl]['total_stock_value'] + \
        my_dataset[ppl]['bonus']

    else:
        my_dataset[ppl]['Total_income'] = 'NaN'

# Create new financial feature: exercised_stock_percentage
for ppl in my_dataset.keys():
    if my_dataset[ppl]['total_stock_value'] != 'NaN' and \
    my_dataset[ppl]['exercised_stock_options'] != 'NaN':
        my_dataset[ppl]['exercised_stock_percentage'] = \
        float(my_dataset[ppl]['exercised_stock_options']) / \
        my_dataset[ppl]['total_stock_value']

    else:
        my_dataset[ppl]['exercised_stock_percentage'] = 'NaN'

# Add the newly created features to the features_list
features_list = features_list + ['from_poi_frequency',
'to_poi_frequency', 'Total_income', 'exercised_stock_percentage']

#print len(features_list)

# There are 12 features in the list, if we want to use those feature to build a classifer,
# it at least has to have some non NaN features values.
# For those who has more than 10 missing values in the dataset, they will be discarded as Outliers.
Outliers = []
for ppl in my_dataset.keys():
    count = 0
    for f in features_list:
        if my_dataset[ppl][f] == 'NaN':
            count = count + 1
    if count >= 10:
        Outliers.append(ppl)


for ppl in Outliers:
    del data_dict[ppl]


# Recalculate the number of POI and Non_POI in the dataset after outliers removal
number_of_POI = 0
number_of_Non_POI = 0
for ppl in my_dataset.keys():
    if my_dataset[ppl]["poi"] == 1:
        number_of_POI  += 1
    else:
        number_of_Non_POI += 1

print("POI in the dataset after outliers removal: ", number_of_POI)
print ("Non-POI in the dataset after outliers removal: ", number_of_Non_POI)

###################################################################
### Task 4: Try a variety of classifiers
###################################################################

##########
# Evaluate the classifiers with accuracy, recall and precision
from sklearn.model_selection import train_test_split
def evaluate_clf(clf, data, features_list, normalize = False, ave = 'binary'):
    """
    evaluate_clf is used to evaluate the performance of POI classifiers

    Parameters
    ----------
    clf: classifier
    data: enron dataset
    features_list: the features that will be used in this classifier
    normalize: default = False. If it equals true, features scaling will be
                perfromed before spliting train and test dataset
    ave: it determines the type of averaging performed on the data.

    Returns
    -------
    accuracy: the accuracy of the classifier
    recall: the ratio of true positive / (true positive + false negative)
    presicion: the ratio of true positive / (true positive + false positive)

    """
    from sklearn.metrics import recall_score
    from sklearn.metrics import precision_score
    from sklearn.metrics import accuracy_score

    test_data = featureFormat(data, features_list, sort_keys = True)
    labels, features = targetFeatureSplit(test_data)
    ### Extract features and labels from dataset for local testing

    if normalize == True:
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        features = scaler.fit_transform(features)


    features_train, features_test, labels_train, labels_test = \
        train_test_split(features, labels, test_size=0.3, random_state=42)
    clf.fit(features_train, labels_train)
    pred = clf.predict(features_test)
    accuracy = accuracy_score(labels_test, pred)
    recall = recall_score(labels_test, pred, average = ave)
    precision = precision_score(labels_test, pred, average = ave)
    return accuracy, recall, precision


###################
# 4.1. Naive Bayes
from sklearn.naive_bayes import GaussianNB
clf_NB = GaussianNB()
accuracy, recall, precision = evaluate_clf(clf_NB, my_dataset, features_list)
print ("The accuracy for Naive bayes: %f" % (accuracy))
print ("The recall for Naive bayes: %f" % (recall))
print ("The precision for Naive bayes: %f" % (precision))

###################
# 4.2. The KNeighborsClassifier - KNN
# KNN performs better with lower dimensionality.
# KNN can't calculate missing value in a dataset
# KNN performs better if all the features have same scale
# Based on the 3 rules,
# SelectKBest & correlation analysis & Scaling will be performed first

# SelectKBest
from sklearn.feature_selection import SelectKBest
KB = SelectKBest(k = 5)
KB.fit(features, labels)
new_list = zip(KB.get_support(), features_list[1:], KB.scores_)
new_list = sorted(new_list, key=lambda x: x[2], reverse=True)
print "K-best features:", new_list

# Correlation matrix
import pandas as pd
import numpy
df = pd.DataFrame.from_dict(my_dataset, orient='index')
df.apply(lambda x: pd.to_numeric(x, errors='coerce'))
df.replace(to_replace='NaN', value=numpy.nan, inplace=True)

def plot_corr(df,size=10):
    '''Function plots a graphical correlation matrix for each pair of columns in the dataframe.

    Input:
        df: pandas DataFrame
        size: vertical and horizontal size of the plot'''

    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size, size))
    ax.matshow(corr)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90);
    plt.yticks(range(len(corr.columns)), corr.columns);

plot_corr(df)
plt.savefig('correlation_matrix.png')
plt.show()

# total_stock_value was picked for KNeighborsClassifier
new_features_list = ['poi', 'exercised_stock_options']

# KNN
from sklearn.neighbors import KNeighborsClassifier
KNN= KNeighborsClassifier(n_neighbors = 5)
accuracy, recall, precision = evaluate_clf(KNN, my_dataset, new_features_list,
normalize = True)
print ("The accuracy for KNeighborsClassifier is: %f" % (accuracy))
print ("The recall for KNeighborsClassifier is: %f" % (recall))
print ("The precision for KNeighborsClassifier is: %f" % (precision))

###################
# 4.3. Decision Tree Classifier
from sklearn.tree import DecisionTreeClassifier
clf_DT = DecisionTreeClassifier(min_samples_split = 5, criterion = 'gini')
accuracy, recall, precision = evaluate_clf(clf_DT, my_dataset, features_list)
print ("The accuracy for DecisionTreeClassifier is: %f" % (accuracy))
print ("The recall for DecisionTreeClassifier is: %f" % (recall))
print ("The precision for DecisionTreeClassifier is: %f" % (precision))

###################
# 4.4. AdaBoostClassifier
from sklearn.ensemble import AdaBoostClassifier
dt = DecisionTreeClassifier(min_samples_split = 5)
clf_Ada = AdaBoostClassifier(base_estimator = dt)
accuracy, recall, precision = evaluate_clf(clf_Ada, my_dataset, features_list)
print ("The accuracy for AdaBoostClassifier is: %f" % (accuracy))
print ("The recall for AdaBoostClassifier is: %f" % (recall))
print ("The precision for AdaBoostClassifier is: %f" % (precision))
###################
# 4.5. RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
clf_RF = RandomForestClassifier(n_estimators=5)
accuracy, recall, precision = evaluate_clf(clf_RF, my_dataset, features_list)
print ("The accuracy for RandomForestClassifier is: %f" % (accuracy))
print ("The recall for RandomForestClassifier is: %f" % (recall))
print ("The precision for RandomForestClassifier is: %f" % (precision))

###################
# 4.6. SVC
from sklearn.svm import SVC
clf_SVC = SVC (C = 0.5, tol = 0.01)
accuracy, recall, precision = evaluate_clf(clf_SVC, my_dataset, features_list,
normalize = True, ave = 'macro')
print ("The accuracy for SVC is: %f" % (accuracy))
print ("The recall for SVC is: %f" % (recall))
print ("The precision for SVC is: %f" % (precision))

###################
# 4.7. LogisticRegression
from sklearn.linear_model import LogisticRegression
clf_log = LogisticRegression (C = 0.5)
accuracy, recall, precision = evaluate_clf(clf_log, my_dataset, features_list,
normalize = True, ave = 'macro')
print ("The accuracy for SVC is: %f" % (accuracy))
print ("The recall for SVC is: %f" % (recall))
print ("The precision for SVC is: %f" % (precision))



###################################################################
### Task 5: Turning
###################################################################

###################
# 5.1. Cross_validation for KNeighborsClassifier
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.cross_validation import StratifiedKFold

pca = PCA ()
selection = SelectKBest ()
combined_features = FeatureUnion([("pca", pca), ("K_best", selection)])


KNN= KNeighborsClassifier()
param_grid = dict(features__pca__n_components = [1, 2, 3],
                  features__K_best__k = [1, 2, 3],
                  KNN__n_neighbors = [2, 3 , 4, 5, 6, 8])

pipeline = Pipeline([("features", combined_features), ("KNN", KNN)])

KNN_clf = GridSearchCV(pipeline,
                    param_grid=param_grid,
                    cv = StratifiedKFold(labels_train, n_folds = 10),
                    verbose=10)

KNN_clf = KNN_clf.fit(features_train, labels_train)
print KNN_clf.best_estimator_
KNN_pred = KNN_clf.predict(features_test)
accuracy = accuracy_score(labels_test, KNN_pred)
recall = recall_score (labels_test, KNN_pred, average = 'macro')
precision = precision_score(labels_test, KNN_pred, average = 'macro')
print ("The accuracy of the best KNeighborsClassifier is: %f" % (accuracy))
print ("The recall of the best KNeighborsClassifier is: %f" % (recall))
print ("The precision of the best KNeighborsClassifier is: %f" % (precision))


###################
# 5.2. cross_validation for SVC
from sklearn.model_selection import GridSearchCV

svc = SVC()
param_grid = [
  {'C': [0.5, 1, 5, 10, 100, 1000],"tol":[10**-1, 10**-10], 'kernel': ['linear']},
  {'C': [0.5, 1, 5, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
 ]

 SVC_clf = GridSearchCV(svc,
                    param_grid=param_grid,
                    cv = StratifiedKFold(labels_train, n_folds = 10),
                    verbose=10)

SVC_clf = SVC_clf.fit(features_train, labels_train)
print SVC_clf.best_estimator_
SVC_pred = SVC_clf.predict(features_test)
accuracy = accuracy_score(labels_test, SVC_pred)
recall = recall_score (labels_test, SVC_pred, average = 'macro')
precision = precision_score(labels_test, SVC_pred, average = 'macro')
print ("The accuracy of the best SVC is: %f" % (accuracy))
print ("The recall of the best SVC is: %f" % (recall))
print ("The precision of the best SVC is: %f" % (precision))

###################
# 5.3. Cross_validation for AdaBoostClassifier
dt = DecisionTreeClassifier()
param_grid =  [{'min_samples_split' :[2, 5, 8, 10], 'criterion': ['gini']},
                {'min_samples_split' :[2, 5, 8, 10], 'criterion': ['entropy']}]

dt_clf = GridSearchCV(dt,
                    param_grid=param_grid,
                    cv = StratifiedKFold(labels_train, n_folds = 10),
                    verbose=10)
dt_clf = dt_clf.fit(features_train, labels_train)
print dt_clf.best_estimator_

clf_Ada = AdaBoostClassifier(base_estimator = dt_clf.best_estimator_)
clf_Ada.fit(features_train, labels_train)
Ada_pred = clf_Ada.predict(features_test)
accuracy = accuracy_score(labels_test, Ada_pred)
recall = recall_score (labels_test, Ada_pred, average = 'macro')
precision = precision_score(labels_test, Ada_pred, average = 'macro')
print ("The accuracy of the best AdaBoostClassifier is: %f" % (accuracy))
print ("The recall of the best AdaBoostClassifier is: %f" % (recall))
print ("The precision of the best AdaBoostClassifier is: %f" % (precision))


###################################################################
### Task 6: validatiing
###################################################################
clf = clf_Ada
### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)
