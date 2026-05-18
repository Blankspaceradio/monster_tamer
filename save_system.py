import pygame
import json

def save_game(player):
    print("SAVE TRIGGERED")
    data = {
        "player": player.to_dict()
    }

    with open("save.json", "w") as f:
        json.dump(data, f, indent=4)

def load_game(move_lookup, item_lookup,):
    from player import Player
    with open("save.json", "r") as f:
        data = json.load(f)

    player = Player.from_dict(
        data["player"],
        move_lookup,
        item_lookup
    )

    return player