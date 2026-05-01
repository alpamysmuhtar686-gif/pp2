import psycopg2
import csv
from config import load_config
import datetime
import json

# =========================
# CONFIG
# =========================

allowed_search_attributes = ['first_name', 'last_name', 'number']

allowed_attributes = [
    'contact_id',
    'contact_first_name',
    'contact_last_name',
    'contact_number',
    'contact_email',
    'contact_extra_info'
]

allowed_sort_types = ['asc', 'desc', '+', '-', '']


# =========================
# INIT SQL FILES
# =========================

def load_sql_files():
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                for file in ['functions.sql', 'procedures.sql']:
                    with open(file, 'r') as f:
                        cursor.execute(f.read())
            conn.commit()
    except Exception as error:
        if conn:
            conn.rollback()
        print(error)


# =========================
# INSERT CONTACT
# =========================

def insert_contact2(contact: dict):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                # 1. insert contact (safe version)
                cur.execute("""
                    INSERT INTO contacts(
                        contact_first_name,
                        contact_last_name,
                        contact_number,
                        contact_email,
                        contact_extra_info,
                        birthday,
                        group_id
                    )
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    RETURNING contact_id;
                """, (
                    contact.get('first_name'),
                    contact.get('last_name'),
                    contact.get("phones")[0]["number"],  # if only one phone, is a main phone
                    contact.get('email'),
                    contact.get('additional_info'),
                    contact.get('birthday'),
                    contact.get('group_id')
                ))

                contact_id = cur.fetchone()[0]

                # 2. insert phones safely
                for phone in contact.get("phones", []):
                    cur.execute(
                        "CALL add_phone(%s, %s, %s, %s)",
                        (
                            contact["first_name"],
                            contact["last_name"],
                            phone["number"],
                            phone["type"]
                        )
                    )

            conn.commit()
            print(f"[OK] contact inserted id={contact_id}")

    except Exception as e:
        if conn:
            conn.rollback()
        print("[ERROR]", e)


# =========================
# CSV IMPORT
# =========================

def import_contacts_from_csv(csv_file_path):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)

                    count = 0

                    for row in reader:

                        contact = {
                            "first_name": row.get("first_name"),
                            "last_name": row.get("last_name") or None,
                            "email": row.get("email") or None,
                            "additional_info": row.get("additional_info") or None,
                            "birthday": row.get("birthday") or None,
                            "group_id": get_group_id(row.get("group")),
                            "phones": [
                                {
                                    "number": row.get("phone_number"),
                                    "type": row.get("phone_type") or "mobile"
                                }
                            ]
                        }

                        insert_contact2(contact)
                        count += 1

            conn.commit()

        print(f"[Success] CSV inserted: {count}")

    except Exception as e:
        print("[ERROR]", e)

# =========================
# UPDATE
# =========================

def update_contact(contact_change_attribute, contact_new_info, contact_number, contact_first_name):
    config = load_config()
    updated_row_count = 0

    if contact_number and contact_first_name is None:
        sql = f"""
            UPDATE contacts
            SET {contact_change_attribute} = %s
            WHERE contact_number = %s
        """
        params = (contact_new_info, contact_number)
    else:
        sql = f"""
            UPDATE contacts
            SET {contact_change_attribute} = %s
            WHERE contact_first_name = %s
        """
        params = (contact_new_info, contact_first_name)

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                updated_row_count = cursor.rowcount
            conn.commit()

        if updated_row_count == 0:
            print("[Error] No rows updated")
        else:
            print(f"[Success] Updated {contact_change_attribute}")

    except Exception as error:
        if conn:
            conn.rollback()
        print(error)

    return updated_row_count


# =========================
# QUERY
# =========================

def get_info(filter, sort_key, sort_type, sort_aggregate_value):
    config = load_config()

    if filter.lower() in ['*', 'all']:
        if sort_key == '':
            sql = "SELECT * FROM contacts"
        else:
            sql = f"SELECT * FROM contacts ORDER BY {sort_key} {sort_type}"
    elif filter.lower() in allowed_attributes:
        sql = f"""
            SELECT * FROM contacts
            WHERE {filter} = %s
        """
    else:
        print("[Error] Invalid filter")
        return

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:

                if filter.lower() in allowed_attributes:
                    cursor.execute(sql, (sort_aggregate_value,))
                else:
                    cursor.execute(sql)

                rows = cursor.fetchall()

                print("Rows:", len(rows))
                for row in rows:
                    print(row)

    except Exception as error:
        if conn:
            conn.rollback()
        print(error)


