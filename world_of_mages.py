import random
import sys
import os
import re
import time
import pathlib


class Mage:
    def __init__(self, typ, weapon, name="Morgan"):
        self.name = name
        self.typ = typ
        self.weapon = weapon

    def postac(self):
        print("Your name is " + self.name + " you are a " + self.typ+" aspect mage " + ",user of " + self.weapon)


class Things:
    def __init__(self, robe="Basic Robe", ring1="Basic Ring", ring2="Basic Ring", necklace="Basic Necklace", gold=100,
                 potion=0, tier1=0, tier2=0, tier3=0):
        self.robe = robe
        self.ring1 = ring1
        self.ring2 = ring2
        self.necklace = necklace
        self.gold = gold
        self.potion = potion
        self.tier1 = tier1
        self.tier2 = tier2
        self.tier3 = tier3

    def eqw(self):
        print("Robe: " + self.robe+"\nRing1: " + self.ring1+"\nRing2: " + self.ring2+"\nNecklace: " + self.necklace +
              "\nGold: " + str(self.gold)+"\nPotion: " + str(self.potion))

    def save(self):
        with open("config/eq.txt", "w") as THREE:
            THREE.write(
                "{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}".format(self.robe, self.ring1, self.ring2, self.necklace,
                                                                     str(self.gold), str(self.potion), str(self.tier1),
                                                                     str(self.tier2), str(self.tier3)))


class Stat:
    basehp = 10
    basearmor = 5
    baseap = 2
    mana = 10

    def __init__(self, hp=0, armor=0, ap=0, mana=0):
        self.hp = hp + Stat.basehp
        self.armor = armor + Stat.basearmor
        self.ap = ap + Stat.baseap
        self.mana = mana + Stat.mana

    def __add__(self, drugi):
        return self.hp+drugi.hp, self.armor + drugi.armor, self.ap+drugi.ap, self.mana+drugi.mana


class ChrStat:
    def __init__(self, hp, armor, ap, mana=0):
        self.hp = hp
        self.armor = armor
        self.ap = ap
        self.mana = mana

    def actuallystat(self):
        print("HP: {0}\nARMOR:{1}\nAP: {2}\nMana: {3}".format(self.hp, self.armor, self.ap, self.mana))


class Spells:
    def __init__(self, ac, apu, manac, name):
        self.ac = ac
        self.apu = apu
        self.manac = manac
        self.name = name


def start():
    if os.stat("config/character.txt").st_size == 0:
        print("#####################################")
        p = pathlib.Path("config/czy.txt")
        with open(p, "w") as czy:
            czy.write(str(1))
        elem = ["wind", "fire", "water", "earth"]
        weap = ["small wand", "big wand", "catalyst"]
        print("Welcome in the world of Mages")
        print("1-creative your character")
        print("2-Randomize your character")
        print("3-Exit game")
        choice = input()
        if choice == "1":
            print("select your element")
            print("1-wind\n2-fire\n3-water\n4-earth")
            element = input()
            element = elem[int(element)-1]
            print("Create your Name")
            name = input()
            print("select your weapon")
            print("1-small wand:high cast speed,low damage\n"
                  "2-big wand:low cast speed,big damage\n3-catalyst: medium cast speed and damage")
            weapon = input()
            weapon = weap[int(weapon)-1]
            character = Mage(element, weapon, name)
            character.postac()
            p = pathlib.Path("config/character.txt")
            with open(p, "w") as static:
                static.write(name+"\n"+element+"\n"+weapon+"\n")
            print("1-to continue")
            tak = input()
            if tak == "1":
                p = pathlib.Path("config/character.txt")
                with open(p, "w") as static:
                    static.write(character.name + "\n" + element + "\n" + weapon + "\n")

                eq = Things()
                eq.save()
                daily_shop()
                main()
        elif choice == "2":
            def randcha():
                element = random.choice(elem)
                weapon = random.choice(weap)
                character = Mage(element, weapon)
                character.postac()
                print("Do you wanna roll again?")
                print("1-Yes\n2-No")
                czy = input()
                if czy == "1":
                    randcha()
                else:
                    p = pathlib.Path("config/character.txt")
                    with open(p, "w") as static:
                        static.write(character.name + "\n" + element + "\n" + weapon + "\n")
                    eq = Things()
                    daily_shop()
                    eq.save()
            randcha()
            main()
        elif choice == "3":
            sys.exit()
    else:
        main()


