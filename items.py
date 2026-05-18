import pygame
from monsters import *
import random

class Item:
    def __init__(self, name, price, target_type=None):
        self.name = name
        self.price = price
        self.target_type = target_type

    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def use(self, battle, user, target):
        pass
    
    

class CatchItem(Item):
    def __init__(self,name,price,capture_bonus=0):
        super().__init__(name,price, target_type="enemy")
        self.capture_bonus = capture_bonus

       
    def use(self, battle, user, target):
            print("Trying capture", target.name)
            success = target.attempt_capture(self.capture_bonus)
            print("TARGET:", target.name)
            print("CAPTURE ROLL:", success)

            if success:
                battle.player.add_to_team(target)

                battle.phase = "battle end"
                battle.end_messages = [
                    f"{target.name} was captured!"
                ]
                return True, "Captured!"
            return False, f"{target.name} broke free!"

class HealingItem(Item):
    def __init__(self,name,price,heal_amount):
        super().__init__(name,price, target_type="monster")
        self.heal_amount = heal_amount

    def use(self,battle, user, target):
        if user.hp < user.max_hp:
        
            user.heal(20)

            return True, f"{user.name} healed 20!"
        else:
            return False, f"{user.name} is already fulled healed"

class TrainingItem(Item):
    def __init__(self,name,price, stat):
        super().__init__(name,price, target_type="monster")
        self.stat = stat

    def use(self,battle, user, target):
        return target.train_stat(self.stat)

catcher = CatchItem("Catcher", 100, 50)
potion = HealingItem("Potion", 200, 20)  
weight = TrainingItem("Weight", 300, "power")
treadmill = TrainingItem("Treadmill", 300, "speed")
book = TrainingItem("Book", 300, "wisdom")
punchingbag = TrainingItem("Punching Bag", 300, "courage")
jumprope = TrainingItem("Jump Rope", 300, "energy")
heartstone = TrainingItem("Heart Stone", 300, "hp")

shop_items = [catcher, potion, weight, treadmill, book, punchingbag, jumprope, heartstone]