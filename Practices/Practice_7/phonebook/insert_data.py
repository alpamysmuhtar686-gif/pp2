import psycopg2                     # Library to connect Python to PostgreSQL
import csv                          # Library to read CSV files
from config import load_config      # Your config.py to load DB credentials

# === Step 1: Function to insert one contact row into DB ===
def insert_contact(contact: dict):
    config = load_config()
    new_id = None
    """
    Inserts a single contact into the contacts table.
    cursor  : psycopg2 cursor object
    contact : dictionary with keys: first_name, last_name, phone_number, email, additional_info
    """
    # SQL statement with placeholders (%s) for parameters
    try:
        sql = """
            INSERT INTO contacts(
                contact_first_name,
                contact_last_name,
                contact_number,
                contact_email,
                contact_extra_info
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING contact_id;
        """

        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                # Execute SQL with data from 'contact' dictionary
                cursor.execute(sql, (
                    contact['first_name'],
                    contact.get('last_name', None),   # use None if missing
                    contact['phone_number'],
                    contact.get('email', None),
                    contact.get('additional_info', None)
                ))
                new_id = cursor.fetchone()[0]
                print(f"Successfully inserted a contact with id: {new_id}")
    except Exception as error:
        print(error)
    finally:
        # Fetch the generated contact_id (Postgres serial primary key)
        return new_id

# === Step 2: Main function to read CSV and insert data ===
def import_contacts_from_csv(csv_file_path):
    """
    Reads a CSV file and inserts all contacts into the database.
    """
    # Load database connection parameters from config.py
    config = load_config()
    
    try:
        # Open connection using 'with' so it closes automatically
        with psycopg2.connect(**config) as conn:
            # Open a cursor to execute SQL commands
            with conn.cursor() as cur:
                # Open CSV file
                with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)  # Reads rows as dictionaries
                    inserted_count = 0
                    
                    # Loop through each row in CSV
                    for row in reader:
                        # Insert each contact into DB
                        new_id = insert_contact(row)
                        inserted_count += 1
                        print(f"Inserted contact {row['first_name']} with ID {new_id}")
                
                # Commit all changes to the database
                conn.commit()
                
        print(f"✅ Successfully inserted {inserted_count} contacts from CSV.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)


# contact = {
#     'first_name': 'Nurdaulet',       # mandatory
#     'last_name': 'Malik',             # optional
#     'phone_number': '+77773485045',   # mandatory
#     'email': 'minafeed645@gmail.com', # optional
#     'additional_info': 'owner_of_the_db' # optional
# }
# config = load_config()
# import_contacts_from_csv("simple_contact.csv")
# insert_contact(contact)

