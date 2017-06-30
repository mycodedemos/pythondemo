from bs4 import BeautifulSoup as bs
import requests


if __name__ == '__main__':
    soup = bs(requests.get('https://www.bbb397.com/htm/movie1/3198.htm').content,'lxml')
    print(soup)