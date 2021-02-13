from bs4 import BeautifulSoup
import urllib.request as req
from urllib import parse

url = "maple.gg/guild/%s/%s" % ("arcane", "미리")
url = 'http://' + parse.quote(url)
res = req.urlopen(url).read()
soup = BeautifulSoup(res, 'html.parser')
b = soup.select_one(
    "#app > div.card.mt-0 > div.card-header.guild-header > section > div.row.mb-4 > div.col-lg-8 > div "
    "> div:nth-child(1) > span > a")
if b:
    # 랭킹에서 아까 얻어온 길마를 토대로 길드를 확인합니다.
    master = b.text
    data3=[None for i in range(3)]
    for i in range(3):
        url = "%s" % "미리"
        url = 'https://maplestory.nexon.com/Ranking/World/Guild?t=%d&n='%(i) + parse.quote(url)
        res = req.urlopen(url).read()
        soup = BeautifulSoup(res, 'html.parser')
        data = "1"
        count = 1
        while data:
            data = soup.select_one(
                "#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr:nth-child(%d) > "
                "td:nth-child(4) > a > span" % count)
            if data:
                if data.text == master:
                    data2 = soup.select_one("#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr:nth-child(%d) > td:nth-child(5)"%count)
                    print(data2)
                    if data2:
                        data3[i]=data2.text
                    break
            count += 1