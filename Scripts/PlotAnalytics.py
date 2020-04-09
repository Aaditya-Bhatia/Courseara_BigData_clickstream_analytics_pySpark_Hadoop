#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 22:15:46 2020
@author: aadityabhatia

Info:
This script automatically generates and saves the plots corresponding to the result csvs
"""

from matplotlib.ticker import PercentFormatter
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
dirName = '/Users/aadityabhatia/spark_clairvoyant_test/'

''' 
    most active people
'''
activePeople = pd.read_csv(dirName+ 'MostActiveUsers.csv')
plt.style.use('seaborn-white')


values, base = np.histogram(activePeople.count_activity, bins=40)

cumulative = np.cumsum(values)

fig, ax = plt.subplots(figsize=(8,6))
ax.plot(base[:-1], cumulative, c='blue')
ax.set_xlabel('Number of users')
ax.set_ylabel('Activity Count')
fig.tight_layout()
fig.savefig(dirName+ 'UserActivity_CumulativeDistribution.pdf', orientation='portrait', papertype=None, format='pdf',
        transparent=False, bbox_inches=None, pad_inches=0.2)

'''
    MostCommonBrowsers
'''
commonBrowsers = pd.read_csv(dirName + 'MostCommonBrowsers.csv')

topBrowsers = commonBrowsers.head(20)
topBrowsers.columns = ['Browser Name', 'Usage Count Per User']
plt.rcParams.update({'font.size': 12})
ax = topBrowsers.plot.bar(x='Browser Name', y='Usage Count Per User', rot=90)
fig = ax.get_figure()
fig.tight_layout()
fig.savefig(dirName+ 'TopBrowsers_Histogram.pdf', orientation='portrait', papertype=None, format='pdf',
        transparent=False, bbox_inches=None, pad_inches=0.2)


'''
    Most Common Devices
'''
commonDevices = pd.read_csv(dirName + 'MostCommonDevices.csv')
commonDevices.columns = ['Device Name', 'Usage Count Per User']
plt.rcParams.update({'font.size': 12})
ax = commonDevices.plot.bar(x='Device Name', y='Usage Count Per User', rot=90)
fig = ax.get_figure()
fig.tight_layout()
fig.savefig(dirName+ 'TopDevices_Histogram.pdf', orientation='portrait', papertype=None, format='pdf',
        transparent=False, bbox_inches=None, pad_inches=0.2)


'''
    Most Common Languages
'''
commonLanguages = pd.read_csv(dirName + 'MostCommonLanguages.csv')
topLang = commonLanguages.head(15)
topLang.columns = ['Language', 'Usage Count Per User']
plt.rcParams.update({'font.size': 16})
ax = topLang.plot.bar(x='Language', y='Usage Count Per User', rot=0)
fig = ax.get_figure()
fig.tight_layout()

fig.savefig(dirName+ 'TopLanguages_Histogram.pdf', orientation='portrait', papertype=None, format='pdf',
        transparent=False, bbox_inches=None, pad_inches=0.2)
