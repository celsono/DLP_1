#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/10 14:30
# @Author  : tzh
# @File    : crawler.py
# @Software: PyCharm

import requests
import bs4

"""
    description:Fetch specified  Web information according to the input 
"""


class Crawler:
    """ this class includes two methods, both of them are used to crawl the Web content,and is will be stored as
    attributes of the object """

    def __init__(self, name):
        self.seq = 0  # it stores the serial number entered by the user
        self.author_soup = None
        self.search_soup = None
        self.name = name  # it stores the scientist's name entered by the user
        self.author = []  # it stores the scientists' name we crawl
        self.author_url = []  # it stores their personal homepages' url we crawl
        self.year_article = {}  # it's a dictionary, the keys are the published year, and values are lists containing
        # correspondingly article titles
        self.appeal = ''  # it 's an appeal about U & R

    """ 
        parameter——name: the name of the scientist you want to search
        restriction: please Enter the standard format
        function: crawl the web and retrieve two lists containing searched scientists' name and their personal homepages 
     """

    def get_url(self):
        prefix = 'https://dblp.org/search?q='
        search_url = prefix + self.name
        res = requests.get(search_url)
        self.search_soup = bs4.BeautifulSoup(res.text, features="lxml")

        info = self.search_soup.find_all('li', itemtype="http://schema.org/Person")
        for i in info:
            self.author.append(i.span.get_text())
            self.author_url.append(i.a.get("href"))

    """
        parameter——seq: it's the serial number the user prefers to look up
        restriction: please do not go out of range
        function: crawl the selected scientist's homepage and get the article titles 
    """

    def get_article(self, seq=0):
        self.seq = seq
        res = requests.get(self.author_url[self.seq])
        self.author_soup = bs4.BeautifulSoup(res.text, features='lxml')
        mess = self.author_soup.find_all('cite', {'class': 'data tts-content'})
        for i in mess:
            year = i.find('span', {'itemprop': 'datePublished'}).get_text().strip()
            if year not in self.year_article.keys():
                self.year_article[year] = []
            self.year_article[year].append(i.find('span', {'class': 'title'}).get_text().strip())

    """
        reason: Why the method's name is 'stop the war'?, I find that every page at this website has this appeal.
        Considering the Web creator is a Germany, I believe he must be a pacifist. So just grab this appeal as an 
        exercise 
    """

    def stop_the_war(self):
        res = requests.get('https://dblp.org')
        soup = bs4.BeautifulSoup(res.text, features='lxml')
        info = soup.find_all('div', {'class': 'drop-down'})
        new_info = bs4.BeautifulSoup(str(info), features='lxml')
        self.appeal = new_info.span.string

# test codes, just ignore them
# a = Crawler("Ya-qin Zhang")
# a.get_url()
# a.get_article(1)
# a.stop_the_war()
