from bs4 import BeautifulSoup
import urllib.request as req
from urllib import parse
import Member


class up4:

    def __init__(self, guild):
        self.member = guild.member

    def get_guild(self):
        guild = []
        for i in self.member:
            url = "maple.gg/u/%s" % i.name
            url = 'http://' + parse.quote(url)
            res = req.urlopen(url).read()
            soup = BeautifulSoup(res, 'html.parser')

            notice = soup.select(
                "#app > div.card.border-bottom-0 > div > section > div.row.text-center > div:nth-child(1) > section > div "
                "> div > div > h1")
            if notice:
                mb = Member.Member()
                mb.mureung = notice[0].text.split("\n")[0]
                guild.append(mb)
            elif notice == []:
                pass
            else:
                pass
        return guild

