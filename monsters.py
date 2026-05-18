import pygame
from moves import *
import random

class Monster:
    def __init__(
            self,
            name,
            elements={None},
            level=1,
            max_hp=50,
            energy=10,
            courage=5,
            power=5,
            wisdom=5,
            speed=5,
            moves=None
        ):
        self.name = name
        self.elements = {e.lower() for e in elements} if elements else set()

        #progression
        self.level = level
        self.exp = 0

        #stats
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_energy = energy
        self.energy = energy
        self.courage = courage
        self.power = power
        self.wisdom = wisdom
        self.speed = speed

        #combat
        self.moves = moves if moves else []

        #training
        self.training_bonus = {
            "hp": 0,
            "energy": 0,
            "courage": 0,
            "power": 0,
            "wisdom": 0,
            "speed": 0
        }

        self.training_points_used = 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp-amount)

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
           self.hp = self.max_hp

    def heal_full(self):
        self.hp = self.max_hp
        self.energy = self.max_energy

    def restore_energy(self,amount):
        self.energy += amount

        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def is_alive(self):
        return self.hp > 0
    
    def attempt_capture(self, capture_bonus=0):

            base_chance = 50 - (self.level *5)
            chance = base_chance + capture_bonus
            chance = max(5, min(95, chance))
            roll = random.randint(1, 100)

            return roll <= chance

    def gain_exp(self,amount):
        self.exp += amount

        while self.exp >= self.exp_to_next_level():
            self.exp -= self.exp_to_next_level()
            self.level_up()

    def exp_to_next_level(self):
        return 100 + (self.level * 20)

    def level_up(self):
        self.level += 1

        self.max_hp +=10
        self.max_energy += 5
        self.power +=2
        self.wisdom += 2
        self.speed += 1
        self.courage += 1

        self.hp = self.max_hp
        self.energy = self.max_energy
        return [f"{self.name} grew to level {self.level}!"]
    
    def train_stat(self,stat):
        if self.training_points_used >= 5:
            return False, "Training limit reached!"
        
        if self.training_bonus[stat] >= 10:
            return False, f"{stat} is already max trained!"
        
        setattr(self, 
                stat, 
                getattr(self, stat) + 5
                )
        
        self.training_bonus[stat] += 5
        self.training_points_used += 1

        return True, f"{stat} increased!"
    
    def to_dict(self):

        return {
            "name": self.name,
            "level": self.level,
            "exp": self.exp,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "energy": self.energy,
            "max_energy": self.max_energy,
            "courage": self.courage,
            "power": self.power,
            "wisdom": self.wisdom,
            "speed": self.speed,
            "elements": list(self.elements),
            "moves": [move.name for move in self.moves],
        }
    @classmethod
    def from_dict(cls, data, move_lookup):
        moves = [move_lookup[name] for name in data["moves"]]

        monster = cls(
            data["name"],
             set(data["elements"]),
            data["level"],
            data["max_hp"],
            data["max_energy"],
            data["courage"],
            data["power"],
            data["wisdom"],
            data["speed"],
            moves
        )

        monster.hp = data["hp"]
        monster.energy = data["energy"]
        monster.exp = data["exp"]

        return monster
        

      
    


testmon = Monster("Testmon",{"fire"}, 1, 40, 20, 10, 15, 20, 25,[tackle,fireball,firestream])
moxmon = Monster("Moxmon", {"None"}, 3, 50, 15, 20, 30,40 ,50, [tackle, fireball])
timon = Monster("Timon", {"water"}, 3, 40, 20, 40, 30, 80, 10, [tackle, heal])
huntmon = Monster("Huntmon", {"earth"}, 1, 30, 20, 50, 40, 10, 20, [tackle, fireball, vine_wrap])
steamon = Monster("Steamon", {"fire", "water"}, 1, 40, 20, 50, 40, 30, 20,[tackle, fireball, firestream])
