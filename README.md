# P1: Test a Perceptual Phenomenon

## Stroop data analysis and visualization

#####1. What is our independent variable? What is our dependent variable?

  -Independent variable: the two conditions of the words
   *congruent (same ink color with word name)*
   *incongruent (different ink color with the word name).*
  -Dependent variable: the time used to name the ink color.

#####2. What is an appropriate set of hypotheses for this task? What kind of statistical test do you expect to perform? Justify your choices.

  -Null hypothesis: The time used to name the colors of incongruent words is the same as the time used to name the congruent words.
  -Alternative Hypothesis: The time used to name the colors of incongruent words is significant different from the time used to name the colors of congruent words.
  -Statistical test: paired student t-test (two-tail)
  *First, we are comparing the difference of the mean (the average time used to name the ink color) from 2 groups, thus student t test would be the choice.*
  *Second, Each participant will go through and record a time from each condition, thus paired analysis should be utilized.*
  *Third, based on our hypothesis, we are going to detect the effect in both directions (the time used to name color of incongruent words is longer or shorter than congruent words), thus two-tail t-test is selected.*

#####3. Report some descriptive statistics regarding this dataset. Include at least one measure of central tendency and at least one measure of variability.

Descriptive statistics:
| Condition | Congruent(ms) | Incongruent(ms) | Comments|
| ------------ |------------ | -------------| ------------- |
| Mean | 14.051 | 22.016 | *measure of central tendency* |
| Std  | 3.5593 | 4.7971 | *measure of variability* |
| Median | 14.357 | 21.018 | *measure of central tendency* |
| Range (max-min) | 13.698 | 19.568 | *measure of variability* |
| Interquartile Range | 4.3055 | 5.3348 | *measure of variability* |

#####4. Provide one or two visualizations that show the distribution of the sample data. Write one or two sentences noting what you observe about the plot or plots.

  - The comparison of Congruent & Incongruent conditions with Boxplot
  ![boxplot](https://github.com/super-penguin/Udacity_Data_Analyst/blob/new_upload/boxplot.png)
  *Boxplot shows the interquartile range, total range, median and potential outlines;  The boxplots for the two conditions are both symmetric; The median of the incongruent group is larger than the congruent group, however, there are two large outliners in the incongruent group which might pull the mean toward the larger side.*
  - The comparison of Congruent & Incongruent conditions with Histogram
  ![Hitogram](https://github.com/super-penguin/Udacity_Data_Analyst/blob/new_upload/histogram.png)
  *Histogram shows the mode, potential outlines and distribution of the data;The mode of the incongruent group (20-22ms) is larger than the mode of the congruent group (14-16ms); The distributions are similar under those two conditions and we can assume that they are both normally distributed with equal variance; From this figure, we expect that the average time for incongruent group is longer than congruent group.*
  - The comparison of Congruent & Incongruent conditions with bar-chart
  ![bar-chart](https://github.com/super-penguin/Udacity_Data_Analyst/blob/new_upload/bar_graph.png)
  *Bar chart shows the mean and variation of the data; The mean of the incongruent group is much larger than the congruent group and the standard deviations are similar; From this figure, we expect that the incongruent group is significantly larger than the congruent group.*

#####5. Now, perform the statistical test and report your results. What is your confidence level and your critical statistic value? Do you reject the null hypothesis or fail to reject it? Come to a conclusion in terms of the experiment task. Did the results match up with your expectations?

  -Paired student t-Test (two-tail)
  *95% confidence interval*
  t Critical (two-tail): 2.0687
  t-statistic = -8.0207
  p-value = 4.103E-08 << 0.05
  **The null hypothesis is rejected;**
  **Conclusion: the average time used to name the colors of incongruent words is significant longer than the congruent words.**
  The results match up with my expectations.

#####6. Optional: What do you think is responsible for the effects observed? Can you think of an alternative or similar task that would result in a similar effect? Some research about the problem will be helpful for thinking about these two questions!

  -The observed effects are caused by the interference between cognitive processing for different tasks in our neural system. Word recognition, which is more automatic because of the large amount of practice everyday, interferes with the color recognition of the word itself, which requires more attention under such circumstance[1]. It is suggested that parallel processing model accounts for this classic stroop effect[2].
  -Alternative tasks: 1) measuring the time to name the font colors of the words by turning the words upside down. I believe this would be faster than the incongruent group and slower than the congruent group.  2) measuring the accuracy of hearing: show a word on the screen and play the audio of the exact word or another word with similar pronunciation. I believe the accuracy would be much higher when the audio matches with the word.  3) measuring the time and accuracy to count: show several print of a number on the screen to count: the counting results either match with the number printed or different from the number printed on the screen. I believe it would be faster with higher accuracy when the number printed on the screen matches with the count.

## Code
The python code generating the statistic results and figures are showed in [stroop.py](https://github.com/super-penguin/Udacity_Data_Analyst/blob/new_upload/stroop.py).

## References:

[1] MacLeod, C.M. and Dunbar, K. (1988) Training and Stroop-like
interference: evidence for a continuum of automaticity. J. Exp. Psychol.
Learn. Mem. Cognit. 10, 304–315
[2] MacLeod and MacDonald (2000) Inter-dimensional interference in the Stroop effect: uncovering the cognitive and neural anatomy of attention. Trends in Cognitive Sciences, 4(10), 383-391.

## On-line resources for python:
[Python data visualizations](http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/)
[Python Pyplot tutorial](http://matplotlib.org/users/pyplot_tutorial.html)
[Python bar-charts tutorial](https://plot.ly/python/bar-charts/)
