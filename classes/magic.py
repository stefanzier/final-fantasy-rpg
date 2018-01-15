import random

# Spell Class - for use within a Person's "Magic" menu
class Spell:
    # Initialize our Spell
    def __init__(self, name, cost, dmg, type):
        self.name = name
        self.cost = cost
        self.dmg = dmg
        self.type = type

    # Generate a damage range our Spell can inflict on our enemy
    def generate_damage(self):
        low = self.dmg - 15
        high = self.dmg + 15
        return random.randrange(low, high)
