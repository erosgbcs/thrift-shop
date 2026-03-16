from datetime import datetime
from typing import List, Dict, Optional, Any

class ThriftShopSystem:
    def __init__(self):
        """Initialize the thrift shop system with in-memory data structures."""
        # In-memory databases
        self.categories = []
        self.clothing_items = []
        self.sales_transactions = []
        self.transaction_details = []
        
        # Auto-increment counters
        self.next_category_id = 1
        self.next_item_id = 1
        self.next_transaction_id = 1
        
        # Initialize with default categories
        self._initialize_default_categories()
    
    def _initialize_default_categories(self):
        """Add default categories to the system."""
        default_categories = [
            'Shirts', 'Pants', 'Dresses', 'Jackets', 'Shoes', 'Accessories'
        ]
        for category_name in default_categories:
            self.categories.append({
                'CategoryID': self.next_category_id,
                'CategoryName': category_name
            })
            self.next_category_id += 1
    
    # ============= CATEGORY MANAGEMENT =============
    
    def add_category(self, category_name):
        """Add a new category."""
        # Check if category already exists
        for cat in self.categories:
            if cat['CategoryName'].lower() == category_name.lower():
                print(f"Category '{category_name}' already exists!")
                return False
        
        new_category = {
            'CategoryID': self.next_category_id,
            'CategoryName': category_name
        }
        self.categories.append(new_category)
        self.next_category_id += 1
        
        print(f"Category '{category_name}' added successfully with ID {new_category['CategoryID']}.")
        return True
    
    def get_all_categories(self):
        """Retrieve all categories."""
        return self.categories.copy()
    
    def get_category_by_id(self, category_id):
        """Get a category by its ID."""
        for category in self.categories:
            if category['CategoryID'] == category_id:
                return category.copy()
        return None
    
    def get_category_by_name(self, category_name):
        """Get a category by its name."""
        for category in self.categories:
            if category['CategoryName'].lower() == category_name.lower():
                return category.copy()
        return None
    
    # ============= CLOTHING ITEM MANAGEMENT =============
    
    def add_clothing_item(self, item_name, size, condition, price, category_id):
        """Add a new clothing item."""
        # Verify category exists
        category = self.get_category_by_id(category_id)
        if not category:
            print(f"Category ID {category_id} does not exist!")
            return False
        
        new_item = {
            'ItemID': self.next_item_id,
            'ItemName': item_name,
            'Size': size,
            'Condition': condition,
            'Price': float(price),
            'Status': 'Available',
            'CategoryID': category_id
        }
        self.clothing_items.append(new_item)
        self.next_item_id += 1
        
        print(f"Clothing item '{item_name}' added successfully with ID {new_item['ItemID']}.")
        return True
    
    def get_all_clothing_items(self):
        """Retrieve all clothing items."""
        return [item.copy() for item in self.clothing_items]
    
    def get_clothing_item_by_id(self, item_id):
        """Get a clothing item by its ID."""
        for item in self.clothing_items:
            if item['ItemID'] == item_id:
                return item.copy()
        return None
    
    def search_clothing_items(self, search_term, search_by='ItemName'):
        """Search clothing items by various criteria."""
        results = []
        search_term = search_term.lower()
        
        for item in self.clothing_items:
            if search_by == 'ItemName' and search_term in item['ItemName'].lower():
                results.append(item.copy())
            elif search_by == 'Size' and search_term in item['Size'].lower():
                results.append(item.copy())
            elif search_by == 'Condition' and search_term in item['Condition'].lower():
                results.append(item.copy())
            elif search_by == 'Status' and search_term in item['Status'].lower():
                results.append(item.copy())
            elif search_by == 'CategoryID' and str(item['CategoryID']) == search_term:
                results.append(item.copy())
        
        return results
    
    def update_clothing_item(self, item_id, **kwargs):
        """Update a clothing item's information."""
        for i, item in enumerate(self.clothing_items):
            if item['ItemID'] == item_id:
                # Update provided fields
                for key, value in kwargs.items():
                    if key in item:
                        if key == 'Price':
                            item[key] = float(value)
                        elif key == 'CategoryID':
                            # Verify category exists
                            if not self.get_category_by_id(int(value)):
                                print(f"Category ID {value} does not exist!")
                                return False
                            item[key] = int(value)
                        else:
                            item[key] = value
                
                print(f"Item ID {item_id} updated successfully.")
                return True
        
        print(f"Item ID {item_id} not found.")
        return False
    
    def delete_clothing_item(self, item_id):
        """Delete a clothing item (only if not sold)."""
        # Check if item exists and is not sold
        item_index = None
        for i, item in enumerate(self.clothing_items):
            if item['ItemID'] == item_id:
                if item['Status'] == 'Sold':
                    print(f"Cannot delete item ID {item_id} because it has been sold.")
                    return False
                item_index = i
                break
        
        if item_index is None:
            print(f"Item ID {item_id} not found.")
            return False
        
        # Remove the item
        deleted_item = self.clothing_items.pop(item_index)
        print(f"Item '{deleted_item['ItemName']}' (ID: {item_id}) deleted successfully.")
        return True
    
    # ============= SALES TRANSACTION MANAGEMENT =============
    
    def create_transaction(self, item_ids):
        """Create a new sales transaction with multiple items."""
        if not item_ids:
            print("No items selected for transaction.")
            return False
        
        # Verify all items exist and are available
        items_to_sell = []
        total_amount = 0
        
        for item_id in item_ids:
            item = self.get_clothing_item_by_id(item_id)
            if not item:
                print(f"Item ID {item_id} not found.")
                return False
            if item['Status'] != 'Available':
                print(f"Item '{item['ItemName']}' (ID: {item_id}) is not available.")
                return False
            items_to_sell.append(item)
            total_amount += item['Price']
        
        # Create transaction
        transaction_id = self.next_transaction_id
        transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Save transaction
        self.sales_transactions.append({
            'TransactionID': transaction_id,
            'TransactionDate': transaction_date,
            'TotalAmount': total_amount
        })
        
        # Save transaction details and update item status
        for item in items_to_sell:
            self.transaction_details.append({
                'TransactionID': transaction_id,
                'ItemID': item['ItemID'],
                'SellingPrice': item['Price']
            })
            # Update item status to Sold
            self.update_clothing_item(item['ItemID'], Status='Sold')
        
        self.next_transaction_id += 1
        
        print(f"Transaction #{transaction_id} created successfully!")
        print(f"Date: {transaction_date}")
        print(f"Total Amount: ${total_amount:.2f}")
        print(f"Items sold: {len(items_to_sell)}")
        
        return transaction_id
    
    def get_all_transactions(self):
        """Retrieve all sales transactions."""
        return [trans.copy() for trans in self.sales_transactions]
    
    def get_transaction_details(self, transaction_id):
        """Get details of a specific transaction."""
        details = []
        for detail in self.transaction_details:
            if detail['TransactionID'] == transaction_id:
                item = self.get_clothing_item_by_id(detail['ItemID'])
                details.append({
                    'TransactionID': detail['TransactionID'],
                    'ItemID': detail['ItemID'],
                    'ItemName': item['ItemName'] if item else 'Unknown',
                    'SellingPrice': detail['SellingPrice']
                })
        return details
    
    # ============= REPORT GENERATION =============
    
    def generate_daily_sales_report(self, date=None):
        """Generate daily sales report."""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        daily_transactions = []
        total_sales = 0
        items_sold = 0
        
        for trans in self.sales_transactions:
            if trans['TransactionDate'].startswith(date):
                daily_transactions.append(trans)
                total_sales += trans['TotalAmount']
                details = self.get_transaction_details(trans['TransactionID'])
                items_sold += len(details)
        
        print("\n" + "="*50)
        print(f"DAILY SALES REPORT - {date}")
        print("="*50)
        print(f"Total Transactions: {len(daily_transactions)}")
        print(f"Total Items Sold: {items_sold}")
        print(f"Total Sales: ${total_sales:.2f}")
        print("-"*50)
        
        for trans in daily_transactions:
            print(f"Transaction #{trans['TransactionID']}: ${trans['TotalAmount']:.2f}")
            details = self.get_transaction_details(trans['TransactionID'])
            for detail in details:
                print(f"  - {detail['ItemName']}: ${detail['SellingPrice']:.2f}")
        
        return daily_transactions
    
    def generate_inventory_report(self):
        """Generate inventory summary report."""
        # Count by status
        available_items = [item for item in self.clothing_items if item['Status'] == 'Available']
        sold_items = [item for item in self.clothing_items if item['Status'] == 'Sold']
        
        # Count by category
        category_counts = {}
        category_values = {}
        
        for category in self.categories:
            cat_id = category['CategoryID']
            cat_items = [item for item in self.clothing_items if item['CategoryID'] == cat_id]
            category_counts[category['CategoryName']] = len(cat_items)
            
            # Calculate total value of available items
            available_cat_items = [item for item in cat_items if item['Status'] == 'Available']
            category_values[category['CategoryName']] = sum(item['Price'] for item in available_cat_items)
        
        print("\n" + "="*50)
        print("INVENTORY SUMMARY REPORT")
        print("="*50)
        print(f"Total Items in Inventory: {len(self.clothing_items)}")
        print(f"Available Items: {len(available_items)}")
        print(f"Sold Items: {len(sold_items)}")
        print(f"Total Inventory Value (Available): ${sum(item['Price'] for item in available_items):.2f}")
        print("-"*50)
        print("ITEMS BY CATEGORY:")
        for category, count in category_counts.items():
            print(f"  {category}: {count} items (Value: ${category_values[category]:.2f})")
    
    def generate_sold_items_report(self):
        """Generate report of all sold items."""
        sold_items = [item for item in self.clothing_items if item['Status'] == 'Sold']
        
        print("\n" + "="*50)
        print("SOLD ITEMS REPORT")
        print("="*50)
        
        if not sold_items:
            print("No items have been sold yet.")
            return
        
        total_revenue = 0
        for item in sold_items:
            category = self.get_category_by_id(item['CategoryID'])
            cat_name = category['CategoryName'] if category else 'Unknown'
            print(f"ID: {item['ItemID']} | {item['ItemName']} | Size: {item['Size']} | "
                  f"Condition: {item['Condition']} | Price: ${item['Price']:.2f} | "
                  f"Category: {cat_name}")
            total_revenue += item['Price']
        
        print("-"*50)
        print(f"Total Sold Items: {len(sold_items)}")
        print(f"Total Revenue: ${total_revenue:.2f}")
    
    def generate_available_items_report(self):
        """Generate report of all available items."""
        available_items = [item for item in self.clothing_items if item['Status'] == 'Available']
        
        print("\n" + "="*50)
        print("AVAILABLE ITEMS REPORT")
        print("="*50)
        
        if not available_items:
            print("No items are currently available.")
            return
        
        # Group by category
        for category in self.categories:
            cat_items = [item for item in available_items if item['CategoryID'] == category['CategoryID']]
            if cat_items:
                print(f"\n{category['CategoryName']}:")
                for item in cat_items:
                    print(f"  ID: {item['ItemID']} | {item['ItemName']} | Size: {item['Size']} | "
                          f"Condition: {item['Condition']} | Price: ${item['Price']:.2f}")
        
        print("-"*50)
        print(f"Total Available Items: {len(available_items)}")
        print(f"Total Value: ${sum(item['Price'] for item in available_items):.2f}")
    
    def generate_category_summary(self):
        """Generate inventory summary per category."""
        print("\n" + "="*50)
        print("CATEGORY SUMMARY REPORT")
        print("="*50)
        
        for category in self.categories:
            cat_items = [item for item in self.clothing_items if item['CategoryID'] == category['CategoryID']]
            available_cat_items = [item for item in cat_items if item['Status'] == 'Available']
            sold_cat_items = [item for item in cat_items if item['Status'] == 'Sold']
            
            print(f"\n{category['CategoryName']}:")
            print(f"  Total Items: {len(cat_items)}")
            print(f"  Available: {len(available_cat_items)}")
            print(f"  Sold: {len(sold_cat_items)}")
            if available_cat_items:
                print(f"  Average Price (Available): ${sum(item['Price'] for item in available_cat_items)/len(available_cat_items):.2f}")
            if sold_cat_items:
                print(f"  Revenue from Sold: ${sum(item['Price'] for item in sold_cat_items):.2f}")


