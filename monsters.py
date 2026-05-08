import pygame
from moves import *

class Monster:
    def __init__(
            self,
            name,
            elements=None,
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
        self.element = set(elements) if elements else set()

        #progression
        self.level = level
        self.exp = 0

        #stats
        self.max_hp = max_hp
        self.hp = max_hp

        self.energy = energy
        self.courage = courage
        self.power = power
        self.wisdom = wisdom
        self.speed = speed

        #combat
        self.moves = moves if moves else []

    def take_damage(self, amount):
        self.hp = max(0, self.hp-amount)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def is_alive(self):
        return self.hp > 0

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
        self.power +=2
        self.wisdom += 2
        self.speed += 1
        self.courage += 1

        self.hp = self.max_hp


testmon = Monster("Testmon",{"fire"}, 1, 40, 20, 10, 15, 20, 25,[tackle, heal])
moxmon = Monster("Moxmon", {"None"}, 3, 50, 15, 20, 30,40 ,50, [tackle, fireball])
timon = Monster("Timon", {"water"}, 3, 40, 20, 40, 30, 80, 10, [tackle, heal])
huntmon = Monster("Huntmon", {"earth"}, 1, 30, 20, 50, 40, 10, 20, [tackle, fireball])
