from parserconf import conf_BD
from mysql.connector import MySQLConnection, Error


class User:
    def check_table(self):
        conn = MySQLConnection(**conf_BD())
        cursor = conn.cursor()
        try:
            with conn:
                cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
                                                        id INT PRIMARY KEY AUTO_INCREMENT,
                                                        id_user INT,
                                                        name TEXT,
                                                        quotes VARCHAR(7) DEFAULT NULL,      
                                                        time TIME DEFAULT NULL)""")
                conn.commit()
        except Error as e:
            print(e)

    def insert_db(self, user_id, name, time):
        self.check_table()
        conn = MySQLConnection(**conf_BD())
        cursor = conn.cursor()
        try:
            with conn:

                args = (user_id, name, time)
                query = "INSERT INTO Users(id_user, name, time) VALUES(%s, %s, %s)"
                cursor.execute(query, args)
                conn.commit()
        except Error as e:
            print(e)

    def update_db(self, quotes):
        self.check_table()
        conn = MySQLConnection(**conf_BD())
        cursor = conn.cursor()
        try:
            with conn:
                args = (quotes, self.return_id())
                query = "UPDATE Users SET quotes= %s WHERE id=%s"
                cursor.execute(query, args)
                conn.commit()
        except Error as e:
            print(e)

    def return_id(self):
        self.check_table()
        conn = MySQLConnection(**conf_BD())
        cursor = conn.cursor()
        try:
            with conn:
                cursor.execute("SELECT id FROM Users")
                all_id = cursor.fetchall()
                last_id = list(max(all_id))
                for i in last_id:
                    return i
        except Error as e:
            print(e)

    def return_quotes(self, id_users):
        conn = MySQLConnection(**conf_BD())
        cursor = conn.cursor()
        quotes = []
        try:
            with conn:
                cursor.execute(f"""SELECT quotes FROM Users WHERE id_user={id_users}""")
                for quots in cursor.fetchall():
                        convert = list(quots[0])
                        quotes.append("".join(convert))
                return quotes
        except Error as e:
            print(e)

    def return_time(self, id_user):
        conn = MySQLConnection(**conf_BD())
        cursor = conn.cursor()

        try:
            with conn:
                cursor.execute(f"""SELECT time FROM Users WHERE id_user={id_user} """)
                time = list()
                for times in cursor.fetchall():
                    time.append(str(times[0]))
                return time
        except Error as e:
            print(e)

"""
a.insert_db(417610028, "Taide", "22:11")
a.update_db("RUB USD")
a.insert_db(417610028, "Taide", "22:12")
a.update_db("SUB SSD")
a.insert_db(417610028, "Taide", "22:12")
a.update_db("DUB DSD")
a.insert_db(417610028, "Taide", "22:13")
a.update_db("ZUB ZSD")
"""


