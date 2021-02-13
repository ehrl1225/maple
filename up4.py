from bs4 import BeautifulSoup
import urllib.request as req
from urllib import parse
import multiprocessing
import Member


class up4:
    def __init__(self, guild):
        self.member = guild.member_names()

    def get(self, name):
        url = "maple.gg/u/%s" % name
        url = 'http://' + parse.quote(url)
        res = req.urlopen(url).read()
        soup = BeautifulSoup(res, 'html.parser')

        notice = soup.select(
            "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div "
            "> div > div > h1")
        mb=Member.Member()
        mb.name=name
        if notice:
            mb.mureung=int(notice[0].text.split("\n")[0])
            return mb
        elif notice == []:
            return mb
        else:
            return mb


    def get_guild(self):
        pool=multiprocessing.Pool(processes=multiprocessing.cpu_count())
        data=pool.map(self.get,tuple(self.member))
        pool.close()
        pool.join()

        return data