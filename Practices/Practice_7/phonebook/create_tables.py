import psycopg2
from config import load_config

def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = [
        """
        CREATE TABLE if not exists contacts (
            contact_id SERIAL PRIMARY KEY,
            contact_first_name varchar(255) not null,
            contact_last_name varchar(255),
            contact_number varchar(15) not null unique,
            contact_email varchar(511),
            contact_extra_info varchar(255)
        )
        """
        ]
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the CREATE TABLE statement
                for command in commands:
                    cur.execute(command)
        print("The table is created.")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    create_tables()