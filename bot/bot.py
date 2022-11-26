from discord.ext import commands, tasks
from discord import Intents, Embed
from datetime import time, datetime

import pandas

nba_schedule_channel = 1024910194167271494
nfl_schedule_channel = 1024879364359323698
nhl_schedule_channel = 1024910545754804294
ncaaf_schedule_channel = 1024910323335045161

bot = commands.Bot(command_prefix="$", intents=Intents.all())

def get_games(games):
    count = 0
    games_part = []
    games_temp = []
    for i, game in games.iterrows():
        count += 1
        games_temp.append(game)
        if count == 6:
            games_part.append(games_temp)
            games_temp = []
            count = 0
    else:
        if games_temp:
            games_part.append(games_temp)
    return games_part

@tasks.loop(time=time(hour=0, minute=4))
async def nba_schedule():
    await bot.wait_until_ready()

    channel = bot.get_channel(nba_schedule_channel)
    now = datetime.now()
    date = now.strftime("%b %d")
    games = pandas.read_csv(f"nba-schedules/{date}.csv")
    games_part = get_games(games)
    
    count = 0
    for game_part in games_part:
        embed = Embed()
        embed.title = f"NBA Schedule for {now.strftime('%A, %b %d')}"
        embed.description = f"Total games: {len(games)}"
        embed.set_thumbnail(url="https://a.espncdn.com/combiner/i?img=/i/teamlogos/leagues/500/nba.png&w=288&h=288&transparent=true")
        for game in game_part:
            count += 1
            name = f"{game[3]} VS {game[5]}"
            link = f"https://www.cbssports.com/nba/gametracker/recap/NBA_{now.strftime('%Y%m%d')}_{game[3][:3].upper()}@{game[5][:3].upper()}/"
            embed.add_field(name=str(count), value="—"*30, inline=False)
            embed.add_field(name=name, value=f"[Preview: {game[3][:3].upper()}@{game[5][:3].upper()}]({link})", inline=True)
            embed.add_field(name="TIME :timer:", value=f"{game[2].replace('p', 'P.M').replace('a', 'A.M')} ET", inline=True)
            embed.add_field(name="ARENA :stadium:", value=f"[{game[10]}](https://www.google.com/search?q={game[10].replace(' ', '+')})", inline=True)
        await channel.send(embed=embed)
    return

@tasks.loop(time=time(hour=0))
async def nfl_schedule():
    await bot.wait_until_ready()

    channel = bot.get_channel(nfl_schedule_channel)
    now = datetime.now()
    date = now.strftime("%Y&m%d")
    games = pandas.read_csv(f"nfl-schedules/{date}.csv")
    games_part = get_games(games)
    count = 0
    for game_part in games_part:
        embed = Embed()
        embed.title = f"NFL Schedule for {now.strftime('%A, %b %d')}"
        embed.description = f"Total games: {len(games)}"
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/National_Football_League_logo.svg/1200px-National_Football_League_logo.svg.png")
        for game in game_part:
            count += 1
            name = f"{game[5]} VS {game[7]}"
            link = f"https://www.cbssports.com/nfl/gametracker/recap/NFL_{now.strftime('%Y%m%d')}_{game[5].split(' ')[-1][:3].upper()}@{game[7].split(' ')[-1][:3].upper()}/"
            embed.add_field(name=str(count), value="—"*30, inline=False)
            embed.add_field(name=name, value=f"[Preview: {game[5].split(' ')[-1][:3].upper()}@{game[7].split(' ')[-1][:3].upper()}]({link})", inline=True)
            embed.add_field(name="TIME :timer:", value=f"{game[4]} ET", inline=True)
        await channel.send(embed=embed)
    return

