# Write a class to hold player information, e.g. what room they are in
# currently.

class Player:
    def __init__(self, room):
        self.room = room
        self.items = []

    def move(self, direction):
        to = None
        if direction in ["n", "e", "s", "w"]:
            to = self.room.room(direction, self)
        
        if to:
            self.room = to
            return True

        return False
