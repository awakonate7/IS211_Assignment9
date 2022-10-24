#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup as soup
import requests as uRequirement
import os
import json

#To avoid crash YOU MUST create a folder in your local HD called C:\Users\xxxxxx\website_download\football_stats to download the files
class parameters:
    """Create a working local directory when the files are going to be stored"""
    def __init__(self):
        if os.name == 'nt':
            self.current_working_folder = "\\website_download\\football_stats\\"
        else:
            self.current_working_folder = "/website_download/football_stats/"
        self.current_working_file = "football_stats.htm"
        self.localpath = os.getcwd() + self.current_working_folder

    def fullpath(self):
        path = self.localpath + self.current_working_file
        return str(path)

    def searchdir(self):
        oplenght = os.listdir(self.localpath)
        return oplenght


def html_pull(files):
    f = files()
    if len(f.SearchDir()) == 0:
        print('directory empty')
        r = uRequirement.get("https://www.nfl.com/stats/player-stats/")
        open(f.localpath + f.current_working_file, 'xb').write(r.content)
    else:
        print('items in dir, skipping download')
    return

#parse URL using BeautifulSoup
def parser_files(files):
    f = files()
    r = open(f.FullPath(), encoding="utf-8")

    soup = BeautifulSoup(r, 'html.parser')
    player_stats = soup.find_all('tr', {"class": "TableBase-bodyTr"})
    num, list_of_players = 0, []
    for players in player_stats:
        player_stat_cols = players.find_all('td')
        player_stat_ttl_td = [ele.text.strip().replace("\\n", "") for ele in player_stat_cols]
        player_stat_info = [ele for ele in player_stat_cols]
        player_stat_info = player_stat_info[0]
        player_name_elem = player_stat_info.find('a', {'class': ""})  #NAME
        player_pos_elem = player_stat_info.find('span', {'class': "CellPlayerName-position"})  #POS
        player_team_elem = player_stat_info.find('span', {'class': "CellPlayerName-team"})  #TEAM
        players_touchdown_elem = player_stat_ttl_td[12]  #TOUCHDOWNS
        if num < 21:            
            jspn_str = {
                        "PLAYER NAME": player_name_elem.text.strip(),
                        "POS": player_pos_elem.text.strip(),
                        "TEAM": player_team_elem.text.strip(),
                        "TOUCHDOWNS": players_touchdown_elem}
            json_out = json.dumps(jspn_str)
            list_of_players.append(json_out)
            num += 1
    for x in list_of_players: print(x)


def main():
    html_pull(parameters)
    parser_files(parameters)


main()
