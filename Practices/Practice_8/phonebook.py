import psycopg2
import csv
from config import load_config


def connect():
    config = load_config()
    return psycopg2.connect(**config)


def load_sql_files():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                for file in ["functions.sql", "procedures.sql"]:
                    with open(file, "r") as f:
                        cur.execute(f.read())
            conn.commit()
    except Exception as error:
        print("[SQL LOAD ERROR]", error)


def insert_contact():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone_number = input("Phone number: ")
    email = input("Email: ")
    extra_info = input("Extra info: ")

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL insert_user(%s, %s, %s, %s, %s)",
                    (first_name, last_name, phone_number, email, extra_info)
                )
            conn.commit()
            print("[Success] Contact inserted or updated.")
    except Exception as error:
        print("[ERROR]", error)


def import_from_csv():
    file_name = input("CSV file name: ")

    try:
        with open(file_name, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            with connect() as conn:
                with conn.cursor() as cur:
                    for row in reader:
                        cur.execute(
                            "CALL insert_user(%s, %s, %s, %s, %s)",
                            (
                                row["first_name"],
                                row["last_name"],
                                row["phone_number"],
                                row["email"],
                                row["extra_info"]
                            )
                        )
                conn.commit()

        print("[Success] Contacts imported from CSV.")

    except Exception as error:
        print("[ERROR]", error)


def update_contact():
    column = input("Column to update: ")
    new_value = input("New value: ")
    phone_number = input("Phone number of contact: ")

    allowed = [
        "contact_first_name",
        "contact_last_name",
        "contact_number",
        "contact_email",
        "contact_extra_info"
    ]

    if column not in allowed:
        print("[ERROR] Wrong column name.")
        return

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                sql = f"UPDATE contacts SET {column} = %s WHERE contact_number = %s"
                cur.execute(sql, (new_value, phone_number))
            conn.commit()
            print("[Success] Contact updated.")
    except Exception as error:
        print("[ERROR]", error)


def get_all_contacts():
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM contacts ORDER BY contact_id")
                rows = cur.fetchall()

                for row in rows:
                    print(row)

    except Exception as error:
        print("[ERROR]", error)


def search_contact():
    search_type = input("Search by first_name / last_name / number: ")
    value = input("Search value: ")

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT get_by_pattern(%s, %s)", (search_type, value))
                rows = cur.fetchall()

                for row in rows:
                    print(row)

    except Exception as error:
        print("[ERROR]", error)


def pagination():
    limit = int(input("Rows per page: "))
    page = int(input("Page number: "))

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT query_pagination(%s, %s)", (limit, page))
                rows = cur.fetchall()

                for row in rows:
                    print(row)

    except Exception as error:
        print("[ERROR]", error)


def delete_contact():
    first_name = input("First name: ")
    last_name = input("Last name: ")
    phone_number = input("Phone number: ")

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "CALL delete_user(%s, %s, %s)",
                    (first_name, last_name, phone_number)
                )
            conn.commit()
            print("[Success] Contact deleted.")
    except Exception as error:
        print("[ERROR]", error)


load_sql_files()

while True:
    print("\nPHONEBOOK MENU")
    print("1 - Insert contact")
    print("2 - Import from CSV")
    print("3 - Update contact")
    print("4 - Show all contacts")
    print("5 - Search contact")
    print("6 - Pagination")
    print("7 - Delete contact")
    print("0 - Exit")

    command = input("Choose command: ")

    if command == "1":
        insert_contact()
    elif command == "2":
        import_from_csv()
    elif command == "3":
        update_contact()
    elif command == "4":
        get_all_contacts()
    elif command == "5":
        search_contact()
    elif command == "6":
        pagination()
    elif command == "7":
        delete_contact()
    elif command == "0":
        print("Exit...")
        break
    else:
        print("Wrong command.")