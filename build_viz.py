import seaborn as sns
import sqlite3
from sqlite3 import Error
import os, json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md

def get_range(df):
    max_profit = 0
    min_profit = 0
    for elem in df.index:
        a_profloss = df['BET PROFIT RT'][elem]
        if a_profloss > max_profit:
            max_profit = a_profloss
        if a_profloss < min_profit:
            min_profit = a_profloss

    the_range = max(max_profit,abs(min_profit))
    return the_range


def viz_go(df, filename):

    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.max_columns', None)

    fig_dims = (24, 8)
    fig, ax = plt.subplots(figsize=fig_dims)
    chart = sns.lineplot(data=df, x='DATE', y='BET PROFIT RT', ax=ax)
    chart.set_ylabel("PROFIT/LOSS", fontsize = 20)
    # specify the position of the major ticks at the beginning of the week
    chart.xaxis.set_major_locator(md.WeekdayLocator(byweekday=1))
    # specify the format of the labels as 'year-month-day'
    chart.xaxis.set_major_formatter(md.DateFormatter('%Y-%m-%d'))
    # (optional) rotate by 90° the labels in order to improve their spacing
    #plt.setp(chart.xaxis.get_majorticklabels(), rotation=90)
    chart.yaxis.get_major_formatter().set_scientific(False)
    chart.get_figure().autofmt_xdate()

    chart.xaxis.set_minor_locator(md.DayLocator(interval=1))
    chart.tick_params(axis='x', which='major', length=10)
    chart.tick_params(axis='x', which='minor', length=5)

    chart.axhline(0)
    range = get_range(df)
    plt.ylim(-1*range,range)
    a_name = filename+'.png'
    a_name = a_name.replace(" ", "")
    plt.savefig(a_name)
    plt.close()
    #plt.show()
    # df = pd.DataFrame(records)
    # print(df)
    # sbs.lineplot(data=df, x=3, y=6)
    return a_name