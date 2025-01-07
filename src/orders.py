import os
import psycopg
from customers import update_spend

def order_menu(conn: psycopg.Connection, menu: callable):

    """
    Menu for managing orders in the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        menu (function): The function to call to go back to the main menu.

    This function provides a menu for managing orders in the database. The user can
    view all orders, create a new order, update an order's status, or view orders by
    status. The user can also go back to the main menu by selecting option 0.
    """

    while True:
        opt = int(input("\n\n1. View orders\n2. Create order\n3. Update order status\n4. Check open orders by status\n0. Main menu\n"))

        if opt == 1:
            view_orders(conn)

        elif opt == 2:
            name = input("Customer name: ")
            address = input("Customer address: ")
            phone = input("Customer phone: ")
            email = input("Customer email: ")
            try:
                courier = courier_with_lowest_orders(conn)
            except ValueError:
                print("\nNo couriers available! Add a courier first before creating an order!\n")
                continue
            items = choose_items(conn)
            id = get_customer_id(conn, name, phone, email)

            
            if len(items) == 0:
                print("\nNo items ordered! Try again!\n")
                continue
            else:
                create_order(conn, name, address, phone,email, courier, items)
                deduct_stock(conn, items)
                update_spend(conn, id, items)
                print("\nOrder created!\n")

        elif opt == 3:
            id = input("Customer Id to update: ")
            new_status = int(input("Choose status:\n1. Ready\n2. Collected\n3. Abandoned\n\nEnter option:  "))
            if new_status == 1:
                new_status = "ready"
            elif new_status == 2:
                new_status = "collected"
            elif new_status == 3:
                new_status = "abandoned"
            else:
                print("\nIncorrect choice! Try again!\n")
                continue
            update_order_status(conn, id, new_status)

        elif opt == 4:
            option = int(input("Choose order status to view all orders:\n1. Preparing\n2. Ready\n3. Collected\n4. Abandoned\n\nEnter choice: "))
            if option == 1:
                option = "preparing"
            elif option == 2:
                option = "ready"    
            elif option == 3:
                option = "collected"
            elif option == 4:
                option = "abandoned"
            else:
                print("\nIncorrect choice! Try again!\n")
                continue
            view_orders_by_status(conn, option)

        elif opt == 0:
            os.system('cls')
            menu(conn) 

        else:
            print("Invalid option!")

def view_orders(conn: psycopg.Connection):
    """
    Retrieve and display all orders from the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.

    This function fetches all order records from the database, sorted by ID, and
    displays them in a formatted table with columns for ID, Name, Email, Phone, 
    Address, Items, Status, and Courier. The table headers and each row are left-aligned.
    """

    print("\nExisting orders are:\n")
    with conn.cursor() as cursor: 
        cursor.execute("SELECT * FROM orders order by id ASC")
        rows = cursor.fetchall()
        print(f"{'ID':<5}{'Name':<20}{'Email':<35}{'Phone':<15}{'Address':<45}{'Items':<35}{'Status':<15}{'Courier':<10}\n{'_'*180}")
        for x in rows:
            print(f"{x[0]}. |{x[1]:<18} |{x[2]:<30} |{x[3]:<15} |{x[4]:<45} |{x[5]:<30}    |{x[6]:<10}  |{x[7]} ")
            print("_"*180 + '|')
            
def create_order(conn: psycopg.Connection, customer_name: str, customer_address: str, customer_phone: str, customer_email: str, courier: int, items: list):
    """
    Create a new order in the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        customer_name (str): The name of the customer.
        customer_address (str): The address of the customer.
        customer_phone (str): The phone number of the customer.
        customer_email (str): The email of the customer.
        courier (int): The ID of the courier assigned to the order.
        items (list): The list of items ordered.

    Inserts a new order into the orders table with the provided customer name, address, phone number, email, courier ID, and items, and commits the changes to the database.
    """
    order = {
        "name": customer_name.title(),
        "address": customer_address.lower(),
        "phone": customer_phone,
        "email": customer_email,
        "courier": courier,
        "status": "preparing",
        "items" : items
    }

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO orders (customer_name, customer_address, customer_phone,customer_email, courier, status, items) VALUES (%s, %s, %s, %s, %s, %s, %s)", (order["name"], order["address"], order["phone"], order["email"], order["courier"], order["status"],order["items"]))
        conn.commit()

