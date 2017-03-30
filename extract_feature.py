# -*- coding: utf-8 -*-
# filename: extract_feature.py

import numpy as np
# import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import os
import datetime

matplotlib.use('Agg')

from sklearn.cross_validation import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics


# 通过时间划分训练集和测试集
def SplitTrainandTestData(users, date):
    test_data = users[users['date'] == date]
    train_data = users[users['date'] < date]
    return (train_data, test_data)


def strtodatetime(datestr, format):
    return datetime.datetime.strptime(datestr, format)


## 计算时间相差天数
def datediff(beginDate, endDate):
    format = "%Y-%m-%d"
    bd = strtodatetime(beginDate, format)
    ed = strtodatetime(endDate, format)
    oneday = datetime.timedelta(days=1)
    count = 0
    while bd != ed:
        ed = ed - oneday
        count += 1
    return count


## Input: hehavior_type, date, 划分时间
def get_label(x, y, time):
    last_day = max(y.split('|'))
    if last_day != time:
        return (0)
    days = y.split('|')
    behaviors = x.split('|')
    flag = 0
    for i in range(len(days)):
        if days[i] == time and behaviors[i] == '4':
            flag = 1
            break
    if flag:
        return (1)
    return (0)


## bahavior_type, date, item_category
## Basic features including:
def get_basic_features(x, y, time):
    x = x.split('|')
    y = y.split('|')
    basic_features = []
    if len(x) == 0:
        return ([0] * 5)
    click_value, store_value, cart_value, buy_value = 0, 0, 0, 0
    last_buy = []
    for i in range(len(x) - 1):
        if y[i] >= time:
            continue
        if x[i] == '1':
            click_value += np.exp(-0.1 * datediff(y[i], time))
        if x[i] == '2':
            store_value += np.exp(-0.1 * datediff(y[i], time))
        if x[i] == '3':
            cart_value += np.exp(-0.1 * datediff(y[i], time))
        if x[i] == '4':
            buy_value += 1
        last_buy.append(datediff(y[i], time))
    if len(last_buy) == 0:
        return ([0] * 5)
    basic_features += [click_value, store_value, cart_value, buy_value, min(last_buy)]
    return (basic_features)


## 读取数据，并示例
items = pd.read_csv(os.path.join(os.getcwd(), r'o2o_data', 'tianchi_fresh_comp_train_item.csv'))
print(items.head(5))

users = pd.read_csv(os.path.join(os.getcwd(), 'o2o_data', 'tianchi_fresh_comp_train_user.csv'),
                    dtype={'user_id': object, 'item_id': object, 'behavior_type': object, 'item_category': object})
print('Read Done!\n')
users['date'] = users.time.map(lambda x: x.split(' ')[0])
users['hours'] = users.time.map(lambda x: x.split(' ')[-1])
users = users.drop(['time'], axis=1)
users[['behavior_type', 'date', 'hours', 'item_category', 'user_geohash']] += '|'
users = users.groupby(['user_id', 'item_id']).sum().reset_index()
users.to_csv(os.path.join(os.getcwd(), 'o2o_data', 'users_items_behavior.csv'), index=False, index_label=False)
print(users.head(5))

train_data_12_18, test_data_12_18 = SplitTrainandTestData(users, '2014-12-18')
print train_data_12_18.head(5)

users.behavior_type = users.behavior_type + '|'
users[['date', 'hours']] += '|'
users_test = users.groupby(['user_id', 'item_id']).sum().reset_index()
print users_test.head(5)
print users.head(5)

users_test = pd.read_csv(os.path.join(os.getcwd(), 'o2o_data', 'users_items_behavior.csv'))
users_test.loc[:, 'item_category'] = users_test['item_category'].apply(lambda x: x.split('|')[0])
# users_test.loc[:,'last_day'] = users_test['date'].apply(lambda x: max(x.split('|')))
users_test.loc[:, 'label'] = users_test[['behavior_type', 'date']].apply(
    lambda x: get_label(x['behavior_type'], x['date'], '2014-12-18'), axis=1)
# users_test[['click_value', 'store_value', 'cart_value', 'buy_value', 'last_buy']] =
users_test.loc[:, 'basic_features'] = users_test.apply(
    lambda x: get_basic_features(x['behavior_type'], x['date'], '2014-12-18'), axis=1)
users_test.loc[:, 'click_value'] = users_test['basic_features'].apply(lambda x: x[0])
users_test.loc[:, 'store_value'] = users_test['basic_features'].apply(lambda x: x[1])
users_test.loc[:, 'cast_value'] = users_test['basic_features'].apply(lambda x: x[2])
users_test.loc[:, 'buy_value'] = users_test['basic_features'].apply(lambda x: x[3])
users_test.loc[:, 'last_buy'] = users_test['basic_features'].apply(lambda x: x[4])
users_test = users_test.drop(['basic_features'], axis=1)
print users_test.head(5)

# X_train = users_test.loc[:,['click_value', 'store_value', 'cast_value', 'buy_value', 'last_buy']]
# y_train = users_test.loc[:, ['label']]
# X_test = users_test.loc[:,['click_value', 'store_value', 'cast_value', 'buy_value', 'last_buy']]
# y_test = users_test.loc[:, ['label']]


clf = RandomForestClassifier(n_estimators=100)
y_pred = clf.fit(users_test.loc[0:4000000, ['click_value', 'store_value', 'cast_value', 'buy_value', 'last_buy']],
                 users_test.loc[0:4000000, ['label']]).predict(
    users_test.loc[:, ['click_value', 'store_value', 'cast_value', 'buy_value', 'last_buy']])
# scores = cross_val_score(clf, X_train, y_train)
# scores.mean()
print(metrics.classification_report(users_test.loc[:, ['label']], y_pred))

users_test = users_test.loc[:, ['user_id', 'item_id']]
users_test['label'] = y_pred
predict = users_test[users_test['label'] == 1].drop(['label'], axis=1)
print predict.head(5)
submission = pd.DataFrame({
    "user_id": predict["user_id"],
    "item_id": predict["item_id"]
})
submission.to_csv(os.path.join(os.getcwd(), 'data', 'result.csv'), index=False, index_label=False)

