# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 22:08:28 2016

@author: Penny
"""
from IPython import get_ipython
get_ipython().magic('reset -sf')


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
import statsmodels.api as sm

##########################################################################
## 1. Read dataset into dataframes.
salary_data = pd.read_csv('Salaries.csv')
team_data=pd.read_csv('Teams.csv')
city_loc = pd.read_csv('MLB Stadiums.csv')

##########################################################################
## 2.Plot the avearage salary for each team in 2015

# A function to input the year interested
def which_year (data, year):
    return data[data['yearID']==year]


df01 = which_year (salary_data, 2015)

# remove na values for salary
df01 = df01.dropna(axis=0, how='any',subset = ['salary']) # rule out nan values
# get the mean salary for each team
df1=df01.groupby(['teamID'])['salary'].mean()


## 2.1. Data Visualization: Bar Graph
# These are the "Tableau 10" colors as RGB. (Modified yellow)
tableau10 = [(114,158,206), (255,158,74), (103,191,92), (237,102,93),
             (173,139,201), (168,120,110), (237,151,202), (162,162,162),
             (255,221,113), (109,204,218)]

for i in range(len(tableau10)):
    r, g, b = tableau10[i]
    tableau10[i] = (r / 255., g / 255., b / 255.)

# Plot resutls into bar graph
index = np.arange(len(df1.index))
width = 0.65 

fig1= plt.figure(1,figsize=(16, 8))
ax = fig1.add_subplot(111)

ax.bar(index,df1.values, width,color = tableau10[0])
ax.set_xlabel('TeamID',fontsize = 12)
ax.set_ylabel('Average Salary in 2015',fontsize = 12)
ax.set_xticks(index+width/2.)
ax.set_xticklabels(df1.index)
ax.set_title('The Average_Salary for MLB Team in 2015',fontsize = 16)

plt.show()
fig1.savefig("average_salary_team_2015.png")

##########################################################################
## 3. Investigate the correlation of different team performance

df02 = which_year (team_data, 2015)
df03 = pd.DataFrame(df1.index, columns=['teamID'])
df04 = pd.DataFrame(df1.values, columns=['average salary'])
df3 = pd.concat([df03, df04], join='outer', axis=1)
df4 = df3.merge(df02, on =['teamID'], how = 'inner')

def Pearson_corr(x, y):
    [r,p] = pearsonr(x,y)
    return r,p
 
# the correlation between BPF (Three-year park factor for batters) and W (total wins)
# BPF represents the performance of batters in a team
[r1,p1] = Pearson_corr(df4['BPF'],df4['W'])
print('The Pearson Correlation between the Team BPF'\
' and W in 2015 is: %6.6f' %r1)

# the correlation between ERA (Earned run average) and W (total wins)
# W/G : total wins /  total games
# ERA represents the performance of pitchers in a team
[r2,p2] = Pearson_corr(df4['ERA'],df4['W'])
[r21,p21] = Pearson_corr(df4['ERA'],df4['W']/df4['G'])
print('The Pearson Correlation between the Team ERA'\
' and W in 2015 is: %6.6f' %r2)
print('The Pearson Correlation between the Team ERA'\
' and W/G in 2015 is: %6.6f' %r21)

# the correlation between a team's Rank and Average Salary

[r3,p3] = Pearson_corr(df4['Rank'],df4['average salary'])
print('The Pearson Correlation between the Team Rank'\
' and averaged salary in 2015 is: %6.6f' %r3)

[r31,p31] = Pearson_corr(df4['HR'],df4['average salary'])
print('The Pearson Correlation between the Team HR'\
' and averaged salary in 2015 is: %6.6f' %r31)

[r4,p4] = Pearson_corr(df4['W']/df4['G'],df4['average salary'])
print('The Pearson Correlation between the Team W/G'\
' and averaged salary in 2015 is: %6.6f' %r4)

## 3.1. Data Visualization: Scatter Graph and regression line
fig2 = plt.figure(2,figsize=(12,9))
ax2 = fig2.add_subplot(111)
ax2.scatter(df4['ERA'],df4['W'],color = tableau10[3])
ax2.set_xlabel('ERA (pitching performance)',fontsize = 12)
ax2.set_ylabel('Total Wins', fontsize = 12)
m, b = np.polyfit(df4['ERA'],df4['W'], deg=1)
ax2.plot(df4['ERA'], m * df4['ERA'] + b, color= tableau10[0])

#equation = str('y = '+np.round(m,2)+'x + '+np.round(b,2)+' ,r^2 = '+r2**2)
ax2.legend(['Regression', 'Data'])

ax2.set_title('The correlation between Team ERA and W',fontsize = 14)
fig2.savefig("Corr_ERA_W.png")

# Print the linear Regression results
results = sm.OLS(df4['W'],sm.add_constant(df4['ERA'])).fit()
print (results.summary())