def update_order_status(conn: psycopg.Connection, id: int, new_status: str):

    """
    Update the status of an order in the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        id (int): The ID of the order to be updated.
        new_status (str): The new status of the order.

    Checks if the order ID exists in the database. If it does, updates the order
    status and commits the changes to the database. If the order ID does not exist,
    prints an error message.
    """
    with conn.cursor() as cursor:        
        cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, id))
        if cursor.rowcount == 0:
            print("Error! Order not found! Try again!")
        else:
            conn.commit()
            print("\nOrder status updated.\n")

def view_orders_by_status(conn: psycopg.Connection, choic: str):
    
    """
    Retrieve orders from the database filtered by status and display them.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        choice (str): The status to filter orders by.

    Retrieves all orders from the database filtered by the provided status and displays them in a formatted table with
    columns for ID, Name, Email, Phone, Address, Items, Status, and Courier. The table headers are left-aligned and each row is
    also left-aligned.
    """
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM orders WHERE status = %s", (choice,))
        rows = cursor.fetchall()    
        print(f"{'ID':<5}{'Name':<20}{'Email':<35}{'Phone':<15}{'Address':<45}{'Items':<35}{'Status':<15}{'Courier':<10}\n{'_'*180}")
        for x in rows:
            print(f"{x[0]}. |{x[1]:<18} |{x[2]:<30} |{x[3]:<15} |{x[4]:<45} |{x[5]:<30}    |{x[6]:<10}  |{x[7]} ")
            print("_"*180 + '|')


def deduct_stock(conn: psycopg.Connection, items: list):
    """
    Deduct stock from each item in the provided list of items.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        items (list): A list of item names to deduct stock from.

    Deducts one from the stock of each item in the provided list and commits
    the changes to the database.
    """
    with conn.cursor() as cursor:
        for item in items:
            cursor.execute(
                "UPDATE products SET stock = stock - 1 WHERE name = %s",
                (item.title(),)  
            )

        conn.commit()

def courier_with_lowest_orders(conn: psycopg.Connection):
    """
    Retrieve the name of the courier with the lowest number of orders from the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.

    Retrieves all courier names from the couriers table and all order courier IDs from the
    orders table. Counts the number of orders each courier has and finds the courier with
    the lowest number of orders. Returns the name of this courier.
    """
    courier = []
    courier_orders = []
    courier_workload = []

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM couriers")
        rows = cursor.fetchall()
        for row in rows:
            courier.append(row[1].rstrip())            

        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()

        for row in rows:
            courier_orders.append(row[4])

        for x in courier:
            courier_workload.append(courier_orders.count(x))

    lowest_num = min(courier_workload)
    index = courier_workload.index(lowest_num)
    courier = courier[index]

    return courier
        

def choose_items(conn: psycopg.Connection):
     
    """
    Allow the user to choose items to order from the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.

    Prompts the user to enter the ID of the item to order, and checks if the item exists and is in stock.
    If the item is in stock, adds it to the order items list. If the item is out of stock, prints an error message.
    Allows the user to continue adding items until they choose to stop.
    Returns the list of items ordered.
    """
    items = []
    on = True
   
    while on:
        choice = input("Enter item Id to order: ")

        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (choice,))
            rows = cursor.fetchone()  
            if rows:
                name = rows[1]
                if rows[3] == 0:
                    print("\nOut of stock! Try again!\n")
                else:
                    items.append(name)
            else:
                print("\nProduct not found! Try again!\n")
        
        cont = input("Do you want to add another item? (y/n): ")
        if cont == "n":
            on = False
        else:
            pass

    return items

def get_customer_id(conn: psycopg.Connection, name: str, phone: str, email: str):
    """
    Check if a customer exists in the database, and if not, add them.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        name (str): The name of the customer.
        phone (str): The phone number of the customer.
        email (str): The email of the customer.

    Returns the ID of the customer, either if they existed or if they were added.
    """
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        for row in rows:
            if email == row[2]:
                return row[0]
        
        cursor.execute("INSERT INTO customers (customer_name, customer_email, customer_phone, total_spend) VALUES (%s, %s, %s, %s) RETURNING id", (name, email, phone, 0))
        id = cursor.fetchone()[0]
        return id