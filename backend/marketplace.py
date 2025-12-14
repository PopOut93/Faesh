class Product:
    def __init__(self, name, brand, price):
        self.name = name
        self.brand = brand
        self.price = price

class Marketplace:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)
        return f"{product.name} added by {product.brand}"

    def list_products(self, limit=10):
        return [f"{p.brand}: {p.name} - ${p.price}" for p in self.products[-limit:]]
