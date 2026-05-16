import pygame\


class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - ${self.price}"
    
    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    

class CatchItem(Item):
    def __init__(self,name,price,catch_rate):
        super().__init__(name,price)
        self.catch_rate = catch_rate

class HealingItem(Item):
    def __init__(self,name,price,heal_amount):
        super().__init__(name,price)
        self.heal_amount = heal_amount

    def use(self,target):
        target.hp = min(target.max_hp, target.hp+self.heal_amount)

class TrainingItem(Item):
    def __init__(self,name,price,train_amount, train_type):
        super().__init__(name,price)
        self.train_amount = train_amount
        self.train_type = train_type

    def use(self,target):
        match self.train_type:
            case "Courage":
                target.courage += self.train_amount
            case "Power":
                target.power += self.train_amount
            case "Wisdom":
                target.wisdom += self.train_amount
            case "Speed":
                target.speed += self.train_amount

catcher = CatchItem("Catcher", 100, 50)
potion = HealingItem("Potion", 200,20)  
weight = TrainingItem("Weights", 300, 5,"Power")


shop_items = [catcher, potion, weight]