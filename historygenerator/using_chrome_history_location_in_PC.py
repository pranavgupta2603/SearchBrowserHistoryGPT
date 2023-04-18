import os
import sqlite3
import datetime
import pandas as pd

con = sqlite3.connect("C:/Users/prana/AppData/Local/Google/Chrome/User Data/Default/History")

cur = con.cursor()
data = cur.execute('SELECT * FROM urls')

# fetch all the rows returned by the query
rows = cur.fetchall()

# create a list containing sublists of the different columns
data_list = [[] for i in range(len(rows[0]))]

for row in rows:
    for i in range(len(row)):
        data_list[i].append(row[i])
df = {}
for index, column in enumerate(data.description):
    if column[0]=="last_visit_time":
        get_time = data_list[index]
        for i in range(len(get_time)):
            
            newdate = str(get_time[i])
            stripped1 = newdate.strip(' (),L')
            ms = int(stripped1)
            utctime = datetime.datetime(1601,1,1) + datetime.timedelta(microseconds = ms, hours =5.5)
            get_time[i] = utctime
        data_list[index] = get_time
        #data_list[index] = pd.to_datetime(data_list[index])
    df[column[0]] = data_list[index]



df = pd.DataFrame(df)
df = df.sort_values(by='last_visit_time', ascending = False)

df.to_csv("../history.csv", index = False)
