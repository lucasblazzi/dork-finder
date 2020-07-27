import requests
import time
import html
import json


# search for the google dork search query on the html code
def findText(html_code):
    start = 'rel="nofollow">'
    end = "</a>"
    raw_dork = (html_code.split(start))[1].split(end)[0]
    dork = html.unescape(raw_dork)
    return dork.strip()     # return only the dork search query


# append the dork list to a json file
def save_dork(dork_list):
    json_dork = json.dumps(dork_list, indent=4)
    with open('dorks.json', mode='w', encoding='utf-8') as file:
        file.write(json_dork)


# cat the last dork id registered
def cat_last_id():
    with open('dorks.json') as file:
        data = json.load(file)
        last = len(data) - 1
        return int(data[last]['id'])


def cat_dork_list():
    with open('dorks.json') as file:
        data = json.load(file)
        return data


def update_dorks():
    n = cat_last_id() + 1
    count = 1
    url = 'https://www.exploit-db.com/ghdb/{}'.format(str(n))
    headers = {
        'Host': 'www.exploit-db.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'
    }

    dork_list = cat_dork_list()
    # recursively search for all dorks in GHDB --> using the id 1 to n
    while True:
        r = requests.get(url, headers=headers, timeout=1000)
        print(url)
        if r.status_code == 200:
            count = 0
            html_code = r.text
            dork = findText(html_code)
            new_dork = {
                'id': n,
                'dork': dork
            }
            print(new_dork)
            dork_list.append(new_dork)

            n += 1
            url = 'https://www.exploit-db.com/ghdb/{}'.format(str(n))
            time.sleep(10)
        else:           # sometimes a dork was deleted, so we have id 1600 and 1602 but not 1601, in this case the
            n += 1      # update the n variable to check the next id
            count += 1  # the count variable represent the retries until the last id is found
            url = 'https://www.exploit-db.com/ghdb/{}'.format(str(n))
            if count == 10:  # if we retry 5 times in a row and 404 is returned all tries, the program saves the data
                break       # representing that is updated
            else:
                continue

    save_dork(dork_list)


