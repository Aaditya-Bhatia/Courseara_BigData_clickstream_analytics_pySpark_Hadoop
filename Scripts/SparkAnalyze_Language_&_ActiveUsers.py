# -*- coding: utf-8 -*-
'''
Created on Thu Feb  6 14:02:09 2020

@author: aadityabhatia

Info:
    This spark script gets the most common used languages and the most active users at coursera
    based on the clicking behaviour of the user.

Prerequisites:
    The clicks.text file is to be converted into a csv file for the purpose of optimization.
    The equivalent csv file is used because it consumes less disk volume (from 2GB to ~300mb).
    The data is present at Hadoop Distributed File System (i.e., hdfs:///user/....)
    
Tasks Performed:
    Getting the top users:    
        We assume that the since the top users are most active, they perform the maximum clicks.
        1. The number of users performing clicks actions are grouped together to get the count of such users. 
        2. Count of users is ordered in descending fashion to get the top users who performed the clicking actions.
        3. The results are saved in a csv file.
    
    Getting the top languages used:
        We get the number of users using a specific language for the course.
        1. String manipulation is performed to get the language from the data.
        2. Since a single user would use a specific language multiple times, there might be duplication (double-counti$
        in the data. Such doubly counted items are removed.
        3. A group by is done to get the count of languages and data is sorted in a descending order.
        4. The results are saved in a csv file.        
'''


from pyspark.sql.types import StringType
from pyspark.sql.functions import udf
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions
from pyspark.sql import SQLContext

'''This function splits string to get the language of the course
We get the overall language (eg, English or Turkish, instead of tu-en, i.e., turkish-english)'''
def getLanguage(string):
    LangStr = str(string).split(';')[0]
    res = min(LangStr.split(','))
    if '-' in res:
        temp = res.split('-')
        res = temp[0]
    return(res)
        
if __name__ == "__main__":
    # defining the directories where data is to be loaded/stored
    dirName = "hdfs:///user/maria_dev/Coursera/"
    datFile = dirName+"data_reduced.csv"
    
    # creating a spark session
    spark = SparkSession.builder.appName("ClairvoyantTest").getOrCreate()
    
    # creating a spark context from the spark session
    sc = spark.sparkContext
    
    # creating a sql context from the spark context
    # this is done to load the data using the sql context
    sqlContext = SQLContext(sc)
    
    # reading the csv file
    df = sqlContext.read.format('csv').options(header='true', inferschema='true').load(datFile)
    
    # just checking if the load is proper, and map-reduce is working in the system
    print(df.columns)
    df.collect() 
    
    
    '''
    Getting the top languages used:
    '''
    print("\n\nGetting the Top users:")
    sub_df = df.select('username', 'language')
    topUsers = sub_df.groupby('username').count().orderBy('count', ascending = False)
    
    
    #printing the top users
    topTen = topUsers.take(10)
    for i in topTen:
        print (i[0], i[1])
    
    # saving the results
    #topUsers.coalesce(1).write.csv(dirName+'MostActiveUsers1', header=True)
    
    
    '''
    Getting the top languages used:
    '''
    print("\n\nGetting the top languages used")
    
    #creating a user defined function for spark
    udf_getLanguage = udf(getLanguage, StringType())
    df2 = sub_df.withColumn("lang", udf_getLanguage("language"))
    
    #removing the double counted values for users with multiple clicking behaviors
    languages = df2.select('lang', 'username').drop_duplicates()
    # group by count, then order by descending value of count 
    topLanguages = languages.groupby('lang').count().orderBy('count', ascending = False)
    # printing the top 10 languages to validate result
    topTen = topLanguages.take(10)
    for i in topTen:
        print (i[0], i[1])
    # saving the results    
    #topLanguages.coalesce(1).write.csv(dirName+'MostCommonLanguages', header=True)
    
    # exiting the spark session
    spark.stop()
    
