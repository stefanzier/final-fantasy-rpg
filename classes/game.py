import random
from .magic import Spell

# Class for coloring text in the terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    # Initialize our Person
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    # Each person has a range of attack damage they can inflict upon the enemy
    # Simply return a random number within this range
    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    # Each spell has a range of  damage it can inflict upon the enemy
    # Simply return a random number within this range
    def generate_spell_damage(self, i):
        mgl = self.magic[i]["dmg"] - 5
        mgh = self.magic[i]["dmg"] + 5
        return random.randrange(mgl, mgh)

    # Simply reduce the Person's HP by the inflicted damage value
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0: self.hp = 0
        return self.hp

    # Getter function that returns a Person's HP
    def get_hp(self):
        return self.hp

    # Getter function that returns a Person's Max HP
    def get_max_hp(self):
        return self.maxhp

    # Getter function that returns a Person's MP
    def get_mp(self):
        return self.mp

    # Getter function that returns a Person's Max MP
    def get_max_mp(self):
        return self.maxmp

    # Reduce a Person's MP value. Occurs when a user casts a spell
    def reduce_mp(self, cost):
        self.mp -= cost

    # Return the name of the spell. Used in main.py to print our spell name
    def get_spell_name(self, i):
        return self.magic[i]["name"]

    # Return the cost of the spell. Used in main.py to print our spell cost
    def get_spell_mp_cost(self, i):
        return self.magic[i]["cost"]

    # Called at the beginning of each Person's turn
    # Simply outputs a list of choices. The Person's choice is returned for use in main.py
    def choose_action(self):
        i = 1
        print("\n" + bcolors.BOLD + "" + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "    ACTIONS" + bcolors.ENDC)
        for action in self.actions:
            print("        " + str(i) + ":", action)
            i += 1

        choice = int(input("    Choose Action: ")) - 1
        return choice

    # Called when a Person chooses "Magic" from the "Action" menu
    # Simply outputs a list of choices. The Person's choice is returned for use in main.py
    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    MAGIC" + bcolors.ENDC)
        for spell in self.magic:
            print("        " + str(i) + ":", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1
        choice = int(input("    Choose Magic: ")) - 1
        return choice

    # Called when a Person chooses "Items" from the "Action" menu
    # Simply outputs a list of choices. The Person's choice is returned for use in main.py
    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "    ITEMS" + bcolors.ENDC)
        for item in self.items:
            print("        " + str(i) + ".", item["item"].name, ":", item["item"].description, " (x" + str(item["quantity"]) + ")")
            i += 1
        choice = int(input("    Choose Item: ")) - 1
        return choice

    # Adds points to the Person's HP. Person cannot exceed their assigned Max HP
    # The Elixir flag will not only set the current HP to Max HP but will also
    #  set the current MP to Max MP
    def heal(self, points, Elixir=False):
        newHP = self.maxhp if Elixir else self.hp + points
        self.hp = newHP if newHP <= self.maxhp else self.maxhp
        if Elixir: self.mp = self.maxmp

    # Called at the beginning of each round
    # Prints out the player's HP and MP in health/magic bar format
    #  It calculates the necessary amount of bars and white space needed
    #  The HP bar is split up into 25 bars
    #  The MP bar is split up into 10 bars
    def get_stats(self):
        hp_bar_ticks = ((self.hp/self.maxhp)*100) / 4
        hp_bar = ""
        while hp_bar_ticks > 0: hp_bar += "█"; hp_bar_ticks -= 1
        while len(hp_bar) < 25: hp_bar += " "

        mp_bar_ticks = ((self.mp/self.maxmp)*100) / 10
        mp_bar = ""
        while mp_bar_ticks > 0: mp_bar += "█"; mp_bar_ticks -= 1
        while len(mp_bar) < 10: mp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)
            while decreased > 0: current_hp += " "; decreased -= 1

        current_hp += hp_string

        mp_string = str(self.mp) + "/" + str(self.maxmp)
        current_mp = ""

        if len(mp_string) < 7:
            decreased = 7 - len(mp_string)
            while decreased > 0: current_mp += " "; decreased -= 1

        current_mp += mp_string

        print(bcolors.BOLD + self.name + ":    " +
              current_hp + "|" + bcolors.OKGREEN + hp_bar + bcolors.ENDC + "|      " + bcolors.BOLD +
              current_mp + "|" + bcolors.OKBLUE + mp_bar + bcolors.ENDC + "|")

    # Similar to the get_stats function but specific to an enemy
    #  An enemy only displays its HP bar
    #  HP bar is split into 50 bars (compared to a regular person's 25 bar HP bar)
    #  An enemy has a red HP bar
    def get_enemy_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp/self.maxhp) * 100 / 2

        while bar_ticks > 0: hp_bar += "█"; bar_ticks -= 1
        while len(hp_bar) < 50: hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.maxhp)
        current_hp = ""

        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)
            while decreased > 0: current_hp += " "; decreased -= 1

        current_hp += hp_string
        print("\n" + bcolors.BOLD + self.name + ":    " +
              current_hp + "|" + bcolors.FAIL + hp_bar + bcolors.ENDC + "|")
