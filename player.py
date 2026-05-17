import pygame
from monsters import *
from items import *
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

    def remove_item(self,item, quantity=1):
        if item in self.inventory:
            self.inventory[item] -= quantity
            if self.inventory[item] <= 0:
                del self.inventory[item]
    
    def has_item(self, item, quantity=1):
        return self.inventory.get(item,0) >= quantity
    
    def add_gold(self, amount):
        self.gold += amount

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
        self.stoage.append(monster)
    
    def move_to_storage(self, monster):
        if monster in self.team:
            self.team.remove(monster)
            self.storage.append(monster)
    
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


def inventory_formatter(item,inventory):
    return f"{item.name}: {inventory[item]}"

def inventory_formatter_sell(item,inventory):
    return f"{item.name}: {inventory[item]}     sell for: ${item.price//2}"