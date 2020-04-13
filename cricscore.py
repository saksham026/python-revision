import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import re
from time import sleep


def get_current_matches():
    
    page = requests.get('http://static.cricinfo.com/rss/livescores.xml') # HTTP Get request to cricinfo rss feed
    soup = BeautifulSoup(page.text,'lxml') # parsing and building xml tree out of the returned xml file default is html5lib
    matches = soup.find_all('description') # description tags contain the score
    live_matches = [s.get_text() for s in matches if '*' in s.get_text()] # returns only the live matches and ignores the completed ones
    return live_matches

def fetch_score(matchNum):
    
    page = requests.get('http://static.cricinfo.com/rss/livescores.xml')
    soup = BeautifulSoup(page.text,'lxml')
    matches = soup.find_all('description')
    live_matches = [s.get_text() for s in matches if '*' in s.get_text()]
    return live_matches[matchNum]
  

def notify(score):
    
    toaster = ToastNotifier()
    toaster.show_toast(score,
                       "score updates",
                       duration=10)



if __name__ == "__main__":
     
    matches = get_current_matches()
    print('Current matches in play')
    print('='*23)
     
    for i,match in enumerate(matches):
                print('[{}] '.format(i) + 
                        re.search('\D+',match.split('v')[0]).group() + 'vs.' +
                        re.search('\D+',match.split('v')[1]).group()
                      )

    print()
    matchNum = int(input('Pick the match number [0,1,2...] => '))


    while True:
        current_score = fetch_score(matchNum)
        notify(current_score)
        sleep(10)
