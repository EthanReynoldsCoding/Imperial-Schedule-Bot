import requests
import pandas
import datetime

year = datetime.datetime.today().year + 1
s_res = requests.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_games.html")

tables = pandas.read_html(s_res.text)

import os
if not os.path.exists("nhl-schedules"):
    os.mkdir("nhl-schedules")

latest_m = ""
for table in tables:
    t_dfs = []
    for i, t in table.iterrows():
        date = t["Date"].replace("-", "")
        if date == latest_m:
            t_dfs.append(t)
        else:
            if t_dfs:
                pandas.concat(t_dfs, axis=1).T.to_csv(f"nhl-schedules/{latest_m}.csv")
            t_dfs = [t.to_frame()]
        latest_m = date