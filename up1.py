from bs4 import BeautifulSoup
import urllib.request as req
import Member

class up1:

	def __init__(self, guild):
		self.guild_id = guild.id
		self.guild_wid = guild.wid
		self.position_standard=guild.position_standard
		self.soup = None

	def get_guild(self):
		if self.guild_id is None or self.guild_wid is None:
			return
		guild=[]
		for j in range(1,14):
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
					mb=Member.Member()
					mb.name=a[i*2]
					mb.level=int(a[i*2+1].strip("Lv."))
					guild.append(mb)
			if a==[]:
				break
				
		if self.position_standard:
			for i in self.position_standard:
				for j in guild:
					if j.name == i[0]:
						j.position_id = i[1]
			for i in range(1,len(guild)):
				if guild[i-1].position_id:
					guild[i].position_id=guild[i-1].position_id
			return guild
		else:
			guild[0].position_id=0
			guild[1].position_id=1
			po=[1,1,0,0,0]
			for i in range(2,len(guild[2:])+2):
				if guild[i].level > guild[i-1].level:
					guild[i].position_id=guild[i-1].position_id+1
				else:
					guild[i].position_id = guild[i-1].position_id
				po[guild[i].position_id] += 1
			if 0 in po:
				for i in range(len(guild)):
					guild[i].position_id=None
			return guild

if __name__=="__main__":
	from Guild import Guild
	guild = Guild()
	guild.name="미리"
	guild.server="arcane"
	guild.get_guild_data(guild.server, guild.name)
	up = up1(guild)
	data = up.get_guild()