def main():
    print("#####################################")
    tab = []
    tab2 = []
    p = pathlib.Path("config/character.txt")
    with open(p, "r") as char:
        char = char.readlines()
        for _ in char:
            tab.append(_.strip())
    character = Mage(tab[1], tab[2], tab[0])
    p = pathlib.Path("config/eq.txt")
    with open(p, "r") as ek:
        ek = ek.readlines()
        for _ in ek:
            tab2.append(_.strip())
    eq = Things(tab2[0], tab2[1], tab2[2], tab2[3], int(tab2[4]),
                int(tab2[5]), int(tab2[6]), int(tab2[7]), int(tab2[8]))
    sta = items_stat(eq.robe, eq.ring1, eq.ring2, eq.necklace)
    stats = ChrStat(sta[0], sta[1], sta[2], sta[3])
    print("1-Go to dungeon\n2-Go to shop\n3-Go to magic tower\n4-Go to tavern\n" 
          "5-Go begging for money on the street\n6-My character\n7-Exit and save game")
    what = input()
    if what == "1":
        czy = open("config/czy.txt", "r+")
        if czy.read() != "1":
            print("You are to exhausted to fight")
            czy.close()
            main()
        else:
            czy.write("0")
            czy.close()
            global maxhp
            global maxmp
            global deep
            maxhp = stats.hp
            maxmp = stats.mana
            deep = 0
            dungeon(eq, character, stats)
    elif what == "2":
        shop1(eq)
    elif what == "3":
        magic_tower(character, eq)
    elif what == "4":
        tavern(eq)
    elif what == "5":
        begging(eq)
    elif what == "6":
        print("#####################################")
        character.postac()
        eq.eqw()
        stats.actuallystat()
        main()
    elif what == "7":
        sys.exit()


def dungeon(eq, character, stats):
    global maxhp
    global maxmp
    global deep
    deep += 1
    print("#####################################")
    print("your hp: "+str(stats.hp)+"/{0}".format(maxhp))
    print("Your mana: "+str(stats.mana)+"/{0}".format(maxmp))
    print("Your hp potion: {0}".format(eq.potion))

    print("1-Go ahead")
    print("2-Use hp potion")
    print("3-Rest")
    print("4-Run")
    co = input()
    if co == "1":
        loot = random.randint(0, 300)
        if loot < 10*deep:
            what = random.randint(1, 6)
            if what != 6:
                g = random.randint(1, 10)*deep
                print("You find {0} gold!!".format(g))
                time.sleep(1)
                eq.gold += g
                eq.save()
                dungeon(eq, character, stats)
            else:
                print("You find hp potion!")
                time.sleep(1)
                eq.potion += 1
                eq.save()
                dungeon(eq, character, stats)
        else:
            battle(eq, character, stats)
    elif co == "2":
        if eq.potion > 0:
            print("#####################################")
            print("You use your hp potion! + 25 hp")
            time.sleep(1)
            stats.hp += 25
            eq.potion -= 1
            if stats.hp > maxhp:
                stats.hp = maxhp
            dungeon(eq, character, stats)
        else:
            print("#####################################")
            print("You dont have hp potion")
            time.sleep(1)
            dungeon(eq, character, stats)
    elif co == "3":
        sa = random.randint(1, 10)
        if sa < 9:
            print("You rest a little")
            print("mana +10")
            time.sleep(1)
            stats.mana += 10
            if stats.mana > maxmp:
                stats.mana = maxmp
            dungeon(eq, character, stats)
        else:
            print("You are under attack!!")
            time.sleep(1)
            battle(eq, character, stats)
    elif co == "4":
        eq.save()
        main()


