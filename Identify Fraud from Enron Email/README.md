## P5: Identify Fraud from Enron Email

### Introduction
Enron Corporation was one of biggest energy and communication companies before 2001. It was named as "American's Most Innovative Company" for six consecutive years. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud. In the resulting Federal investigation, a significant amount of typically confidential information entered into the public record, including tens of thousands of emails and detailed financial data for top executives. The goal of this project is to identify potential individuals who was involved in Enron scandal by utilizing machine learning algorithm based on the financial and email data available.

There were 146 subjects in the dataset. Each subject had same fields describing different financial and email features.

1. financial features:
    ['salary', 'deferral_payments', 'total_payments', 'loan_advances', 'bonus', 'restricted_stock_deferred', 'deferred_income', 'total_stock_value', 'expenses', 'exercised_stock_options', 'other', 'long_term_incentive', 'restricted_stock', 'director_fees'] (all units are in US dollars)

2. email features:
    ['to_messages', 'email_address', 'from_poi_to_this_person', 'from_messages', 'from_this_person_to_poi', 'shared_receipt_with_poi'] (units are generally number of emails messages; notable exception is ‘email_address’, which is a text string)

3. POI label: [‘poi’] (boolean, represented as integer)
    Individuals with "True" in POI label were indicted, reached a settlement or plea deal with the government, or testified in exchange for prosecution immunity.


#### 1. Feature selection
Collecting data for such a dramatic business failure was not easy. Although the Enron Data Set has become the “industry standard” corpus for scientists and researchers, there are still a lot of missing values in the dataset. So the first step is to look at the number of "NaN" values in each feature.

1. Counting the number of useful values for each feature

    - There are 146 subjects in the data, 18 of them were labeled as POI.
    - For those 18 POIs, the number after each feature indicating how many of them were **not** "NaN".
    {'salary': 17, 'to_messages': 14, 'deferral_payments': 5, 'total_payments': 18, 'loan_advances': 1, 'bonus': 16, 'email_address': 18, 'restricted_stock_deferred': 0, 'total_stock_value': 18, 'shared_receipt_with_poi': 14, 'long_term_incentive': 12, 'exercised_stock_options': 12, 'from_messages': 14, 'other': 18, 'from_poi_to_this_person': 14, 'from_this_person_to_poi': 14, 'poi': 18, 'deferred_income': 11, 'expenses': 18, 'restricted_stock': 17, 'director_fees': 0}

    - The rest 128 subjects were labeled as Non-POI.
    - For those 128 Non-POIs, the number after each feature indicating how many of them were **not** "NaN".
    {'salary': 78, 'to_messages': 72, 'deferral_payments': 34, 'total_payments': 107, 'loan_advances': 3, 'bonus': 66, 'email_address': 93, 'restricted_stock_deferred': 18, 'total_stock_value': 108, 'shared_receipt_with_poi': 72, 'long_term_incentive': 54, 'exercised_stock_options': 90, 'from_messages': 72, 'other': 75, 'from_poi_to_this_person': 72, 'from_this_person_to_poi': 72, 'poi': 128, 'deferred_income': 38, 'expenses': 77, 'restricted_stock': 93, 'director_fees': 17}

2. Features with too many "NaN" could not be used effectively to classify our data. We would like to have features containing comparatively sufficient information in our algorithm. Based on this rule, here is the list of features I am going to dive in further:

    - financial features: salary, total_payments, bonus, total_stock_value, exercised_stock_options, expenses, restricted_stock
    - email features: to_messages, shared_receipt_with_poi, from_messages, from_poi_to_this_person, from_this_person_to_poi


#### 2. Remove outliers
1. The biggest outlier in this dataset is "TOTAL", which describes the sum of each financial features for all the subjects. It could not be used to identify POIs, thus it is removed first.

