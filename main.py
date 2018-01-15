import random

from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Create Black Magic
fire = Spell("Fire", 10, 600, "black")
thunder = Spell("Thunder", 10, 600, "black")
blizzard = Spell("Blizzard", 10, 600, "black")
meteor = Spell("Meteor", 20, 1200, "black")
quake = Spell("Quake", 14, 140, "black")

# Create White Magic
cure = Spell("Cure", 12, 620, "white")
cura = Spell("Cura", 18, 1500, "white")

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super-Potion", "potion", "Heals 500 HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
hielixir = Item("MegaElixir", "elixir", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

# Instantiate People
player_magic = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 3},
                {"item": hipotion, "quantity": 5},
                {"item": elixir, "quantity": 5},
                {"item": hielixir, "quantity": 5},
                {"item": grenade, "quantity": 5}]

player1 = Person("Locke", 3260, 132, 60, 34, player_magic, player_items)
player2 = Person("Edgar", 4160, 188, 60, 34, player_magic, player_items)
player3 = Person("Sabin", 3089, 150, 174, 34, player_magic, player_items)

# Players are put into a players list
players = [player1, player2, player3]

# The enemy is created here
enemy = Person("Siren", 9999, 701, 600, 805, [], [])

# Now that we have players and an enemy, let's start the game!
running = True;

print("=======================================================================")
print(bcolors.FAIL + bcolors.BOLD + "                          AN ENEMY ATTACKS!" + bcolors.ENDC)
print("=======================================================================")
while (running):
    # List all players' Name, HP, and MP
    print("NAME:               HP                                      MP               ")
    for player in players:
        player.get_stats()

    # List enemy HP and MP
    enemy.get_enemy_stats()

    # Each player needs a turn - loop over players in list
    for player in players:
        # Get player choice to determine action
        choice = player.choose_action()

        if choice == 0:
            # Player chose "Attack"
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print(bcolors.OKBLUE + "\n" + player.name + " attacked for", dmg, "points of damage." + bcolors.ENDC)
        elif choice == 1:
            # Player chose "Magic" so present them with "Magic" menu
            magic_choice = player.choose_magic()

            # Player's spell choice and the magic damage associated with that spell
            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            # Get player's current MP. If their MP is less than the cost of the spell they shouldn't be able to cast it
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\n    Not enough MP\n" + bcolors.ENDC)
                continue

            # Reduce MP and cast spell
            player.reduce_mp(spell.cost)
            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy.take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage" + bcolors.ENDC)

        elif choice == 2:
            # Player chose "Items" so present them with the "Items" menu
            item_choice = player.choose_item()

            # Check if player chose an item with a quantity of 0
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            # Player chose an item with a quantity > 1 so reduce the inventory count associated with that item
            item = player.items[item_choice]["item"]
            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "Elixir":
                    player.heal(item.prop, Elixir=True)
                    print(
                        bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP for " + player.name + bcolors.ENDC)
                elif item.name == "MegaElixir":
                    for p in players: p.heal(item.prop, Elixir=True)
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP for whole team" + bcolors.ENDC)
            elif item.type == "attack":
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", item.prop, "points of damage" + bcolors.ENDC)

    # Make enemy attack after players have selected their moves
    enemy_choice = 1
    # Enemy choose a random player to inflict damage on - this random player is called the "target"
    target = random.randrange(0, len(players))
    enemy_dmg = enemy.generate_damage()

    # Target takes the damage
    players[target].take_damage(enemy_dmg)
    print(bcolors.FAIL + bcolors.BOLD, "\nEnemy attacked", players[target].name, "for", str(enemy_dmg),
          "points of damage.", bcolors.ENDC)

    print("-------------------------------")

    # If the enemy has HP <= 0 we won!
    if enemy.get_hp() <= 0:
        print(bcolors.OKGREEN + "Your team wins! Congratulations!" + bcolors.ENDC)
        # End our game
        running = False

    # Our players list should only contain players with HP > 0
    players = [player for player in players if player.hp > 0]

    # If we have no players left in our list we lost the game
    if len(players) == 0:
        print(bcolors.FAIL + bcolors.BOLD + "Your enemy has defeated you! Better luck next time!")
        # End our game
        running = False
