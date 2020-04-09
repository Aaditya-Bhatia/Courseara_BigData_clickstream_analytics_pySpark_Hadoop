# Big Data Analytics on Coursera Clickstream
  
  
Data never stops. Over 2.5 quintillion bytes of data are generated every day. Organizations need to analyze and understand this data and enabling themselves efficiently handling operations better.  
This project leverages the distributed processing capabilities of the Hadoop ecosystem to perform analytics on massive data in parallel. Users perform millions of actions (i.e., millions of clicks on the course page) while working on courses in online MOOCs like Coursera. Analyzing such massive clickstream helps MOOC providers in understanding their users better, enabling them efficiently handling operations to better manage user needs.  
In this project, we use RDD (Resilient Distributed Datasets), a fault-tolerant collection of elements. RDD's operate in parallel over the Hadoop cluster.  
  
**To Run The Code:**  
  
* The JSON file input file from Coursera is converted into tabular form (CSV):  
Run _"python getSchemaToCSV.py"._  
* Distributed processing on Hadoop cluster using pySpark-  
Run _"spark-submit Scripts/SparkAnalyze_Browser_&_Device.py"_  
Run _"spark-submit /Scripts/SparkAnalyze_Language_&_ActiveUsers.py"_    
* Visualization using matplotlib:  
Run _"python PlotAnalytics.py"_  
  
**RESULTS**
  
* Top Device Count:
![device](https://github.com/Aaditya-Bhatia/Courseara_BigData_clickstream_analytics_pySpark_Hadoop/blob/master/Analytics/Plots/Device.png)
  
* The top most browsers used at the coursera course are:
![browser](https://github.com/Aaditya-Bhatia/Courseara_BigData_clickstream_analytics_pySpark_Hadoop/blob/master/Analytics/Plots/Browser.png)
  
* Cumulative Distributive function for Activity at the course:
![CDF_Activity_Count](https://github.com/Aaditya-Bhatia/Courseara_BigData_clickstream_analytics_pySpark_Hadoop/blob/master/Analytics/Plots/ActivityCount.png)
  
  
**Program Scheme**
1. Converting text (JSON schema) to a CSV file:  
There are two advantages of doing this: a)Reduced memory usage: As compared to the text file(2GB) the CSV file only consumed ~300MB disk space. b)Quicker read time: Faster data loading, leading to quicker debugging. We use pandas to convert the psy-001_clickstream_export.text file into a data.csv file.  
3. Loading Data to HDFS: Used Ambari to load and download the data to HDFS.  
4. The common pseudocode for spark scripts is:
	- Gather the required columns from the spark RDD
	- Apply the function for the required task (string manipulation in task 2 and task 3 Group by and Order by the required columns.
	- Save the results.  
5. Plotting the results: We downloaded the CSV from HDFS and processed them on python. We used matplotlib to plot the results for each task.  
6. Future Improvements: Instead of manually using CSVs to generate plots on python, Tableau can be used as a future improvement for this project. 


**Assumptions**  
*Finding the users performing the maximum activity:*  
	Users who perform the maximum clicks on Coursera will be the most active users. Our metric to measure activity is the number of clicks performed by each user.  
  
*Finding the commonly used languages:*  
	We get the overall language that the user chooses to get the course in. There are many variants of the same language, for instance, “en-tu” is the Turkish variant of the English language. These small variants have been ignored and a broad phenomenon has been shown. In other words, “en-tu” is counted as “en” or the English language.
