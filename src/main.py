import os
import psycopg
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from database import create_database
from graphics.ascii import welcome, products, couriers, orders, customers
from products import product_menu
from orders import order_menu
from couriers import courier_menu
from customers import customer_menu

load_dotenv()

dbname = os.getenv('POSTGRES_DB')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')

def menu(conn):
    create_database(conn)
        
    print(welcome)

    while True:

        opt = int(input("To open the products menu, type '1'\nTo open the orders menu, type '2'\n\
To open the couriers menu, type '3'\nTo open the customers menu, type '4'\n\
To export data to CSV, type '5'\nTo exit the app, type '0'\n"))

        if opt == 1:
            os.system('cls')
            print(products)
            product_menu(conn, menu)

        elif opt == 2:
            os.system('cls')
            print(orders)
            order_menu(conn, menu)

        elif opt == 3:
            os.system('cls')
            print(couriers)
            courier_menu(conn, menu)

        elif opt == 4:
            os.system('cls')
            print(customers)
            customer_menu(conn, menu)

        elif opt == 5:
            timestamp = datetime.now().strftime('%Y-%m-%d')
            query = "SELECT * FROM orders"
            df = pd.read_sql_query(query, conn)
            df.to_csv(f'csv/orders_{timestamp}.csv', index=False)
            query = "SELECT * FROM products"
            df = pd.read_sql_query(query, conn)
            df.to_csv(f'csv/products_{timestamp}.csv', index=False)
            query = "SELECT * FROM couriers"
            df = pd.read_sql_query(query, conn)
            df.to_csv(f'csv/couriers_{timestamp}.csv', index=False)
            query = "SELECT * FROM customers"
            df = pd.read_sql_query(query, conn)
            df.to_csv(f'csv/customers_{timestamp}.csv', index=False)
            print("\nData exported!\n")

        elif opt == 0:
            os.system('cls')
            conn.close()
            exit()

        else:
            print("\nInvalid option!\n")

if __name__ == '__main__':
    try:
        conn = psycopg.connect(dbname=dbname, host=host, port=port, user=user, password=password)
        menu(conn)
    finally:
        conn.close()
