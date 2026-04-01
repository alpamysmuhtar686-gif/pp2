import psycopg2
import csv 
conn = psycopg2.connect(
    host= "localhost",
    database = "phonebook_db",
    user = "postgres",
    password = "Asdfghjkl23@"
)
cur = conn.cursor()
def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook(
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL
            );
    """)
    conn.commit()
def add_cons():
    numb = input("Номер:")
    name = input("Имя:")
    cur.execute("""
        INSERT INTO phonebook(username, phone)
        VALUES (%s,%s);
    """, (name,numb))
    conn.commit()
def select():
    cur.execute("""
        SELECT * FROM phonebook;
    """)
    rows = cur.fetchall()
    for row in rows:
        print(row)
def delete():
    r = input("айди для удаления:")
    cur.execute("""
        DELETE FROM phonebook
        WHERE id = %s;
""",(r,))
    conn.commit()
def Update(q):
    def namee():
        qw= input("Введите новое имя:")
        qww=input("Введите айди:")
        cur.execute("""
            UPDATE phonebook
            SET username = %s
            WHERE id = %s
""",(qw,qww))
        conn.commit()
    
    def number():
        rre=input("Введите новый номер:")
        rrt=input("Введите айди:")
        cur.execute("""
            UPDATE phonebook
            SET phone=%s
            WHERE id=%s
""",(rre,rrt))
        conn.commit()
    if q ==1:
        namee()
    else:
        number()


    
def filter_12():
    tt = input()
    cur.execute("""
        SELECT * FROM phonebook
        WHERE id<%s;
""",(tt,))
    irir=cur.fetchall()
    for i in irir:
        print (i)
def chit():
    with open("contacts.csv", "r",encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for i in reader:
            us= i[0]
            ph = i[1]

            cur.execute("""
                INSERT INTO phonebook(username,phone)
                VALUES(%s,%s)
""",(us,ph))
    conn.commit()

menu = True
while menu:
    print("\nВыберите функцию:")
    print("1 - Добавить контакт")
    print("2 - Показать все контакты")
    print("3 - Удалить контакт")
    print("4 - Обновить имя")
    print("5 - Фильтр")
    print("6 - читать с файла")
    print("7-создать таблицу ponebook")
    print("0 - Выход")

    tr = input("Ваш выбор: ")

    if tr == "1":
        add_cons()
    elif tr == "2":
        select()
    elif tr == "3":
        delete()
    elif tr == "4":
        
        print("1. изменить  имя")
        print("2. Изменить номер")
        rere=int(input())
        Update(rere)
    elif tr =='6':
        chit()
    elif tr == "5":
        filter_12()
    elif tr == "0":
        menu = False
        print("Программа завершена")
    elif tr =='7':
        create_table()
    else:
        print("Неправильный ввод, попробуйте снова")
    
cur.close()
conn.close()