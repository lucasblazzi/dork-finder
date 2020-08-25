import urllib3
import urllib.parse
import requests
import argparse
from updateDorks import cat_dork_list
from bs4 import BeautifulSoup
import time



def search_dork(target, dork_list):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {'user-agent': USER_AGENT}
    for dork in dork_list:
        time.sleep(10)
        query = dork['dork'] + ' site:{}' .format(target)
        print(query)
        query = urllib.parse.quote(query)
        url = "https://google.com/search?q={}" .format(query)
        resp = requests.get(url, headers=headers)
        results = []
        print(resp.status_code)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            for g in soup.find_all('div', class_='r'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    title = g.find('h3').text
                    item = {
                        "title": title,
                        'link': link
                    }
                    results.append(item)
            for result in results:
                print('\t[*] FOUND  -  ' + result['title'] + ' --> ' + result['link'] + '\n')
        resp.cookies.clear()


def full_search(target):
    full_dork_list = cat_dork_list()
    search_dork(target, full_dork_list)


def restricted_search(target, word):
    full_dork_list = cat_dork_list()
    restricted_list = []
    for data in full_dork_list:
        query = data['dork']
        if word in query:
            restricted_list.append(data)
    search_dork(target, restricted_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="target, ex: example.com")
    #parser.add_argument("word", help="word restriction, ex: admin")

    args = parser.parse_args()
    if args.target:
        full_search(args.target)
    #elif args.target and args.word:
    #    restricted_search(args.target, args.word)
