# -*- coding: utf-8 -*-
"""
P1: Test a Perceptual Phenomenon
Stroop data analysis and visualization in python
04/20/16
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

##########################################################################
## 1. Read stroop dataset into a dataframe:data.
data = pd.read_csv ('stroopdata.csv', sep =',', header = 0)

##########################################################################
## 2. Descriptive statistics and statistical test
## 2.1 Save the descriptive statistics into a dataframe: D_data.
D_data = data.describe()
D_data.to_csv('Descriptive_stat.csv', sep=',')

t, p = stats.ttest_rel(data['Congruent'],data['Incongruent'])

print('t-statistic = %6.3f\np-value = %6.4f' % (t,p),sep=',')
if p <0.05:
    print('The null hypothesis is rejected;')
    print('Conclusion: the average time used to name the colors of incongruent words is significant longer than the congruent words.')

else:
    print('The null hypothesis is not rejected;')
    print('Conclusion: the average time used to name the colors of incongruent words is the same as the congruent words.')

##########################################################################
## 3. Visualization of the dataset.

# These are the "Tableau 10" colors as RGB. (Modified yellow)
tableau10 = [(114,158,206), (255,158,74), (103,191,92), (237,102,93),
             (173,139,201), (168,120,110), (237,151,202), (162,162,162),
             (255,221,113), (109,204,218)]

for i in range(len(tableau10)):
    r, g, b = tableau10[i]
    tableau10[i] = (r / 255., g / 255., b / 255.)

##########################################################################
## 3.1. Boxplot
##########################################################################

## combine dataset into a list
data_to_plot = [data['Congruent'],data['Incongruent']]
## plot
fig1 = plt.figure(1, figsize=(12, 9))
ax1 = fig1.add_subplot(111)
bp = ax1.boxplot(data_to_plot)
plt.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
plt.setp(bp['boxes'], color=tableau10[7])

# Modify the color of box plot
bp = ax1.boxplot(data_to_plot, patch_artist=True)
bp['boxes'][0].set(facecolor =tableau10[0])
bp['boxes'][1].set(facecolor =tableau10[3])

for whisker in bp['whiskers']:
    whisker.set(color=tableau10[7], linewidth=2)

for cap in bp['caps']:
    cap.set(color=tableau10[7], linewidth=2)

for median in bp['medians']:
    median.set(color=tableau10[8], linewidth=2)


## add labels
ax1.set_xticklabels(['Congruent', 'Incongruent'],fontsize=16)
ax1.get_xaxis().tick_bottom()
ax1.get_yaxis().tick_left()
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

ax1.set_ylabel('Time(ms)',fontsize=16)
ax1.set_title('Comparison of Congruent & Incongruent',fontsize=22)
fig1.savefig('boxplot.png', bbox_inches='tight')


##########################################################################
## 3.2. Histogram
##########################################################################

fig2= plt.figure(2,figsize=(12, 9))
bins = np.linspace(0, 40, 21)

## histogram for Congruent
ax21 = fig2.add_subplot(2,1,1)

ax21.spines["top"].set_visible(False)
ax21.spines["right"].set_visible(False)
ax21.get_xaxis().tick_bottom()
ax21.get_yaxis().tick_left()
ax21.hist(data['Congruent'],bins,color=tableau10[0],alpha=0.5)
ax21.set_ylabel('Count',fontsize=14)
ax21.set_xlabel('Time (ms) to name the colors',fontsize=14)
ax21.legend(fontsize=16)


## histogram for Incongruent
ax22 = fig2.add_subplot(2,1,2)

ax22.spines["top"].set_visible(False)
ax22.spines["right"].set_visible(False)
ax22.get_xaxis().tick_bottom()
ax22.get_yaxis().tick_left()
ax22.hist(data['Incongruent'],bins,color=tableau10[3],alpha=0.5)
ax22.set_ylabel('Count',fontsize=14)
ax22.set_xlabel('Time (ms) to name the colors',fontsize=14)
ax22.legend(fontsize=16)

# Save the figure
fig2.savefig('histogram.png', bbox_inches='tight')

##########################################################################
## 3.3. Bar figure
##########################################################################

mu_Congruent, sig_Congruent = np.mean(data['Congruent']), np.std(data['Congruent'])
mu_Incongruent, sig_Incongruent = np.mean(data['Incongruent']), np.std(data['Incongruent'])

width = 0.2
fig3 = plt.figure(3,figsize=(12, 9))
ax3 = fig3.add_subplot(111)

bar1 = ax3.bar(0.2, mu_Congruent, width, color =tableau10[0],alpha=0.5)
err_bar1 = ax3.errorbar(0.3, mu_Congruent,yerr= sig_Congruent,capsize =20, markeredgewidth =2, elinewidth =2, ecolor=tableau10[7])
bar2 = ax3.bar(0.6, mu_Incongruent, width, color =tableau10[3], alpha=0.5)
err_bar2 = ax3.errorbar(0.7,mu_Incongruent, yerr=sig_Incongruent,capsize =20,markeredgewidth =2, elinewidth =2, ecolor=tableau10[7] )


ax3.set_ylabel('Time(ms)',fontsize=16)
ax3.set_xlabel('Conditions',fontsize=16)
ax3.set_title('Comparison of Congruent & Incongruent',fontsize=22)
ax3.set_xlim([0,1])
ax3.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
plt.setp(ax3.get_xticklabels(), visible=False)
ax3.get_xaxis().tick_bottom()
ax3.get_yaxis().tick_left()
ax3.legend((bar1[0], bar2[0]), ('Congruent', 'Incongruent'),bbox_to_anchor=(1, 0.9), loc=2, borderaxespad=0.,fontsize=16)
fig3.savefig('bar_graph.png', bbox_inches='tight')
