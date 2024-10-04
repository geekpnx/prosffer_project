import psycopg2
import json

# Connection parameters
DB_NAME = "prosffer_db"
DB_USER = "prosffer_user"
DB_PWD = "prosffer_user"
HOST = "localhost"  # Or your remote server address

# Read JSON data from file
with open(
    "/home/dci-student/prosffer/prosferr_project/data/aldi_sued_products_modified.json",
    "r",
) as file:

    json_data = json.load(
        file
    )  # This will load the JSON data as a Python list of dictionaries

try:
    # Connect to PostgreSQL database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PWD, host=HOST)
    cursor = conn.cursor()

    # SQL query to insert data
    insert_query = """INSERT INTO product_product (store, name, description, price, currency, category, image, link, id_tag) 
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    # Loop over each product in the JSON data
    for product in json_data:
        # Extract individual fields from the JSON object, using .get() to handle missing optional fields
        values = (
            product.get("store"),  # Required field
            product.get("name"),  # Required field
            product.get("description"),  # Optional field, might be None
            product.get("price"),  # Required field
            product.get("currency"),  # Required field
            product.get("category"),  # Required field
            product.get("image"),  # Required field
            product.get("link"),  # Required field
            product.get("id_tag"),  # Required field
        )

        # Execute the query for each product
        cursor.execute(insert_query, values)

    # Commit the transaction
    conn.commit()

    print("Data inserted successfully from file.")

except (Exception, psycopg2.DatabaseError) as error:
    print(f"Error while inserting data: {error}")
finally:
    if conn:
        cursor.close()
        conn.close()
