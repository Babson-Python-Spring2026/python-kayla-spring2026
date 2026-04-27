class BankAccount:

    bank_name = 'Babson Bank'

    def __init__(self, name, amount):
        self._name = name
        self._amount = amount 

    def __str__(self):
        return f'my account name is {self.name} and has ${self.amount:,.2f}'
    
    def __add__(self, other):
        name = self.name + ' and ' + other.name
        amount = self.amount + other.amount
        a = BankAccount (name, amount)
        return a
    
    @property 
    def name(self):
        if len(self._name == 3):
            self._name = 'jim'
        return self._name 
    
    @name.setter 
    def name(self, name):
        self._name = name 

    @classmethod
    def change_bank_name(cls, name):
        cls.bank_name = name

BankAccount.change_bank_name('new bank')


'''
bob = BankAccount('bob', 5000.25)
carol = BankAccount('carol', 10000)

joint = bob + carol

print (joint)
'''

class BankAccount: 

    def __init__(self, name, amount):
        self.name = name 
        self.amount = amount 

    @classmethod
    def from_string(cls, info):
        tokens = info.split(',')
        object = BankAccount(tokens[0], tokens[1])
        return object
    
new_account = BankAccount.from_string('bob, 500')

print(new_account.name, new_account.amount)