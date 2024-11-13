# Library Management Project
# By: Jujhar Singh
import time
import mysql.connector as m
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
                return True, con
        return False, None
    except Exception as e:
        print(e)
        print("No Connection!")

def updateInv(con, column, value, condition=None):
    print()


class Book:
    def __init__(self, con, bookid, book_sno, book_name, book_quantity, book_price, book_theme, book_author):
        self.bookid = bookid
        self.book_sno = book_sno
        self.book_name = book_name
        self.book_quantity = book_quantity
        self.book_price = book_price
        self.book_theme = book_theme
        self.book_author = book_author
        self.mysql_con = con

    def insertBook(self):
        if self.mysql_con:
            try:
                cur = self.mysql_con.cursor()
                cur.execute(f"insert into inventory values('{self.bookid}', {self.book_sno}, '{self.book_name}', {self.book_quantity}, {self.book_price}, '{self.book_theme}', '{self.book_author}')")
                self.mysql_con.commit()
            except:
                cur.execute(f"select * from table where bookid = {self.bookid}")
                if (cur):
                    print("(!) Unable to add as bookid already exists (!)")
                else:
                    print("Error: (!) Unable to add Book (!)")

    def deleteBook(self, bookid):
        cur=self.mysql_con.cursor()
        cur.execute(f"delete from inventory where bookid = '{bookid}'")
        self.mysql_con.commit()


def inventory():
    conExist, Mysql_con = checkMySQL()

    if conExist:
        cur = Mysql_con.cursor()
        print("\n\nOptions Available")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. Update Book")
        user_opt = int(input("Option: "))
        if (user_opt == 1):
            while True:
                cur.execute("SHOW COLUMNS from inventory")
                columns = cur.fetchall()
                columns = [column[0] for column in columns]
                temp_book_value = {}
                for column in columns:
                    temp_book_value[column] = input(f"Inset Value for {column}: ")
                book = Book(Mysql_con, temp_book_value["bookid"], temp_book_value["book_sno"], temp_book_value["book_name"], temp_book_value["book_quantity"], temp_book_value["book_price"], temp_book_value["book_theme"], temp_book_value["book_author"])
                book.insertBook()

                cur.execute("select * from inventory")
                for row in cur:
                    print(row)


    # con=m.connect(host='localhost', user='root', password='20062006', database= 'Library')
    # cur=con.cursor()
    # a="create database Library"
    # b="create table inventory(bookid varchar(10) primary key, Sno int(15), name varchar(35), quantity int(35), price float(6,2), theme varchar(30), author varchar(25) )"
    # c="""insert into inventory values
    # ("b0001", 1, "Harry Potter", 5, 150, "fantasy", "J.K. Rowling"),
    # ("b0002", 2, "Metamorphosis", 10, 250, "surreal", "Franz Kafka"),
    # ("b0003", 3, "The Great Gatsby", 8, 200, "tragedy", "F.Scott Fitzgerald"),
    # ("b0004", 4, "The Adventures Of Sherlock Holmes", 15, 300, "Thriller", "Sir Arthur Conan Doyle" ),
    # ("b0005", 5, "Pride And Prejudice", 10, 200,"fiction", "Jane Austen")"""




while True:
    print("Welcome to My Library")
    print("\n\nPrograms you can perform:")
    print("1. Inventory")
    print("2. Issue book")
    print("3. Stats")
    print("4. Exit\n")

    user_value = input("What action do you want to perform: ").strip().lower()
    if (user_value == "inventory" or user_value == "1"):
        inventory()
    elif (user_value == "issue book" or user_value == "2"):
        issue_book()
    elif (user_value == "stats" or user_value == "3"):
        library_stats()
    elif (user_value == "exit" or user_value == "4"):
        break
    else:
        print("\n(!) Invalid Choice (!)\n")
        time.sleep(1)
