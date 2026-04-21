class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def is_square(self):
        if self.width == self.height:
            return True
        return False
    
rec1 = Rectangle (3,5)
rec2 = Rectangle (2,2)

print(rec1.area())
print(rec1.perimeter())

print(rec2.area())
print(rec2.perimeter())

print(rec1.is_square())
print(rec2.is_square())

class Box:
    def __init__(self, value):
        self.value = value

    def add_one(self):
        self.value += 1

class BankAccount:
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount

    def deposit(self): 
        self.balance += self.amount
        return self.balance
    
transaction1 = BankAccount (1000, 500)

print(transaction1.deposit())

class PortfolioSystem:
    def __init__(self, ticker_universe, mkt_dates):
        self.ticker_universe = ticker_universe
        self.mkt_dates = mkt_dates

    def get_num_market_dates(self):
        return len(self.mkt_dates)

    def get_num_tickers(self):
        return len(self.ticker_universe)

    def is_valid_ticker(self, ticker):
        return ticker in self.ticker_universe
    
    def is_market_date(self, date):
        return date in self.mkt_dates
    
    def get_first_market_date(self): 
        return self.mkt_dates[0]
    
    def get_last_market_date(self):
        return self.mkt_dates[-1]
    
    my_port = PortfolioSystem([],[])
    