def battle(eq, character, stats):
    global maxhp
    global maxmp
    global deep
    goblin = ChrStat(15, 0.90, 1)
    hobgoblin = ChrStat(40, 0.70, 2)
    kingoblin = ChrStat(100, 0.50, 3)
    spe = spell_stat(eq, character)
    dic = {}
    for _ in range(len(spe)):
        dic[spe[_]] = _ + 1
    enemy = random.randint(0, 100)*deep
    weapons = [["small wand", 60, 0.30], ["big wand", 40, 0.75], ["catalyst", 50, 0.50]]

    en = [goblin, hobgoblin, kingoblin]
    if enemy > 900:
        enn = en[2]
        name = "King Goblin"
    elif enemy > 600:
        enn = en[1]
        name = "Hob Goblin"
    else:
        enn = en[0]
        name = "goblin"
    print("#####################################")
    time.sleep(1)
    print("You meet {0}!!".format(name))
    time.sleep(0.5)
    for _ in range(len(weapons)):
        if re.match(character.weapon, weapons[_][0]):
            while enn.hp > 0 and stats.hp > 0:
                ile = 0
                who = random.randint(1, 100)
                if who > weapons[_][1]:
                    dmg_get = (random.randint(3, 7) * enn.ap) * (100 - stats.armor) / 100
                    dmg_get = int(round(dmg_get, 0))
                    stats.hp -= dmg_get
                    print("{0} is faster than you".format(name))
                    time.sleep(1)
                    print("He deals you {0} dmg".format(dmg_get))
                    time.sleep(1)
                else:
                    print("#####################################")
                    print("You are faster than {0}.".format(name))
                    print("your hp: " + str(stats.hp) + "/{0}".format(maxhp))
                    print("Your mana: " + str(stats.mana) + "/{0}".format(maxmp))
                    print("Your hp potion: {0}".format(eq.potion))
                    print("hoblin hp: {0}".format(enn.hp))
                    time.sleep(1)
                    for b in range(len(spe)):
                        ile += 1
                        spell = spe[b]
                        print("{0}-Use {1} Spell: {2}-Accuraty {3}-Mana cost".format
                              (ile, spell.name, spell.ac, spell.manac))
                    ile += 1
                    pot = ile
                    print("{0}-Use hp potion".format(ile))
                    ile += 1
                    print("{0}-Run".format(ile))
                    run = ile
                    co = input()
                    if co == str(pot):
                        if eq.potion > 0:
                            print("#####################################")
                            print("You use your hp potion! + 25 hp")
                            time.sleep(1)

                            stats.hp += 25
                            eq.potion -= 1
                            if stats.hp > maxhp:
                                stats.hp = maxhp
                        else:
                            print("#####################################")
                            print("You trying to pick potion from your bag")
                            print("unfortunately you dont have any hp potion")
                            print("You missed your tour")
                            time.sleep(1)
                    elif co == str(run):
                        czy = random.randint(0, 10)
                        if czy > 9:

                            print("You failed")
                            time.sleep(1)

                        else:
                            print("You run successfully")
                            time.sleep(1)
                            main()
                    else:
                        lic = - 1
                        for c in dic.keys():
                            lic += 1
                            if co == str(dic[c]):
                                us = spe[lic]
                                dmg = weapons[lic][2] * us.apu * stats.ap * 10 * enn.armor
                                dmg = int(round(dmg, 0))
                                cel = random.randint(1, 100)
                                if us.ac < cel:
                                    print("You missed")
                                    time.sleep(1)
                                    stats.mana -= us.manac
                                    if stats.mana < 0:
                                        stats.mana = 0
                                elif us.manac > stats.mana:
                                    print("#####################################")
                                    print("You are trying to cast a spell")
                                    print("unfortunately you dont have enoght mana")
                                    print("You missed your tour")
                                    time.sleep(1)
                                else:
                                    print("You hit {0} dmg".format(dmg))
                                    enn.hp -= dmg
                                    stats.mana -= us.manac
                                    if stats.mana < 0:
                                        stats.mana = 0
                                        print("#####################################")
                                        time.sleep(1)
    if stats.hp <= 0:
        time.sleep(1)
        print("#####################################")
        print("You died")
        print("You lost all gold and potions")
        time.sleep(1)
        eq.gold = 0
        eq.potion = 0
        eq.save()
        main()
    elif goblin.hp <= 0:
        time.sleep(1)
        print("#####################################")
        print("You defeat a monster!!")
        what = random.randint(1, 6)
        if what != 6:
            time.sleep(1)
            g = random.randint(1, 15) * deep
            print("You find {0} gold!!".format(g))
            eq.gold += g
            eq.save()
            dungeon(eq, character, stats)
        else:
            time.sleep(1)
            print("You find hp potion!")
            eq.potion += 1
            eq.save()
            dungeon(eq, character, stats)


