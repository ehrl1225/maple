from bs4 import BeautifulSoup
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from selenium.common.exceptions import *
import urllib3.exceptions
import os
import Member

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
			os.chdir("..")
			# webdirver옵션에서 headless기능을 사용하겠다 라는 내용
			webdriver_options = webdriver.ChromeOptions()
			webdriver_options .add_argument('headless')
			driver = webdriver.Chrome(file, options=webdriver_options)
			url = "maple.gg/guild/%s/%s" % (self.server, self.name)
			url = 'http://' + parse.quote(url)
			driver.get(url)
			xpath = "//*[@id='guild-content']/section/div[1]/div[1]/section/div[2]/div/div[1]/b/a"
			try:
				element = WebDriverWait(driver, 20).until(
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
			mb=Member.Member()
			mb.name=i[0]
			mb.job=i[1]
			mb.activity=int(i[2].strip("일 전"))
			guild.append(mb)

		return guild
