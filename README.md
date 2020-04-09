			-README-
========= ========= ========= ========= ========= =========
To Run The Code:
1. Run      "python getSchemaToCSV.py" This file converts the text file into CSV.
2. Run       "spark-submit ClairvoyantTask_1_2.py" This file processes Task 1 and Task 2 in the same file. 3. Run        "spark-submit ClairvoyantTask_1_2.py" This file processes Task 3. 4. Run       "python PlotAnalytics.py" This script generates plots for the tasks 1,2, and 3.

========= ========= ========= ========= ========= =========
Thought Process:

1. Converting text (JSON schema) to a CSV file
There are two advantages of doing this: a)Reduced memory usage: As compared to the text file(2GB) the CSV file only consumed ~300MB disk space. b)Quicker read time: Faster data loading, leading to quicker debugging. I used pandas to convert the psy-001_clickstream_export.text file into a data.csv file.
Challenge: I faced issues with installing a working version of pyspark in my local Mac machine. Due to this reason, I had to use pandas to convert the "psy-001_clickstream_export.txt" file into a data.csv file.


3. Loading Data to HDFS: I used Ambari to load and download the data to HDFS.  
4. Solving Tasks: I created pseudocode to provide waypoints for the code. Since all tasks which I chose had a very similar structure, I created a common pseudocode:-
- Gather the required columns from the spark RDD - Apply the function for the required task (string manipulation in task 2 and task 3) - Group by and Order by the required columns. - Visualize (print) data. - Save the results. 

5. Plotting the results: I downloaded the csvs from hdfs, and processed them on python. I used matplotlib to plot the results for each task.   6. Future Improvements: Instead of manually using CSVs to generate plots on python, Tableau can be used as a future improvement for this project. 


 ========= ========= ========= ========= ========= =========
Assumptions and their rationale:
While finding the users performing the maximum activity:
Users who perform the maximum clicks on Coursera will be the most active users. Our metric to measure activity is the number of clicks performed by each user.

While finding the commonly used languages:
We get the overall language that the user chooses to get the course in. There are many variants of the same language, for instance, “en-tu” is the Turkish variant of the English language. These small variants have been ignored and a broad phenomenon has been shown. In other words, “en-tu” is counted as “en” or the English language.
