import sqlite3
import string
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from getpass import getpass

hasher = PasswordHasher(time_cost=3, parallelism=4, memory_cost=65536)

querys = [
    "",

    'SELECT Name,"top speed", "payload capacity", "cruising altitude", \
    generation, type From Planes ORDER BY Name DESC;',

    'SELECT Country.country_name, SUM(Ownership.Quantity) AS Total_Planes \
    FROM Ownership JOIN Country ON Ownership.country_id = \
    Country.country_id GROUP BY Country.country_name;'
]
break_code = 0
database = 'planes.db'
user_databace = 'users.db'


def login():
    with sqlite3.connect(user_databace) as db:
        cursor = db.cursor()
        try:
            loginsignup = int(input("Login: 1 Sign up: 2 Quit: 0 "))
            if loginsignup == 0:
                return 0
            elif loginsignup == 1:
                while True:
                    username = input("Username ")
                    pasword = getpass()
                    cursor.execute(f'SELECT username,pasword_hashed FROM user \
                                   WHERE username = "{username}";')
                    results = cursor.fetchall()
                    if len(results) == 1:
                        try:
                            hasher.verify(results[0][1], pasword)
                            print(f"Welcome {username.title()}")
                            return 1
                        except VerifyMismatchError:
                            print("Incorrect Password")
                    else:
                        print("User does not exist")
            elif loginsignup == 2:
                username = input("Username: ")
                pasword = getpass()
                first_name = input("First name: ")
                last_name = input("Last name: ")
                email = input("Email address: ")
                pasword = hasher.hash(pasword)
                cursor.execute(f'INSERT INTO user (username, pasword_hashed, \
                               first_name, last_name, email) Values \
                               ("{username}", "{pasword}", "{first_name}", \
                               "{last_name}", "{email}")')
        except ValueError:
            print("Invalid Input")
            login()


def return_database_query(query: string):
    with sqlite3.connect(database) as db:
        cursor = db.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        db.close
        return results


def databace_interface():
    while True:
        try:
            inputs = int(input("Input "))
            if inputs == break_code:
                break
            elif inputs == 1:
                tmp = return_database_query(querys[1])
                for tuple in tmp:
                    print(f"Name: {tuple[0]}  |  Top speed: {tuple[1]}km/h  \
|  Payload Capacity: {tuple[2]}kg  |  Cruising altitude: {tuple[3]}m  |  \
Generation: {tuple[4]}  |  Type: {tuple[5]}")
            elif inputs == 2:
                tmp = return_database_query(querys[2])
                for tuples in tmp:
                    print(F"Country: {tuples[0]} | Planes owned: {tuples[1]}")
        except (EOFError, ValueError):
            print("Invalid input must be a number")


if __name__ == "__main__":
    loginresult = login()
    if loginresult == 0:
        quit
    elif loginresult == 1:
        # sucseful login
        databace_interface()
        # sucsesfull signup
    elif loginresult == 2:
        databace_interface()
