### P2: Investigate a dataset
#### Baseball(MLB) data analysis and visualization

##### Datasets analyzed & Variables used in this project

| Salaries table | Batting Table       | Pitching Table          | Teams table                       |
| -------------- | ------------------- | ----------------------- | --------------------------------- |
| yearID         | yearID              | yearID                  | yearID                            |
| playerID       | playerID            | playerID                | G(Games played)                   |   
| salary         | G(Games)            | G(Games)                | Rank(Position in final standings) |
|                | AB(At Bats)         | ERA(Earned Run Average) | W(Wins)                           |    
|                | H(Hits)             |                         | BPF(3y park factor for batters)   |
|                | BB(Base on Balls)   |                         | HR(Homeruns by batters)           |
|                | HBP(Hit by pitch)   |                         | ERA(Earned run average)           |
|                | SF(Sacrifice flies) |                         |                                   |
|                | HR(Homeruns)        |                         |                                   |
|                | RBI(Runs Batted In) |                         |                                   |

All the datasets used here are downloaded from [Baseball data](http://www.seanlahman.com/baseball-archive/statistics/)

#### Q1. Is there a strong positive correlation between a player's salary and his batting performance?
1. Different parameters for batting performance were analyzed:
  1. Calculating batting average: BA (batting average) = H(Hits)/AB(At Bats)
  2. Calculate On-base percentage: On Base Percentage is calculated by adding hits, walks, and hit-by-pitches and dividing by the sum of at bats, walks, hit by pitches, and sacrifice flies: OBP=(H+BB+HBP)/(AB+BB+HBP+SF)
2. Spearman's rank correlation between a player's different batting metrics and salary were analyzed:

  1. Due to the amount of data, a function called **Which_year** is created to determine which year's data to explore. I am exploring the year of 2015 in this project.
  2. Only the batters whose AB(at bats) is no less than 130 times in 2015 were considered in this analysis. (AB>=130) is used to rule out the data from rookies.  

3. Data Wrangling Steps:
  1. Merge salaries table with pitching table based on the the playerID, yearID, teamID and lgID.
  2. Discard the rows with NA values and with AB less than 130.
  3. Create new batting metrics BA and OBP. They were saved as new columns in the original dataframe.
  4. Perform correlation analysis. Since the salary variable is not normally distributed, Spearman's rank correlation was used to explore the relationship between player's salary and different performance metrics, and Pearson's correlation was used to examine the relationship between different performance metrics.

4. Results & Data visualization
  1. The Spearman Correlation between the players salary(2015) and BA (2015) is: 0.185445
  2. The Spearman Correlation between the players salary (2015) and BA (2014) is: 0.217967
  3. The Spearman Correlation between the players salary(2015) and RBI(2015) is: 0.375105
  4. The Spearman Correlation between the players salary (2015) and RBI (2014) is: 0.456645
  5. The Spearman Correlation between the players salary(2015) and OBP(2015) is: 0.241051
  6. The Spearman Correlation between the players salary (2015) and OBP (2014) is: 0.340708
  7. The Spearman Correlation between the players salary(2015) and HR (2015) is: 0.351503
  8. The Spearman Correlation between the players salary (2015) and HR (2014) is: 0.331338
  9. The Pearson Correlation between the players RBI(2015) and OBP (2015) is: 0.498064
  10. The Pearson Correlation between the players HR(2015) and OBP (2015) is: 0.441864
  11. The Pearson Correlation between the players HR(2015) and RBI (2015) is: 0.885034

  **Data visualization: Examples of histogram and scatter plot**

  A function called **Multiplots** is used to plot the relationship between any two variables.

  ![Salary(2015) & RBI(2014)](https://github.com/super-penguin/Udacity_Data_Analyst/blob/master/P2/RBI_2014_Salary_2015.png)

  *This figure shows that the salary data is not normally distributed but skewed to the left. The correlation coefficient between salary (2015) and RBI (2014) is the highest in the results (0.456645), so we plotted it in this scatterplot.*


5. Conclusion

  Before performing the analysis, I hypothesized that there is a strong positive correlation between the players batting performance and salary.

  BA (batting average), OBP (On Base Percentage), RBI (Runs Batted In) and HR (Homeruns) were used to represent a player's batting performance. The larger those values are, the better the player performs. Because the salary level is not normally distributed, Spearman's Rank Correlation was used to calculate the correlation between different batting metrics and salary. Pearson's Correlation was used to calculate the correlation between those batting metrics.

  However, the results disapprove my hypothesis. There is only a moderate positive correlation between baseball players' batting performance and salary level. What's more, the players' salary in current year is slightly more correlated with the batting performance from previous year. Finally, there is a strong correlation between a player's HR and RBI.


####Q2. Is there a strong positive correlation between a player's salary and his pitching performance?
1. ERA (Earned Run Average) was used to represent a player's pitching performance. The smaller the ERA value is, the better the pitcher performs.
2. Spearman's rank correlation between a player's ERA and salary were analyzed:
  1. Exploring the year of 2015.
  2. Only the pitchers whose G (Games) is no less than 10 were considered in this analysis to rule out the data from rookies.  
3. Data Wrangling Steps: same as Q1.
4. Results & Data visualization
  1. The Spearman Correlation between the players salary(2015) and Pitching performance (2015) is: -0.091880
  2. The Spearman Correlation between the players salary (2015) and Pitching performance (2014) is: -0.098451

  **Data visualization: An example of histogram and scatter plot**

  ![Salary(2015) & ERA(2014)](https://github.com/super-penguin/Udacity_Data_Analyst/blob/master/P2/ERA_2014_Salary_2015.png)

  *The correlation coefficient between salary (2015) and ERA (2014) is -0.098451*

5. Conclusions

  There is no correlation between a baseball players' pitching performance and salary level (correlation coefficient: |r| < 0.1). There are at least two reasons which might lead to this result: First, a pitcher's performance could not be correctly measured by ERA; Second, even for a good pitcher, ERA is a highly unstable variable. Some pitchers might be really good in a season or in a game, however, it might be hard to maintain once the other teams start to analyze his pitching speed and trajectory. When a person becomes good in a certain motor skill, the trajectories of movements are usually highly stereotyped. With the video analyzing techniques, it would become harder and harder for a pitcher to maintain their record in the long run.  

  **Python Code for Q1 & Q2**
  [Q1_2.py](https://github.com/super-penguin/Udacity_Data_Analyst/blob/master/P2/Q1_2.py).


####Q3. Is there a strong positive correlation between a team's average salary and Winning record?
1. Data Wrangling Steps:
  1. Calculate the averaged salary for each team in 2015.
  2. Merge the team performance table with the averaged salary based on teamID.
  3. Perform correlation analysis. BPF (Three-year park factor for batters) was used to represent the batting performance (hitting) of a team and ERA (Earned run average) was used to represent the pitching performance (defense) of a team. Pearson correlation was used to examine the relationship between different team performance and averaged salary.

2. Results & Data visualization
  1. The Pearson Correlation between the Team BPF and W in 2015 is: -0.051974
  2. The Pearson Correlation between the Team ERA and W in 2015 is: -0.819600
  3. The Pearson Correlation between the Team ERA and W/G in 2015 is: -0.819131
  4. The Pearson Correlation between the Team Rank and averaged salary in 2015 is: -0.170484
  5. The Pearson Correlation between the Team HR and averaged salary in 2015 is: 0.238656
  6. The Pearson Correlation between the Team W/G and averaged salary in 2015 is: 0.205825

  ![Bar Plot](https://github.com/super-penguin/Udacity_Data_Analyst/blob/master/P2/average_salary_team_2015.png)
  *This plot shows the averaged salary of all the MLB team in 2015.*

  ![Scatter plot & Regression](https://github.com/super-penguin/Udacity_Data_Analyst/blob/master/P2/Corr_ERA_W.png)
  *This plot shows the winning record of a team is highly correlated with the ERA. Smaller ERA represents better pitching performance. The correlation coefficient is -0.819131. It is suggested that a team's success is largely dependent on their pitchers' pitching performance*

3. Conclusions
  1. A team's winning record is highly correlated with the team's pitching performance, which means a baseball team who has good defense strategies and good pitchers is more likely to win.
  2. A team's winning record has no correlation with the team's BPF.
  3. A team's averaged salary is only slightly correlated with the winning record or performance of a team.

  **The python code for Q3**
  [Q3.py](https://github.com/super-penguin/Udacity_Data_Analyst/blob/master/P2/Q3.py).  


####Q4. The distribution of MLB teams location and averaged salary.
  1. **Map the team's averaged salary in 2015 on the USA maps.**
    The team's locations are marked by the location of the MBL Stadiums.
    The size and color of each circle represents the salary level, the color is matched with the color bar on the right.

  Here is the figure:
  ![Team Salary Map](https://github.com/super-penguin/Udacity_Data_Analyst/blob/master/P2/Team_Salary_map.png)
  *This plot shows very clearly that the baseball teams on the east and west coast have higher salary compared with teams at the middle or south part of the USA*

  **The python code for Q4**
  [map_team_salary.py](https://github.com/super-penguin/Udacity_Data_Analyst/blob/master/P2/map_team_salary.py).


*Final thoughts: I knew nothing about baseball before this project, it was a lot of fun to explore and analyze those datasets. There are still more analysis I want to perform and I hope I could use other knowledge to make predication of a team's performance in the future. I would keep learning and modifying the code and update the results.*