# =========================
# DELETE
# =========================

def delete_contact(first_name, last_name, number):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:

                if number:   # priority case
                    sql = "DELETE FROM contacts WHERE contact_number = %s"
                    cursor.execute(sql, (number,))

                elif first_name:
                    sql = """
                        DELETE FROM contacts
                        WHERE contact_first_name = %s
                        AND contact_last_name = %s
                    """
                    cursor.execute(sql, (first_name, last_name))

                else:
                    print("[Error] No valid input provided")
                    return

            conn.commit()

    except Exception as error:
        if conn:
            conn.rollback()
        print(error)


# =========================
# SEARCH FUNCTION
# =========================

def search_by_pattern(pattern_type, pattern_value):
    config = load_config()

    sql = "SELECT * FROM get_by_pattern(%s, %s)"

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (pattern_type, pattern_value))
                rows = cursor.fetchall()

                print("Rows:", len(rows))
                for row in rows:
                    print(row)

    except Exception as error:
        if conn:
            conn.rollback()
        print(error)


# =========================
# PAGINATION
# =========================

def query_pagination(rows_per_page, page_index):
    config = load_config()

    sql = "SELECT * FROM query_pagination(%s, %s)"

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (rows_per_page, page_index))
                rows = cursor.fetchall()

                for row in rows:
                    print(row)

    except Exception as error:
        if conn:
            conn.rollback()
        print(error)

def is_valid_date(date: str) -> bool:
    try:
        datetime.datetime.strptime(date, "%Y-%M-%d")
        return True
    except Exception:
        return False

def filter_by_group(group_name):
    config = load_config()

    sql = "SELECT * FROM get_contacts_by_group(%s)"

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (group_name,))
                rows = cursor.fetchall()

                for row in rows:
                    print(row)

    except Exception as error:
        print(error)


def search_by_email(email_part):
    config = load_config()

    sql = """
        SELECT * FROM contacts
        WHERE contact_email ILIKE %s
    """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (f"%{email_part}%",))
                rows = cursor.fetchall()

                for row in rows:
                    print(row)

    except Exception as error:
        print(error)

def get_sorted_contacts(sort_by, order):
    config = load_config()

    mapping = {
        "name": "contact_first_name",
        "birthday": "birthday",
        "id": "contact_id"
    }

    if sort_by not in mapping:
        print("Invalid sort field")
        return

    sql = f"""
        SELECT * FROM contacts
        ORDER BY {mapping[sort_by]} {order.upper()}
    """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()

                for row in rows:
                    print(row)

    except Exception as error:
        print(error)


def pagination_menu():
    config = load_config()

    rows_per_page = int(input("Rows per page: "))
    page = 1

    while True:
        print(f"\n--- PAGE {page} ---")

        sql = "SELECT * FROM query_pagination(%s, %s)"

        try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (rows_per_page, page))
                    rows = cursor.fetchall()

                    for row in rows:
                        print(row)

        except Exception as error:
            print(error)

        cmd = input("\n[next / prev / quit]: ").lower()

        if cmd == "next":
            page += 1

        elif cmd == "prev":
            if page > 1:
                page -= 1
            else:
                print("Already first page")

        elif cmd == "quit":
            break

        else:
            print("Invalid command")


def export_contacts_to_json(file_path="contacts.json"):
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:

                # 1. get contacts + group
                cursor.execute("""
                    SELECT 
                        c.contact_id,
                        c.contact_first_name,
                        c.contact_last_name,
                        c.contact_email,
                        c.contact_extra_info,
                        c.birthday,
                        g.name AS group_name
                    FROM contacts c
                    LEFT JOIN groups g ON c.group_id = g.id
                """)

                contacts = cursor.fetchall()

                result = []

                for c in contacts:
                    contact_id = c[0]

                    # 2. get phones
                    cursor.execute("""
                        SELECT phone_number, phone_type
                        FROM phones
                        WHERE contact_id = %s
                    """, (contact_id,))

                    phones = [
                        {"number": p[0], "type": p[1]}
                        for p in cursor.fetchall()
                    ]

                    result.append({
                        "contact_id": contact_id,
                        "first_name": c[1],
                        "last_name": c[2],
                        "email": c[3],
                        "extra_info": c[4],
                        "birthday": str(c[5]) if c[5] else None,
                        "group": c[6],
                        "phones": phones
                    })

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)

        print(f"[Success] Exported to {file_path}")

    except Exception as e:
        print("[Error]", e)

