import mysql.connector
import csv

# 1. Database Connection Details
db_config = {
    'host': 'localhost',      # server name
    'user': 'root',  # MySQL username
    'password': 'paswrd', 
    'database': 'userdb'  # Ensure this database exists first
}

def setup_and_import_csv():
    try:
        # 1. Connect to MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="paswrd",
            database="userdb"
        )
        cursor = conn.cursor()

        # 2. Create the table if it doesn't exist
        # We use backticks (`) because names like "Index" and "Organization Id" are reserved or have spaces
        create_table_query = """
        CREATE TABLE IF NOT EXISTS userdetails (
            `Index` INT,
            `Organization Id` VARCHAR(255),
            Name VARCHAR(255),
            Website VARCHAR(255),
            Country VARCHAR(100),
            Description TEXT,
            Founded YEAR,
            Industry VARCHAR(255),
            `Number of employees` INT
        )
        """
        cursor.execute(create_table_query)
        print("Table 'userdetails' is ready.")

        # 3. Read and insert CSV data
        with open('organizations-100000.csv', mode='r', encoding='utf-8') as file:
            csv_data = csv.reader(file)
            next(csv_data)  # Skip the header row

            insert_query = """
            INSERT INTO userdetails (
                `Index`, `Organization Id`, Name, Website, Country, 
                Description, Founded, Industry, `Number of employees`
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Convert reader to list for executemany
            rows = list(csv_data)
            cursor.executemany(insert_query, rows)

        conn.commit()
        print(f"Successfully imported {cursor.rowcount} records.")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    setup_and_import_csv()

