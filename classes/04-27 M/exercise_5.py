
class Vehicle: 

    def __init__(self, name):
        self.name = name 

    def __str__(self):
        return "i'm electric"
    
    def move(self):
        print ("moving")
    
class Car(Vehicle):

    def __init__(self, name):
        super().__init__(name)

    def move(self):
        print ("drives")

chevy = Car("chevy")

class Boat(Vehicle):

    def __init__(self, name):
        super().__init__(name)

    def move(self):
        print("sails")

floats = Boat("floats")

transports = [chevy, floats]

for t in transports:
    t.move()
