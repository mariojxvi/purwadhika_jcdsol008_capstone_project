from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

import json
import re
from dataclasses import dataclass
from typing import Dict

CREATE = 1
READ = 2
UPDATE = 3
DELETE = 4
EXIT = 5

EMAIL_REGEX_RFC5322 = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

MAIN_MENU = """
# Aplikasi CRUD Yellow Pages 
## Main Menu :
1. Create - Membuat data kontak telefon baru
2. Read   - Melihat data kotak telefon
3. Update - Memperbaharui data kontak telefon
4. Delete - Menghapus data kontak telefon
5. Exit   - Keluar dari aplikasi
"""

CREATE_MENU = """
## Create Menu:
1. Membuat data kontak telefon baru
2. Kembali ke menu utama
"""

READ_MENU = """
## Read Menu:
1. Tampilkan semua data kontak telefon
2. Cari data kontak telefon
3. Kembali ke menu utama
"""

SEARCH_MENU = """
### Search Menu:
1. Cari berdasarkan id
2. Cari berdasarkan nama
3. Kembali
"""

UPDATE_MENU = """
## Update Menu:
1. Memperbaharui data kontak telefon
2. Kembali ke menu utama
"""

COLUMN_MENU = """
### Edit Column:
1. Update kolom nama
2. Update kolom no_telefon
3. Update kolom email
4. Update kolom alamat
5. Kembali
"""

DELETE_MENU = """
## Delete Menu:
1. Menghapus data kontak telefon
2. Kembali ke menu utama
"""

console = Console()

DATA_CONTACTS = []

def generate_table(contacts_data):
    table = Table(expand=True)
    table.add_column("ID")
    table.add_column("NAMA")
    table.add_column("NO TELEFON")
    table.add_column("EMAIL")
    table.add_column("ALAMAT")

    for contact_data in contacts_data:
        table.add_row(
            str(contact_data['id']),
            contact_data['nama'],
            contact_data['no_telefon'],
            contact_data['email'],
            contact_data['alamat']
        )
    return table

def ask_for_id():
    while(True):
        try:
            id = int(input("Masukan id (integer): "))
            return id
        except:
            print(f"Invalid id: {id}")
            continue

def check_for_duplicate(id):
    for contact in DATA_CONTACTS:
        if id == contact['id']:
            return True
    return False
    
def ask_for_name():
    while(True):
        try:
            name = input("Masukan nama: ")
            if name == "":
                raise Exception("Nama tidak boleh kosong")
            return name
        except Exception as e:
            print(f"Invalid name: {name} ", e)

def ask_for_phone_number():
    while(True):
        try:
            phone_number = input("Masukan nomor telefon (12 atau 6 digit angka): ")
            validate_phone_number(phone_number)
            return phone_number
        except Exception as e:
            print(e)
            continue

def validate_phone_number(input_number):
    if not (input_number.isnumeric() and (len(input_number) == 12 or len(input_number) == 6)):
        raise Exception("Nomor telefon yang dimasukan tidak valid")


def ask_for_address():
    while(True):
        try:
            address = input("Masukan alamat: ")
            if address == "":
                raise Exception("Alamat tidak boleh kosong")
            return address
        except Exception as e:
            print(e)

def ask_for_email():
    while(True):
        try:
            email = input("Masukan email: ")
            validate_email(email)
            return email
        except Exception as e:
            print(e)

def validate_email(input_email):
    if not re.fullmatch(EMAIL_REGEX_RFC5322, input_email):
        raise Exception("Email yang dimasukan tidak valid")

def ask_form_confirmation(word):
    confirm = input(f"Ada yakin ingin {word} kontak ini [y/n]?: ")
    if confirm.upper() == 'Y':
        return True
    else:
        return False

def create():
    while(True):
        console.print(Markdown(CREATE_MENU))
        print()
        try:
            choice = int(input("Pilih menu [1/2]: "))
        except:
            choice = -1
        if choice == 1:
            print("\nMembuat kontak baru, harap isi beberapa data berikut dengan benar: \n")
            id = ask_for_id()
            if check_for_duplicate(id) == True:
                print(f'Kontak id {id} sudah digunakan')
                continue
            nama = ask_for_name()
            no_telefon = ask_for_phone_number()
            email = ask_for_email()
            alamat = ask_for_address()

            new_contact = {'id' : id, 'nama' : nama, 'no_telefon' : no_telefon, 'email' : email, 'alamat' : alamat }

            table = generate_table([new_contact])
            console.print(table)
            confirm = ask_form_confirmation("menambahkan")
            if confirm:
                DATA_CONTACTS.append(new_contact)
                print("Kontak berhasil ditambahkan")
            
        elif choice == 2:
            print()
            break
        else:
            print("\nInvalid Input\n")

def read():
    while(True):
        console.print(Markdown(READ_MENU))
        print()
        try:
            choice = int(input("Pilih menu [1/2/3]: "))
        except:
            choice = -1
        if choice == 1:
            if not DATA_CONTACTS:
                print("\nTidak ada data kontak ditemukan")
            table = generate_table(DATA_CONTACTS)
            print()
            console.print(table)
        elif choice == 2:
            search()
        elif choice == 3:
            print()
            break
        else:
            print("\nInvalid Input\n") 

