import os
import psycopg

def courier_menu(conn: psycopg.Connection, menu: callable):

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
            name = int(input("Courier Id: "))
            check_courier_orders(conn, name)

        elif opt == 0:
            os.system('cls')
            menu()

        else:
            print("Invalid option!")

def view_couriers(conn):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM couriers")    
            rows = cursor.fetchall()
            print("\n\n Available couriers:\n")
            for x in rows:
                print(f"{x[0]}. {x[1]}") 

def add_courier(conn, courier_name):
    with conn.cursor() as cursor:      
        cursor.execute("INSERT INTO couriers (name) VALUES (%s)", (courier_name.capitalize(),))
        conn.commit()

    print("\nCourier added.\n")

def delete_courier(conn, courier_id):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM couriers WHERE id = %s", (courier_id,))
        if cursor.rowcount == 0:
            print("Error! Courier not found! Try again!")
        else:
            print("\nCourier deleted.\n")
            conn.commit()

    
def check_courier_orders(conn, courier_id):
    count = 0
    couriers = []
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM couriers")
        rows = cursor.fetchall()
        for x in rows:
            couriers.append(x[0])
        if courier_id not in couriers:
            print(couriers)
            print("Error! Courier not found! Try again!")
            return
        else:
            pass
        cursor.execute("SELECT * FROM orders WHERE courier_id = %s", (courier_id,))
        rows = cursor.fetchall()
        for x in rows:
            count += 1
            print(x)
            print("-"*100)

        if count == 0:
            print("No orders found!")
        else:
            print(f"\nThere are {count} orders for courier number: {courier_id}.\n")