2. Histogram showing all the financial features and email features of both POI and Non-POI. It seems to have 1 or 2 extreme large values in most of the financial features, and they were from 'LAY KENNETH L' and 'SKILLING JEFFREY K'. Kenneth Lay and Jeffrey Skilling are both the major POIs involved in the scandal, thus it is not appropriate to consider them as outliers. In conclusion, all the data points are included in this project.

    ![Histogram of the financial features](_https://github.com/super-penguin/Udacity_Data_Analyst/blob/master/Identify%20Fraud%20from%20Enron%20Email/financial_features.png)

    ![Histogram of the email features](https://github.com/super-penguin/Udacity_Data_Analyst/blob/master/Identify%20Fraud%20from%20Enron%20Email/email_features.png)



#### 3. Create new features
1. New email features were created trough dividing the email from_poi_to_this_person by the total number of from_messages, or dividing the email from_this_person_to_poi by the total number of to_messages.
    - from_poi_frequency = from_poi_to_this_person / from_messages
    - to_poi_frequency = from_this_person_to_poi / to_messages

2. New financial feature was created by adding the salary, bonus and total_stock_value together.
    - Total_income = salary + bonus + total_stock_value
    - exercised_stock_percentage = exercised_stock_options / total_stock_value

3. Second time to remove outliers
    When screening the dataset, I found out that some subjects have a lot of missing values. If we are going to use those features to build the classifier, it wouldn't be useful if there are too many missing values. In the newly created feature list, we have 12 features in total. We are going to discard the subjects who has more than 10 missing values in those 12 features.
    Through this method, there turned out to be 6 more outliers. After outlier removal, the remaining dataset has 18 POI and 121 Non-POI.


#### 4. Try a variety of classifiers

1. Different classifiers were tried out and each of them were evaluated by recall and precision.
    According to the [estimator choosing map on scikit-learn](http://scikit-learn.org/stable/tutorial/machine_learning_map/), 7 classifiers were tested first. The rough performance (without parameters tuning) are listed in the following table.


    |  Classifiers            |  Accuracy  |  Recall    |  Precision  |  Parameters            |  Others                                         |
    | ----------------------- | ---------- | ---------- | ----------- | ---------------------- | ----------------------------------------------- |
    |  Naive Bayes            | 0.928571   | 0.666667   | 0.5         |                        |                                                 |
    |  K Nearest Neighbor     | 0.935484   | 0.666667   | 0.666667    | n_neighbors = 5        | Feature reduction were performed before fitting |
    |  Decision Tree          | 0.809524   | 0.333333   | 0.142857    | min_samples_split = 5  |                                                 |
    |  AdaBoost               | 0.928571   | 0.333333   | 0.500000    | min_samples_split = 5  |  Improved the performance of decision tree      |
    |  RandomForest           | 0.833333   | 0.333333   | 0.166667    | n_estimators = 5       |  The output will be different each time         |
    |  SVC                    | 0.928571   | 0.500000   | 0.464286    | C = 0.5, tol = 0.01    |  Features were scaled before fitting            |
    |  LogisticRegression     | 0.928571   | 0.500000   | 0.464286    | C = 0.5                |  Features were scaled before fitting            |       


    - Naive Bayes.
    Naive Bayes is a simple but powerful supervised learning algorithm. The performance is pretty good by measuring the evaluation metrics. It is very powerful especially in text discrimination. However, Naive Bayes treats each feature as independent and classify the dataset based on their conditional probabilities. The features in our dataset are not independent, on contrary, a lot of them are highly correlated. Thus, I will pick other classifiers over Naive Bayes in this project.


    - K Nearest Neighbor
    As an non parametric learning algorithm, K nearest neighbor is the first classifier came to my mind for this project. However, preprocessing steps are necessary for K Nearest Neighbor before fitting to ensure good performance. [1-2]
        * KNN performs better with lower dimensionality.
        * KNN can't calculate missing value in a dataset.
        * KNN performs better if all the features have same scale

        Based on the those rules, preprocessing steps including SelectKBest, correlation analysis and feature scaling were performed before fitting the data.

        * Score of the K-best features:

        | features                        | Scores                       |    Rank    |
        | ------------------------------- | ---------------------------- | ---------- |
        | 'exercised_stock_options'       | 23.686304622052319           |  Top 1     |
        | 'total_stock_value'             | 23.045072784811413           |  Top 2     |
        | 'Total_income'                  | 18.297007092784408           |  Top 3     |
        | 'salary'                        | 17.14638410991779            |  Top 4     |
        | 'restricted_stock'              | 8.68127878637506             |  Top 5     |
        | 'total_payments'                | 8.3751340762030502           |            |
        | 'shared_receipt_with_poi'       | 7.9640443730969981           |            |
        | 'expenses'                      | 5.5381926257043759           |            |
        | 'from_poi_frequency'            | 4.7828357055421122           |            |
        | 'to_poi_frequency'              | 3.7988022348381127           |            |
        | 'exercised_stock_percentage'    | 0.14069235754394752          |            |

        For the top 5 features, 'exercised_stock_options' is highly correlated with 'total_stock_value', 'Total_income' and 'restricted_stock', and it is moderately correlated with 'salary' as well.
        ![Correlation matrix](https://github.com/super-penguin/Udacity_Data_Analyst/blob/master/Identify%20Fraud%20from%20Enron%20Email/correlation_matrix.png)
        Thus, in our initial testing phase, only 'poi' and 'exercised_stock_options' were used to train the dataset. In the next parameter tuning phase, PCA and SelectKBest will be used together to make feature selection.

    - Decision Tree Classifier
    Decision tree is good with data that is not linearly separable and it could handle outliers pretty well. However, it gets overfit easily. In order to improve the performance of decision tree, AdaBoost and RandomForest will be tested next.[3]

    - AdaBoostClassifier
    AdaBoost is an efficient boosting algorithm for binary classification. It builds an initial model from the training data, then creates new models by correcting the errors from the previous model. New models are added until the training set is predicted perfectly or a maximum number of models are added[4].
    By using the same parameter, AdaBoost did improved the performance of the decision tree classifier. Feature scaling and dimensional reduction are not necessary for AdaBoost. It seems to be one of the best classifiers for this project. Parameter tuning and Cross-validation will be performed later for AdaBoost.

    - RandomForestClassifier
    RandomForest generates an internal unbiased estimate of the generalization error as the forest building progresses. It is an effective method to handle large dataset and a lot of missing values. However, it did not classify Enron Dataset as well as AdaBoost.

    - SVC
    SVC has high accuracy, nice theoretical guarantees regarding overfitting, and with an appropriate kernel they can work well even if the data isn’t linearly separable in the base feature space[3]. Feature scaling is a very important preprocessing step for SVC classifier. It minimizes the distance between the separating plane and the support vectors. If one feature has large value compared with other features, it will have a bigger influence on the distance metric in SVC. Thus feature scaling were performed before fitting. The performance of SVC is very good, thus Parameter tuning and Cross-validation will be performed later.

    - LogisticRegression
    A fast and simple algorithm to classify linearly separable dataset. For this project, the performance is similar with the linear SVC classifier.


2. Based on our original testing with different classifiers, **K Nearest Neighbors and SVC** will be further tuned with Cross-validation.

#### 5. Parameter tuning   
Final results:

| Classifiers            |  Accuracy           |  Recall          |  Precision       |
| ---------------------- | ------------------- | ---------------- | ---------------- |
| K Nearest Neighbors    | 0.904762            | 0.641026         | 0.641026         |
| SVC                    | 0.928571            | 0.500000         | 0.464286         |
| **AdaBoostClassifier** | **0.928571**        | **0.653846**     | **0.725000**     |



1. Cross-validation for K Nearest Neighbors

   Pipeline(steps=[('features', FeatureUnion(n_jobs=1,
          transformer_list=[('pca', PCA(copy=True, iterated_power='auto', n_components=2, random_state=None,
     svd_solver='auto', tol=0.0, whiten=False)), ('K_best', SelectKBest(k=1, score_func=<function f_classif at 0x10f2c4398>))],
          transformer_weights=None)), ('KNN', KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
              metric_params=None, n_jobs=1, n_neighbors=5, p=2,
              weights='uniform'))])

2. Cross-validation for SVC

SVC(C=0.5, cache_size=200, class_weight=None, coef0=0.0,
  decision_function_shape=None, degree=3, gamma='auto', kernel='linear',
  max_iter=-1, probability=False, random_state=None, shrinking=True,
  tol=0.1, verbose=False)

3. Cross-validation for AdaBoost

AdaBoostClassifier(algorithm='SAMME.R',
          base_estimator=DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=None,
            max_features=None, max_leaf_nodes=None,
            min_impurity_split=1e-07, min_samples_leaf=1,
            min_samples_split=10, min_weight_fraction_leaf=0.0,
            presort=False, random_state=None, splitter='best'),
          learning_rate=1.0, n_estimators=50, random_state=None)

4. Conclusions
The best estimator is AdaBoostClassifier in this project. The accuracy of our final POI classifier is 0.928571. The recall (the ratio of POIs this classifier could correctly recall to a number of all POIs) is 0.653846. It is not perfect, but is already the best in all the classifiers we tried in this project. The precision (the ratio of correctly classified POIs to the mix of correct and wrong recalls) in this project is less important than recall. We would want this classifier to recognize all possible POIs. Even if some of them are actually non-POIs, it is easier to exclude them later with further analysis than missing them totally. The precision of the final AdaBoostClassifier is 0.725, which is pretty good. In conclusion, AdaBoostClassifier is an effective POI classifier in this project.




References:
    [1] https://saravananthirumuruganathan.wordpress.com/2010/05/17/a-detailed-introduction-to-k-nearest-neighbor-knn-algorithm/
    [2] http://machinelearningmastery.com/k-nearest-neighbors-for-machine-learning/
    [3] http://blog.echen.me/2011/04/27/choosing-a-machine-learning-classifier/
    [4] http://machinelearningmastery.com/boosting-and-adaboost-for-machine-learning/
