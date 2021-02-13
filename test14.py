from bs4 import BeautifulSoup
import urllib.request as req
from urllib import parse
url = "%s" % "미리"
url = 'https://maplestory.nexon.com/Ranking/World/Guild?t=%d&n=' % (0) + parse.quote(url)
res = req.urlopen(url).read()
soup = BeautifulSoup(res, 'html.parser')
