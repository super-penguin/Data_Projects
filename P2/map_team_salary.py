# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 23:55:46 2016

@author: Penny
"""
## 4. Map the team's averaged salary in 2015 on the USA maps 
## The team's locations are marked by the location of the MBL Stadiums
## The size and color of each circle represents the salary level 

from IPython import get_ipython
get_ipython().magic('reset -sf')

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

##########################################################################
## 1. Read dataset into dataframes.
team_data=pd.read_csv('Teams.csv')
city_loc = pd.read_csv('MLB Stadiums.csv')
salary_data = pd.read_csv('Salaries.csv')


##########################################################################
## 2. Create a new dataframe (df) with all the team stadium location and salary in 2015
def which_year (data, year):
    return data[data['yearID']==year]

# I am interested in 2015
df_team = which_year (team_data, 2015)
df01 = which_year (salary_data, 2015)

# remove na values for salary
df01 = df01.dropna(axis=0, how='any',subset = ['salary']) # rule out nan values
# get the mean salary for each team
df1=df01.groupby(['teamID'])['salary'].mean()
df03 = pd.DataFrame(df1.index, columns=['teamID'])
df04 = pd.DataFrame(df1.values, columns=['average salary'])
df3 = pd.concat([df03, df04], join='outer', axis=1)

team_city = city_loc.merge(df_team, left_on = 'Team Name',right_on = 'name', how ='left')
team_loc = team_city[['teamID','Latitude','Longitude','Team Name']]

df = team_loc.merge(df3, on='teamID')

##########################################################################
## 3. Data visulation: map salary data on USA map

# Load USA map with Basemap fucntion
map = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',resolution ='h',lat_1=33,lat_2=45,lon_0=-95)
map.drawmapboundary()
map.fillcontinents(color='0.95')
map.drawcoastlines(color='0.50', linewidth=0.25)
map.drawstates(color='0.50')

# Convert the latitude and longitude into lists
# Map the location on the USA 
lats = df['Latitude'].tolist()
lons = df['Longitude'].tolist()
#txt = df['teamID'].tolist()

x, y = map(lons, lats)

min_sal = df['average salary'].min()-100
max_sal = df['average salary'].max()+100

temp = df['average salary'].tolist()

plot_var = []
for val in temp:
    val=round((val-min_sal)/(max_sal-min_sal),2)
    plot_var.append(val)

sizes = [ ((x)*500) for x in plot_var]
color = [int(x*100) for x in plot_var]

fig=plt.figure(1, figsize=(70, 50))
fig.suptitle('The Average Salary Distribution for MLB Teams', fontsize=14, fontweight='bold')

m = map.scatter(x, y, marker='o', s=sizes, alpha=0.5, zorder=10, c=color)

# Add color map on the right side
cbar = map.colorbar(m,location='right',pad="3%",ticks=[10,50,90])
cbar.ax.set_yticklabels(['Low', 'Medium', 'High'])


#for i in range(30):
   # plt.annotate(txt[i], xy=(x[i]+30000,y[i]-30000))
    #xycoords='data', xytext=(x[i]+30000, y[i]-30000),textcoords='offset points',arrowprops=dict(arrowstyle="fancy", color='b'))

plt.show()
fig.savefig("Team_salary_map.png", dpi=600)  