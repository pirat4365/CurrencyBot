from parserconf import conf_BD
from mysql.connector import MySQLConnection


def insert_db(id_users, name, choice, times):
    query = "INSERT INTO Users(id_users, name, quotes, time) VALUES(%s, %s, %s, %s)"
    args = (id_users, name, choice, times)
    db_config = conf_BD()
    conn = MySQLConnection(**db_config)
    with conn:
        cursor = conn.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS Users(
                                            id_users INT, 
                                            name TEXT, 
                                            quotes TEXT, 
                                            time TIME)""")
        cursor.execute(query, args)
        conn.commit()


def check_data(args, text):
    db_config = conf_BD()
    conn = MySQLConnection(**db_config)
    id_users = []
    quotes_users = []
    time_users = []
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Users")

        rows = cur.fetchall()

        for row in rows:
            if row[0] == args:
                id_users.append(row[0])
                time_users.append(row[3])
                quotes_users.append(row[2])

    if args in id_users:
        if text == "quotes":
            return quotes_users
        elif text == "time":
            return time_users
    else:
        return False
