import psycopg2
from config import load_config

def delete_contact(first_name):
    config = load_config()
    sql = """
        delete from contacts where contact_first_name=%s
    """
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (first_name,))
                print(f"Successfully deleted row with first name '{first_name}'")
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)