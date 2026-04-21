import csv
from connect import connect

conn = connect()
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


def filter_cont():
    print("1 - фильтроать по номеру ")
    print("2 - фильтровать по имени ")
    op= int(input())
    if op ==1:
        op1=input("Введите с чего начинается номер ")
        cur.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s;"
        ,(op1+'%',))
        itit=cur.fetchall()
        for i in itit:
            print(i)
    elif op==2:
        op2= input("Введите с чего начинается имя ")
        cur.execute(
            "SELECT * FROM phonebook WHERE username LIKE %s"
        ,(op2+'%',))
        rere = cur.fetchall()
        for l in rere:
            print(l)

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


import os
import csv

def insert_from_csv():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "contacts.csv")

        with open(file_path, "r", encoding="utf-8") as file:
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

create_table()

menu = True
while menu:
    print("\nВыберите функцию:")
    print("1 - Добавить контакт вручную")
    print("2 - Показать все контакты")
    print("3 - Обновить контакт")
    print("4 - Фильтр")
    print("5 - Удалить контакт")
    print("6 - Загрузить контакты из CSV")
    print("0 - Выход")

    choice = input("Ваш выбор: ")

    if choice == "1":
        add_contact()
    elif choice == "2":
        show_all_contacts()
    elif choice == "3":
        update_contact()
    elif choice == "4":
        filter_cont()
    elif choice == "5":
        delete_contact()
    elif choice == "6":
        insert_from_csv()
    elif choice == "0":
        menu = False
        print("Программа завершена")
    else:
        print("Неправильный ввод, попробуйте снова")

cur.close()
conn.close()