# ============= MAIN MENU INTERFACE =============

def main():
    """Main menu interface for the thrift shop system."""
    shop = ThriftShopSystem()
    
    while True:
        print("\n" + "="*50)
        print("THRIFT SHOP MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add Category")
        print("2. Add Clothing Item")
        print("3. View All Items")
        print("4. Search Items")
        print("5. Update Item")
        print("6. Delete Item")
        print("7. Create Sales Transaction")
        print("8. View Transactions")
        print("9. Generate Reports")
        print("10. View Categories")
        print("11. Exit")
        print("-"*50)
        
        choice = input("Enter your choice (1-11): ").strip()
        
        if choice == '1':
            # Add Category
            name = input("Enter category name: ").strip()
            shop.add_category(name)
        
        elif choice == '2':
            # Add Clothing Item
            categories = shop.get_all_categories()
            if not categories:
                print("Please add a category first!")
                continue
            
            print("\nAvailable Categories:")
            for cat in categories:
                print(f"  {cat['CategoryID']}: {cat['CategoryName']}")
            
            try:
                name = input("Enter item name: ").strip()
                size = input("Enter size: ").strip()
                condition = input("Enter condition (New/Like New/Good/Fair): ").strip()
                price = float(input("Enter price: "))
                cat_id = int(input("Enter category ID: "))
                
                shop.add_clothing_item(name, size, condition, price, cat_id)
            except ValueError:
                print("Invalid input! Please enter valid numbers.")
        
        elif choice == '3':
            # View All Items
            items = shop.get_all_clothing_items()
            if not items:
                print("No items in inventory.")
            else:
                print("\nALL ITEMS:")
                for item in items:
                    category = shop.get_category_by_id(item['CategoryID'])
                    cat_name = category['CategoryName'] if category else 'Unknown'
                    print(f"ID: {item['ItemID']} | {item['ItemName']} | Size: {item['Size']} | "
                          f"Condition: {item['Condition']} | Price: ${item['Price']:.2f} | "
                          f"Status: {item['Status']} | Category: {cat_name}")
        
        elif choice == '4':
            # Search Items
            print("\nSearch by:")
            print("1. Item Name")
            print("2. Size")
            print("3. Condition")
            print("4. Status")
            search_choice = input("Choose search type (1-4): ").strip()
            
            search_fields = {
                '1': 'ItemName',
                '2': 'Size',
                '3': 'Condition',
                '4': 'Status'
            }
            
            if search_choice in search_fields:
                term = input(f"Enter {search_fields[search_choice]} to search: ").strip()
                results = shop.search_clothing_items(term, search_fields[search_choice])
                
                if not results:
                    print("No items found.")
                else:
                    print(f"\nFound {len(results)} item(s):")
                    for item in results:
                        category = shop.get_category_by_id(item['CategoryID'])
                        cat_name = category['CategoryName'] if category else 'Unknown'
                        print(f"ID: {item['ItemID']} | {item['ItemName']} | Size: {item['Size']} | "
                              f"Condition: {item['Condition']} | Price: ${item['Price']:.2f} | "
                              f"Status: {item['Status']} | Category: {cat_name}")
        
        elif choice == '5':
            # Update Item
            try:
                item_id = int(input("Enter item ID to update: "))
                item = shop.get_clothing_item_by_id(item_id)
                
                if not item:
                    print(f"Item ID {item_id} not found.")
                    continue
                
                print(f"\nUpdating: {item['ItemName']}")
                print("Leave blank to keep current value.")
                
                updates = {}
                
                new_name = input(f"New name [{item['ItemName']}]: ").strip()
                if new_name:
                    updates['ItemName'] = new_name
                
                new_size = input(f"New size [{item['Size']}]: ").strip()
                if new_size:
                    updates['Size'] = new_size
                
                new_condition = input(f"New condition [{item['Condition']}]: ").strip()
                if new_condition:
                    updates['Condition'] = new_condition
                
                new_price = input(f"New price [{item['Price']}]: ").strip()
                if new_price:
                    updates['Price'] = float(new_price)
                
                new_status = input(f"New status [{item['Status']}] (Available/Sold): ").strip()
                if new_status and new_status in ['Available', 'Sold']:
                    updates['Status'] = new_status
                
                if updates:
                    shop.update_clothing_item(item_id, **updates)
                else:
                    print("No updates provided.")
            
            except ValueError:
                print("Invalid input!")
        
        elif choice == '6':
            # Delete Item
            try:
                item_id = int(input("Enter item ID to delete: "))
                shop.delete_clothing_item(item_id)
            except ValueError:
                print("Invalid item ID!")
        
        elif choice == '7':
            # Create Sales Transaction
            items = shop.get_all_clothing_items()
            available_items = [item for item in items if item['Status'] == 'Available']
            
            if not available_items:
                print("No available items to sell.")
                continue
            
            print("\nAVAILABLE ITEMS:")
            for item in available_items:
                category = shop.get_category_by_id(item['CategoryID'])
                cat_name = category['CategoryName'] if category else 'Unknown'
                print(f"ID: {item['ItemID']} | {item['ItemName']} | Size: {item['Size']} | "
                      f"Price: ${item['Price']:.2f} | Category: {cat_name}")
            
            try:
                item_ids_input = input("\nEnter item IDs to sell (comma-separated): ").strip()
                item_ids = [int(id.strip()) for id in item_ids_input.split(',') if id.strip()]
                shop.create_transaction(item_ids)
            except ValueError:
                print("Invalid input! Please enter valid item IDs.")
        
        elif choice == '8':
            # View Transactions
            transactions = shop.get_all_transactions()
            if not transactions:
                print("No transactions found.")
            else:
                print("\nALL TRANSACTIONS:")
                for trans in transactions:
                    print(f"ID: {trans['TransactionID']} | Date: {trans['TransactionDate']} | "
                          f"Total: ${trans['TotalAmount']:.2f}")
                
                # Option to view details
                view_details = input("\nView transaction details? (Enter Transaction ID or 'no'): ").strip()
                if view_details.lower() != 'no' and view_details.isdigit():
                    details = shop.get_transaction_details(int(view_details))
                    if details:
                        print(f"\nTransaction #{view_details} Details:")
                        for detail in details:
                            print(f"  - {detail['ItemName']}: ${detail['SellingPrice']:.2f}")
        
        elif choice == '9':
            # Generate Reports
            while True:
                print("\nREPORTS MENU:")
                print("1. Daily Sales Report")
                print("2. Sold Items Report")
                print("3. Available Items Report")
                print("4. Category Summary")
                print("5. Inventory Summary")
                print("6. Back to Main Menu")
                
                report_choice = input("Enter choice (1-6): ").strip()
                
                if report_choice == '1':
                    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
                    shop.generate_daily_sales_report(date if date else None)
                
                elif report_choice == '2':
                    shop.generate_sold_items_report()
                
                elif report_choice == '3':
                    shop.generate_available_items_report()
                
                elif report_choice == '4':
                    shop.generate_category_summary()
                
                elif report_choice == '5':
                    shop.generate_inventory_report()
                
                elif report_choice == '6':
                    break
                
                else:
                    print("Invalid choice!")
        
        elif choice == '10':
            # View Categories
            categories = shop.get_all_categories()
            if not categories:
                print("No categories found.")
            else:
                print("\nCATEGORIES:")
                for cat in categories:
                    print(f"ID: {cat['CategoryID']} | {cat['CategoryName']}")
        
        elif choice == '11':
            print("Thank you for using Thrift Shop Management System!")
            break
        
        else:
            print("Invalid choice! Please enter a number between 1 and 11.")


if __name__ == "__main__":
    main()
