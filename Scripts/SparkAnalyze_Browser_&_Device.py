# -*- coding: utf-8 -*-
'''
Created on Thu Feb  6 20:32:52 2020

@author: aadityabhatia

Info:
    This spark script gets the most common browsers and devices used at coursera
    Data is based on the clicking behaviour of the user.
    A parsing tool, DeviceDetector is used. Can be installed by: "pip install device_detector"

Prerequisites:
    The clicks.text file is to be converted into a csv file for the purpose of optimization.
    The equivalent csv file is used because it consumes less disk volume (from 2GB to ~300mb).
    The data is present at Hadoop Distributed File System (i.e., hdfs:///user/....)
    
Tasks Performed:
    A third party tool, "DeviceDetector" is used to parse the user agent string to get the corresponding browser and device values for each click.
    To prevent double counting of results, duplicate users using the same Device and browser are removed.
    Getting the top browsers:          
        1. The number of browsers used by each user are grouped together to get their count. 
        2. Count of browsers is ordered in descending fashion to get the top most browsers used.
        3. The results are saved in a csv file.
    
    Getting the top browsers:          
        1. The number of devices used by each user are grouped together to get their count. 
        2. Count of devices is ordered in descending fashion to get the top most devices used.
        3. The results are saved in a csv file.
'''


from pyspark.sql.types import StringType
from pyspark.sql.functions import udf
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql import functions
from pyspark.sql import SQLContext
from user_agents import parse
'''This function splits string to get the language of the course
We get the overall language (eg, English or Turkish, instead of tu-en, i.e., turkish-english)'''

def getUserAgentBrowserDevice(string):
    ua = parse(string)
    return str(ua.os.family) +';'+ str(ua.device.family)

def splitBrowser(string):
    return string.split(";")[0]

def splitDevice(string):
    return string.split(";")[1]

        
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
    
    
    
    #Getting the top browsers and :
    print("\n\nGetting the top Browsers and Devices ")
    
    #creating a user defined functions for spark
    # this uses the parser to get both browser and device info
    udf_getBrowserDevice = udf(getUserAgentBrowserDevice, StringType())
    df2 = df.withColumn("browserNdevice", udf_getBrowserDevice("user_agent"))
    
    #remove the same users who use the same device and browsers
    df2 = df2.select('browserNdevice', 'username').drop_duplicates()
    
    # this splits the browser and device info into only browser info
    udf_getBrowser = udf(splitBrowser, StringType())
    df3 = df2.withColumn("browser", udf_getBrowser("browserNdevice"))

    # this splits the browser and device info to only device info
    udf_getDevice = udf(splitDevice, StringType())
    df4 = df3.withColumn("device", udf_getDevice("browserNdevice"))
    
    # process 
    df4.collect()
    print(df4.columns)
    
    '''getting the top browsers'''
    # group by count, then order by descending value of count 
    sub_df = df4.select('username', 'browser')
    topBrowsers = sub_df.groupby('browser').count().orderBy('count', ascending = False)
    # printing the top 10 languages to validate result
    topTen = topBrowsers.take(10)
    for i in topTen:
        print (i[0], i[1])
    # saving the results    
    #topBrowsers.coalesce(1).write.csv(dirName+'topBrowsers', header=True)
    
    
    '''
    getting the top devices'''
    # group by count, then order by descending value of count 
    sub_df = df4.select('username', 'device')
    topdevices = sub_df.groupby('device').count().orderBy('count', ascending = False)
    # printing the top 10 languages to validate result
    topTen = topdevices.take(10)
    for i in topTen:
        print (i[0], i[1])
    # saving the results    
    #topdevices.coalesce(1).write.csv(dirName+'topdevices', header=True)

    # exiting the spark session
    spark.stop()