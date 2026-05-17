import pygame
import random


class Move:
    def __init__(self,name,power,cost,elements=None, accuracy=100, move_type="damage", effect=None, bonus_effect=None, target_type="enemy",elemental_bonuses=None):
        self.name = name
        self.power = power
        self.cost = cost
        self.elements = {e.lower() for e in elements} if elements else set()
        self.accuracy = accuracy
        self.move_type = move_type
        self.effect = effect
        self.bonus_effect = bonus_effect
        self.target_type = target_type
        self.elemental_bonuses = elemental_bonuses or {}

    def __str__(self):
        return f"{self.name} (Cost: {self.cost})"

    def use(self, user, target):
        actual_target = target
        if self.target_type == "self":
            actual_target = user

        messages = []
        
        #check energy
        if user.energy < self.cost:
            return {"success": False,
                    "messages": ["Not enough energy!"]} 
            
        #spend energy
        user.energy -= self.cost
        #accuracy check
        if random.randint(1,100) > self.accuracy:
            
            return {"success": False,
                    "messages": [f"{user.name}'s attack missed!"]} 
        
        #apply effect
        if self.move_type == "damage":
            damage = self.calculate_damage(user)
            messages.append(f"{user.name} used {self.name}!")
            messages.append(f"It dealt {damage} damage!")
            actual_target.take_damage(damage)
           

        elif self.move_type == "heal":
            messages.append(f"{user.name} healed {self.power} HP!")
            actual_target.heal(self.power)
           
        
        #custom effect hook
        if self.effect:
            self.effect(user,actual_target)
        if self.elements & user.elements and self.bonus_effect:
            self.bonus_effect(user,actual_target)

        return {
            "success": True,
            "messages": messages
        }
    
    def calculate_damage(self, user):
        damage = self.power
        for element in user.elements:
            damage += self.elemental_bonuses.get(element, 0)
        return max(1, int(damage))
    
   
def lower_speed(user, target):
    target.speed -= 5

    if target.speed <1:
        target.speed = 1
    


tackle = Move("Tackle", power=10, cost=2, elements={"none"})

fireball = Move("Fireball", power=10, cost=5, elements={"fire"}, elemental_bonuses={"fire": 10})

heal = Move("Heal", power=20, cost=4, elements={"none"}, move_type="heal", target_type="self")

vine_wrap = Move("Vine Wrap", power=10, cost=5, elements={"earth"}, bonus_effect=lower_speed)

firestream = Move("Firestream", power=5, cost=3,elemental_bonuses={"fire":5, "water":5})