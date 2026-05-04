import pygame

class Player:
    def __init__(self,name):
        self.name = name
        self.gold = 1000
        

        self.team = []
        self.storage = []

        self.inventory = {}

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


def inventory_formatter(item,inventory):
    return f"{item.name}: {inventory[item]}"