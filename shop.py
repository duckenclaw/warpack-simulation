import json
import random

class Item:
    def __init__(self, name, category, activation, effect, effect_stacks, cooldown, chance, width, height, space, cost, rarity):
        self.name = name
        self.category = category
        self.activation = activation
        self.effect = effect
        self.effect_stacks = effect_stacks
        self.cooldown = cooldown
        self.chance = chance
        self.width = width
        self.height = height
        self.space = space
        self.cost = cost
        self.rarity = rarity

    def __repr__(self):
        return f"{self.name} (Category: {self.category}, Cost: {self.cost}, Space: {self.space})"


class Player:
    def __init__(self, level):
        self.level = level
        self.hp = 25 + 5 * min(level, 11)
        self.gold = 8 + 5 * level
        self.space = 10
        self.items = []
        self.regeneration = 0
        self.armor = 0
        self.reflect = 0
        self.poison = 0
        self.empower = 0
        self.received_damage = 0

    def add_item(self, item):
        if self.space >= item.space and self.gold >= item.cost:
            if item.effect == "Expand pack":
                self.space += item.effect_stacks
                self.gold -= item.cost
                print(f"Player's space increased by {item.effect_stacks} from {item.name}")
            else:
                self.items.append(item)
                self.space -= item.space
                self.gold -= item.cost
                print(f"Player bought {item.name}")
            return True
        return False

    def __repr__(self):
        return f"Player(Level: {self.level}, HP: {self.hp}, Gold: {self.gold}, Space: {self.space}, Items: {self.items})"


class Shop:
    def __init__(self, items):
        self.items = items
        self.rarity_weights = {
            'None': 0,
            'Common': 55,
            'Rare': 35,
            'Legendary': 10
        }
        self.current_items = []

    def get_random_items(self, count=4):
        weighted_items = []
        for item in self.items:
            weighted_items.extend([item] * self.rarity_weights[item.rarity])
        self.current_items = random.sample(weighted_items, count)

    def sell_items(self, player):
        # choose_manually = input("Do you want to choose items manually? (yes/no): ").strip().lower() == "yes"
        choose_manually = False

        while player.gold > 0:
            if not self.current_items:
                self.get_random_items()
            
            print(f"| Gold: {player.gold} | Space: {player.space} |")
            print("Items available for purchase:")
            for i, item in enumerate(self.current_items, start=1):
                print(f"{i}. {item.name} GP: {item.cost} S: {item.space}")

            if choose_manually:
                choice = int(input("Choose an item (1-4) or 0 to skip: ")) - 1
            else:
                choice = random.randint(-1, len(self.current_items)-1)
                print(f"Randomly choosing item {choice + 1}")

            if choice in range(4):
                selected_item = self.current_items.pop(choice)
                if not player.add_item(selected_item):
                    print("Not enough space or gold to buy this item.")
                    self.current_items.insert(choice, selected_item)  # Put the item back if it couldn't be bought
                
            else:
                print("Skipping purchase.")
                self.current_items = []
                if player.gold >= 1:
                    player.gold -= 1  # Spend 1 gold to get new items
                else:
                    break

# Load item database from JSON file
with open('items.json', 'r') as file:
    item_data = json.load(file)
    item_database = [Item(**item) for item in item_data]