import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
service = Service('../chromedriver')


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-web-security')


class Scraper:
    """
    Make request with different settings and return bs-object

    Methods:
        get_response(),
        get_bs_response(),
    """

    def __init__(self, url):
        self.url = url

    def _get_response_request(self):
        return requests.get(self.url).text

    def _get_response_selenium(self):
        with webdriver.Chrome(options=chrome_options, service=service) as wd:
            wd.get(self.url)
            return wd.page_source

    def get_bs_response(self, selenium_on=False):
        if selenium_on:
            return BeautifulSoup(self._get_response_selenium(), 'html.parser')
        return BeautifulSoup(self._get_response_request(), 'html.parser')
