

class skill:

    def __init__(self):
        self.job=None
        self.name=None
        self.apply_type=None
        self.apply_range=None
        self.kinds=None
        self.effect=None
        self.duration=None
        self.cooltime=None
        self.etc=None

if __name__ == '__main__':
    data=[]
    with open("skill2.txt","r",encoding='UTF8') as f:
        [data.append(i.strip("\n")) for i in f.readlines()]

    for i in data:
        if i!="":
            print(i)