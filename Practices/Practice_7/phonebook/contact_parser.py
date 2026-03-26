import insert_data
from update_data import update_contact
from query_data import get_info
from delete_data import delete_contact

print("Welcome to the terminal of parsing data. Here you can insert, update, get information, or delete your contacts")
allowed_attributes = ['contact_id','contact_first_name', 'contact_last_name', 'contact_number', 'contact_email', 'contact_extra_info']
while True:
    contact = {}
    command = input("Insert a command (insert/update/get/delete/exit): ").lower()
    if command == 'insert' or command == 'i':
        insertion_type = input("Enter the type of insertion (csv - for csv, b - basic): ").lower()
        if insertion_type == '' or insertion_type == 'basic' or insertion_type == 'b':
            first_name = input("Input the first_name: ")
            if first_name == '':
                print("First name can't be empty! Restart the session.")
                break

            last_name = input("Input the last_name (optional): ")
        
            phone_number = input("Input the phone_number: ")
            if phone_number == '':
                print("Phone number can't be empty! Restart the session.")
                break

            email = input("Input the email (optional): ")
            additional_info = input("Input the additional information (optional): ")

            contact["first_name"] = first_name
            contact["last_name"] = last_name if last_name != '' else None
            contact["phone_number"] = phone_number
            contact["email"] = email if email != '' else None
            contact["additional_info"] = additional_info if additional_info != '' else None
            insert_data.insert_contact(contact)

        elif insertion_type == 'csv' or insertion_type == 'c':
            path = input("index a path where the .csv file is located \n(only the name of the file if it's located in the same direction as this file): ")
            insert_data.import_contacts_from_csv(path)

    elif command == 'update' or command == 'u':
        changing_attribute = input(f"Input which attribute (column) you want to change\nThe list of all attributes: {allowed_attributes[1:]}\n")
        if changing_attribute not in allowed_attributes:
            print(f"The attribute {changing_attribute} doesn't found. Please ensure you've typed the attribute correctly\nThe list of all attributes: {allowed_attributes}\n")
        else:
            new_value = input("Input a value you want to set: ")
            phone_number = input("Input a phone_number for which you want to change the attribute: ")
        update_contact(changing_attribute, new_value, phone_number)
    
    elif command == "get" or command == "g":
        filter = input(f"Input the filter you want to apply\n'*' - displays all data\nOr, you can write attribute's name\nList of all attributes: {allowed_attributes}\n").lower()
        if filter == '':
            print("You didn't input the filter! Please, retype it again.")
        sort_key = input("Now, input a key by which your data will be sorted (you can ignore this line if you've already parsed key in filter's line): ")
        sort_type = input("Input a type of sort (asc/desc): ")
        sort_aggregation_value = input("Input a value that will specify and filter the data (optional): ")
        get_info(filter, sort_key, sort_type, sort_aggregation_value)
    elif command == "delete" or command == "d":
        first_name = input("Input a first name, which contact will be deleted (Warning: FIRST NAME!): ")
        if first_name == '':
            print("Invalid first name! Please ensure you've written it correctly")
        else: delete_contact(first_name)
    elif command == "quit" or command == "q" or command == "exit":
        print("Exiting the programm...")
        break
    else:
        print("The command is wrong! Please assure you've written the command correct\n")