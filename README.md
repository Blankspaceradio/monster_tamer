# Monster Tamer


## Description
As the name implies it's a monster tamer game. There are a couple monsters, moves, and items to use. It also has a capture system so you can catch new mosnters.

## Motivation 
My motivation for making this specific project was a mix of being a fan of monster tamers, i.e. Pokemon and Digimon, and a bit of nostalgia for the Chaotic TCG that came out in 2006 and lasted until 2012. Which shaped some of the moves for this game. Though, after creating this project it was announced that the Chaotic TCG is relaunching in October of 2026 for hobby stores and Janurary of 2027 for big box stores. YAY!


## Quick Start

Clone the repository:

```bash
git clone https://github.com/Blankspaceradio/monster_tamer.git
cd monster_tamer
```

Create a virtual enviornment:

```bash
python -m venv .venv
```

Activate it:

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows

```cmd
.venv\Scripts\activate
```

## Running the Game

```bash
python main.py
```

## Save Data

Game progress is stored in:

```text
save.json
```

Delete this file to start a new game.

## Usage
There is a save state in the game, so if you have not already played the game then pick New Game. Otherwise, you may pick Continue. However, there is only one save state, so if you have a save state and pick New Game then you will lose all your previous data. 

You nagivate by using the arrow keys and enter/return to select an menu option. You can go back with backspace or escape.

### Current Items:
Catch items: Catcher
Healing items: Potion
Training items: weights, treadmill, book, jump rope, heart stone, punching bag

### Additional information 
Some moves have elements as well that boost damage or add additional effects.

The training items allow you to give bonus stats to your monster, but only to a 
max of 10 to a single stat and 25 additional poins total. Each item adds 5 points.

## Contributing

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/monster_tamer.git
cd monster_tamer
```

Install dependencies:

### Using UV

```bash
uv sync
```

### Using pip

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

Run the game:

```bash
uv run main.py
```

or

```bash
python main.py
```