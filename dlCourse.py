import os
import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from .dlChapter import getId, getIdO, dlVideo, dlAll, getCookie

cookie=sys.argv[1]
url=sys.argv[2]

dlAll(cookie,url)