def magic_tower(character, eq):
    def bought(eq, character):
        print("You bought a new spell")
        time.sleep(1)
        eq.save()
        magic_tower(character, eq)
    print("#####################################")
    print("Welcome in magic tower")
    print("1-Buy hp potion 20g")
    ile = 2
    windspells = ["Airball", "Call the Wind", "Rain Storm"]
    firespells = ["Fireball", "Call the Fire", "Inferno"]
    waterspells = ["Waterball", "Call the Water", "Tsunami"]
    earthspells = ["Earthball", "Call the Earth", "Earthquake"]
    typs = {"wind": windspells, "fire": firespells, "water": waterspells, "earth": earthspells}
    slo = {}

    for _ in typs.keys():
        if character.typ == _:
            tr = 0
            if eq.tier1 == 0:
                print('{0}-Learn "{1}" spell 150g'.format(str(ile), typs[_][tr]))
                slo[typs[_][tr]] = 150
                ile += 1
            tr += 1
            if eq.tier2 == 0:
                print('{0}-Learn "{1}" spell 300g'.format(str(ile), typs[_][tr]))
                ile += 1
                slo[typs[_][tr]] = 300
            tr += 1
            if eq.tier3 == 0:
                print('{0}-Learn "{1}" spell 500g'.format(str(ile), typs[_][tr]))
                slo[typs[_][tr]] = 500
                ile += 1
    print("{0}-Exit".format(ile))
    co = input()
    if co == "1":
        print("How much?")
        ile = input()
        if eq.gold >= 20 * int(ile):
            eq.potion += int(ile)
            eq.gold -= 20 * int(ile)
            eq.save()
            magic_tower(character, eq)
        else:
            print("You dont have enought money")
            time.sleep(1)
            magic_tower(character, eq)
    elif co == str(ile):
        main()
    else:
        for _ in range(2, ile):
            if co == str(_):
                tak = 0
                for b in slo:
                    if slo[b] == 150 and eq.gold >= slo[b] and tak == _ - 2:
                        eq.tier1 = 1
                        eq.gold -= slo[b]
                        bought(eq, character)
                    elif slo[b] == 300 and eq.gold >= slo[b] and tak == _ - 2:
                        eq.tier2 = 1
                        eq.gold -= slo[b]
                        bought(eq, character)
                    elif slo[b] == 500 and eq.gold >= slo[b] and tak == _ - 2:
                        eq.tier3 = 1
                        eq.gold -= slo[b]
                        bought(eq, character)
                    elif eq.gold < slo[b] and tak == 0:
                        print("You dont have enought money")
                        time.sleep(1)
                        magic_tower(character, eq)
                    tak += 1


