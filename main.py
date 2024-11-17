# Library Management Project
# By: Jujhar Singh
import time
import mysql.connector as m
import re
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "20062006"
MYSQL_DATABASE = "library"

def checkMySQL():
    try:
        con = m.connect(host="localhost", user=MYSQL_USERNAME, password=MYSQL_PASSWORD)
        # Check if database exists
        cursor = con.cursor()
        cursor.execute("SHOW DATABASES")
        for db in cursor:
            if db[0] == MYSQL_DATABASE:
                con.close()
                con = m.connect(host="localhost", user=MYSQL_USERNAME, password=MYSQL_PASSWORD, database=MYSQL_DATABASE)
                return con
        try:
            cursor.execute("create database library")
            con.commit()
            cursor.execute("use library")
            con.commit()
            con = m.connect(host="localhost", user=MYSQL_USERNAME, password=MYSQL_PASSWORD, database=MYSQL_DATABASE)
            return con
        except:
            print("Error!!!!")
            return False, None
    except Exception as e:
        print(e)
        print("No Connection!")
        return None


class Book:
    def __init__(self, con, book_info):
        self.bookid = book_info["bookid"]
        self.book_sno = book_info["book_sno"]
        self.book_name = book_info["book_name"]
        self.book_quantity = book_info["book_quantity"]
        self.book_price = book_info["book_price"]
        self.book_theme = book_info["book_theme"]
        self.book_author = book_info["book_author"]
        self.mysql_con = con

    def insertBook(self):
        if self.mysql_con:
            try:
                cur = self.mysql_con.cursor()
                cur.execute(f"insert into inventory values('{self.bookid}', {self.book_sno}, '{self.book_name}', {self.book_quantity}, {self.book_price}, '{self.book_theme}', '{self.book_author}')")
                self.mysql_con.commit()
                print("(!) Book added successfully (!)\n")
            except:
                try:
                    cur.execute(f"select * from inventory where bookid = {self.bookid}")
                    if (cur):
                        print("\n(!) Unable to add as bookid already exists (!)\n")
                    else:
                        print("\nError: (!) Unable to add Book (!)\n")
                except:  
                    print("\nError: (!) Unable to add Book (!)\n")

def ShowBooksFromInventory(cur):
    # Option for (10 each time, custom range)
    while True:
        print("(!) Show Books (!)\n")
        print("1. 10 each iteration")
        print("2. Custom (Custom Query)")
        print("3. Go Back")
        user_opt = int(input("(!) Value: "))
        if (user_opt == 1):
            start = 1
            stop = 10
            while True:
                cur.execute(f"select * from inventory where book_sno >= {start} and book_sno <= {stop}")
                records = cur.fetchall()
                print("\n(!) Records in Database: (!) \n")
                for row in records:
                    print(row)
                if (len(records) > 10):
                    wantMore = ""
                    while (wantMore != "n"):
                        wantMore = input("\n(!) Do you want to see 10 more records?(y/n): ").strip().lower()
                        if (wantMore == "y"):
                            start = stop
                            stop += 10
                            break
                        elif (wantMore == "n"):
                            pass
                        else:
                            print("(!) Enter Valid Option (!)")
                else:
                    print(f"\n(!) Going Back... Only {len(records)} Records Exists! (!)\n")
                    ShowBooksFromInventory(cur)
                    break
            break
        elif (user_opt == 2):
            print("\n(!) Custom Query (!)\n")
            while True:
                cur.execute("SHOW COLUMNS from inventory")
                columns = cur.fetchall()
                columns = [column[0] for column in columns]
                print("(!) HELP (!) Existing Columns: ", columns)
                try:
                    user_query = input("(!) MySQL Query: ").strip()
                    cur.execute(user_query)
                except:
                    print("\n(!) Invalid Query (!)\n")
                output = cur.fetchall()
                print("(!) Output: (!)\n")
                for record in output:
                    print(record)
                print()
                run_more = input("\nWant to run more?(y/n): ").strip()
                if (run_more == "y"):
                    pass
                elif (run_more == "n"):
                    break
                else:
                    print("(!) Enter Valid Option (!)\n")
        elif (user_opt == 3):
            print("\n(!) Going Back.... (!)\n")
            inventory(con)
        else:
            print("\nInvalid Option!\n")