@tasks.loop(time=time(hour=0, minute=1))
async def nhl_schedule():
    channel = bot.get_channel(nfl_schedule_channel)
    now = datetime.now()
    date = now.strftime("%Y%m%d")
    games = pandas.read_csv(f"nhl-schedules/{date}.csv")
    games_part = get_games(games)
    count = 0
    for game_part in games_part:
        embed = Embed()
        embed.title = f"NHL Schedule for {now.strftime('%A, %b %d')}"
        embed.description = f"Total games: {len(games)}"
        embed.set_thumbnail(url="https://logos-world.net/wp-content/uploads/2021/09/NHL-Logo.png")
        for game in game_part:
            count += 1
            name = f"{game[2]} VS {game[4]}"
            link = f"https://www.cbssports.com/nhl/gametracker/recap/NHL_{now.strftime('%Y%m%d')}_{game[2].split(' ')[-1][:3].upper()}@{game[4].split(' ')[-1][:3].upper()}/"
            embed.add_field(name=str(count), value="—"*30, inline=False)
            embed.add_field(name=name, value=f"[Preview: {game[2].split(' ')[-1][:3].upper()}@{game[4].split(' ')[-1][:3].upper()}]({link})", inline=True)
            # embed.add_field(name="TIME :timer:", value=f"{game[4]} ET", inline=True)
        await channel.send(embed=embed)
    return

@tasks.loop(time=time(hour=0, minute=2))
async def ncaaf_schedule():
    await bot.wait_until_ready()

    channel = bot.get_channel(nba_schedule_channel)
    now = datetime.now()
    date = now.strftime("%b %d, %Y")
    games = pandas.read_csv(f"ncaaf-schedules/{date}.csv")
    games_part = get_games(games)
    
    count = 0
    for game_part in games_part:
        embed = Embed()
        embed.title = f"NCAAB Schedule for {now.strftime('%A, %b %d')}"
        embed.description = f"Total games: {len(games)}"
        embed.set_thumbnail(url="https://assets.b365api.com/images/wp/o/3246676ce39b729733e4efc75dd56226.svg")
        for game in game_part:
            count += 1
            name = f"{game[6]} VS {game[9]}"
            with open("./bot/ncaaf-team.txt") as f:
                teams = [a.strip().split(",") for a in f.readlines()]
            
            
            t1 = ""
            t2 = ""
            for tn, ta in teams:
                if game[6].lower().strip() == tn.lower().strip():
                    t1 = ta
                
                if game[9].lower().strip() == tn.lower().strip():
                    t2 = ta
                
            for tn, ta in teams:
                if not t1:
                    if game[6].lower().strip() in tn.lower().strip() or tn.lower().strip() in game[6].lower().strip():
                        t1 = ta
                if not t2:
                    if game[9].lower().strip() in tn.lower().strip() or tn.lower().strip() in game[9].lower().strip():
                        t2 = ta
            
            if not t1:
                t1 = game[6].strip()[:3].upper()
            if not t2:
                t2 = game[9].strip()[:3].upper()
            
            if t1:=t1.split(" "):
                t1 = t1[-1]
            if t2:=t2.split(" "):
                t2 = t2[-1]
            
            link = f"https://www.cbssports.com/college-football/gametracker/preview/NCAAF_{now.strftime('%Y%m%d')}_{t1}@{t2}/"
            embed.add_field(name=str(count), value="—"*30, inline=False)
            embed.add_field(name=name, value=f"[Preview: {t1}@{t2}]({link})", inline=True)
            embed.add_field(name="TIME :timer:", value=f"{game[4].replace('p', 'P.M').replace('a', 'A.M')} ET", inline=True)
        await channel.send(embed=embed)
    return

@bot.event
async def on_ready():
    if not nba_schedule.is_running():
        nba_schedule.start()
    
    if not nfl_schedule.is_running():
        nfl_schedule.start()
    
    if not nhl_schedule.is_running():
        nhl_schedule.start()

    if not ncaaf_schedule.is_running():
        ncaaf_schedule.start()
    # called_once_a_day.start()
    print(bot.user)

if __name__ == "__main__":
    bot.run("MTA0NTg4NjEzOTM0MjU0MDg2MA.G9xZEp.83uhAli4aoWIhXW2sc5BO3NG_MTap4Z3b2vzaI")
    # bot.run("Insert TOKEN Here")