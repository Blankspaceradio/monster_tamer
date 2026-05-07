import pygame
import random
from monster_factory import *

class Area:
    def __init__ (self, name, monster_pool, min_level, max_level):
        self.name = name
        self.monster_pool = monster_pool

        self.min_level = min_level
        self.max_level = max_level

    def generate_encounters(self, count=5):
        encounters = []

        for _ in range(count):
            monster_factory = random.choice(self.monster_pool)

            level = random.randint(self.min_level, self.max_level)

            monster = monster_factory(level)

            encounters.append(monster)

        return encounters
    
forest = Area(
    "Forest",
    [create_huntmon, create_testmon],
    min_level=1,
    max_level=3
)

mountain = Area(
    "Mountain",
    [create_huntmon, create_moxmon],
    min_level=1,
    max_level=3
)