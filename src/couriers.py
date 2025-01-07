import os
import psycopg

def courier_menu(conn: psycopg.Connection, menu: callable):

    """
    Menu for managing couriers in the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        menu (function): The function to call to go back to the main menu.

    This function provides a menu for managing couriers in the database. The
    user can view all couriers, add a new courier, delete a courier or open
    orders by courier. The user can also go back to the main menu by selecting
    option 0.
    """
    while True:

        opt = int(input("\n\n1. View couriers\n2. Add courier\n3. Delete courier\n4. Open orders by courier\n0. Main menu\n"))

        if opt == 1:
            view_couriers(conn)

        elif opt == 2:
            name = input("Courier name: ")
            add_courier(conn, name)

        elif opt == 3:
            id = input("Courier Id to delete: ")
            delete_courier(conn, id)

        elif opt == 4:
            id = int(input("Courier Id: "))
            check_courier_orders(conn, id)

        elif opt == 0:
            os.system('cls')
            menu(conn)

        else:
            print("Invalid option!")

def view_couriers(conn):
        
        """
        Retrieve all couriers from the database and display them.

        Args:
            conn (psycopg.Connection): A connection to the PostgreSQL database.

        Retrieves all couriers from the database and displays them in a formatted
        table with columns for ID and Name. The table headers are left-aligned and
        each row is also left-aligned.
        """
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM couriers")    
            rows = cursor.fetchall()
            print("\n\n Available couriers:\n")
            
            for x in rows:
                print(f"{x[0]}. {x[1]}") 

def add_courier(conn, courier_name):

    """
    Add a new courier to the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        courier_name (str): The name of the courier to be added.

    Inserts a new courier into the couriers table with the given name,
    capitalizing the first letter, and commits the changes to the database.
    """

    with conn.cursor() as cursor:      
        cursor.execute("INSERT INTO couriers (name) VALUES (%s)", (courier_name.capitalize(),))
        conn.commit()

    print("\nCourier added.\n")

def delete_courier(conn, courier_id):

    """
    Delete a courier from the database.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        courier_id (int): The ID of the courier to be deleted.

    Deletes the courier with the given ID from the couriers table and commits the
    changes to the database. If the courier is not found, an error message is printed.
    """
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM couriers WHERE id = %s", (courier_id,))

        if cursor.rowcount == 0:
            print("Error! Courier not found! Try again!")
        else:
            print("\nCourier deleted.\n")
            conn.commit()

    
def check_courier_orders(conn, id):

    """
    Check and display orders for a specific courier.

    Args:
        conn (psycopg.Connection): A connection to the PostgreSQL database.
        courier_name (str): The name of the courier whose orders need to be checked.

    This function retrieves and displays all orders associated with the specified
    courier ID. It first checks if the courier ID exists in the database. If not
    found, it prints an error message. If the courier ID is valid, it retrieves
    orders for that courier and displays each order. Additionally, it prints the
    total number of orders found for the specified courier. If no orders are found,
    it notifies the user.
    """

    count = 0
    couriers = {}

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM couriers")
        rows = cursor.fetchall()

        for x in rows:
            couriers[x[0]] = x[1]

        try:
            courier_name = couriers[id]
        except KeyError:
            print("Error! Courier not found! Try again!")
            return   

        cursor.execute("SELECT * FROM orders WHERE courier = %s", (courier_name,))
        rows = cursor.fetchall()

        for x in rows:
            count += 1
            print(x)
            print("-"*100)

        if count == 0:
            print("No orders found!")
        else:
            print(f"\nThere are {count} orders for courier: {courier_name}.\n")