def search():
    while(True):
        console.print(Markdown(SEARCH_MENU))
        print()
        try:
            choice = int(input("Pilih menu [1/2/3]: "))
        except:
            choice = 0

        if choice == 1:
            try:
                id = int(input("Masukan id kontak yang ingin dicari: "))
            except:
                id = -1
            
            target_contact = []
            for contact in DATA_CONTACTS:
                if contact['id'] == id:
                    target_contact.append(contact)
                    break
            
            if not target_contact:
                print(f"\nTidak ada kontak dengan id: {id}")

            table = generate_table(target_contact)
            print()
            console.print(table)
            break
        elif choice == 2:
            nama = input("Masukan nama kontak yang ingin dicari: ")

            target_contacts = []
            
            if nama == "":
                pass
            else:
                for contact in DATA_CONTACTS:
                    if nama.upper() in contact['nama'].upper():
                        target_contacts.append(contact)
            
            if not target_contacts:
                print(f"Tidak ada kontak dengan nama: {nama}")

            table = generate_table(target_contacts)
            print()
            console.print(table)
            break
        elif choice == 3:
            print()
            break
        else:
            print("\nInvalid Input\n") 


def update():
    while True:
        console.print(Markdown(UPDATE_MENU))
        print()
        try:
            choice = int(input("Pilih menu [1/2]: "))
        except:
            choice = -1

        if choice == 1:
            table = generate_table(DATA_CONTACTS)
            console.print(table)
            print()
            try:
                id = int(input("Masukan id kontak yang ingin diperbaharui: "))
            except:
                id = -1
            
            target_contact = []
            for contact in DATA_CONTACTS:
                if contact['id'] == id:
                    target_contact.append(contact)
                    break
            
            if not target_contact:
                print(f"\nTidak ada kontak dengan id: {id}")
                break

            table = generate_table(target_contact)
            print()
            console.print(table)

            temp_contact = target_contact[0].copy()
            console.print(Markdown(COLUMN_MENU))
            print()
            try:
                column = int(input("Pilih kolum yang ingin diperbaharui [1/2/3/4]: "))
            except:
                column = -1
            
            if column == 1:
                nama = ask_for_name()
                temp_contact['nama'] = nama
            elif column == 2:
                no_telefon = ask_for_phone_number()
                temp_contact['no_telefon'] = no_telefon
            elif column == 3:
                email = ask_for_email()
                temp_contact['email'] = email
            elif column == 4:
                address = ask_for_address()
                temp_contact['alamat'] = address
            else:
                break
            
            table = generate_table([temp_contact])
            console.print(table)
            confirm = ask_form_confirmation("memperbaharui")
            if confirm:  
                for target_index, contact in enumerate(DATA_CONTACTS):
                    if contact['id'] == id:
                        break
                DATA_CONTACTS[target_index] = temp_contact
                print("Kontak berhasil diperbaharui")

        elif choice == 2:
            print()
            break
        else:
            print("\nInvalid Input\n")

def delete():
    while True:
        console.print(Markdown(DELETE_MENU))
        print()
        try:
            choice = int(input("Pilih menu [1/2]: "))
        except:
            choice = -1

        if choice == 1:
            table = generate_table(DATA_CONTACTS)
            console.print(table)
            print()
            try:
                id = int(input("Masukan id kontak yang ingin anda hapus: "))
            except:
                id = -1
            
            target_contact = []
            for contact in DATA_CONTACTS:
                if contact['id'] == id:
                    target_contact.append(contact)
                    break
            
            if not target_contact:
                print(f"\nTidak ada kontak dengan id: {id}")
                break
            
            table = generate_table(target_contact)
            console.print(table)
            confirm = ask_form_confirmation("menghapus")
            if confirm:
                DATA_CONTACTS.remove(target_contact[0])
                print("Kontak berhasil dihapus\n")
            break
        elif choice == 2:
            print()
            break
        else:
            print("\nInvalid Input\n")


def main():
    while(True):
        console.print(Markdown(MAIN_MENU))
        print()
        try:
            choice = int(input("Pilih menu [1/2/3/4/5]: "))
        except:
            choice = 0
        if choice == CREATE:
            create()
        elif choice == READ:
            read()
        elif choice == UPDATE:
            update()
        elif choice == DELETE:
            delete()
        elif choice == EXIT:
            print("\nBye bye\n")
            break
        else:
            print("\nInvalid input\n")

    with open("data_contacts.json", "w") as final:
        json.dump(DATA_CONTACTS, final, indent= 3)


if __name__ == '__main__':

    # INIT_DATA = [ {'id': 1, 'nama' : 'Mario Jaya',    'no_telefon' : '080738079635', 'email' : 'mario@mail.com', 'alamat' : 'Kudus,Indonesia'}, 
    #               {'id': 2, 'nama' : 'Paul Atreides', 'no_telefon' : '080775798859', 'email' : 'paul_atreides@arrakis.com', 'alamat' : 'Arrakis'}, 
    #               {'id': 3, 'nama' : 'Luna Lovewood', 'no_telefon' : '089765432190', 'email' : 'luna_lovewood@hogwarts.com', 'alamat' : 'Hogwarts'}]

    # with open("data_contacts.json", "w") as final:
    #     json.dump(INIT_DATA, final, indent= 3)

    try:
        with open('data_contacts.json') as json_file:
            DATA_CONTACTS = json.load(json_file)
    except Exception as e:
        print("Cannot open file: ", e)
        DATA_CONTACTS = []
    
    main()
    


