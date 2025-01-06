import psycopg

def create_database(conn: psycopg.Connection):
    """Create the tables in the PostgreSQL database if they don't already exist.

    Args:
        conn (psycopg2.extensions.connection): A connection to the PostgreSQL database.
    """
    with conn as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS products (id SERIAL PRIMARY KEY, name VARCHAR(255), price DECIMAL)")
        cur.execute("CREATE TABLE IF NOT EXISTS orders (id SERIAL PRIMARY KEY, product_name VARCHAR(255), quantity INT, customer_id INT, courier_id INT)")
        cur.execute("CREATE TABLE IF NOT EXISTS customers (id SERIAL PRIMARY KEY, name VARCHAR(255), address VARCHAR(255), phone VARCHAR(255), email VARCHAR(255))")
        cur.execute("CREATE TABLE IF NOT EXISTS couriers (id SERIAL PRIMARY KEY, name VARCHAR(255))")
