import sqlite3

DATABASE_NAME = 'mortgage.db'

def get_db_connection():
    """Return a connection to the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Create the tables in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dni TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            capital REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS simulations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT NOT NULL,
            tae REAL NOT NULL,
            years INTEGER NOT NULL,
            monthly_payment REAL NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (dni) REFERENCES customers(dni)
        )
    """)

    conn.commit()
    conn.close()

# Create the tables in the database
create_tables()