from error import GameEndError

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def __str__(self):
        return f"{self.name}: {self.description}"

    def on_drop(self):
        return {
            "print": f"Dropped the item '{self.name}'",
        }
    
    def on_take(self):
        return {
            "print": f"Got the item '{self.name}'",
        }

class BBQ(Item):
    def __init__(self, name, description):
        super().__init__(name, description)
    
    def on_take(self):
        raise GameEndError("Congratulations, you ate the bbq steak! Much win, such savory, wow")