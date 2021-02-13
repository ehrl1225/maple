import multiprocessing

from Guild import Guild
import up1
import up2
import up3
import up4

guild = Guild()

def update(number):
    print(number)
    if number == 1:
        up = up1.up1(guild)
    elif number == 2:
        up = up2.up2(guild)
        up.get()
    elif number == 3:
        up = up3.up3(guild)
        if up.get()<0:
            return
    elif number == 4:
        up = up4.up4(guild)
    new = up.get_guild()
    if new:
        for i in new:
            check = False
            for j in guild.member:
                if i.name == j.name:
                    check = True
                    j.set_data(i)
            if not check:
                guild.member.append(i)

if __name__=="__main__":
    guild.get_guild_data('arcane','미리')

    guild.account_type=0
    guild.account="ehrl1225@daum.net"
    guild.password="happy0506!@#~"
    pool= multiprocessing.Pool(processes=3)
    pool.map(update,[num for num in range(1,4)])
    pool.close()
    pool.join()
    for i in guild.get_member():
        print(i.get_list())