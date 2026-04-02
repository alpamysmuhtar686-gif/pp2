import psycopg2
import csv

conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="Asdfghjkl23@"
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


def add_contact():
    name = input("Введите имя: ")
    phone = input("Введите номер: ")

    cur.execute("""
        INSERT INTO phonebook(username, phone)
        VALUES (%s, %s);
    """, (name, phone))
    conn.commit()
    print("Контакт добавлен")


def show_all_contacts():
    cur.execute("""
        SELECT * FROM phonebook;
    """)
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("Таблица пустая")


def update_contact():
    print("1 - Изменить имя")
    print("2 - Изменить номер")
    choice = input("Ваш выбор: ")

    if choice == "1":
        old_name = input("Введите текущее имя контакта: ")
        new_name = input("Введите новое имя: ")

        cur.execute("""
            UPDATE phonebook
            SET username = %s
            WHERE username = %s;
        """, (new_name, old_name))
        conn.commit()
        print("Имя обновлено")

    elif choice == "2":
        name = input("Введите имя контакта: ")
        new_phone = input("Введите новый номер: ")

        cur.execute("""
            UPDATE phonebook
            SET phone = %s
            WHERE username = %s;
        """, (new_phone, name))
        conn.commit()
        print("Номер обновлён")

    else:
        print("Неправильный выбор")


def find_by_name():
    name = input("Введите имя для поиска: ")

    cur.execute("""
        SELECT * FROM phonebook
        WHERE username = %s;
    """, (name,))
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("Контакты не найдены")


def find_by_phone_prefix():
    prefix = input("Введите начало номера: ")

    cur.execute("""
        SELECT * FROM phonebook
        WHERE phone LIKE %s;
    """, (prefix + '%',))
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("Контакты не найдены")


def delete_contact():
    print("1 - Удалить по имени")
    print("2 - Удалить по номеру")
    choice = input("Ваш выбор: ")

    if choice == "1":
        name = input("Введите имя для удаления: ")
        cur.execute("""
            DELETE FROM phonebook
            WHERE username = %s;
        """, (name,))
        conn.commit()
        print("Контакт удалён")

    elif choice == "2":
        phone = input("Введите номер для удаления: ")
        cur.execute("""
            DELETE FROM phonebook
            WHERE phone = %s;
        """, (phone,))
        conn.commit()
        print("Контакт удалён")

    else:
        print("Неправильный выбор")


def insert_from_csv():
    try:
        with open("contacts.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                username = row[0]
                phone = row[1]

                cur.execute("""
                    INSERT INTO phonebook(username, phone)
                    VALUES (%s, %s);
                """, (username, phone))

        conn.commit()
        print("Данные из CSV добавлены")

    except FileNotFoundError:
        print("Файл contacts.csv не найден")


def clear_table():
    cur.execute("""
        TRUNCATE TABLE phonebook RESTART IDENTITY;
    """)
    conn.commit()
    print("Таблица очищена")


create_table()

menu = True
while menu:
    print("\nВыберите функцию:")
    print("1 - Добавить контакт вручную")
    print("2 - Показать все контакты")
    print("3 - Обновить контакт")
    print("4 - Найти по имени")
    print("5 - Найти по префиксу номера")
    print("6 - Удалить контакт")
    print("7 - Загрузить контакты из CSV")
    print("8 - Очистить таблицу")
    print("0 - Выход")

    choice = input("Ваш выбор: ")

    if choice == "1":
        add_contact()
    elif choice == "2":
        show_all_contacts()
    elif choice == "3":
        update_contact()
    elif choice == "4":
        find_by_name()
    elif choice == "5":
        find_by_phone_prefix()
    elif choice == "6":
        delete_contact()
    elif choice == "7":
        insert_from_csv()
    elif choice == "8":
        clear_table()
    elif choice == "0":
        menu = False
        print("Программа завершена")
    else:
        print("Неправильный ввод, попробуйте снова")

cur.close()
conn.close()