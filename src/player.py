# Write a class to hold player information, e.g. what room they are in
# currently.

class Player:
    def __init__(self, room):
        self.room = room
        self.items = []

    def move(self, direction):
        to = None
        if direction == "n":
            to = self.room.n_to
        elif direction == "e":
            to = self.room.e_to
        elif direction == "s":
            to = self.room.s_to
        elif direction == "w":
            to = self.room.w_to
        
        if to:
            self.room = to
            return True

        return False
