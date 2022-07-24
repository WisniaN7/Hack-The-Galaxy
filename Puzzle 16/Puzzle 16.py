#%%
import re
import requests
import sys
from bs4 import BeautifulSoup

topFilms = {}

#%% DATA ACQUISITION
url = "https://en.wikipedia.org/w/api.php?action=parse&page={year}_in_film&format=json&section={section}"
section2years = [2000, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]

for i in range(1992, 2023):
    print("Getting", i)

    if i in section2years:
        response = requests.get(url.format(year=i, section=2))
    else:
        response = requests.get(url.format(year=i, section=1))

    if response.status_code == 200:
        data = response.json()
        text = data['parse']['text']['*']
        
        tableHTML = re.findall(r'<table(.*?)</table>', text, re.DOTALL)[0]
        table = BeautifulSoup(tableHTML, 'html.parser')

        topFilms[i] = {}

        for row in table.find_all('tr')[1:]:
            tmp = row.text.strip().split('\n')
            topFilms[i][tmp[0]] = tmp[2]        
    else:
        print(response.status_code)
        print(response.text)
        print(url.format(year=i))
        print()
        sys.exit(-response.status_code)

print(topFilms)
#%%

eligableFimls = []

for year in topFilms:
    # print(year)
    i = 0

    for rank in topFilms[year]:
        if (i < 100):
            # print(rank, topFilms[year][rank])
            i += 1

            if topFilms[year][rank].count(' ') == 1 and topFilms[year][rank].find('The ') == -1:
                eligableFimls.append(topFilms[year][rank])
            elif topFilms[year][rank].count(' ') == 2 and topFilms[year][rank].find('The ') != -1:
                eligableFimls.append(topFilms[year][rank])
            
    # print()

print(eligableFimls)
# %%
letters = [
    'BCEHKLNPTR',
    'DEFGIIMNO',
    'EEIIMNNORRSTTUVY',
    'ADELNORSV',
    'ACDDGHINRRSSW',
    'AACIJKPSSU',
    'GKLNNO',
    'EEHINSTX',
    'ACEIRSS',
    'DDEEILMORRTX',
    'AABEMNNRRSU',
    'RSTTYY',
    'ADEMNNRWW',
    'BEILMMNOOPSSSS',
    'AIMOR',
    'AGGHMNRSU',
]

ignored = '.\\/:;,.-'

solutions = {}

for words in range(len(letters)):
    solutions[letters[words]] = []

for film in eligableFimls:
    
    for i in range(len(letters)):
        # if len(film) - film.count(' ') != len(letters[i]) + 2:
        #     continue
        
        missingLetter = False

        for letter in letters[i]:
            # print(film, letter, film.upper().find(letter), letters[i])

            if film.upper().find(letter) == -1 and letter not in ignored:
                missingLetter = True
                break

        if not missingLetter:
            solutions[letters[i]].append(film)

print(solutions)

# %%
