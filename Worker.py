from PyQt5.QtCore import QThread, pyqtSignal
from bs4 import BeautifulSoup
import urllib.request as req
from urllib import parse
from PyQt5.QtGui import QPixmap
from up1 import up1
from up2 import up2
from up3 import up3
from up4 import up4


class worker(QThread):
    finished = pyqtSignal(list)
    progress = pyqtSignal(list)

    def __init__(self, guild):
        super().__init__()
        self.guild = guild
        self.perpose = None
        self.name = None

    def run(self):
        if self.perpose == "update":
            self.guild.member = []
            # data=[]
            # up = up1(self.guild)
            # for i in up.get_guild():
            #     data.append(i)
            # self.progress.emit(data)
            # data=[]
            # up = up2(self.guild)
            # up.get()
            # for i in up.get_guild():
            #     data.append(i)
            # self.progress.emit(data)
            # data=[]
            # up = up3(self.guild)
            # up.get()
            # for i in up.get_guild():
            #     data.append(i)
            # self.progress.emit(data)

            # up = up4(self.guild)
            # for i in up.get_guild():
            #     print(i)
            #     data.append(i)
            # self.progress.emit(data)

            for i in range(1,4):
                self.guild.update(i)
                self.progress.emit([])
            self.guild.update(4)
            self.progress.emit([])


            self.finished.emit([])

        elif self.perpose == "img":
            url = "maple.gg/u/%s" % self.name
            url = 'http://' + parse.quote(url)
            res = req.urlopen(url).read()
            soup = BeautifulSoup(res, 'html.parser')
            p = soup.select_one(
                "#user-profile > section > div > div.col-lg-4.pt-1.pt-sm-0.pb-1.pb-sm-0.text-center.mt-2.mt-lg-0 > "
                "div > div.col-6.col-md-8.col-lg-6 > img")
            if p:
                image = req.urlopen(p.get('src')).read()
                pixmap = QPixmap()
                pixmap.loadFromData(image)
                self.finished.emit([pixmap])

        elif self.perpose == "guild_info":
            url = "maple.gg/guild/%s/%s" % (self.guild.server, self.guild.name)
            url = 'http://' + parse.quote(url)
            res = req.urlopen(url).read()
            soup = BeautifulSoup(res, 'html.parser')
            b = soup.select_one(
                "#app > div.card.mt-0 > div.card-header.guild-header > section > div.row.mb-4 > div.col-lg-8 > div "
                "> div:nth-child(1) > span > a")
            servers = ["전체월드", "리부트2", "리부트", "오로라", "레드", "이노시스", "유니온", "스카니아", "루나", "제니스", "크로아", "베라", "엘리시움",
                       "아케인", "노바"]
            server_kor_eng = ["루나 luna",
                              "스카니아 scania",
                              "엘리시움 elysium",
                              "크로아 croa",
                              "오로라 aurora",
                              "베라 bera",
                              "레드 red",
                              "유니온 union",
                              "제니스 zenith",
                              "이노시스 enosis",
                              "아케인 arcane",
                              "노바 nova",
                              "리부트 reboot",
                              "리부트2 reboot2"]
            server_kor_eng = [i.split(' ') for i in server_kor_eng]

            if b:
                # 랭킹에서 아까 얻어온 길마를 토대로 길드를 확인합니다.
                self.guild.master = b.text
                data3 = [None for i in range(6)]
                for i in range(3):
                    url = "%s" % self.guild.name
                    url = 'https://maplestory.nexon.com/Ranking/World/Guild?t=%d&n=' % (i) + parse.quote(url)
                    res = req.urlopen(url).read()
                    soup = BeautifulSoup(res, 'html.parser')
                    data = "1"
                    count = 1
                    while data:
                        data = soup.select_one(
                            "#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr:nth-child(%d) > "
                            "td:nth-child(4) > a > span" % count)
                        if data:
                            if data.text == self.guild.master:
                                data2 = soup.select_one(
                                    "#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr:nth-child(%d) > td:nth-child(5)" % count)
                                if data2:
                                    data3[i] = data2.text
                                break
                        count += 1
                    count = 1
                    server_kor=None
                    for j in range(len(server_kor_eng)):
                        if server_kor_eng[j][1] == self.guild.server:
                            server_kor = server_kor_eng[j][0]
                    server_id = servers.index(server_kor)
                    url = "https://maplestory.nexon.com/Ranking/World/Guild?page=%d&w=%d&t=%d" % (
                        count, server_id, i)
                    res = req.urlopen(url).read()
                    soup = BeautifulSoup(res, 'html.parser')

                    for j in range(10):
                        print(j)
                        data4 = soup.select_one(
                            "#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > "
                            "tr:nth-child(%d) > td:nth-child(4) > a > span" % (j))
                        if data4:
                            if str(data4.text) == self.guild.master:
                                data3[i + 3] = (count - 1) * 10 + j
                                break
                        else:
                            break
                    if data3[i+3]:
                        break
                    if data3[i] is None:
                        break

                self.guild.reputation = data3[1]
                self.guild.flag = data3[0]
                self.guild.water_way = data3[2]
                self.finished.emit(data3)
