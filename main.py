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
        print("5. Go Back")
        user_opt = int(input("Option: "))
        if user_opt == 1:
            ShowBooksFromInventory(cursor)
                
        elif user_opt == 2:
            AddBookToInventory(con, cursor)
                
        elif user_opt == 3:
            while True:
                deleteBookFromInventory(con)
                run_again = ""
                while run_again != "n":
                    run_again = input("\nDo you want to delete more books?(y/n): ").strip().lower()
                    if run_again == "y":
                        deleteBookFromInventory(con)
                        break
                    elif run_again == "n":
                        print("\n(!) Going Back... (!)\n")
                        pass
                    else:
                        print("(!) Invalid Choice (!)\n")
        elif user_opt == 4:
            UpdateRecordInInventory(con, cursor)
        elif user_opt == 5:
            break
        else:
            print("\n(!) Invalid Option (!)\n")

def issueBookMenu():
    while True:
        print("\n(!) Issue Book Menu (!)\n")
        print("1. Issue a Book")
        print("2. View Issued Books")
        print("3. Delete Issued Book Record")
        print("4. Update Issued Book Record")
        print("5. Go Back")
        user_opt = input("Choose an option: ").strip()

        if user_opt == "1":
            issueBook()
        elif user_opt == "2":
            viewIssuedBooks()
        elif user_opt == "3":
            deleteIssuedBook()
        elif user_opt == "4":
            updateIssuedBook()
        elif user_opt == "5":
            break
        else:
            print("(!) Invalid Choice (!)\n")

def issueBook():
    con = checkMySQL()
    if not con:
        print("(!) No Connection! (!)")
        return

    cursor = con.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                issue_id VARCHAR(10) PRIMARY KEY,
                bookid VARCHAR(5),
                enrollment_no VARCHAR(15),
                issue_date DATE,
                return_date DATE,
                FOREIGN KEY (bookid) REFERENCES inventory(bookid)
            )
        """)
        con.commit()
    except Exception as e:
        print("(!) Error creating issues table (!)\nError: ", e)
        return

    print("(!) Issue Book (!)\n")
    issue_id = input("Enter Issue ID: ").strip()
    bookid = input("Enter Book ID: ").strip()
    enrollment_no = input("Enter Enrollment No: ").strip()
    issue_date = input("Enter Issue Date (YYYY-MM-DD): ").strip()
    return_date = input("Enter Return Date (YYYY-MM-DD): ").strip()

    try:
        cursor.execute(f"""
            INSERT INTO issues (issue_id, bookid, enrollment_no, issue_date, return_date)
            VALUES ('{issue_id}', '{bookid}', '{enrollment_no}', '{issue_date}', '{return_date}')
        """)
        con.commit()
        print("(!) Book issued successfully (!)\n")
    except Exception as e:
        print("(!) Error issuing book (!)\nError: ", e)

def viewIssuedBooks():
    con = checkMySQL()
    if not con:
        print("(!) No Connection! (!)")
        return

    cursor = con.cursor()
    try:
        cursor.execute("SELECT * FROM issues")
        records = cursor.fetchall()
        print("\n(!) Issued Books: (!)\n")
        for record in records:
            print(record)
    except Exception as e:
        print("(!) Error fetching issued books (!)\nError: ", e)

def deleteIssuedBook():
    con = checkMySQL()
    if not con:
        print("(!) No Connection! (!)")
        return

    cursor = con.cursor()
    issue_id = input("Enter Issue ID to delete: ").strip()
    try:
        cursor.execute(f"DELETE FROM issues WHERE issue_id = '{issue_id}'")
        con.commit()
        print("(!) Issued book record deleted successfully (!)\n")
    except Exception as e:
        print("(!) Error deleting issued book record (!)\nError: ", e)

def updateIssuedBook():
    con = checkMySQL()
    if not con:
        print("(!) No Connection! (!)")
        return

    cursor = con.cursor()
    issue_id = input("Enter Issue ID to update: ").strip()
    try:
        cursor.execute(f"SELECT * FROM issues WHERE issue_id = '{issue_id}'")
        record = cursor.fetchone()
        if not record:
            print("(!) No record found with the given Issue ID (!)\n")
            return

        print("Current Record: ", record)
        bookid = input("Enter new Book ID (leave blank to keep current): ").strip() or record[1]
        enrollment_no = input("Enter new Enrollment No (leave blank to keep current): ").strip() or record[2]
        issue_date = input("Enter new Issue Date (YYYY-MM-DD, leave blank to keep current): ").strip() or record[3]
        return_date = input("Enter new Return Date (YYYY-MM-DD, leave blank to keep current): ").strip() or record[4]

        cursor.execute(f"""
            UPDATE issues
            SET bookid = '{bookid}', enrollment_no = '{enrollment_no}', issue_date = '{issue_date}', return_date = '{return_date}'
            WHERE issue_id = '{issue_id}'
        """)
        con.commit()
        print("(!) Issued book record updated successfully (!)\n")
    except Exception as e:
        print("(!) Error updating issued book record (!)\nError: ", e)

def library_stats():
    con = checkMySQL()
    if not con:
        print("(!) No Connection! (!)")
        return

    cursor = con.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM inventory")
        total_books = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM issues")
        total_issued_books = cursor.fetchone()[0]

        print("\n(!) Library Stats (!)\n")
        print(f"Total Books: {total_books}")
        print(f"Total Issued Books: {total_issued_books}")
    except Exception as e:
        print("(!) Error fetching library stats (!)\nError: ", e)

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
            issueBookMenu()
        elif (user_value == "stats" or user_value == "3"):
            library_stats()
        elif (user_value == "exit" or user_value == "4"):
            break
        else:
            print("\n(!) Invalid Choice (!)\n")
            time.sleep(1)
    else:
        print("(!) No Connection! (!)")
