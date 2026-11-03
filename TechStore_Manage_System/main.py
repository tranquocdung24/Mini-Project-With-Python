from models import *
from manage import *
from utils import *

def main():
    store = StoreManager()

    store.add_products(
        Laptop("LP-101", "Macbook Air M3", 27500000, 16),
        Laptop("LP-102", "Dell XPS 15", 35000000, 32),
        Phone("PH-201", "iPhone 16 Pro", 28900000, True),
        Phone("PH-202", "Galaxy S24", 21000000, True)
    )

    while True:
        store_name, hotline = store.STORE_INFO

        print("\n" + "=" * 60)
        print(f"{store_name:^60}")
        print(f"{'Hotline: ' + hotline:^60}")
        print("=" * 60)
        print("1. View Inventory")
        print("2. Add New Product")
        print("3. Update Product")
        print("4. Remove Product from Inventory")
        print("5. Search & Filter by Budget")
        print("6. Shopping Cart")
        print("7. Export Inventory Report & View Activity Log")
        print("0. Exit Program")
        print("-" * 60)

        choice = input("Enter your choice (0-7): ").strip()

        match choice:
            case "1":
                print(f"\n[*] Total products ever created: {Product.get_count()}")
                print(f"[*] Current SKUs in stock: {store.skus}")

                status = "In Stock" if len(store.inventory) > 0 else "Out of Stock"
                print(f"[*] Inventory Status: {status} ({len(store.inventory)} items available)")

                store.inventory.sort()
                print("\n--- PRODUCT LIST ---")
                
                for i in range(len(store.inventory)):
                    print(f"{i + 1}. {store.inventory[i]}")

            case "2":
                print("\n--- ADD NEW LAPTOP TO INVENTORY ---")
                sku = input("Enter SKU (Must be exactly 6 chars, e.g., LP-105): ").strip().upper()

                if not Product.is_valid_sku(sku):
                    print("   [!] Error: SKU must be exactly 6 characters long!")
                    continue

                name = input("Enter Laptop Name: ").strip().title()

                try:
                    price = float(input("Enter Price (VND): "))
                    ram = int(input("Enter RAM capacity (GB): "))

                    if price <= 0 or ram <= 0:
                        print("   [!] Price and RAM must be greater than 0!")
                    else:
                        new_laptop = Laptop(sku, name, price, ram)
                        store.add_products(new_laptop)
                        print(f"   [+] Successfully added: {new_laptop}")
                except ValueError:
                    print("   [!] ValueError: Please enter valid numbers for Price and RAM!")
                finally:
                    print("   --> Finished product addition process.")

            case "3":
                print("\n--- UPDATE PRODUCT ---")
                sku = input("Enter SKU to update (e.g., LP-101): ").strip().upper()
                try:
                    new_price = float(input("Enter new price: "))
                    new_name = input("Enter new name Or press Enter to keep current name: ").strip()

                    if new_name != "":
                        ok = store.update_product(sku, price=new_price, name=new_name)
                    else:
                        ok = store.update_product(sku, price=new_price)

                    if ok:
                        print("   [+] Update request processed!")
                    else:
                        print(f"   [!] Product with SKU '{sku}' not found!")
                except ValueError:
                    print("   [!] Error: Price must be a valid number!")

            case "4":
                sku = input("\nEnter SKU to remove (e.g., PH-202): ").strip().upper()
                if store.remove_product(sku):
                    print(f"   [+] Removed product '{sku}' from inventory!")
                else:
                    print(f"   [!] SKU '{sku}' not found in inventory!")

            case "5":
                print("\n--- SEARCH & FILTER PRODUCTS ---")
                kw = input("1. Enter keyword to search (e.g., Macbook, iPhone): ").strip()
                found_items = store.search_by_keyword(kw)
                print(f"--> Search results for '{kw}':")
                for item in found_items:
                    print(f"   - SKU: {item['sku']} | Name: {item['name']} | Base Price: {item['price']:,.0f} VND")

                try:
                    max_p = float(input("\n2. Enter your maximum budget (VND): "))
                    affordable = store.filter_by_max_price(max_p)
                    print(f"--> Products with price <= {max_p:,.0f} VND:")
                    for item in affordable:
                        print("  ", item)
                except ValueError:
                    print("   [!] Invalid budget amount entered!")

            case "6":
                print("\n--- SHOPPING CART ---")
                if len(store.inventory) >= 2:
                    sp1 = store.inventory[0]
                    sp2 = store.inventory[1]
                    warranty = WarrantyService(years=2, fee_per_year=500000)

                    print(f"[*] Combined base price of first 2 items: {sp1 + sp2:,.0f} VND")

                    cart = [sp1, sp2, warranty]
                    total_bill = 0

                    print("\nInvoice Details (Laptop +10% tax / Phone -500k subsidy):")
                    for item in cart:
                        final_price = item.calculate_final_price()
                        total_bill += final_price
                        print(f" - {item.name:<25}: {final_price:>14,.0f} VND")

                    print(f"\nAvailable discount codes: {list(store.vouchers.keys())}")
                    code = input("Enter discount code (Press Enter to skip): ").strip().upper()
                    discount = store.vouchers.get(code, 0)

                    print(f"==> TOTAL PAYMENT: {total_bill - discount:,.0f} VND (Discount applied: {discount:,.0f} VND)")
                else:
                    print("   [!] Inventory needs at least 2 products to simulate the shopping cart!")

            case "7":
                print("\n--- INVENTORY REPORT ---")
                print(store.export_report())
                
                print("--- ACTIVITY LOG ---")
                print(read_activity())

            case "0":
                print("Thank you for using the TechStore Management System. Goodbye!")
                break

            case _:
                print("   [!] Invalid choice! Please enter a number from 0 to 7.")

if __name__ == "__main__":
    main()