from mysql.connector import connect, Error
from datetime import datetime
import csv, logging


class DB:
    def __init__(self, host, username, password, db_name):
        self.host = host
        self.username = username
        self.password = password
        self.db_name = db_name
        self.db = None
        self.cur = None

    def create_db(self):
        try:
            temp_db = connect(host=self.host, user=self.username, password=self.password)
            temp_cur = temp_db.cursor()
            temp_cur.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
            temp_db.close()
        except Error as e:
            self.log_error(f"Database creation Error: {e}")
    
    def connect_db(self):
        self.db = connect(host=self.host, user=self.username, password=self.password, database=self.db_name)
        self.cur = self.db.cursor()
    
    def show_table(self):
        self.cur.execute("SHOW TABLES")
        for table in self.cur:
            print(table)


    def create_user_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY, access_hash BIGINT, name TEXT, username TEXT, phone TEXT, date DATETIME)")

    def create_admins_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS admins (id BIGINT PRIMARY KEY, name TEXT, username TEXT, promotion_date DATETIME)")

    def create_bans_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS ban_list (id BIGINT PRIMARY KEY, name TEXT, username TEXT, banned_date DATETIME)")


    def insert_admin(self, user_id):
        self.cur.execute("SELECT id, name, username FROM users WHERE id = %s LIMIT 1", (user_id,))
        res = self.cur.fetchone()

        if res:
            data = (res[0], res[1], res[2], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.cur.execute(f"INSERT INTO admins (id, name, username, promotion_date) VALUES (%s, %s, %s, %s)", data)
            self.db.commit()
            return 1
        return 0

    def insert_user(self, user, access_hash):
        data = (user.id, access_hash, user.first_name + (user.last_name or ''), user.username or "None", getattr(user, 'phone', 'hidden'), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        try:
            self.cur.execute(f"INSERT INTO users (id, access_hash, name, username, phone, date) VALUES (%s, %s, %s, %s, %s, %s)", data)
            self.db.commit()
        except: # if User already exists
            pass


    def select_admins(self):
        self.cur.execute("SELECT id, name, username, promotion_date FROM admins")
        try:
            users = list(map(lambda a: list(a), self.cur.fetchall()))
            users = sorted(users, key=lambda a: a[3])
            with open("files\\admins.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Username", "Promotion_Date"])
                writer.writerows(users)

            self.cur.execute("SELECT COUNT(*) FROM admins")
            total_admins = self.cur.fetchone()
            return total_admins[0]

        except Exception as e:
            self.log_error(f"Error selecting admins: {e}")

    def select_users(self):
        try:
            self.cur.execute("SELECT id, access_hash, name, username, date FROM users")
            users = list(map(lambda a: list(a), self.cur.fetchall()))
            users = sorted(users, key=lambda a: a[4])
            with open("files\\users.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Access Hash", "Name", "Username", "Date"])
                writer.writerows(users)

            self.cur.execute("SELECT COUNT(*) FROM users")
            total_users = self.cur.fetchone()
            return total_users[0]

        except Exception as e:
            self.log_error(f"Error selecting users: {e}")


    def select_user(self, user_id):
        self.cur.execute("SELECT date FROM users WHERE id = %s", (user_id,))
        return self.cur.fetchone()[0]
    
    def select_bans(self):
        try:
            self.cur.execute("SELECT id, name, username, banned_date FROM ban_list")
            users = list(map(lambda a: list(a), self.cur.fetchall()))
            users = sorted(users, key=lambda a: a[3])
            with open("files\\banned_users.csv", 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Username", "Banned_Date"])
                writer.writerows(users)

            self.cur.execute("SELECT COUNT(*) FROM ban_list")
            total_users = self.cur.fetchone()
            return total_users[0]

        except Exception as e:
            self.log_error(f"Error selecting banned_list: {e}")


    def del_admin(self, user_id):
        self.cur.execute("DELETE FROM admins WHERE id = %s", (user_id,))
        self.db.commit()

        return self.cur.rowcount

    def ban_user(self, user_id):
        self.cur.execute("SELECT id, name, username FROM users WHERE id = %s LIMIT 1", (user_id,))
        res = self.cur.fetchone()
        if res:
            data = (res[0], res[1], res[2], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.cur.execute(f"INSERT INTO ban_list (id, name, username, banned_date) VALUES (%s, %s, %s, %s)", data)
            self.db.commit()
            return 1

        return 0

    def unban_user(self, user_id):
        self.cur.execute("DELETE FROM ban_list WHERE id = %s", (user_id,))
        self.db.commit()

        return self.cur.rowcount


    def ban_list(self):
        self.cur.execute("SELECT id FROM ban_list")
        ids = [row[0] for row in self.cur.fetchall()]
        return ids

    def admins_list(self):
        self.cur.execute("SELECT id FROM admins")
        ids = [row[0] for row in self.cur.fetchall()]
        return ids

    def users_list(self):
        self.cur.execute("SELECT id FROM users")
        ids = [row[0] for row in self.cur.fetchall()]
        return ids

    def show_dbs(self):
        self.cur.execute("SHOW DATABASES")
        for i in self.cur:
            print(i)

    def edit_tabel(self, table, column):
        self.cur.execute(f"ALTER TABLE {table} ADD COLUMN {column}")

    def delete_db(self):
        self.cur.execute("DROP DATABASE bot")

    def delete_table(self, table):
        self.cur.execute(f"DROP TABLE {table}")

    def close(self):
        self.cur.close()
        self.db.close()
        
    def log_error(self, error):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("errors.log", "a") as f:
            f.write(f"[{date}]\n{error}\n")
        logging.error(error)
    
    def edit(self):
        pass


def get_db():
    with open("files\\tokens.csv", "r") as f:
        c = csv.reader(f)
        c = list(c)[2]
        return c[0].strip(), c[1].strip(), c[2].strip(), c[3].strip()


if __name__ == "__main__":
    HOST, USERNAME, PASSWORD, DB_NAME = get_db()
    db = DB(host=HOST, username=USERNAME, password=PASSWORD, db_name=DB_NAME)
    db.connect_db()
    # db.create_db()
    # db.show_dbs()
    # db.create_user_table()
    # db.create_admins_table()
    # db.create_bans_table()
    # db.show_table()
    # db.select_admins()
    # db.select_bans()
    db.close()
    print("ALL DONE")

# inp = input()
# while inp != '0':
#     eval(f"db.{inp}")
#     inp = input()


