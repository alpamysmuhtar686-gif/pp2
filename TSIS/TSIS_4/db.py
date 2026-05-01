from config import load_config
import psycopg2
import datetime

def execute_query(sql_query, parameters=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log = f"""\n
    ----------------------
    {timestamp}
    """
    """ Connect to the PostgreSQL database server """
    conn = None
    result = None
    try:
        # read connection parameters
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cursor:
                # execute a statement
                if not parameters:
                    cursor.execute(sql_query)
                else:
                    cursor.execute(sql_query, parameters)
                log = log + sql_query + "\n"
                if parameters:
                    log = log + f"Parameters: {parameters}\n"
                
                # Try to fetch results for SELECT queries
                if sql_query.strip().upper().startswith("SELECT"):
                    result = cursor.fetchall()
                
                log = log + "Query executed successfully.\n"
    except (Exception, psycopg2.DatabaseError) as error:
        log = log + f'Error: {error}'
    with open('db_connection.log', 'a') as log_file:
        log_file.write(log)
    
    return result

sql = """
CREATE TABLE if not exists players (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE if not exists game_sessions (
    id            SERIAL PRIMARY KEY,
    player_id     INTEGER REFERENCES players(id),
    score         INTEGER   NOT NULL,
    level_reached INTEGER   NOT NULL,
    played_at     TIMESTAMP DEFAULT NOW()
);
"""
execute_query(sql)