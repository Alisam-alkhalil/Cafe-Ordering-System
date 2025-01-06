import sys
import os
import psycopg
import pandas as pd
from dotenv import load_dotenv
from src.database import create_database
from graphics.ascii import welcome, products, couriers, orders, customers

load_dotenv()

dbname = os.getenv('POSTGRES_DB')
host = os.getenv('POSTGRES_HOST')
port = os.getenv('POSTGRES_PORT')
user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')

conn = psycopg.connect(
    dbname=dbname,
    host=host,
    port=port,
    user=user,
    password=password
    
)

def main():
    create_database(conn)
        
    print(welcome)

    while True:
        opt = int(input("To open the products menu, type '1'\nTo open the orders menu, type '2'\nTo open the couriers menu, type '3'\nTo export data to CSV, type '4'\nTo open the customers menu, type '5'\nTo exit the app, type '0'\n"))

        if opt == 1:
            os.system('cls')
            print(products)
            product_menu(product_manager)
        elif opt == 2:
            os.system('cls')
            print(orders)
            order_menu(order_manager, customer_manager)
        elif opt == 3:
            os.system('cls')
            print(couriers)
            courier_menu(courier_manager)
        elif opt == 4:
            query = "SELECT * FROM orders"
            df = pd.read_sql_query(query, conn)
            df.to_csv('orders.csv', index=False)
            query = "SELECT * FROM products"
            df = pd.read_sql_query(query, conn)
            df.to_csv('products.csv', index=False)
            query = "SELECT * FROM couriers"
            df = pd.read_sql_query(query, conn)
            df.to_csv('couriers.csv', index=False)
            query = "SELECT * FROM customers"
            df = pd.read_sql_query(query, conn)
            df.to_csv('customers.csv', index=False)
            print("\nData exported!\n")
        elif opt == 5:
            os.system('cls')
            print(customers)
            customer_menu(customer_manager)
        elif opt == 0:
            os.system('cls')
            exit()     
        else:
            print("\nInvalid option!")

if __name__ == '__main__':
    main()