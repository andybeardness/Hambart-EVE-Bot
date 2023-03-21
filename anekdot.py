import requests
import botsecrets
import re
from bs4 import BeautifulSoup

ANEKDOT_URL = botsecrets.ANEKDOT_URL

__clean_pattern = re.compile('<.*?>')

def __replace_br_to_newline(raw_html):
    return raw_html.replace('<br/>', '\n')

def __clean_html(raw_html):
    return re.sub(__clean_pattern, '', raw_html)

def __trim(raw_string):
    return raw_string.strip()

def __request_anekot():
    response = requests.get(ANEKDOT_URL)
    bs = BeautifulSoup(response.text, features="html.parser")
    
    anekdot = bs.find('div', class_='text')
    anekdot = str(anekdot)

    replaced = __replace_br_to_newline(raw_html=anekdot)
    cleaned = __clean_html(raw_html=replaced)
    trimmed = __trim(raw_string=cleaned)

    return trimmed

def get_anekdot():
    return __request_anekot()

if __name__ == '__main__':
    print(get_anekdot())