import browserhistory as bh
import pandas as pd
from datetime import datetime

browserhistory = bh.get_browserhistory()
his = browserhistory["chrome"]
df = {"url":[], "title":[], "last_visit_time":[]}


for i in his:
    df["url"].append(i[0])
    df["title"].append(i[1])
    df["last_visit_time"].append(datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S"))
df = pd.DataFrame(df)
df.to_csv('./history.csv', index=False)