def AddBookToInventory(con, cur):
    print("(!) Add New Book (!)\n")
    cur.execute("SHOW COLUMNS from inventory")
    columns = cur.fetchall()
    columns = [column[0] for column in columns if column[0] != "bookid"]
    temp_book_value = {}
    while True:
        book_id = input("(!) Value for bookid: ")
        if re.match(r'^\d{5}$', book_id):
            break
        else:
            print("(!) bookid should be of 5 digits (!) and cannot contain non-numeric characters.")
    for column in columns:
        temp_book_value[column] = input(f"(!) Value for {column.title()}: ")
    temp_book_value["bookid"] = book_id
    book = Book(con, temp_book_value)
    book.insertBook()
    temp_book_value = {}
    run_again = ""
    while (run_again != "n"):
        run_again = input("\nDo you want to add more books?(y/n): ").strip().lower()
        if run_again == "y":
            AddBookToInventory(con, cur)
            break
        elif run_again == "n":
            break
        else:
            print("(!) Invalid Choice (!)\n")

def deleteBookFromInventory(con):
    cur = con.cursor()
    print("(!) Delete A Book (!)\n")
    user_opt = input("(!) Enter 'bookid' you want to remove?(eg. 00001 or 'goback'): ")
    if user_opt == "goback":
        inventory(con)
    else:
        cur.execute(f"select * from inventory where bookid = {user_opt}")
        result = cur.fetchall()
        if (len(result) == 0):
            print("\n(!) No record Exist (!)\nPlease enter a valid 'bookid' (!)\n")
            deleteBookFromInventory(con)
        else:
            print(result[0])
            confirm = ""
            while (confirm != "y"):
                confirm = input("(!) Confirm do you want to delete this book data? (!) (y/n): ").strip().lower()
                if confirm == "y":
                    cur.execute(f"delete from inventory where bookid = {user_opt}")
                    con.commit()
                    print("(!) Book Record Deleted (!)")
                elif confirm == "n":
                    deleteBookFromInventory(con)
                else:
                    print("(!) Invalid Chocie (!)")
                    deleteBookFromInventory(con)

def UpdateRecordInInventory(con, cur):
    print("(!) Update Book Record (!)\n")
    user_book = int(input("(!) In which 'bookid' do you want to make changes?(eg. 00001): "))
    cur.execute(f"select * from inventory where bookid = {user_book}")
    result = cur.fetchall()
    if (len(result) == 0):
        print("\n(!) No record Exist (!)\nPlease enter a valid 'bookid' (!)\n")
    else:
        print("Book Record Found! - ", result)
        cur.execute("SHOW COLUMNS from inventory")
        columns = cur.fetchall()
        columns = [column[0] for column in columns]
        while True:
            print(columns,'\n')
            user_column = input("(!) Choose Column: ").strip()
            if user_column not in columns:
                print("(!) Column Doesn't Exists (!)")
            else:
                column_value = input("(!) Value: ")
                if column_value.isdigit(): 
                    column_value = int(column_value)
                else:
                    column_value = f"'{column_value}'"
                try:
                    cur.execute(f"update inventory set {user_column} = {column_value} where bookid = {user_book}")
                    con.commit()
                except Exception as e:
                    print("(!) Error Occured while updating record (!)\nError: ", e)
                break
    while True:
        run_again = input("Do you want to update more book records?(y/n): ").strip().lower()
        if run_again == "y":
            UpdateRecordInInventory(con, cur)
            break
        elif run_again == "n":
            print("\n(!) Going Back... (!)\n")
            inventory(con)
            break
        else:
            print("(!) Invalid Choice (!)\n")

