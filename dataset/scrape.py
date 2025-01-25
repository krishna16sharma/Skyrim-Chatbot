import requests
from bs4 import BeautifulSoup
import csv
  
URL = "https://en.uesp.net/wiki/Skyrim:Guard_Dialogue"
r = requests.get(URL)
  
soup = BeautifulSoup(r.content, 'html5lib')
dialogues = []
data = []
fields = ['Dialogue', 'Requirement']

tables = soup.find_all('table', attrs = {'class':'wikitable'})
passing = tables[0]
witnessed = tables[1]
condition = tables[2]
skill = tables[5]
quests = tables[8]
dawnguard = tables[9]

list_of_tables = [passing, witnessed, condition, skill, quests, dawnguard]
for t in list_of_tables:
    rows = t.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        if(len(cols)):
            data.append([ele for ele in cols if ele])
print(data)

with open('guard_dialogues.csv', 'w', newline='', encoding='utf-8') as f:
    write = csv.writer(f)
      
    write.writerow(fields)
    write.writerows(data)