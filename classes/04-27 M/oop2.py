
class Animal: 

    def __init__(self, species, name, age):
        self.species = species
        self.name = name 
        self.age = age 

    def speak(self):
        return 'growl'

class Cat(Animal):
    def __init__(self, species, name, age, wiskers, lives_used):
        super().__init__(species, name, age)
        self.wiskers = wiskers
        self.lives_used = lives_used

    def speak(self):
        print(super().speak())
        return 'meow meow meow'
    
luna = Cat('tabby', 'luna', 10, True, 5)

class Dog(Animal):
    def __init__(self, species, name, age):
        super().__init__(species, name, age)

    def speak(self):
        return 'bow wow'
    
rover = Dog('lab', 'rover', 6)

animals = [luna, rover]

for a in animals:
    print (a.speak())

print (Animal.speak(luna))