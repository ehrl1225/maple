from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from selenium.common.exceptions import *
import urllib3.exceptions
import os
import Member


class up2:

	def __init__(self, guild):
		self.account_type=guild.account_type
		self.account=guild.account
		self.password=guild.password
		self.soup = None
		self.driver=None

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
			self.driver = webdriver.Chrome(file, options=webdriver_options)
			#driver = webdriver.Chrome(file)
			self.driver.get("https://maplestory.nexon.com/Authentication/Login#a")
			try:
				element = WebDriverWait(self.driver, 5).until(
					EC.presence_of_element_located((By.ID, 'eid'))
				)

			finally:
				if self.account_type == 0:
					try:
						element = WebDriverWait(self.driver, 20).until(
							EC.presence_of_element_located((By.ID, 'eid'))
						)

					finally:
						element.send_keys(self.account)
						element = self.driver.find_element_by_id("epw")
						element.send_keys(self.password)

				elif self.account_type == 1:
					xpath = "//*[@id='wrap']/div[3]/div/div[1]/ul/li[2]/a/img"
					self.driver.find_element_by_xpath(xpath).click()
					try:
						element = WebDriverWait(self.driver, 20).until(
							EC.presence_of_element_located((By.ID, 'mid'))
						)

					finally:
						element.send_keys(self.account)
						element = self.driver.find_element_by_id("mpw")
						element.send_keys(self.password)
				else:
					self.driver.quit()
					return -5

			xpath = "//*[@id='wrap']/div[3]/div/div[2]/div[3]/a/img"
			self.driver.find_element_by_xpath(xpath).click()
			try:
				element = WebDriverWait(self.driver, 20).until(
					EC.element_to_be_clickable((By.XPATH, '//*[@id="gnbMyInfo"]/a/span[1]'))
				)
			except TimeoutException:
				self.driver.quit()
				return -3

			if self.driver.current_url == "https://maplestory.nexon.com/Authentication/Login#a":
				self.driver.quit()
				return -3
			else:
				self.driver.get("https://maplestory.nexon.com/MyMaple/Profile")

			xpath = "//*[@id='container']/div/div/div/div[1]/div[2]/a/img"
			try:
				element = WebDriverWait(self.driver, 10).until(
					EC.element_to_be_clickable((By.XPATH, xpath))
				)

			finally:
				self.driver.find_element_by_xpath(xpath).click()
			try:
				self.driver.switch_to.window(self.driver.window_handles[1])

			except:
				if self.driver.current_url == "https://maplestory.nexon.com/MyMaple/Profile":
					self.driver.quit()
					return -4

			xpath = "//*[@id='wrap']/div[2]/div[1]/span[1]/a/img"
			try:
				element = WebDriverWait(self.driver, 20).until(
					EC.element_to_be_clickable((By.XPATH, xpath))
				)

			finally:
				self.driver.find_element_by_xpath(xpath).click()

			xpath = "//*[@id='container']/div[2]/div[2]/div/div[1]/ul/li[2]/a/img"
			try:
				element = WebDriverWait(self.driver, 20).until(
					EC.element_to_be_clickable((By.XPATH, xpath))
				)

			finally:
				self.driver.find_element_by_xpath(xpath).click()
			xpath = "//*[@id='container']/div[2]/div[2]/div/div[2]/div[1]/ul/li[4]/a/img"
			try:
				element = WebDriverWait(self.driver, 20).until(
					EC.element_to_be_clickable((By.XPATH, xpath))
				)

			finally:
				html = self.driver.page_source

			self.driver.quit()
			self.soup = BeautifulSoup(html, 'html.parser')
		except SessionNotCreatedException:
			self.driver.quit()
			return -1
		except urllib3.exceptions.ProtocolError:
			self.driver.quit()
			return -2
		except WebDriverException:
			self.driver.quit()
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
				mb=Member.Member()
				mb.name=a[i*2]
				mb.contribution=int(a[i*2+1])
				guild.append(mb)
		return guild