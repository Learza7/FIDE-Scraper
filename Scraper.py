from turtle import bgcolor
from urllib.request import urlopen

from selenium import webdriver

# lancement du driver et ouverture de la page
driver = webdriver.Chrome('C:/chromedriver.exe')
driver.get('https://ratings.fide.com/calculations.phtml?id_number=651077493&period=2022-06-01&rating=0')

# tableau
calc_table = driver.find_elements_by_class_name('calc_table')[0]
# Liste des lignes
rows = calc_table.find_elements_by_tag_name('tr')
rows[1]
#index des noms des compétitions
titles_index = []
for i, row in enumerate(rows):
    if row.get_attribute('bgcolor') == '#b7b7b7':
        titles_index.append(i-1)

result = []

for i in titles_index:
    Tournoi = {}
    Tournoi["event_name"] = rows[i].find_element_by_class_name('head1').get_attribute('innerText').replace('\xa0', '')
    Tournoi["games"] = []
    Tournoi["change"] = 0.0
    result.append(Tournoi)
        

j = -1
for i, row in enumerate(rows):
    if i in titles_index:
        j += 1
        
    else:
        td = row.find_elements_by_class_name("list4")
        if len(td) > 1:
            game = {}
            game["opponent_name"] = td[0].get_attribute('innerText').replace('\xa0', '')[1:]
            game["opponent_elo"] = int(td[3].get_attribute('innerText').replace('\xa0', '').replace(' *', ''))
            game["result"] = float(td[5].get_attribute('innerText').replace('\xa0', ''))
            game["K"] = int(td[8].get_attribute('innerText').replace('\xa0', ''))
            game["change"] = round(float(td[9].get_attribute('innerText').replace('\xa0', '')),3)

            result[j]["change"] = round(result[j]["change"] + game["change"],3)
            result[j]["games"].append(game)


driver.quit()

import json
print(json.dumps(result))


#DATABASE
#Person
"""
    fide_id
    first_name
    last_name
    standard_elo
    rapid_elo
    blitz_elo
    totem
    bday_date
    nationality

    variation?
    


"""