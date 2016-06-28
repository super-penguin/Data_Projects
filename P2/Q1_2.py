# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 15:44:32 2016
P2: Investigate a Dataset
Baseball (MLB) batting, pitching & salary data 

@author: Penny
"""
### Reset
from IPython import get_ipython
get_ipython().magic('reset -sf')


import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.stats.stats import spearmanr


##########################################################################
## 1. Read dataset into dataframes.

salary_data = pd.read_csv('Salaries.csv')
batting_data = pd.read_csv('Batting.csv')
pitching_data=pd.read_csv('Pitching.csv')

##########################################################################
## 2. Explore the relationship between a player's salary and batting performance 
##    Pearson and Spearman Correlation are used to determine
##    the correlate between a player's batting performance and salary

#  2.1. Merge data with salary and batting performance into a new dataframe: df1
df1 = salary_data.merge(batting_data, on =['yearID','teamID','playerID','lgID'], how = 'inner')

#  2.2. Calculate batting average: BA = H/AB
#       Batting average: hits divided by at bats—the traditional measure of batting ability
df1 = df1.dropna(axis=0, how='any',subset = ['AB','H','BB','HBP','AB','SF']) # rule out nan values
df1 = df1[df1['AB'] >=130] # rule out rookies
df1['BA'] = df1['H']/df1['AB']
    
#  2.3. Calculate On-base percentage: OBP
#       On Base Percentage is calculated by adding hits, walks, and hit-by-pitches 
#       and dividing by the sum of at bats, walks, hit by pitches, and sacrifice flies:
#       OBP=(H+BB+HBP)/(AB+BB+HBP+SF)
df1['OBP']=(df1['H']+df1['BB']+df1['HBP'])/(df1['AB']+df1['BB']+df1['HBP']+df1['SF'])
    

####### functions
# Pick a year's data to explore
def Which_year(data,year):
    data= data[data['yearID']==year]
    return data
# Investigate the previous year's effect on the year we are interested
def Pre_year_on_current (data,year):
    temp_current = data[data['yearID']==year][['playerID','salary']]
    temp_pre = data[data['yearID']==(year-1)][['playerID','BA','RBI','OBP','HR']]
    new_data = temp_pre.merge(temp_current, on ='playerID', how = 'inner')
    return new_data
    
# Calculate the Person Correlation : normal distribution
def Pearson_corr(x, y):
    [r,p] = pearsonr(x,y)
    return r,p
    
# Calculate the Spearman Correlation : not normal distribution
def Spearman_corr(x,y):
    [r,p] = spearmanr(x,y)
    return r,p
    
# 2.4. Calculate the correlation between a plyer's batting performance with salary.
# Correlation: salary (2015) vs. BA or RBI or OBP or HR (2015)
Which_year(df1,2015)
[r1,p1]=Spearman_corr(df1['salary'], df1['BA'])
[r2,p2]=Spearman_corr(df1['salary'], df1['RBI'])
[r3,p3]=Spearman_corr(df1['salary'], df1['OBP'])
[r4,p4]=Spearman_corr(df1['salary'], df1['HR'])

# Print the results
print('The Spearman Correlation between the players salary(2015)'\
' and BA (2015) is: %6.6f' %r1)
print('The Spearman Correlation between the players salary(2015)'\
' and RBI(2015) is: %6.6f' %r2)
print('The Spearman Correlation between the players salary(2015)'\
' and OBP(2015) is: %6.6f' %r3)
print('The Spearman Correlation between the players salary(2015)'\
' and HR (2015) is: %6.6f' %r4)

# Correlation: salary (2015) vs. BA or RBI or OBP or HR (2014)
new_df1 = Pre_year_on_current(df1,2015)
[r11,p11] = Spearman_corr(new_df1['salary'],new_df1['BA'])
[r21,p21] = Spearman_corr(new_df1['salary'],new_df1['RBI'])
[r31,p31] = Spearman_corr(new_df1['salary'],new_df1['OBP'])
[r41,p41] = Spearman_corr(new_df1['salary'],new_df1['HR'])

print('The Spearman Correlation between the players salary (2015)'\
' and BA (2014) is: %6.6f '%r11)
print('The Spearman Correlation between the players salary (2015)'\
' and RBI (2014) is: %6.6f '%r21)
print('The Spearman Correlation between the players salary (2015)'\
' and OBP (2014) is: %6.6f '%r31)
print('The Spearman Correlation between the players salary (2015)'\
' and HR (2014) is: %6.6f '%r41)

# 2.5. Calculate correlation between RBI, OBP and HR in 2015
[r5,p5]=Pearson_corr(df1['RBI'], df1['OBP'])
[r6,p6]=Pearson_corr(df1['HR'], df1['OBP'])
[r7,p7]=Pearson_corr(df1['HR'], df1['RBI'])
print('The Pearson Correlation between the players RBI(2015)'\
' and OBP (2015) is: %6.6f' %r5)
print('The Pearson Correlation between the players HR(2015)'\
' and OBP (2015) is: %6.6f' %r6)
print('The Pearson Correlation between the players HR(2015)'\
' and RBI (2015) is: %6.6f' %r7)

# 2.6. Data visualization

# These are the "Tableau 10" colors as RGB. (Modified yellow)
tableau10 = [(114,158,206), (255,158,74), (103,191,92), (237,102,93),
             (173,139,201), (168,120,110), (237,151,202), (162,162,162),
             (255,221,113), (109,204,218)]

for i in range(len(tableau10)):
    r, g, b = tableau10[i]
    tableau10[i] = (r / 255., g / 255., b / 255.)


def Multiplots(data_A, data_B):
    # The dimention of the plot
    left, width = 0.1, 0.60
    bottom, height = 0.1, 0.60
    bottom_h = left_h = left + width + 0.05
    
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]
    
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]

    fig=plt.figure(1, figsize=(10, 10))


    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)
   
    # Scatter plot
    axScatter.scatter(data_A,data_B,color=tableau10[5])
    # Histograms
    axHistx.hist(data_A, color=tableau10[0])
    x_range = data_A.max() - data_A.min()
    x_min_lim = data_A.min() - int(x_range/20)
    x_max_lim = data_A.max() + int(x_range/20)
    axScatter.set_xlim(x_min_lim,x_max_lim )
    
   
    
    axHisty.hist(data_B, color=tableau10[3], orientation='horizontal')
    y_range = data_B.max() - data_B.min()
    y_min_lim = data_B.min() - int(y_range/20)
    y_max_lim = data_B.max() + int(y_range/20)
    axScatter.set_ylim(y_min_lim, y_max_lim)
    
    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())
    
    axScatter.set_xlabel('Salary',fontsize=16)
    axScatter.set_ylabel('Performance',fontsize=16)
    axHistx.set_title('Histogram of Salary',x=0.5, y=0.85, fontsize=14)
    axHisty.set_title('Histogram of Performance',fontsize=14)
    
    plt.show()
    return fig
    
    
    
# eg. Plot of Salary (2015) and  RBI (2014)

my_plot = Multiplots(new_df1['salary'], new_df1['RBI'])
my_plot.savefig("RBI(2014)&Salary(2015).png")



##########################################################################
## 3. Explore the relationship between a player's salary and pitching performance 
##    Spearman Correlation are used to determine
##    the correlate between a player's pitching performance and salary

# 3.1. Merge data with salary and pitching performance into a new dataframe: df2
df2 = salary_data.merge(pitching_data, on =['yearID','teamID','playerID','lgID'], how = 'inner')
df2 = df2.dropna(axis=0, how='any',subset = ['ERA']) # rule out nan values
df2 = df2[df2['G'] >=10] # rule out rookies

# 3.2. Calculate correlation between salary with ERA in 2015
Which_year(df2,2015)
# Correlation: salary (2015) and ERA (2015) 
[r8,p8]=Spearman_corr(df2['salary'], df2['ERA'])

def Pre_year_on_current_pitch (data,year):
    temp_current = data[data['yearID']==year][['playerID','salary']]
    temp_pre = data[data['yearID']==(year-1)][['playerID','ERA']]
    new_data = temp_pre.merge(temp_current, on ='playerID', how = 'inner')
    return new_data

# Correlation: salary (2015) and ERA (2014)
new_df2= Pre_year_on_current_pitch(df2,2015)
[r81,p81]=Spearman_corr(new_df2['salary'], new_df2['ERA'])

print('The Spearman Correlation between the players salary(2015)'\
' and Pitching performance (2015) is: %6.6f' %r8)
print('The Spearman Correlation between the players salary (2015)'\
' and Pitching performance (2014) is: %6.6f '%r81)


# 3.3. Data visualization
# Players salary (2015) and RBI (2014) first

my_plot_1 = Multiplots(new_df2['salary'], new_df2['ERA'])
my_plot_1.savefig("ERA(2014)&Salary(2015).png")

