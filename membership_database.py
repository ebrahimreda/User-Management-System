from time import sleep
import os
import sqlite3

# الاتصال بقاعدة البيانات وإنشاء الجدول إذا لم يكن موجودًا
db= sqlite3.connect("users.db")
rc = db.cursor()
rc.execute('''
CREATE TABLE IF NOT EXISTS users(
    Passport_numper TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone INTEGER
)
''')

class Member:
    def __init__(self):
        while True:
            choice = self.screen()
            if choice == "1":
                self.write()
            elif choice == "2":
                self.search()
            elif choice == "3":
                self.edit()
            elif choice == "4":
                self.delete()
            elif choice == "5":
                print("Thank you for using the system. Goodbye!")
                db.commit()  
                db.close()   
                break
    
    def screen(self):
        os.system("cls" if os.name == "nt" else "clear")
       
        print('''
    1 - Register as a new member
    2 - Find a member
    3 - Edit member
    4 - Delete a member
    5 - Exit
        ''')
    
        return input('Enter your choice: ')

    def write(self):
        passport = input('Enter your passport number: ').strip()
        name = input('Enter your name: ').strip()
        email = input('Enter your email: ').strip()
        phone = input('Enter your phone number: ').strip()

        try:
            try:
                validet=self.valid(passport,name,email,phone)
                if validet==True:
                    rc.execute(" INSERT INTO users(Passport_numper, name, email, phone) VALUES (?, ?, ?, ?) " ,(passport, name, email, phone))
                       
                else:
                    print("the data invalid try agen...")
            except sqlite3.IntegrityError:
                print("A member with this passport number already exists.")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

        sleep(2)

    def search(self):
        try:
            passport = input("Enter the passport number to search: ")
            rc.execute("SELECT * FROM users WHERE Passport_numper = ?", (passport,))
            result = rc.fetchone()

            if result:
                print(f"Member found: Passport: {result[0]}, Name: {result[1]}, Email: {result[2]}, Phone: {result[3]}")

            else:
                print("No member found with this passport number.")
            
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

        sleep(2)

    def edit(self):
        try:
            passport = input("Enter the passport number of the member to edit: ")
            rc.execute("SELECT * FROM users WHERE Passport_numper = ?", (passport,))
            result = rc.fetchone()

            if result:
                new_passport = input("Enter the new passport number (or press Enter to keep current): ") or result[0]
                new_name = input("Enter the new name (or press Enter to keep current): ") or result[1]
                new_email = input("Enter the new email (or press Enter to keep current): ") or result[2]
                new_phone = input("Enter the new phone number (or press Enter to keep current): ") or result[3]
                validet=self.valid(new_passport,new_name,new_email,new_phone)
                if validet==True:
                    rc.execute("UPDATE users SET Passport_numper = ?, name = ?, email = ?, phone = ? WHERE Passport_numper = ?",(new_passport, new_name, new_email, new_phone, passport))
                    print("Member information updated successfully.")
                else:
                    print("the data invalid try agen...")       
            else:
                print("No member found with this passport number.")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            sleep(2)

    def delete(self):
        try:
            passport = input("Enter the passport number of the member to delete: ")
            rc.execute("SELECT * FROM users WHERE Passport_numper = ?", (passport,))
            result = rc.fetchone()
            if result:
                rc.execute("DELETE FROM users WHERE Passport_numper = ?", (passport,))
                print("Member deleted successfully.")

            else:
                print("No member found with this passport number.")
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        sleep(2)
   
    def valid(self,Passport_number,name,email,phone):
        try:
                # التأكد من صحة المدخلات
            if (
                "@" in  email and "." in  email
                and len( Passport_number) == 9
                and isinstance( name, str)
                and isinstance( phone, str) and  phone.isdigit() and len( phone) >= 8
            ):
                print("All inputs are valid!")
                return True  # المدخلات صحيحة
            else:
                print("Invalid inputs. Please check your data.")
                return False  # المدخلات غير صحيحة
        except Exception as e:  # التقاط الأخطاء غير المتوقعة
            print(f"Unexpected Error: {e}")
            return False
  

Member()
"""
Passport_number = type==str and len =9
name== any way writ
email "@" and "." in input
phone len>=8
"""