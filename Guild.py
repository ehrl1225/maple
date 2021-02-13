import up1
import up2
import up3
import up4
from urllib import parse
import urllib.request as req
from bs4 import BeautifulSoup
import os
import Member


class Guild:
    def __init__(self, data=None):
        self.up = None
        if data is None:
            self.name = None
            self.id = None
            self.account_type = None
            self.account = None
            self.password = None
            self.server = None
            self.position_name = ["길드 마스터", "부마스터", "길드원 1", "길드원 2", "길드원 3"]
            self.position_standard = None
            self.wid = None
            self.cadre = []
            self.member = []
            self.mercenary = []
            self.master = None
            self.reputation=None
            self.flag=None
            self.water_way=None

    def __getitem__(self, num):
        if type(num)==int:
            return self.member[num]
        elif num in self.member_names():
            return self.get_member(num)

    def __len__(self):
        return len(self.member)

    def get_member(self, name=None):
        data = []
        if name:
            for i in self.member:
                if i.name == name:
                    data.append(i)
        if len(data) == 0:
            return 0
        elif len(data) == 1:
            return data[0]
        else:
            return data

    def get_member_list(self):
        data = list()
        for i in self.member:
            data.append(i.get_list())
        return data

    def get_guild_list(self):
        data = []
        data.append(self.name)
        data.append(self.id)
        data.append(self.account_type)
        data.append(self.account)
        data.append(self.password)
        data.append(self.server)
        data.append(self.position_name)
        data.append(self.position_standard)
        data.append(self.wid)
        return data

    def set_data(self, data):
        # 노가다 귀찮음 나중에 할래
        # 다함
        if data[0]:
            self.name = data[0]
        if data[1]:
            self.id = int(data[1])
        if data[2]:
            self.account_type = int(data[2])
        if data[3]:
            self.account = data[3]
        if data[4]:
            self.password = data[4]
        if data[5]:
            self.server = data[5]
        if data[6]:
            self.position_name = data[6].split(":")
        if data[7]:
            self.position_standard = [i.split(":") for i in data[7].split(";")]
        if data[8]:
            self.wid = int(data[8])

    def sort_member(self):
        pass

    def member_names(self):
        name = [i.name for i in self.member]
        return name

    def get_guild_data(self, server, name):
        servers = ["루나 luna",
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
                   "리부트2 reboot2", ]
        for i in range(len(servers)):
            servers[i] = servers[i].split(" ")
        kor = []
        eng = []
        for i in servers:
            kor.append(i[0])
            eng.append(i[1])
        # a = input("서버")
        # a="아케인"
        if server not in eng:
            if server in kor:
                self.server = eng[kor.index(server)]
            else:
                self.server = None
        else:
            self.server = server
        # a = input("길드")
        #	a="미리"
        self.name = name

        if self.server != None:
            # 메이플 GG에서 길마 닉네임을 얻어옵니다.
            url = "maple.gg/guild/%s/%s" % (self.server, self.name)
            url = 'http://' + parse.quote(url)
            res = req.urlopen(url).read()
            soup = BeautifulSoup(res, 'html.parser')
            b = soup.select_one(
                "#app > div.card.mt-0 > div.card-header.guild-header > section > div.row.mb-4 > div.col-lg-8 > div "
                "> div:nth-child(1) > span > a")
            if b:
                # 랭킹에서 아까 얻어온 길마를 토대로 길드를 확인합니다.
                self.master = b.text
                url = "%s" % self.name
                url = 'https://maplestory.nexon.com/Ranking/World/Guild?t=1&n=' + parse.quote(url)
                res = req.urlopen(url).read()
                soup = BeautifulSoup(res, 'html.parser')
                data = "1"
                count = 1
                while data:
                    data = soup.select_one(
                        "#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr:nth-child(%d) > "
                        "td:nth-child(4) > a > span" % count)
                    if data.text == self.master:
                        break
                        count += 1

                if data != None:
                    data2 = soup.select_one(
                        "#container > div > div > div:nth-child(4) > div.rank_table_wrap > table > tbody > tr:nth-child(%d) > "
                        "td:nth-child(2) > span > a" % count)
                    guild_data = data2['href'].strip('/Common/Guild?gid=')
                    for i in range(len(guild_data)):
                        if guild_data[i] == "&":
                            self.id = int(guild_data[:i])
                            self.wid = int(guild_data[i:].split("=")[-1])
                            break
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def update(self, number):
        if number == 1:
            self.up = up1.up1(self)
        elif number == 2:
            self.up = up2.up2(self)
            state = self.up.get()
            if state!=0:
                return 0
        elif number == 3:
            self.up = up3.up3(self)
            state = self.up.get()
            if state!=0:
                return
        elif number == 4:
            self.up = up4.up4(self)
        if self.up:
            new = self.up.get_guild()
            for i in new:
                check = False
                for j in self.member:
                    if i.name == j.name:
                        check = True
                        j.set_data(i)
                if not check:
                    self.member.append(i)

    def update_all(self):
        [self.update(num) for num in range(1, 4)]
        self.update(4)

    def save_as_file(self, directory="data"):
        here = os.getcwd()
        if os.path.isdir(directory):
            os.chdir(directory)
        else:
            os.mkdir(directory)
            os.chdir(directory)
        data = self.get_guild_list()
        for i in range(len(data)):
            if data[i] is None:
                data[i] = ""

        text = ""
        for i in data[6]:
            text += str(i) + ':'
        data[6] = text.strip(":")
        text = ""
        for i in data[7]:
            text = text + i[0] + ':' + i[1] + ';'
        data[7]=text.strip(";")
        with open("guild.txt", 'w') as f:
            f.writelines([str(i) + '\n' for i in data])

        with open("member.txt", 'w') as f:
            data = self.get_member_list()
            for i in range(len(data)):
                line = ""
                for j in range(7):
                    line += str(data[i][j]) + ':'
                data[i] = line.strip(":") + '\n'
            f.writelines(data)
        os.chdir(here)

    def load_as_file(self, directory="data"):
        here = os.getcwd()
        if os.path.isdir(directory):
            os.chdir(directory)
            if os.path.isfile("guild.txt"):
                with open("guild.txt", 'r') as f:
                    data = [i.strip("\n") for i in f.readlines()]
                    for i in range(len(data)):
                        if data[i] =="":
                            data[i]=None
                    self.set_data(data)
            if os.path.isfile("member.txt"):
                member = []
                with open("member.txt", 'r') as f:
                    data = f.readlines()
                    for i in range(len(data)):
                        data[i] = data[i].strip('\n').split(':')
                        mb = Member.Member()
                        mb.set_data(data[i])
                        member.append(mb)
                self.member = member
        else:
            return
        os.chdir(here)

    def sort_guild(self, sort_type, up=True):
        if type(sort_type)==str:
            num = ["닉네임", "직위", "레벨", "직업", "무릉", "활동일", "기여도"].index(sort_type)
        elif type(sort_type)==int:
            num = sort_type
        max_num = len(self.member)
        for i in range(max_num-1):
            min_index=i
            for j in range(i,max_num):
                if self.member[j][num] is not None:
                    self.member[i], self.member[j]=self.member[j],self.member[i]
            if self.member[min_index][num] is None:
                continue
            for j in range(i + 1, max_num):
                if self.member[j][num] or self.member[j][num]==0:
                    if up:
                        if self.member[j].get_list()[num] < self.member[min_index].get_list()[num]:
                            min_index = j
                    elif not up:
                        if self.member[j].get_list()[num] > self.member[min_index].get_list()[num]:
                            min_index = j
            self.member[i], self.member[min_index] = self.member[min_index], self.member[i]






if __name__ == "__main__":
    import time
    guild = Guild()
    
    

