import os
import psycopg

def product_menu(conn: psycopg.Connection, menu: callable):
    """
    Menu for managing products in the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        menu (function): The function to call to go back to the main menu.

    This function provides a menu for managing products in the database. The
    user can view all products, create a new product, update a product or delete
    a product. The user can also go back to the main menu by selecting option 0.
    """
    while True:

        opt = int(input("\n\n1. View products\n2. Create product\n3. Update product\n4. Delete product\n0. Main menu\n"))

        if opt == 1:
            view_products(conn)

        elif opt == 2:
            new_product = input("Enter new product name: ")
            new_price = input("Enter new product price: ")
            stock = input("Enter new product stock Qty: ")
            create_product(new_product, new_price,stock, conn)

        elif opt == 3:
            to_update = int(input("Enter product Id to update: "))
            choice = input("Would you like to update the name? (y/n): ").lower()
            if choice == 'y':
                new_update = input("Enter new product name: ")
            else:
                new_update = ''
            choice = input("Would you like to update the price? (y/n): ").lower()
            if choice == 'y':
                new_price = input("Enter new product price: ")
            else:
                new_price = ''
            choice = input("Would you like to update the stock? (y/n): ").lower()
            if choice == 'y':
                new_stock = input("Enter new product stock: ")
            else:
                new_stock = ''
            update_product(to_update, new_update.capitalize(), new_price, new_stock, conn)

        elif opt == 4:
            to_delete = int(input("Enter product Id to delete: "))
            delete_product(to_delete, conn)

        elif opt == 0:
            os.system('cls')
            menu(conn)

        else:
            print("Invalid option!")

def view_products(conn: psycopg.Connection):

        """
        Retrieve all products from the database and display them.

        Args:
            conn (psycopg.Connection): A connection to the PostgreSQL database.

        Retrieves all products from the database, sorted by ID, and displays them in a formatted table with
        columns for ID, Name, Price, and Quantity in Stock. The table headers are left-aligned and each row is
        also left-aligned.
        """
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products ORDER BY id ASC")
            rows = cursor.fetchall()

            print(f"\nOur available products are:\n")
            print(f"{'ID':<5}{'Name':<25}{'Price':<10}{'Qty in Stock':<10}")
            for x in rows:
                print(f"{x[0]:<}. {x[1]:<25}  £{x[2]:<10}  {x[3]:<10}")

def create_product(new_product: str, new_price: float, stock: int, conn: psycopg.Connection):
    """
    Add a new product to the database.

    Args:
        new_product (str): The name of the new product.
        new_price (Decimal): The price of the new product.
        stock (int): The stock quantity of the new product.
        conn (psycopg.Connection): A connection to the PostgreSQL database.

    Inserts the new product with its name, price, and stock quantity into the products table, and commits the changes to the database.
    """

    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)", (new_product.title(), new_price, stock))
        conn.commit()
        print("\nProduct created!\n")


def update_product(to_update: int, new_update: str, new_price: float, new_stock: int, conn: psycopg.Connection):
    """
    Update the details of a product in the database using its ID.

    Args:
        to_update (int): The ID of the product to be updated.
        new_update (str): The new name of the product. If not updating, pass an empty string.
        new_price (str): The new price of the product. If not updating, pass an empty string.
        new_stock (str): The new stock quantity of the product. If not updating, pass an empty string.
        conn (psycopg.Connection): A connection to the PostgreSQL database.

    Updates the product's name, price, and/or stock if specified, and commits the changes to the database.
    If the product ID does not exist, prints a message indicating the product was not found.
    """

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        names = []
        for x in rows:
            names.append(x[0])

        if to_update in names:
            
            if len(new_update) > 0:
                cursor.execute("UPDATE products SET name = %s WHERE id = %s", (new_update.title(), to_update,))
            if len(new_price) > 0:
                cursor.execute("UPDATE products SET price = %s WHERE id = %s", (new_price, to_update,))
            if len(new_stock) > 0:
                cursor.execute("UPDATE products SET stock = %s WHERE id = %s", (new_stock, to_update,))

            conn.commit()
            print("\nProduct updated!\n")
        else:
            print("\nProduct to update not found! Try again!\n")
        cursor.execute("SELECT setval('products_id_seq', (SELECT MAX(id) FROM products));")
        conn.commit()

def delete_product(to_delete: int, conn: psycopg.Connection):

    """
    Delete a product from the database by its ID.

    Args:
        to_delete (int): The ID of the product to be deleted.
        conn (psycopg.Connection): A connection to the PostgreSQL database.

    The function checks if the product ID exists in the database. If it does, 
    it deletes the product and updates the products_id_seq. If the product 
    is not found, it notifies the user.
    """

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        names = []
        for x in rows:
            names.append(x[0])

        if to_delete in names:
            cursor.execute("DELETE FROM products WHERE id = %s", (to_delete,))
            conn.commit()
            print("\nProduct deleted.\n")
        else:
            print("\nProduct to delete not found! Try again!\n")
        
        cursor.execute("SELECT setval('products_id_seq', (SELECT MAX(id) FROM products));")
        conn.commit()