def daily_shop():
    list_items = ["Better Ring", "Best Ring", "Better Necklace", "Best Necklace", "Better Robe", "Best Robe"]
    p = pathlib.Path("config/shop.txt")
    with open(p, "w") as sklep:
        for _ in range(random.randint(2, 4)):
            przedmiot = list_items[random.randint(0, len(list_items) - 1)]
            list_items.remove(przedmiot)
            if re.match("Better", przedmiot):
                c = random.randint(75, 100)
                sklep.write(przedmiot+"\n"+str(c)+"\n")
            elif re.match("Best", przedmiot):
                c = random.randint(300, 500)
                sklep.write(przedmiot+"\n"+str(c)+"\n")


def shop1(eq):
    print("#####################################")
    print("Welcome in my Shop\nBuy by select number\nYour money:{0} \nToday product available:".format(str(eq.gold)))
    p = pathlib.Path("config/shop.txt")
    with open(p, "r") as sklep:

        counter = 0
        prze = []
        cen = []
        for _ in sklep:
            counter += 1
            if counter % 2 == 0:
                cen.append(_.strip())
            else:
                prze.append(_.strip())
        counter = 0
    for _ in range(len(cen)):
        counter += 1
        print(str(counter) + " " + prze[_] + ": " + str(cen[_]) + " gold")
    print(str(counter+1)+" Return")
    co = input()
    if counter == 0:
        main()
    else:
        for _ in range(counter):
            li = counter+1
            if co == str(li):
                main()
            if co == str(_+1):
                if int(eq.gold) >= int(cen[_]):
                    if re.search("Robe", prze[_]):
                        eq.robe = prze[_]
                        eq.gold -= int(cen[_])
                    elif re.search("Necklace", prze[_]):
                        eq.necklace = prze[_]
                        eq.gold -= int(cen[_])
                    else:
                        print("Which slot you want to use")
                        print("1-first slot")
                        print("2-second slot")
                        how = input()
                        if how == "1":
                            eq.ring1 = prze[_]
                            eq.gold -= int(cen[_])
                            eq.save()
                        elif how == "2":
                            eq.ring2 = prze[_]
                            eq.gold -= int(cen[_])
                            eq.save()
                    prze.pop(_)
                    cen.pop(_)
                    p = pathlib.Path("config/shop.txt")
                    with open(p, "w") as skl:

                        for _ in range(len(cen)):
                            skl.write(prze[_] + "\n" + str(cen[_]) + "\n")

                    print("Do you wanna buy something else?")
                    print("1-Yes")
                    print("2-No")
                    czy = input()
                    if czy == "1":
                        eq.save()
                        shop1(eq)
                    else:
                        eq.save()
                        main()
                else:
                    print("you dont have enought money")
                    main()


def tavern(eq):
    print("#####################################")
    print("Welcome in tavern")
    print("1-To sleep 5g")
    print("2-Play stone, paper, scissors for the money")
    print("3-Exit")
    co = input()
    if co == "1" and eq.gold >= 5:
        p = pathlib.Path("config/czy.txt")
        with open(p, "w") as czy:
            czy.write("1")
        daily_shop()
        print("You slepp well")
        eq.gold -= 5
        eq.save()
        time.sleep(2)
        main()
    elif co == "1" and eq.gold < 5:
        print("You dont have enought money")
        tavern(eq)
    elif co == "2":
        gambling(eq)
    elif co == "3":
        main()


def gambling(eq):
    global wybur
    print("Your money: {}".format(eq.gold))
    print("What is your bet?")
    ile = input()
    if int(ile) > eq.gold:
        print("You dont have enought money")
        tavern(eq)
    bet = int(ile)

    def again(eq):
        print("Your money: {}".format(eq.gold))
        print("Wanna play again?\n1-Yes\n2-No")
        ca = input()
        if ca == "1":
            gambling(eq)
        elif ca == "2":
            eq.save()
            tavern(eq)
    print("Select:\n1-Stone\n2-Paper\n3-Scissors")
    tab = ["Stone", "Paper", "Scissors"]
    opp = tab[random.randint(0, 2)]
    what = input()
    if what == "1":
        wybur = "Stone"
    elif what == "2":
        wybur = "Paper"
    elif what == "3":
        wybur = "Scissors"
    print("Your opponent pick {0}".format(opp))
    time.sleep(0.8)
    if opp == wybur:
        print("Draw\nWanna play again?\n1-Yes\n2-No")
        again(eq)
    elif re.match("Stone", wybur) and re.match("Scissors", opp) or re.match("Paper", wybur) and re.match("Stone", opp) \
            or re.match("Scissors", wybur) and re.match("Paper", opp):
        print("You win")
        eq.gold += bet
        again(eq)
    else:
        print("You lose")
        eq.gold -= bet
        again(eq)


