from abc import ABC, abstractmethod

class Product(ABC):
    total_product=0

    def __init__(self,sku, name, price):
        self._price = price
        self.sku = sku
        self.name = name
        Product.total_product+=1

    @property
    def price(self):
        return self._price
    
    @price.setter
    def price(self,new_price):
        if(new_price<0): print("Price is invalid!")
        else: self._price=new_price

    @price.deleter
    def price(self):
        return f"{self._price:,.0f} VND"

    @abstractmethod
    def calculate_final_price(self):
        pass
    
    @classmethod
    def get_count(cls):
        return cls.total_product

    @staticmethod
    def is_valid_sku(sku):
        return len(sku)==6

    def __str__(self):
        return f"[{self.sku}] {self.name:<20} | Price: {self.price}"

    def __eq__(self, other):
        return self.sku == other.sku

    def __lt__(self, other):
        return self._price < other._price

    def __gt__(self, other):
        return self._price > other._price

    def __add__(self, other):
        return self._price + other._price

    def __contains__(self, keyword):
        return keyword.lower() in self.name.lower()

    def __getitem__(self, key):
        match key:
            case "sku": return self.sku
            case "name": return self.name
            case "price": return self._price
            case _: return f"Key '{key}' not found"

class Laptop(Product):
    def __init__(self, sku, name, price, ram_gb):
        super().__init__(sku, name, price)
        self.ram_gb = ram_gb

    def calculate_final_price(self):
        return self._price * 1.1

class Phone(Product):
    def __init__(self, sku, name, price, is_gb):
        super().__init__(sku, name, price)
        self.is_gb=is_gb

    def calculate_final_price(self):
        return self._price - 500000

class WarrantyService:
    def __init__(self, years, free_per_year):
        self.name = f"Warranty for{years} years"
        self.years = years
        self.free_per_years = free_per_year

    def calculate_final_price(self):
        return self.years * self.free_per_years 
