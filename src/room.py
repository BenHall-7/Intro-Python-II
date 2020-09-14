from error import GameEndError

class Room:
    def __init__(self, name, description, items=[]):
        self.name = name
        self.description = description
        self.n_to = None
        self.e_to = None
        self.s_to = None
        self.w_to = None
        self.items = items

    def room(self, direction, player):
        if direction == "n":
            return self.n_to
        elif direction == "e":
            return self.e_to
        elif direction == "s":
            return self.s_to
        elif direction == "w":
            return self.w_to

        return None

class Room_Overlook(Room):
    def __init__(self, name, description, items=[]):
        super().__init__(name, description, items)
    
    def room(self, direction, player):
        if direction == "n":
            if input("\nJump? (y/Y for yes)\n> ").lower() == "y":
                if "parachute" in [item.name.lower() for item in player.items]:
                    return self.n_to
                
                raise GameEndError("You fell to your death")
            else:
                return self
        else:
            return Room.room(self, direction, player)
