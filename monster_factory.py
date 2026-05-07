import pygame
from monsters import *
import random

def create_testmon(level):
    return Monster(
        name = "Testmon",
        elements = "Fire",
        level = level,
        max_hp=random.randint(30,50) + (level * 5),
        energy=random.randint(15, 25) + (level * 5),
        courage=random.randint(5, 10) + (level * 5),
        power=random.randint(5,10) + (level * 5),
        wisdom=random.randint(5,10) + (level * 5),
        speed=random.randint(15,20) + (level * 5),
        moves=[tackle, heal]

    )

def create_moxmon(level):
     return Monster(
        name = "Moxmon",
        elements = "None",
        level = level,
        max_hp=random.randint(30,50) + (level * 5),
        energy=random.randint(15, 25) + (level * 5),
        courage=random.randint(30, 40) + (level * 5),
        power=random.randint(20,30) + (level * 5),
        wisdom=random.randint(50,60) + (level * 5),
        speed=random.randint(50,60) + (level * 5),
        moves=[tackle, fireball]

    )

def create_huntmon(level):
     return Monster(
        name = "Huntmon",
        elements = "Eartj",
        level = level,
        max_hp=random.randint(30,50) + (level * 5),
        energy=random.randint(15, 25) + (level * 5),
        courage=random.randint(30, 50) + (level * 5),
        power=random.randint(40,50) + (level * 5),
        wisdom=random.randint(20,30) + (level * 5),
        speed=random.randint(15,20) + (level * 5),
        moves=[tackle, fireball]

    )