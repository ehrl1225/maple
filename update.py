import os

import chromedriver_autoinstaller
import urllib3.exceptions
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
import urllib.request as req
from urllib import parse
import Member


class up1:

    def __init__(self, guild):
        self.guild_id = guild.id
        self.guild_wid = guild.wid
        self.position_standard = guild.position_standard
        self.soup = None

    def get_guild(self):
        if self.guild_id is None or self.guild_wid is None:
            return
        guild = []
        for j in range(1, 6):
            page = j
            url = "https://maplestory.nexon.com/Common/Guild?gid=%d&wid=%d&orderby=1&page=%d"
            res = req.urlopen(url % (self.guild_id, self.guild_wid, page)).read()
            self.soup = BeautifulSoup(res, 'html.parser')
            a = []
            p = self.soup.findChildren("td")
            if p != None:
                for i in range(len(p)):
                    if (i % 5) == 1:
                        a.append(p[i].text.strip("\n").split("\n")[0])
                    if (i % 5) == 2:
                        a.append(p[i].text.strip("\n"))
                for i in range(int(len(a) / 2)):
                    mb = Member.Member()
                    mb.name = a[i * 2]
                    mb.level = a[i * 2 + 1]
                    guild.append(mb)
            if a == []:
                break

        po = [1, 1, 0, 0, 0]
        lv = guild[1].level
        count = 1

        for i in guild[2:]:
            if lv < i.level:
                count += 1
            else:
                po[count] += 1
            lv = i.level
        if 0 in po:
            if self.position_standard == None:
                return guild
            else:
                for i in self.position_standard:
                    for j in guild:
                        if i.name == j.name:
                            j.position_id = i.position_id
                for i in range(1, len(guild)):
                    if guild[i] == None:
                        guild[i].position_id = guild[i - 1].position_id
                po = [0, 0, 0, 0, 0]
                for i in guild:
                    po[i.position_id] += 1
                if 0 not in po:
                    return guild
                else:
                    for i in guild:
                        i.position_id = None
                    return guild
        else:
            for i in range(5):
                if i == 0:
                    guild[0].position_id = i
                elif i == 4:
                    for j in range(po[i], len(guild)):
                        guild[j].position_id = i
                else:
                    for j in range(po[i], po[i + 1]):
                        guild[j].position_id = i
            return guild
        return 0


