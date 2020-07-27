from googlesearch import search
import argparse
from DorkFinder import cat_dork_list


def search_dork(target, dork_list):
    for data in dork_list:
        query = data['dork'] + " site:{}" .format(target)
        print("--> Dork: {}" .format(query))
        for url in search(query, num=10, start=0, stop=10, pause=2):
            print("\t[+] FOUND - {}" .format(url))


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
    parser.add_argument("word", help="word restriction, ex: admin")

    args = parser.parse_args()

    restricted_search(args.target, args.word)
