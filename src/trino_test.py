import trino

def main():
    # Create a Trino connection (dbapi interface)
    conn = trino.dbapi.connect(
        host='localhost',
        port=8080,
        user='admin',        # can be anything
        catalog='hive',      # matching hive connector
        schema='default',    # "default" schema
    )

    cursor = conn.cursor()

    # 1. Show catalogs
    cursor.execute("SHOW CATALOGS")
    catalogs = cursor.fetchall()
    print("Catalogs:", catalogs)

    # 2. Show schemas in 'hive'
    cursor.execute("SHOW SCHEMAS IN hive")
    schemas = cursor.fetchall()
    print("Schemas in hive:", schemas)

    # 3. Simple query (e.g., SELECT 1)
    cursor.execute("SELECT 1")
    result = cursor.fetchall()
    print("SELECT 1 result:", result)

    # If you have a table created, you could do:
    # cursor.execute("SELECT * FROM hive.default.mytable LIMIT 10")
    # rows = cursor.fetchall()
    # print("My table rows:", rows)

if __name__ == "__main__":
    main()
