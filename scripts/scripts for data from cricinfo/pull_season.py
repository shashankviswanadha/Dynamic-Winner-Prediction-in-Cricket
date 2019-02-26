from bs4 import BeautifulSoup
import requests
import re
import yaml
from bs_csricinfo import *
import sys
def get_career_averages_url(url):
    r = requests.get(url)
    html_content = r.text
    soup = BeautifulSoup(html_content)#,"html_parser")
    span = soup.find_all("span",{"class":"cardMenu"})
    for sp in span:
        temp = sp.find_all('a',{"class":"cardMenu"})
        if len(temp) != 0:
            if temp[0].text == 'Career averages':
                print temp
                return temp[0].get('href')
    return 0


seasons = {2008:'http://www.espncricinfo.com/ipl/content/series/313494.html?template=fixtures',2009:'http://www.espncricinfo.com/ipl2009/content/series/374163.html?template=fixtures',2010:'http://www.espncricinfo.com/ipl2010/content/series/418064.html?template=fixtures',2011:'http://www.espncricinfo.com/indian-premier-league-2011/content/series/466304.html?template=fixtures',2012:'http://www.espncricinfo.com/indian-premier-league-2012/content/series/520932.html?template=fixtures',2013:'http://www.espncricinfo.com/indian-premier-league-2013/content/series/586733.html?template=fixtures',2014:'http://www.espncricinfo.com/indian-premier-league-2014/content/series/1078425.html?template=fixtures',2015:'http://www.espncricinfo.com/indian-premier-league-2015/content/series/791129.html?template=fixtures',2016:'http://www.espncricinfo.com/indian-premier-league-2016/content/series/968923.html?template=fixtures',2017:'http://www.espncricinfo.com/indian-premier-league-2017/content/series/1078425.html?template=fixtures'}

base_url = "http://www.espncricinfo.com"
url = seasons[int(sys.argv[1])]
r = requests.get(url)
html_content = r.text
soup = BeautifulSoup(html_content)#,"html_parser")

div = soup.find_all("div", {"class": "fixtures_list clearfix"})
matches = div[0].find_all("a")
for match in matches:
    link_match = base_url + match.get('href')
    temp = get_career_averages_url(link_match)
    if temp != 0:
        link = base_url + temp
        pull_player_stats_to_yaml(link)



#print div[0].find_all('class')

#print links
