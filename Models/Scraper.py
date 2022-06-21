from bs4 import BeautifulSoup as bs
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

browser_options = Options()
browser_options.headless= True

import json




def getEloHistory(fide_id : int):
    """ 
        Takes the FIDE id of the player and returns a list containing monthly elos and the number of games
        played by month.
    """
    url= f'https://ratings.fide.com/profile/{fide_id}/chart'
   
    html = requests.get(url).content
    soup = bs(html, 'lxml')

    table = soup.find('table', class_='profile-table profile-table_chart-table')
    rows = table.find_all('tr')

    history = []

    for row in rows[1:]:    # First row is thead
        tds = row.find_all('td')

        std_elo = tds[1].get_text().replace('\xa0', '')     # The encoding of the page adds \xa0 to the beginning
        rapid_elo = tds[3].get_text().replace('\xa0', '')   # of each string retrieved
        blitz_elo = tds[5].get_text().replace('\xa0', '')

        history.append({                                    # None <=> Unranked

            'date': tds[0].get_text().replace('\xa0', ''),

            'standard_elo': int(std_elo) if std_elo else None,
            'num_standard_games': int(tds[2].get_text().replace('\xa0', '')) if std_elo else 0,

            'rapid_elo': int(rapid_elo) if rapid_elo else None,
            'num_rapid_games': int(tds[4].get_text().replace('\xa0', '')) if rapid_elo else 0,

            'blitz_elo': int(blitz_elo) if blitz_elo else None,
            'num_blitz_games': int(tds[6].get_text().replace('\xa0', '')) if blitz_elo else 0,

        })

    return history


def getPlayerInfo(fide_id : int):
    """ Takes the FIDE id of a player and returns their profile page info """

    url= f'https://ratings.fide.com/profile/{fide_id}'
    
    html = requests.get(url).content
    soup = bs(html, 'lxml')

    profile = soup.find_all('div', class_ = 'profile-top-info__block__row__data')
    rank_table = soup.find_all('table', class_='profile-table profile-table_offset_3')
    ranked = len(rank_table) > 2
    info = {

        'federation': profile[1].get_text().replace('\xa0', ''),
        'birth_year': int(profile[3].get_text().replace('\xa0', '')),
        'sex': profile[4].get_text().replace('\xa0', ''),
        'title': profile[5].get_text().replace('\xa0', '').replace('None', ''),
        'world_rank': int(rank_table[1].find_all('tr')[2].find_all('td')[1].get_text()) if ranked else None,
        'continental_rank': int(rank_table[3].find_all('tr')[2].find_all('td')[1].get_text()) if ranked else None,
        'national_rank': int(rank_table[3].find_all('tr')[2].find_all('td')[1].get_text()) if ranked else None,

    }

    return info

def getGamesHistory(fide_id : int, period : str, time_control : int):

    url = f'https://ratings.fide.com/calculations.phtml?id_number={fide_id}&period={period}&rating={time_control}'

    driver = webdriver.Chrome('C:/chromedriver.exe', options=browser_options)
    driver.get(url)

    calc_tables = driver.find_elements_by_class_name('calc_table')
    if not calc_tables:
        return []
    calc_table = driver.find_elements_by_class_name('calc_table')[0]

    rows = calc_table.find_elements_by_tag_name('tr')
    
    # I need to get the indexes of the rows that delimitate each tournament
    titles_index = []
    for i, row in enumerate(rows):
        if row.get_attribute('bgcolor') == '#b7b7b7':
            titles_index.append(i-1)


    history = []

    for i in titles_index:

        tournament = {

            'event_name': rows[i].find_element_by_class_name('head1').get_attribute('innerText').replace('\xa0', ''),
            'games': [],
            'change': 0.0

        }
        history.append(tournament)
            
    j = -1 # index of the current tournament
    for i, row in enumerate(rows):
        
        if i in titles_index:
            j += 1
            
        else:
            td = row.find_elements_by_class_name("list4")

            if len(td) > 1:
                game = {
                    
                    'opponent_name':  td[0].get_attribute('innerText').replace('\xa0', '')[1:],
                    'opponent_elo': int(td[3].get_attribute('innerText').replace('\xa0', '').replace(' *', '')),
                    'result': float(td[5].get_attribute('innerText').replace('\xa0', '')),
                    'K': int(td[8].get_attribute('innerText').replace('\xa0', '')) if td[8].get_attribute('innerText').replace('\xa0', '') else 0,
                    'change':  round(float(td[9].get_attribute('innerText').replace('\xa0', '')), 3),
                    'color': 'white' if 'wh' in td[0].find_element_by_tag_name('img').get_attribute('src') else 'black',

                }

                history[j]["change"] = round(history[j]["change"] + game["change"], 3)

                history[j]["games"].append(game)

    # maybe I can let the driver opened h24 to gain in perfomances, needs a try
    driver.quit()
    return history


# DATABASE
# Person
"""
    fide_id
    first_name
    last_name
    standard_elo
    rapid_elo
    blitz_elo
    totem
    bday_date #initialiser avec année de fide puis raffiner
    nationality
    world_rank
    continental_rank
    national_rank

    variation?
      sex
      title
    


"""

# print(json.dumps(getPlayerInfo(651077493), indent=4))
# print(json.dumps(getEloHistory(651077493), indent=4))

#print(json.dumps(getGamesHistory(651077493, '2022-06-01', 0), indent = 4))





