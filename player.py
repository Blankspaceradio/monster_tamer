import pygame
from monsters import *
from items import *
from save_system import *
class Player:
    def __init__(self,name):
        self.name = name
        self.gold = 1000
        

        self.team = [testmon, huntmon]
        self.storage = [timon, huntmon, steamon]

        self.inventory = {}
        self.add_item(potion, 5)
        self.add_item(catcher, 5)

    def add_item(self, item, quantity = 1):
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity
        save_game(self)

    def remove_item(self,item, quantity=1):
        if item in self.inventory:
            self.inventory[item] -= quantity
            if self.inventory[item] <= 0:
                del self.inventory[item]
        save_game(self)

    def has_item(self, item, quantity=1):
        return self.inventory.get(item,0) >= quantity
    
    def add_gold(self, amount):
        self.gold += amount
        save_game(self)

    def spend_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
        

    def add_to_team(self,monster):
        if len(self.team) < 6:
            self.team.append(monster)
            return True
        else:
            self.storage.append(monster)
            return False
        

    def add_to_storage(self, monster):
        self.storage.append(monster)
        save_game(self)
    def move_to_storage(self, monster):
        if monster in self.team:
            self.team.remove(monster)
            self.storage.append(monster)
        save_game(self)
    
    def move_to_team(self, monster):
        if monster in self.storage and len(self.team) < 6:
            self.storage.remove(monster)
            self.team.append(monster)
            return True
        else:
            return False
    
    def heal_team(self):
        for monster in self.team:
            monster.heal_full()
        save_game(self)

    def swap_team_positions(self,index1,index2):
        self.team[index1], self.team[index2] = (
            self.team[index2],
            self.team[index1]
        )
    
    def to_dict(self):
       
        return {
            "gold": self.gold,
            "team": [m.to_dict() for m in self.team],
            "storage": [m.to_dict() for m in self.storage],
            "inventory": {
                item.name: qty
                for item, qty in self.inventory.items()
            }
        }
    @classmethod
    def from_dict(cls, data, move_lookup, item_lookup):

        player = cls("player")

        player.gold = data["gold"]

        player.team = [
            Monster.from_dict(monster_data, move_lookup)
            for monster_data in data["team"]
        ]

        player.storage = [
            Monster.from_dict(monster_data, move_lookup)
            for monster_data in data["storage"]
        ]

        player.inventory = {
            item_lookup[name]: qty
            for name, qty in data["inventory"].items()
        }

        return player

def inventory_formatter(item,inventory):
    return f"{item.name}: {inventory[item]}"

def inventory_formatter_sell(item,inventory):
    return f"{item.name}: {inventory[item]}     sell for: ${item.price//2}"