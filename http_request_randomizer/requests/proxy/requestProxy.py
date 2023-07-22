import logging
import os
import random
import sys
import time

import json

import requests
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import TooManyRedirects
from requests.exceptions import ConnectionError
from requests.exceptions import ReadTimeout

from http_request_randomizer.requests.proxy.ProxyObject import Protocol
from http_request_randomizer.requests.errors.ProxyListException import ProxyListException
from http_request_randomizer.requests.parsers.FreeProxyParser import FreeProxyParser
from http_request_randomizer.requests.parsers.ProxyForEuParser import ProxyForEuParser
from http_request_randomizer.requests.parsers.RebroWeeblyParser import RebroWeeblyParser
from http_request_randomizer.requests.parsers.PremProxyParser import PremProxyParser
from http_request_randomizer.requests.parsers.SslProxyParser import SslProxyParser
from http_request_randomizer.requests.useragent.userAgent import UserAgentManager

__author__ = 'pgaref'
sys.path.insert(0, os.path.abspath('../../../../'))

# Push back requests library to at least warnings
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-6s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)


class RequestProxy:
    def __init__(self, web_proxy_list=[], sustain=False, timeout=5, protocol=Protocol.HTTP, log_level=0):
        self.logger = logging.getLogger()
        self.logger.addHandler(handler)
        self.logger.setLevel(log_level)
        self.userAgent = UserAgentManager(file=os.path.join(os.path.dirname(__file__), '../data/user_agents.txt'))

        with open(f'C:\\Users\\user\\Desktop\\배정원\\UNIST\\대회\\한국관광공사 Gen AI 해커톤\\bbabam\\crawlingmodels\\Modules\\proxies.json', 'r') as f:
            self.memory = json.load(f)

        #####
        # Each of the classes below implements a specific URL Parser
        #####
        parsers = list([])
        parsers.append(FreeProxyParser('FreeProxy', 'http://free-proxy-list.net', timeout=timeout))
        parsers.append(SslProxyParser('SslProxy', 'https://www.sslproxies.org', timeout=timeout))

        self.logger.debug("=== Initialized Proxy Parsers ===")
        for i in range(len(parsers)):
            self.logger.debug("\t {0}".format(parsers[i].__str__()))
        self.logger.debug("=================================")

        self.sustain = sustain
        self.parsers = parsers
        self.proxy_list = web_proxy_list
        for parser in parsers:
            try:
                size = len(self.proxy_list)
                self.proxy_list += parser.parse_proxyList()
                self.logger.debug('Added {} proxies from {}'.format(len(self.proxy_list)-size, parser.id))
            except ReadTimeout:
                self.logger.warning("Proxy Parser: '{}' TimedOut!".format(parser.url))
        self.logger.debug('Total proxies = '+str(len(self.proxy_list)))
        # filtering the list of available proxies according to user preferences
        self.proxy_list = [p for p in self.proxy_list if protocol in p.protocols]
        random.shuffle(self.proxy_list)
        for i in range(len(self.proxy_list)):
            if self.proxy_list[i].get_address() not in self.memory['address']:
                self.memory['type'].append('http')
                self.memory['address'].append(self.proxy_list[i].get_address())
                self.memory['usable'].append('unknown')

        with open(f'C:\\Users\\user\\Desktop\\배정원\\UNIST\\대회\\한국관광공사 Gen AI 해커톤\\bbabam\\crawlingmodels\\Modules\\proxies.json', 'w') as make_file:
                json.dump(self.memory, make_file, indent="\t")

        self.logger.debug('Filtered proxies = '+str(len(self.proxy_list)))

    def set_logger_level(self, level):
        self.logger.setLevel(level)

    def get_proxy_list(self):
        return self.proxy_list

    def generate_random_request_headers(self):
        headers = {
            "Connection": "close",  # another way to cover tracks
            "User-Agent": self.userAgent.get_random_user_agent()
        }  # select a random user agent
        return headers

    #####
    # Proxy format:
    # http://<USERNAME>:<PASSWORD>@<IP-ADDR>:<PORT>
    #####
    def generate_proxied_request(self, url, method="GET", params={}, data={}, headers={}, req_timeout=30):
            for i in range(len(self.memory)):
                with open(f'C:\\Users\\user\\Desktop\\배정원\\UNIST\\대회\\한국관광공사 Gen AI 해커톤\\bbabam\\crawlingmodels\\Modules\\proxies.json', 'r') as f:
                    self.memory = json.load(f)
                if self.memory['usable'] == 'false':
                    pass

                try:
                    req_headers = dict(params.items())
                    req_headers_random = dict(self.generate_random_request_headers().items())
                    req_headers.update(req_headers_random)

                    headers.update(req_headers)
                    proxies={
                                "http": "http://{0}".format(self.memory['address'][i]),
                                "https": "https://{0}".format(self.memory['address'][i])
                            }
                    request = requests.request(method, url, headers=headers, data=data, params=params, timeout=req_timeout, proxies=proxies)

                    self.logger.debug("Using headers: {0}".format(str(headers)))
                    self.logger.debug("Using proxy: {0}".format(str(self.memory['address'][i])))
                    
                    if request is not None:
                        self.memory['address'].insert(0, self.memory['address'][i])
                        self.memory['usable'][i] = 'true'
                        with open(f'C:\\Users\\user\\Desktop\\배정원\\UNIST\\대회\\한국관광공사 Gen AI 해커톤\\bbabam\\crawlingmodels\\Modules\\proxies.json', 'w') as make_file:
                            json.dump(self.memory, make_file, indent="\t")
                        return {'http': 'http://%s' % self.memory['address'][i]}
                        
                    else:
                        self.memory['usable'][i] = 'false'
                        with open(f'C:\\Users\\user\\Desktop\\배정원\\UNIST\\대회\\한국관광공사 Gen AI 해커톤\\bbabam\\crawlingmodels\\Modules\\proxies.json', 'w') as make_file:
                            json.dump(self.memory, make_file, indent="\t")

                except ConnectionError:
                    self.logger.debug("Proxy unreachable - Removed Straggling proxy: {0} PL Size = {1}".format(
                        self.memory['address'][i], len(self.proxy_list)))

                except ReadTimeout:
                    self.logger.debug("Read timed out - Removed Straggling proxy: {0} PL Size = {1}".format(
                        self.memory['address'][i], len(self.proxy_list)))
            
                except ChunkedEncodingError:
                    self.logger.debug("Wrong server chunked encoding - Removed Straggling proxy: {0} PL Size = {1}".format(
                        self.memory['address'][i], len(self.proxy_list)))
                    
                except TooManyRedirects:
                    self.logger.debug("Too many redirects - Removed Straggling proxy: {0} PL Size = {1}".format(
                        self.memory['address'][i], len(self.proxy_list)))