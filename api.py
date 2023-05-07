import requests
import re
from copy import deepcopy as dc
from bs4 import BeautifulSoup

URL = 'https://1337x.to'
DAILY =  URL + '/trending/d/movies/'
WEEKLY = URL + '/trending/w/movies/'
SEARCH = URL + '/search/{}/1/'

def get_search_result(url):
    # extracts the 1337x search table
    results = []
    count = 0
    pg = requests.get(url, headers={'User-Agent':'Chrome'})
    soup = BeautifulSoup(pg.content, "html.parser")
    for row in soup.findAll('tr'):
        anchor = row.find('a', href=re.compile('/torrent/*'))
        if not anchor: continue
        ctx = {}
        count += 1
        ctx['no'] = count
        ctx['name'] = anchor.text
        ctx['url'] = anchor['href']
        ctx['seeds'] = row.find('td', class_='seeds').text
        ctx['leeches'] = row.find('td', class_='leeches').text
        size = row.find('td', class_='size').text
        ctx['size'] = re.findall('.*B',size)[0]
        results.append(ctx)
    return results

def get_magnet(url):
    # gets the magnet from the given url
    pg = requests.get(URL+ url)
    soup = BeautifulSoup(pg.content, "html.parser")
    anchor = soup.find('a', href=re.compile('magnet.*'))
    return anchor['href']

def build_search_url(key):
    # generated the search url
    key = re.sub( '\W', ' ', key )
    key = key.replace("  ", " ")
    key = key.strip()
    key = key.replace(" ", '+')
    url = SEARCH.format(key)
    return url