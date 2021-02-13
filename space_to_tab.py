import os
files=os.listdir()
for i in files:
	print(i)
	if os.path.isdir(i):
		continue
	elif ".py" not in i:
		continue
	elif i=="space_to_tab.py":
		continue
	f=open(i,"r")
	data=f.readlines()
	f.close()
	new_data=[]
	for j in data:
		new_data.append(j.replace("    ","\t"))
	f=open(i,"w")
	for j in new_data:
		f.write(j)