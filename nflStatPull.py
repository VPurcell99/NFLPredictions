""" import nflgame

years = [2019]

for year in years:
    games = nflgame.games(year=year)
    for game in games:
        game_doc = {}
        game_doc['schedule'] = game.schedule
        game_doc['stats_home'] = game.stats_home._asdict()
        game_doc['stats_away'] = game.stats_away._asdict() """

import requests
import datahelp
import pandas  as pd
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://www.pro-football-reference.com'
years = range(2010,2021)
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
for team in datahelp.team_strs.values():
    for year in range(2010,2012):
        r = requests.get(url + '/teams/' + team + '/' + str(year) + '.htm')
        soup = BeautifulSoup(r.content, 'html.parser')
        team_tables = soup.find_all('table')
        for table in team_tables:
            if table.attrs['id'] == 'games':
                column_headers = table.findAll('tr')[1]
                column_headers = [i.getText() for i in column_headers.findAll('th')]
                rows = table.findAll('tr')[2:]
                #game_results = []
                for i in range(len(rows)):
                    #game_results.append([col.getText() for col in rows[i].findAll('td')])
                    row = [col.getText() for col in rows[i].findAll('td')]
                    if row[7] != '@':
                        date = str(year) + datahelp.month_dict[row[1].split(' ')[0]] + row[1].split(' ')[1] + '0'
                        bs_url = url + '/boxscores/' + date + team + '.htm'
                        driver = webdriver.Chrome(executable_path=r'C:/Users/vin99/AppData/Local/ChromeDriver/chromedriver.exe')
                        driver.get(bs_url)
                        driver.implicitly_wait(2)
                        bs_soup = BeautifulSoup(driver.page_source, 'lxml')
                        bs_tables = bs_soup.find_all('table')
                        for bs_table in bs_tables:
                            try:
                                if bs_table['id'] == 'team_stats':
                                    bs_column_headers = bs_table.findAll('tr')[0]
                                    bs_column_headers = [i.getText() for i in bs_column_headers.findAll('th')]
                                    bs_rows = bs_table.findAll('tr')[1:]
                            except:
                                pass
                        
                            