def begging(eq):
    print("#####################################")
    print("You are begging for the money on the street\n1-to beg for money\n2- to stop")
    while True:
        co = input()
        if co == "1":
            czy = random.randint(0, 10)
            if czy == 1:
                eq.gold += 1
                print("+1 gold")
            else:
                print("not this time")
        elif co == "2":
            break
    eq.save()
    main()


def items_stat(a, b, c, d):
    stat_basic_ring = Stat()
    sta_bette_ring = Stat(10, 10, 5, 10)
    stat_best_ring = Stat(20, 20, 10, 15)

    stat_basic_neclake = Stat()
    stat_betternec_lake = Stat(5, 10, 10, 20)
    stat_best_beclake = Stat(10, 20, 20, 30)

    stat_basis_robe = Stat()
    stat_better_robe = Stat(5, 5, 10, 15)
    stat_best_robe = Stat(10, 10, 25, 20)
    items = {"Basic Ring": stat_basic_ring, "Better Ring": sta_bette_ring, "Best Ring": stat_best_ring,
             "Basic Necklace": stat_basic_neclake, "Better Necklace": stat_betternec_lake,
             "Best Necklace": stat_best_beclake, "Basic Robe": stat_basis_robe,
             "Better Robe": stat_better_robe, "Best Robe": stat_best_robe}
    stat1 = items[a]
    stat2 = items[b]
    stat3 = items[c]
    stat4 = items[d]
    ekwi = [stat1, stat2, stat3, stat4]
    fullhp = 0
    fullarmor = 0
    fullap = 0
    fullmana = 0
    for a in ekwi:
        fullhp += a.hp
        fullarmor += a.armor
        fullap += a.ap
        fullmana += a.mana
    return [fullhp, fullarmor, fullap, fullmana]


def spell_stat(eq, character):
    magic_bullet = Spells(70, 0.20, 10, "Magic Bullet")

    airball = Spells(60, 0.20, 20, "Airball")
    call_the_wind = Spells(40, 0.70, 50, "Call the Wind")
    rain_storm = Spells(50, 2.00, 100, "Rain Storm")

    fireball = Spells(60, 0.30, 20, "Fireball")
    call_the_fire = Spells(20, 0.90, 50, "Call the Fire")
    inferno = Spells(30, 2.20, 125, "Inferno")

    waterball = Spells(60, 0.50, 20, "Waterball")
    call_the_water = Spells(80, 0.50, 50, "Call the Water")
    tsunami = Spells(900, 1.80, 100, "Tsunami")

    earthball = Spells(60, 0.30, 20, "Earthball")
    call_the_earth = Spells(80, 0.70, 50, "Call the Earth")
    earthquake = Spells(80, 1.80, 100, "Earthquake")

    windspells = [airball, call_the_wind, rain_storm]
    firespells = [fireball, call_the_fire, inferno]
    waterspells = [waterball, call_the_water, tsunami]
    earthspells = [earthball, call_the_earth, earthquake]
    typs = {"wind": windspells, "fire": firespells, "water": waterspells, "earth": earthspells}
    spe = [magic_bullet]

    for _ in typs.keys():
        if character.typ == _:
            if eq.tier1 == 1:
                spe.append(typs[_][0])
            if eq.tier2 == 1:
                spe.append(typs[_][1])
            if eq.tier3 == 1:
                spe.append(typs[_][0])
    return spe


start()
