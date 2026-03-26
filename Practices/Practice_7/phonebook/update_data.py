import psycopg2
from config import load_config

def update_contact(contact_change_attribute, contact_new_info, contact_number):
    config = load_config()
    updated_row_count = 0

    sql = f"""
        update contacts 
        set {contact_change_attribute}='{contact_new_info}'
        where contact_number='{contact_number}'
    """
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, None)
                updated_row_count = cursor.rowcount
            conn.commit()
            print(f"The update operation have completed successfully: attribute {contact_change_attribute}'s value -> {contact_new_info}")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return updated_row_count