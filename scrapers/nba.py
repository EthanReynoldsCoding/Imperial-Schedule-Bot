from bs4 import BeautifulSoup

import requests
import pandas
import datetime

year = datetime.datetime.today().year + 1
months = [f"https://www.basketball-reference.com/leagues/NBA_{year}_games.html"]
s_res = requests.get(months[0])

if s_res.status_code == 200:
    schedule = BeautifulSoup(s_res.text, "lxml")

### Months
months_filter = schedule.find("div", {"class": "filter"})

if months_filter:
    months = [a.get("href") for a in months_filter.find_all("a")]

tables = []
for m in months:
    s = requests.get(f"https://www.basketball-reference.com{m}")
    table = pandas.read_html(s.text)
    tables.extend(table)

import os
if not os.path.exists("nba-schedules"):
    os.mkdir("nba-schedules")

latest_m = ""
for table in tables:
    t_dfs = []
    for i, t in table.iterrows():
        date = t["Date"].split(",")[1].strip()
        if date == latest_m:
            t_dfs.append(t)
        else:
            if t_dfs:
                pandas.concat(t_dfs, axis=1).T.to_csv(f"nba-schedules/{latest_m}.csv")
            t_dfs = [t.to_frame()]
        latest_m = date