def import_contacts_from_json(file_path):
    config = load_config()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:

                for c in data:

                    # 1. check duplicate
                    cursor.execute("""
                        SELECT contact_id
                        FROM contacts
                        WHERE contact_first_name = %s
                        AND contact_last_name = %s
                    """, (c["first_name"], c["last_name"]))

                    existing = cursor.fetchone()

                    if existing:
                        decision = input(
                            f"[Duplicate] {c['first_name']} {c['last_name']} (skip/overwrite): "
                        ).lower()

                        if decision == "skip":
                            continue

                        contact_id = existing[0]

                        # overwrite contact fields
                        cursor.execute("""
                            UPDATE contacts
                            SET contact_email = %s,
                                contact_extra_info = %s,
                                birthday = %s
                            WHERE contact_id = %s
                        """, (
                            c.get("email"),
                            c.get("extra_info"),
                            c.get("birthday"),
                            contact_id
                        ))

                        # remove old phones
                        cursor.execute("""
                            DELETE FROM phones WHERE contact_id = %s
                        """, (contact_id,))

                    else:
                        # insert contact
                        cursor.execute("""
                            INSERT INTO contacts(
                                contact_first_name,
                                contact_last_name,
                                contact_email,
                                contact_extra_info,
                                birthday
                            )
                            VALUES (%s,%s,%s,%s,%s)
                            RETURNING contact_id
                        """, (
                            c["first_name"],
                            c["last_name"],
                            c.get("email"),
                            c.get("extra_info"),
                            c.get("birthday")
                        ))

                        contact_id = cursor.fetchone()[0]

                    # 2. resolve group
                    group_id = None
                    if c.get("group"):
                        cursor.execute("""
                            SELECT id FROM groups WHERE name = %s
                        """, (c["group"],))
                        res = cursor.fetchone()
                        if res:
                            group_id = res[0]

                        cursor.execute("""
                            UPDATE contacts
                            SET group_id = %s
                            WHERE contact_id = %s
                        """, (group_id, contact_id))

                    # 3. insert phones
                    for p in c.get("phones", []):
                        cursor.execute("""
                            INSERT INTO phones(contact_id, phone_number, phone_type)
                            VALUES (%s, %s, %s)
                        """, (
                            contact_id,
                            p["number"],
                            p.get("type", "mobile")
                        ))

            conn.commit()

        print("[Success] JSON import completed")

    except Exception as e:
        print("[Error]", e)

def get_group_id(group_name):
    if not group_name:
        return None
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id FROM groups WHERE name = %s",
                    (group_name,)
                )
                res = cur.fetchone()
                return res[0] if res else None

    except Exception as e:
        print("[GROUP ERROR]", e)
        return None

def get_or_create_group(cursor, name):
    cursor.execute("SELECT id FROM groups WHERE name=%s", (name,))
    res = cursor.fetchone()

    if res:
        return res[0]

    cursor.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (name,))
    return cursor.fetchone()[0]

# =========================
# MAIN LOOP
# =========================

load_sql_files()
print("Phonebook system started")

