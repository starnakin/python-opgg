from bs4 import BeautifulSoup
import urllib
import requests

def get_stat(username: str, region="www"):
    if type(username) != str:
        print("error:", username, "is not an string !")
        return
    if " " in username:
        print("error : username contain space")
        return

    url="https://"+region+".op.gg/summoner/userName="+username
    html_content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html_content, 'html.parser')

    if soup.find("h2", {"class": "Title"}) != None:
        for i in soup.find("ul", {"class": "List"}).findAll("li", {"class": "Item"}):
            url="https://www.op.gg/summoner/userName=".replace("www.op.gg", i["data-host"])+username
            print(url)
            html_content = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html_content, 'html.parser')
            if soup.find("h2", {"class": "Title"}) == None:

                last_ten_games_win = soup.find("span", {"class": "win"})
                if last_ten_games_win == None:
                    last_ten_games_win=0
                else:
                    last_ten_games_win=int(last_ten_games_win.text)

                last_ten_games_lose = soup.find("span", {"class": "lose"})
                if last_ten_games_lose == None:
                    last_ten_games_lose=0
                else:
                    last_ten_games_lose=int(last_ten_games_lose.text)

                last_ten_games_win_rate = last_ten_games_win/(last_ten_games_lose, 1)[last_ten_games_lose==0]

                name = soup.find("span", {"class": "Name"})

                solo_rank=soup.find("div", {"class": "TierRank"})

                if solo_rank == None:
                    solo_rank="unranked"
                else:
                    solo_rank=solo_rank.text.replace("\n", "").replace("\t", "")

                flex_rank=soup.find("div", {"class": "sub-tier__rank-tier"})
                if flex_rank == None:
                    flex_rank="unranked"
                else:
                    flex_rank=flex_rank.text.replace("\n", "").replace("\t", "").replace("  ", "")

                kill = soup.find("span", {"class": ""})

                games=[]
                for game_content in soup.findAll("div", {"class": "GameItemWrap"}):
                    games+=[Game(game_content)]
                
                return Stat(name, solo_rank, flex_rank, last_ten_games_win, last_ten_games_lose, last_ten_games_win_rate, games)

        else:
            print("error:", username, "not exists")
            return

    user_id = int(soup.find("div", {"class": "GameListContainer"})["data-summoner-id"])

    with requests.Session() as s:
        s.post("https://"+region+".op.gg/summoner/ajax/renew.json/",data={"summonerId": user_id})

    url="https://"+region+".op.gg/summoner/userName="+username
    html_content = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html_content, 'html.parser')

    last_ten_games_win = soup.find("span", {"class": "win"})
    if last_ten_games_win == None:
        last_ten_games_win=0
    else:
        last_ten_games_win=int(last_ten_games_win.text)

    last_ten_games_lose = soup.find("span", {"class": "lose"})
    if last_ten_games_lose == None:
        last_ten_games_lose=0
    else:
        last_ten_games_lose=int(last_ten_games_lose.text)

    last_ten_games_win_rate=last_ten_games_win/10

    name = soup.find("span", {"class": "Name"}).text

    solo_rank=soup.find("div", {"class": "TierRank"})

    if solo_rank == None:
        solo_rank="unranked"
    else:
        solo_rank=solo_rank.text.replace("\n", "").replace("\t", "")

    flex_rank=soup.find("div", {"class": "sub-tier__rank-tier"})
    if flex_rank == None:
        flex_rank="unranked"
    else:
        flex_rank=flex_rank.text.replace("\n", "").replace("\t", "").replace("  ", "")

    kill = soup.find("span", {"class": ""})

    games=[]
    for game_content in soup.findAll("div", {"class": "GameItemWrap"}):
        games+=[Game(game_content)]

    return Stat(name, solo_rank, flex_rank, last_ten_games_win, last_ten_games_lose, last_ten_games_win_rate, games)

class Stat:
    def __init__(self, name, solo_rank, flex_rank, last_ten_games_win, last_ten_games_lose, last_ten_games_win_rate, game_data):
        self.name = name
        self.solo_rank = solo_rank
        self.flex_rank = flex_rank
        self.last_ten_games_lose = last_ten_games_lose
        self.last_ten_games_win = last_ten_games_win
        self.last_ten_games_win_rate = last_ten_games_win_rate
        self.last_ten_games = game_data

class Game:
    def __init__(self, game_item_wrap):
        self.type = game_item_wrap.find("div", {"class": "GameType"}).text.replace("\n", "").replace("\t", "")
        self.played_at = game_item_wrap.find("div", {"class": "TimeStamp"}).text.replace("\n", "").replace("\t", "")
        self.kill = int(game_item_wrap.find("span", {"class": "Kill"}).text)
        self.death = int(game_item_wrap.find("span", {"class": "Death"}).text)
        self.assist = int(game_item_wrap.find("span", {"class": "Assist"}).text)
        self.kda = game_item_wrap.find("span", {"class": "KDARatio"}).text.replace("\n", "").replace("\t", "")
        self.kd = (self.kill/self.death, self.kill)[self.death==0]
        self.level = int(game_item_wrap.find("div", {"class": "Level"}).text.replace("\n", "").replace("\t", "").replace("Level", ""))
        self.game_length = game_item_wrap.find("div", {"class":"GameLength"}).text.replace("\n", "").replace("\t", "")
        self.kill_participation = float(game_item_wrap.find("div", {"title":"Kill Participation"}).text.replace("\n", "").replace("\t", "").replace("P/Kill ", "").replace("%", ""))/100
        self.result = game_item_wrap.find("div", {"class":"GameResult"}).text.replace("\n", "").replace("\t", "")
        if self.result == "Defeat":
            self.lose=True
            self.win=False
        else:
            self.win=True
            self.lose=False