import psycopg

def create_database(conn: psycopg.Connection):
    """Create the tables in the PostgreSQL database if they don't already exist.

    Args:
        conn (psycopg2.extensions.connection): A connection to the PostgreSQL database.
    """
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS products (id SERIAL PRIMARY KEY, name VARCHAR(255), price DECIMAL)")
    cur.execute("CREATE TABLE IF NOT EXISTS orders (id SERIAL PRIMARY KEY, customer_name VARCHAR(255), customer_email VARCHAR(255), customer_phone VARCHAR(255), items VARCHAR(255), status VARCHAR(255), courier_id INT)")
    cur.execute("CREATE TABLE IF NOT EXISTS customers (id SERIAL PRIMARY KEY, customer_name VARCHAR(255), customer_email VARCHAR(255), customer_phone VARCHAR(255))")
    cur.execute("CREATE TABLE IF NOT EXISTS couriers (id SERIAL PRIMARY KEY, name VARCHAR(255))")

    conn.commit()