class up2:

    def __init__(self, guild):
        self.account_type = guild.account_type
        self.account = guild.account
        self.password = guild.password
        self.soup = None

    def get(self):
        try:
            if not os.path.isdir("chrome"):
                os.mkdir("chrome")
            os.chdir("chrome")
            file = chromedriver_autoinstaller.install(True)
            os.chdir("")
            # webdirver옵션에서 headless기능을 사용하겠다 라는 내용
            webdriver_options = webdriver.ChromeOptions()
            webdriver_options.add_argument('headless')
            driver = webdriver.Chrome(file, options=webdriver_options)
            # driver = webdriver.Chrome(file)
            driver.get("https://maplestory.nexon.com/Authentication/Login#a")
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, 'eid'))
                )

            finally:
                if self.account_type == 0:
                    try:
                        element = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.ID, 'eid'))
                        )

                    finally:
                        element.send_keys(self.account)
                        element = driver.find_element_by_id("epw")
                        element.send_keys(self.password)

                elif self.account_type == 1:
                    xpath = "//*[@id='wrap']/div[3]/div/div[1]/ul/li[2]/a/img"
                    driver.find_element_by_xpath(xpath).click()
                    try:
                        element = WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.ID, 'mid'))
                        )

                    finally:
                        element.send_keys(self.account)
                        element = driver.find_element_by_id("mpw")
                        element.send_keys(self.password)
                else:
                    driver.quit()
                    return -5

            xpath = "//*[@id='wrap']/div[3]/div/div[2]/div[3]/a/img"
            driver.find_element_by_xpath(xpath).click()
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="gnbMyInfo"]/a/span[1]'))
                )
            except TimeoutException:
                driver.quit()
                return -3

            if driver.current_url == "https://maplestory.nexon.com/Authentication/Login#a":
                driver.quit()
                return -3
            else:
                driver.get("https://maplestory.nexon.com/MyMaple/Profile")

            xpath = "//*[@id='container']/div/div/div/div[1]/div[2]/a/img"
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )

            finally:
                driver.find_element_by_xpath(xpath).click()
            try:
                driver.switch_to.window(driver.window_handles[1])

            except:
                if driver.current_url == "https://maplestory.nexon.com/MyMaple/Profile":
                    driver.quit()
                    return -4

            xpath = "//*[@id='wrap']/div[2]/div[1]/span[1]/a/img"
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )

            finally:
                driver.find_element_by_xpath(xpath).click()

            xpath = "//*[@id='container']/div[2]/div[2]/div/div[1]/ul/li[2]/a/img"
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )

            finally:
                driver.find_element_by_xpath(xpath).click()
            xpath = "//*[@id='container']/div[2]/div[2]/div/div[2]/div[1]/ul/li[4]/a/img"
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )

            finally:
                html = driver.page_source

            driver.quit()
            self.soup = BeautifulSoup(html, 'html.parser')
        except SessionNotCreatedException:
            driver.quit()
            return -1
        except urllib3.exceptions.ProtocolError:
            driver.quit()
            return -2
        except WebDriverException:
            driver.quit()
            return -1
        return 0

    def get_guild(self):
        notice = self.soup.findChildren("ul")
        a = []
        if notice is not None:
            guild = []
            for i in notice[-1].text.split("\n"):
                if i != "":
                    a.append(i)
            for i in range(len(a)):
                if i % 2 == 1:
                    a[i] = a[i].split("기여도 ")[1]
            for i in range(int(len(a) / 2)):
                mb = Member.Member()
                mb.name = a[i * 2]
                mb.contribution = a[i * 2 + 1]
                guild.append(mb)
        return guild


# 이상함 어디선가 버그가 발생하는데 이유는 못찾겠고 대부분의 상황에서 작동함
class up3:
    def __init__(self, guild):
        self.soup = None
        self.name = guild.name
        self.server = guild.server

    def get(self):
        try:
            if not os.path.isdir("chrome"):
                os.mkdir("chrome")
            os.chdir("chrome")
            file = chromedriver_autoinstaller.install(True)
            os.chdir("")
            # webdirver옵션에서 headless기능을 사용하겠다 라는 내용
            webdriver_options = webdriver.ChromeOptions()
            webdriver_options.add_argument('headless')
            driver = webdriver.Chrome(file, options=webdriver_options)
            url = "maple.gg/guild/%s/%s" % (self.server, self.name)
            url = 'http://' + parse.quote(url)
            driver.get(url)
            xpath = "//*[@id='guild-content']/section/div[1]/div[1]/section/div[2]/div/div[1]/b/a"
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )

            finally:
                html = driver.page_source
            driver.quit()
            self.soup = BeautifulSoup(html, 'html.parser')

        except SessionNotCreatedException:
            print("error")
            return -1
        except urllib3.exceptions.ProtocolError:
            print("error")
            return -2
        except TimeoutException:
            print("error")
            return -3
        return 0

    def get_guild(self):
        data = self.soup.findChildren("div")
        a = []
        for i in data[0].text.split("\n"):
            if i != "":
                a.append(i)
        b = []
        for i in range(len(a)):
            if "마지막 활동일" in a[i]:
                b.append([a[i - 2], a[i - 1], a[i]])
        b = b[3:]
        for i in range(len(b)):
            b[i][1] = b[i][1].split("/")[0]
            b[i][2] = b[i][2].split(": ")[1]
        guild = []
        for i in b:
            mb = Member.Member()
            mb.name = i[0]
            mb.job = i[1]
            mb.activity = i[2]
            guild.append(mb)

        return guild


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


class update:
    def __init__(self, guild):
        self.guild_id = guild.id
        self.guild_wid = guild.wid
        self.position_standard = guild.position_standard
        self.name = guild.name
        self.server = guild.server
        self.account_type = guild.account_type
        self.account = guild.account
        self.password = guild.password
        self.member = guild.member
        self.soup = None
