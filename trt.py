class Product:
    totalProducts = 0   
    def __init__(self, name, price):
        self.name = name
        self.price = price
        Product.totalProducts += 1
    def get_info(self):
        return f"Product: {self.name}, Price: {self.price}"
    def apply_discount(self, percent):
        discount_amount = self.price * percent / 100
        self.price -= discount_amount
        return self.get_info()   
class DigitalProduct(Product):
    def __init__(self, name, price, file_size):
        super().__init__(name, price)
        self.file_size = file_size

    def download(self):
        return f"{self.name} is downloading... File size: {self.file_size}MB"
class PhysicalProduct(Product):
    def __init__(self, name, price, weight):
        super().__init__(name, price)
        self.weight = weight
    def ship(self):
        return f"{self.name} is being shipped. Weight: {self.weight}kg"



p1 = DigitalProduct("Python Course", 10000, 500)
print(p1.get_info())
print(p1.apply_discount(10))
print(p1.download())

p2 = PhysicalProduct("Laptop", 500000, 2.5)
print(p2.get_info())
print(p2.ship())

print("Total products:", Product.totalProducts)