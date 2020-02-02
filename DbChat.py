import sys
import os
from time import sleep
import bcrypt
import sqlite3
from sqlite3 import Error

#Sherlock - 1234
#Watson - Hamish
#Mycroft - Eurus



userAction = ""
username = ""
password = ""
login = 1
clear = lambda: os.system('cls')


def main():
    clear()
    print("Welcome to PyChat 1.0")
    conn = create_connection("chat.sqlite")
    #select_all_users(conn)

    username = input("Type your username: ")
    password = input("Type your password: ")
    valid = select_PWH(conn, username)
    if valid and bcrypt.checkpw(password.encode(), valid.encode()):
        print("Login sucessful")
        print("")

        chat(username)
    else:
        print("The submitted credentials do not match")
        print("Access Denied, try again in a few seconds")
        sleep(4)
        main()



def chat(user):
    while login == 1:
        clear()
        print("Welcome " + user)
        print("Inbox:")
        conn = create_connection("chat.sqlite")
        getMessages(conn, user)
        print("")
        print("What would you like to do?")
        userAction = input("1: Refresh messages, 2: Send messages , 3: Log out  ")

        if userAction == "1":
            clear()


        elif userAction == "2":
            toUser = input("Send message to: ")
            if(checkforUser(conn, toUser)):
                toUser = str(usernameToId(conn, toUser))
                content = input("Type your message: ")
                sendMessage(conn, str(usernameToId(conn, user)), toUser, content)
            else:
                print("No such user")
        elif userAction =="3":
            main()


def checkforUser(conn, username):
    cur = conn.cursor()
    cur.execute("SELECT Username FROM Users")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == username:
            return True
    else:
        return False

def sendMessage(conn, fromUser, toUser, content):
    cur = conn.cursor()
    cur.execute("Insert into Messages(fromUser, toUser, Content) Values('" +fromUser+  "', '"  +toUser+    "','"  +content+   "')")
    conn.commit()

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_PWH(conn, user):
    cur = conn.cursor()
    cur.execute("SELECT Password FROM users WHERE Username = '"+user+"'")
    row = cur.fetchone()
    return row[0] if row else None

def select_all_users(conn):

    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def usernameToId(conn, user):
    cur = conn.cursor()
    cur.execute("SELECT ID FROM users WHERE Username = '"+user+"'")
    row = cur.fetchone()
    return row[0] if row else None

def idToUsername(conn, id):
    cur = conn.cursor()
    cur.execute("SELECT Username FROM users WHERE ID = '"+str(id)+"'")
    row = cur.fetchone()
    return row[0] if row else None


def getMessages(conn, user):
    cur = conn.cursor()
    if isinstance(user, str):
        user = str(usernameToId(conn,user))
    cur.execute("SELECT * FROM Messages WHERE toUser = '"+user+"'")
    rows = cur.fetchall()
    for row in rows:
        print(f"{idToUsername(conn,row[1]):>10} : {row[3]:>10}")



main()
