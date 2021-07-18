# python-opgg
The Riot API doesn't want me, I don't need it. This is a web scraper to get League of Legends stats.

# usage examples:
```Python
import python_opgg

stat = python_opgg.get_stat("yanis360", region="euw")

#get rank in solo
print("rank in solo :", stat.solo_rank)

#get rank in 5vs5
print("rank in flex :", stat.flex_rank)

#get the number of losed game
print("game losed in last 10 :",stat.last_ten_games_lose)

#get the number of won game
print("game won in last 10 :",stat.last_ten_games_win)

#get the winrate the 10 last game
print("winrate the 10 last game :", stat.last_ten_games_win_rate)

#get the stat of the last game
last_game=stat.last_ten_games[0]

#get the result of the last game
print("result of last game :", last_game.result)

#get if the last game is won
print("have won :", last_game.win)

#get if the last game is losed
print("have losed :", last_game.lose)

#get how many kill have been made in the last game
print("kill :", last_game.kill)

#get how many death have been made in the last game
print("death :", last_game.death)

#get how many assist have been made in the last game
print("assist :", last_game.assist)

#get the kd of the last game
print("kd :", last_game.kd)

#get the kda of the last game
print("kda :", last_game.kda)

#get the level of the last game
print("level :", last_game.level)

#get the game length of the last game
print("game length :", last_game.game_length)

#get the game kill participation of the last game
print("game kill participation :", last_game.kill_participation)
```
##### made on code-server