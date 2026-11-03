from utils import activity
import os

class StoreManager:
    STORE_INFO = ("TECHSTORE VN", "1900-8888")

    def __init__(self):
        self.inventory = []
        self.skus = set()
        self.vouchers = {
            "GIAM100": 100000, 
            "VIP500": 500000
        }

    @activity
    def add_products(self, *args):
        for item in args:
            if item not in self.inventory:
                self.inventory.append(item)
                self.skus.add(item.sku)

    @activity
    def remove_product(self, sku):
        for item in self.inventory:
            if item.sku == sku:
                self.inventory.remove(item)
                self.skus.remove(sku)
                print(f"Have removed product with sku: {sku}")
                return True
        print(f"We don't find product with sku: {sku}")   
        return False

    @activity
    def update_product(self, sku, **kwargs):
        for item in self.inventory:
            if item.sku == sku:
                for key, value in kwargs.items():
                    if key == "price":
                        item.price = value
                    elif key == "name":
                        item.name = value
                return True
        return False

    @activity
    def filter_by_max_price(self, max_price):
        return [item for item in self.inventory if item.price <= max_price]

    @activity
    def search_by_keyword(self, keyword):
        return [item for item in self.inventory if keyword in item]

    @activity
    def export_report(self, file_path="report.txt"):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"=== REPORT OF : {self.STORE_INFO[0]} ===\n")
            for item in self.inventory:
                file.write(str(item) + "\n")

        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()

