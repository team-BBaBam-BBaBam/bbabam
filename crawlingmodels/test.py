from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
import logging

import requests
from bs4 import BeautifulSoup

from http_request_randomizer.requests.parsers.UrlParser import UrlParser

response = requests.get('http://free-proxy-list.net')

content = response.content
soup = BeautifulSoup(content, "html.parser")
table = soup.find("div", attrs={"class": "modal-body"}).get_text().split('\n')

#print(soup)
print(table)