def inventory(con):
    cursor = con.cursor()

    try:
        cursor.execute("create table inventory(bookid varchar(5) primary key, book_sno int(30), book_name varchar(30), book_quantity int(15), book_price int(8),book_theme varchar (20), book_author varchar (20))")
        con.close()
    except:
        pass
    while True:
        print("\nOptions Available")
        print("1. Show Books")
        print("2. Add Book")
        print("3. Delete Book")
        print("4. Update Book")
        user_opt = int(input("Option: "))
        if (user_opt == 1):
            ShowBooksFromInventory(cursor)
                
        elif (user_opt == 2):
            AddBookToInventory(con, cursor)
                
        elif (user_opt == 3):
            while True:
                deleteBookFromInventory(con)
                run_again = ""
                while (run_again != "n"):
                    run_again = input("\nDo you want to delete more books?(y/n): ").strip().lower()
                    if run_again == "y":
                        deleteBookFromInventory(con)
                        break
                    elif run_again == "n":
                        print("\n(!) Going Back... (!)\n")
                        pass
                    else:
                        print("(!) Invalid Choice (!)\n")
        elif (user_opt == 4):
            UpdateRecordInInventory(con, cursor)
        else:
            print("\n(!) Invalid Option (!)\n")

def issueBook():
    print("\n(!) Issue Book (!)\n")
    # Step 1: Get the book ID
    book_id = input("Enter the 'bookid' of the book you want to issue (e.g., 00001): ").strip()
    
    # Step 2: Check if the book exists in the inventory
    cur = con.cursor()
    cur.execute(f"SELECT * FROM inventory WHERE bookid = '{book_id}'")
    book = cur.fetchone()
    
    if not book:
        print("\n(!) No such book found with that 'bookid'. Please try again. (!)\n")
        return
    
    # Step 3: Check if the book has available quantity
    available_quantity = book[3]  # book_quantity is the 4th column (index 3)
    
    if available_quantity <= 0:
        print("\n(!) Sorry, this book is currently out of stock. Please try again later. (!)\n")
        return
    
    # Step 4: Record the transaction (for simplicity, just a print for now)
    # You could extend this by adding a table like 'issued_books' where you log who issued the book, etc.
    
    print(f"\n(!) Issuing Book: {book[2]} ({book_id}) - Quantity: {available_quantity} (!)\n")
    
    # Update the book quantity in the inventory (decrease by 1)
    new_quantity = available_quantity - 1
    cur.execute(f"UPDATE inventory SET book_quantity = {new_quantity} WHERE bookid = '{book_id}'")
    con.commit()
    
    print(f"\n(!) Book '{book[2]}' has been issued successfully. Remaining Quantity: {new_quantity} (!)\n")
    
    # Step 5: Option to issue more books
    run_again = input("\nDo you want to issue another book? (y/n): ").strip().lower()
    if run_again == "y":
        issueBook()  # Recursively call to issue another book
    else:
        print("\n(!) Going Back to Main Menu... (!)\n")
        return


while True:
    con = checkMySQL()
    if (con):
        print("Welcome to My Library")
        print("\n\nPrograms you can perform:")
        print("1. Inventory")
        print("2. Issue book")
        print("3. Stats")
        print("4. Exit\n")

        user_value = input("What action do you want to perform: ").strip().lower()
        if (user_value == "inventory" or user_value == "1"):
            inventory(con)
        elif (user_value == "issue book" or user_value == "2"):
            issueBook()
        elif (user_value == "stats" or user_value == "3"):
            library_stats()
        elif (user_value == "exit" or user_value == "4"):
            break
        else:
            print("\n(!) Invalid Choice (!)\n")
            time.sleep(1)
    else:
        print("(!) No Connection! (!)")
