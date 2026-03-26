import psycopg2
from config import load_config

allowed_attributes = ['contact_id', 'contact_first_name', 'contact_last_name', 'contact_number', 'contact_email', 'contact_extra_info']
allowed_sort_types = ['asc', '+', '-', 'desc', '']
def get_info(filter, sort_key, sort_type, sort_aggregate_value):
    config = load_config()
    if filter.lower() == '*' or filter.lower() == 'all':
        if sort_key == '':
            sql = """
                select * from contacts 
            """
        elif (sort_key not in allowed_attributes) or (sort_type not in allowed_sort_types):
            print("Key/type error: Please ensure you've typed sort_key and sort_type correctly.")
            print(f"Arguments you've written: sort_key: {sort_key}, sort_type: {sort_type}",)
            print("Allowed attributes:", *allowed_attributes)
            print("Allowed sort_types:", *allowed_sort_types)
        else:
            sql = f"""
                select * from contacts order by {sort_key} {sort_type}
            """
    elif filter.lower() in allowed_attributes:
        sql = f"""
            select * from contacts where {filter}='{sort_aggregate_value}'
        """
    else:
        print("Error: The filter isn't correct. You can choose: '*' (diplaying all data), 'key_name' and needed key value")
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                print("The number of parts: ", cursor.rowcount)
                row = cursor.fetchone()
                while row is not None:
                    print(row)
                    row = cursor.fetchone()
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)