while True:

    contact = {}

    command = input("Command (insert/update/get/search/page/delete/filter/import/export/add_phone/move/exit): ").lower()

    if command in ['insert', 'i']:
        insertion_mode = input("Choose a type of insertion (basic / csv): ")
        if insertion_mode == "basic":
            first_name = input("First name: ")
            last_name = input("Last name (optional): ")
            email = input("Email (optional): ")
            extra = input("Extra info (optional): ")
            birthday = input("Birthday (YYYY-MM-DD format otherwise error): ")
            if not is_valid_date(birthday):
                print("Invalid date!")
                continue

            # =========================
            # PHONE COLLECTION (NEW)
            # =========================
            phones = []

            print("\nEnter phone numbers (format: number type)")
            print("Example: +123456 work")
            print("Type 'done' when finished\n")

            while True:
                line = input("Phone: ")

                if line.lower() == "done" or line == "":
                    break

                parts = line.split()

                if len(parts) != 2:
                    print("[Error] Format must be: number type")
                    continue

                phone_number = parts[0]
                phone_type = parts[1]

                if phone_type not in ['home', 'work', 'mobile']:
                    print("[Error] type must be: home/work/mobile")
                    continue

                phones.append({
                    "number": phone_number,
                    "type": phone_type
                })

            # fallback if user enters nothing
            if len(phones) == 0:
                print("[Error] At least one phone is required")
                continue

            # main contact dictionary
            contact = {
                "first_name": first_name,
                "last_name": last_name if last_name != '' else None,
                "email": email if email != '' else None,
                "additional_info": extra if extra != '' else None,
                "phones": phones
            }

            insert_contact2(contact)
        elif insertion_mode == "csv":
            path = input("Enter CSV file path: ")
            try:
                with open(path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        birthday = row.get('birthday')
                        if birthday and not is_valid_date(birthday):
                            print(f"[Skip] Invalid date for {row.get('first_name')}")
                            continue
                        contact = {
                            "first_name": row.get('first_name'),
                            "last_name": row.get('last_name') or None,
                            "email": row.get('email') or None,
                            "additional_info": row.get('additional_info') or None,
                            "birthday": birthday or None,
                            "phones": [
                                {
                                    "number": row.get('phone_number'),
                                    "type": row.get('phone_type') or "mobile"
                                }
                            ]
                        }
                        insert_contact2(contact)
                print("[Success] CSV imported successfully")
            except Exception as e:
                print("[Error]", e)
    elif command in ['update', 'u']:
        attr = input("Attribute: ")
        value = input("New value: ")
        anchor = input("Search by (number/name): ")

        if anchor == "number":
            num = input("Number: ")
            update_contact(attr, value, num, None)
        else:
            name = input("Name: ")
            update_contact(attr, value, None, name)

    elif command in ['get', 'g']:
        filter = input("Filter (* or attribute): ")
        sort_key = input("Sort key: ")
        sort_type = input("Sort type: ")
        value = input("Value: ")
        get_info(filter, sort_key, sort_type, value)

    elif command == "search":
        attr = input("Attribute (first_name, last_name, number): ")
        val = input("Value: ")
        search_by_pattern(attr, val)

    elif command == "page":
        r = int(input("Rows: "))
        p = int(input("Page: "))
        query_pagination(r, p)

    elif command in ['delete', 'd']:
        first = input("First name: ")
        last = input("Last name: ")
        number = input("Number: ")
        delete_contact(first, last, number)

    elif command == "filter":
        print("""
        1. Filter by group
        2. Search by email
        3. Sort contacts
        4. Pagination
        """)
        choice = input("Choose option: ")

        if choice == "1":
            group = input("Enter group name: ")
            filter_by_group(group)

        elif choice == "2":
            email = input("Email keyword: ")
            search_by_email(email)

        elif choice == "3":
            sort_by = input("Sort by (name/birthday/id): ")
            order = input("asc / desc: ")
            get_sorted_contacts(sort_by, order)

        elif choice == "4":
            pagination_menu()

        else:
            print("Invalid choice")
    elif command == "export":
        export_contacts_to_json()
    elif command == "import":
        path = input("Input a path to a file .json: ")
        try: import_contacts_from_json(path)
        except Exception as error: print(f"[Error]: {error}")
    elif command == "add_phone":
        name = input("Contact full name: ")
        first, last = name.split()
        phone = input("Phone number: ")
        ptype = input("Type (mobile/work/home): ")

        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "CALL add_phone(%s, %s, %s, %s)",
                    (first, last, phone, ptype)
                )
    elif command == "move":
        name = input("Contact full name (first last): ")
        first, last = name.split()
        group = input("New group name: ")
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "CALL move_to_group(%s, %s, %s)",
                    (first, last, group)
                )
    elif command in ['exit', 'quit', 'q']:
        print("Exiting...")
        break
    else:
        print("Unknown command")