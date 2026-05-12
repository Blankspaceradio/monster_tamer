import pygame
import random


class Move:
    def __init__(self,name,power,cost,elements=None, accuracy=100, move_type="damage", effect=None, bonus_effect=None, target_type="enemy"):
        self.name = name
        self.power = power
        self.cost = cost
        self.element = set(elements) if elements else set()
        self.accuracy = accuracy
        self.move_type = move_type
        self.effect = effect
        self.bonus_effect = bonus_effect
        self.target_type = target_type

    def __str__(self):
        return f"{self.name} (Cost: {self.cost})"

    def use(self, user, target):
        actual_target = target
        if self.target_type == "self":
            actual_target = user


        
        #check energy
        if user.energy < self.cost:
            print(f"{user.name} doesn't have enough energy!")
            return False
        #spend energy
        user.energy -= self.cost
        #accuracy check
        if random.randint(1,100) > self.accuracy:
            print(f"{user.name}'s {self.name} missed!")
            return False 
        
        #apply effect
        if self.move_type == "damage":
            damage = self.calculate_damage(user)
            actual_target.take_damage(damage)
            print(f"{user.name} used {self.name} and dealt {self.power} damage!")

        elif self.move_type == "heal":
            actual_target.heal(self.power)
            print(f"{user.name} healed for {self.power}!")
        
        #custom effect hook
        if self.effect:
            self.effect(user,actual_target)

        if self.element == user.element and self.bonus_effect:
            self.bonus_effect(user,actual_target)

        return True
    
    def calculate_damage(self, user):
        damage = self.power

        matching_elements = self.element & user.element

        bonus = 1 + (0.5 * len(matching_elements))
        damage *= bonus
        return max(1, int(damage))
    
    


tackle = Move("Tackle", power=10, cost=2, elements="none")

fireball = Move("Fireball", power=15, cost=5, elements="fire")

heal = Move("Heal", power=20, cost=4, elements="none", move_type="heal", target_type="self")