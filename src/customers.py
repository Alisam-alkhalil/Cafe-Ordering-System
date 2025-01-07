import os
import psycopg

def customer_menu(conn: psycopg.Connection, menu: callable):
    """
    Menu for managing customers in the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        menu (function): The function to call to go back to the main menu.

    This function provides a menu for managing customers in the database. The
    user can view all customers, add a new customer, delete a customer or update
    a customer. The user can also go back to the main menu by selecting option 0.
    """
    while True:
        opt = int(input("\n\n1. View customers\n2. Add customer\n3. Delete customer\n4. Update customer\n0. Main menu\n"))

        if opt == 1:
            view_customers(conn)

        elif opt == 2:
            name = input("Customer name: ")
            email = input("Customer email: ")
            phone = input("Customer phone: ")
            add_customer(conn, name, email, phone)

        elif opt == 3:
            id = input("Customer Id to delete: ")
            delete_customer(conn, id)

        elif opt == 4:
            id = input("Customer Id to update: ")
            choice = input("Would you like to update the name? (y/n): ").lower()
            if choice == 'y':
                new_name = input("New name: ")
            else:
                new_name = ""
            choice = input("Would you like to update the email? (y/n): ").lower()
            if choice == 'y':
                email = input("Customer email: ")
            else:
                email = ""
            choice = input("Would you like to update the phone? (y/n): ").lower()
            if choice == 'y':
                phone = input("Customer phone: ")
            else:
                phone = ""
            update_customer(conn, id, email, phone, new_name)

        elif opt == 0:
            os.system('cls')
            menu(conn)

        else:
            print("Invalid option!")

def view_customers(conn: psycopg.Connection):
    """
    Retrieve and display all customers from the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.

    This function fetches all customer records from the database and displays
    them in a formatted table with columns for ID, Name, Email, Phone, and Spending.
    The table headers and each row are left-aligned.
    """

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM customers")    
        rows = cursor.fetchall()
        print(f"""\n\n{'ID':<5}{'Name':<25}{'Email':<28}{'Phone':<11}{'Spending':<10}\n{'-'*100}""")
        for x in rows:
            print(f"{x[0]}. |{x[1]:<25} |{x[2]:<25} |{x[3]:<11} |£{x[4]:<10}")

def add_customer(conn: psycopg.Connection, customer_name: str, customer_email: str, customer_phone: str):
    """
    Add a new customer to the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        customer_name (str): The name of the customer to be added.
        customer_email (str): The email of the customer to be added.
        customer_phone (str): The phone number of the customer to be added.

    Inserts the customer with the given name, email, and phone number into the customers table, and commits the
    changes to the database. If the customer is not found, an error message is printed.
    """
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO customers (customer_name, customer_email, customer_phone) VALUES (%s, %s, %s)", (customer_name.title(), customer_email, customer_phone))
        conn.commit()

    print("\nCustomer created!\n")

def delete_customer(conn: psycopg.Connection, customer_id: int):
    """
    Delete a customer from the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        customer_id (int): The ID of the customer to be deleted.

    Deletes the customer with the given ID from the customers table, and commits the
    changes to the database. If the customer is not found, an error message is printed.
    """

    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM customers WHERE id = %s", (customer_id,))
        if cursor.rowcount == 0:
            print("Error! Customer not found! Try again!")
            return
        else:
            conn.commit()

    print("\nCustomer deleted.\n")

def update_customer(conn: psycopg.Connection, id: int, email: str, phone: str, new_name: str):
    """
    Update a customer in the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        id (int): The ID of the customer to be updated.
        email (str): The new email of the customer to be updated.
        phone (str): The new phone number of the customer to be updated.
        new_name (str): The new name of the customer to be updated.

    Updates the customer with the given ID in the customers table, and commits the
    changes to the database. If the customer is not found, an error message is printed.
    """
    with conn.cursor() as cursor:
        if len(email) > 0:
            cursor.execute("UPDATE customers SET customer_email = %s WHERE id = %s", (email, id))
        if len(phone) > 0:
            cursor.execute("UPDATE customers SET customer_phone = %s WHERE id = %s", (phone, id))
        if len(new_name) > 0:
            cursor.execute("UPDATE customers SET customer_name = %s WHERE id = %s", (new_name, id))

        if cursor.rowcount == 0:
            print("Error! Customer not found! Try again!")
            return
        else:
            conn.commit()
            print("\nCustomer updated.\n")

def update_spend(conn: psycopg.Connection, id, items):
    """
    Update the total spend and number of orders for a customer.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        id (int): The ID of the customer whose spend and orders need to be updated.
        items (list of str): A list of item names representing the products purchased by the customer.

    This function calculates the total spend for the given items by summing their prices
    from the products table. It then updates the customer's total spend and increments
    the number of orders in the customers table. The changes are committed to the database.
    """

    totalspend = 0
    with conn.cursor() as cursor:
        for item in items:
            cursor.execute(
                "SELECT price FROM products WHERE name = %s",
                (item.title(),)
            )
            rows = cursor.fetchall()
            for x in rows:
                totalspend += x[0]

        cursor.execute(
            "UPDATE customers SET total_spend = total_spend + %s WHERE id = %s",
            (totalspend, id,)
        )
            
        conn.commit()