

class Member:
	def __init__(self, data=None):
		if data is None:
			self.name=None
			self.position_id=None
			self.position_name=["길드 마스터","부마스터", "길드원 1", "길드원 2", "길드원 3"]
			self.level=None
			self.job=None
			self.mureung=None
			self.activity=None
			self.contribution=None

	def __getitem__(self, item):
		if type(item)==int:
			return self.get_list()[item]

	def get_list(self):
		data=list()
		data.append(self.name)
		data.append(self.position_id)
		data.append(self.level)
		data.append(self.job)
		data.append(self.mureung)
		data.append(self.activity)
		data.append(self.contribution)
		return data
	
	def set_data(self, data):
		if type(data)==Member:
			if data.name:
				self.name=data.name
			if data.position_id is not None:
				self.position_id=data.position_id
			if data.level:
				self.level=data.level
			if data.job:
				self.job=data.job
			if data.mureung:
				self.mureung=data.mureung
			if data.activity:
				self.activity=data.activity
			if data.contribution:
				self.contribution=data.contribution
		elif type(data)==list:
			self.name=data[0]
			if data[1].isdecimal():
				self.position_id=int(data[1])
			if data[2].isdecimal():
				self.level=int(data[2])
			self.job=data[3]
			if data[4].isdecimal():
				self.mureung=int(data[4])
			if data[5].isdecimal():
				self.activity=int(data[5])
			if data[6].isdecimal():
				self.contribution=int(data[6])
			
	def utility(self):
		pass
		