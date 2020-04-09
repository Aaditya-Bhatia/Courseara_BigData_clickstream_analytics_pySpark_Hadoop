#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 10:55:53 2020

@author: aadityabhatia

Info: This script converts the text file into a csv file
"""
import pandas as pd


dirName = '/Users/aadityabhatia/spark_clairvoyant_test/'
datFile = dirName+"psy-001_clickstream_export.txt"

df = pd.read_json(datFile, lines=True, convert_dates=True,numpy=False)

#saving the entire file
df.to_csv(dirName+'data.csv', index=False)

#saving only the columns required for the tasks
df[['username', 'language', 'user-agent']].to_csv(dirName+'data_reduced.csv', index=False)