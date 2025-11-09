from mysql.connector import connect, Error
from datetime import datetime
import csv, logging, os


class DB:
    def __init__(self, host, username, password, db_name):
        self.host = host
        self.username = username
        self.password = password
        self.db_name = db_name

    def create_db(self):
        try:
            with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
                con.ping(True)
                cur = con.cursor()
                cur.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
        except Error as e:
            self.log_error(f"Database creation Error: {e}")

    def connect_db(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
    
    def show_table(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("SHOW TABLES")
            for table in cur:
                print(table)


    def create_user_table(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY, access_hash BIGINT, name TEXT, username TEXT, phone TEXT, date DATETIME)")

    def create_admins_table(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS admins (id BIGINT PRIMARY KEY, name TEXT, username TEXT, promotion_date DATETIME)")

    def create_bans_table(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS ban_list (id BIGINT PRIMARY KEY, name TEXT, username TEXT, banned_date DATETIME)")


    def insert_admin(self, user_id):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("SELECT id, name, username FROM users WHERE id = %s LIMIT 1", (user_id,))
            res = cur.fetchone()

            if res:
                data = (res[0], res[1], res[2], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                cur.execute(f"INSERT INTO admins (id, name, username, promotion_date) VALUES (%s, %s, %s, %s)", data)
                con.commit()
                return 1
            return 0

    def insert_user(self, user, access_hash):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            data = (user.id, access_hash, user.first_name + (user.last_name or ''), user.username or "None", getattr(user, 'phone', 'hidden'), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            try:
                cur.execute(f"INSERT INTO users (id, access_hash, name, username, phone, date) VALUES (%s, %s, %s, %s, %s, %s)", data)
                con.commit()
            except: # if User already exists
                pass


    def select_admins(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("SELECT id, name, username, promotion_date FROM admins")
            try:
                users = list(map(lambda a: list(a), cur.fetchall()))
                users = sorted(users, key=lambda a: a[3])
                with open(os.path.join("files", "admins.csv"), 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Name", "Username", "Promotion_Date"])
                    writer.writerows(users)

                cur.execute("SELECT COUNT(*) FROM admins")
                total_admins = cur.fetchone()
                return total_admins[0]

            except Exception as e:
                self.log_error(f"Error selecting admins: {e}")

    def select_users(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            try:
                cur.execute("SELECT id, access_hash, name, username, date FROM users")
                users = list(map(lambda a: list(a), cur.fetchall()))
                users = sorted(users, key=lambda a: a[4])
                with open(os.path.join("files", "users.csv"), 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Access Hash", "Name", "Username", "Date"])
                    writer.writerows(users)

                cur.execute("SELECT COUNT(*) FROM users")
                total_users = cur.fetchone()
                return total_users[0]

            except Exception as e:
                self.log_error(f"Error selecting users: {e}")


    def select_user(self, user_id):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("SELECT date FROM users WHERE id = %s", (user_id,))
            return cur.fetchone()[0]

    def select_bans(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            try:
                cur.execute("SELECT id, name, username, banned_date FROM ban_list")
                users = list(map(lambda a: list(a), cur.fetchall()))
                users = sorted(users, key=lambda a: a[3])
                with open(os.path.join("files", "banned_users.csv"), 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["ID", "Name", "Username", "Banned_Date"])
                    writer.writerows(users)

                cur.execute("SELECT COUNT(*) FROM ban_list")
                total_users = cur.fetchone()
                return total_users[0]

            except Exception as e:
                self.log_error(f"Error selecting banned_list: {e}")


    def del_admin(self, user_id):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("DELETE FROM admins WHERE id = %s", (user_id,))
            con.commit()

            return cur.rowcount

    def ban_user(self, user_id):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("SELECT id, name, username FROM users WHERE id = %s LIMIT 1", (user_id,))
            res = cur.fetchone()
            if res:
                data = (res[0], res[1], res[2], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                cur.execute(f"INSERT INTO ban_list (id, name, username, banned_date) VALUES (%s, %s, %s, %s)", data)
                con.commit()
                return 1

            return 0

    def unban_user(self, user_id):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("DELETE FROM ban_list WHERE id = %s", (user_id,))
            con.commit()

            return cur.rowcount


    def ban_list(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("SELECT id FROM ban_list")
            ids = [row[0] for row in cur.fetchall()]
            return ids

    def admins_list(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("SELECT id FROM admins")
            ids = [row[0] for row in cur.fetchall()]
            return ids

    def users_list(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("SELECT id FROM users")
            ids = [row[0] for row in cur.fetchall()]
            return ids

    def show_dbs(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("SHOW DATABASES")
            for i in cur:
                print(i)

    def edit_tabel(self, table, column):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column}")

    def delete_db(self):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute("DROP DATABASE bot")

    def delete_table(self, table):
        with connect(host=self.host, user=self.username, password=self.password, database=self.db_name) as con:
            con.ping(True)
            cur = con.cursor()
            cur.execute(f"DROP TABLE {table}")


    def log_error(self, error):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(os.path.join("files", "errors.log"), "a") as f:
            f.write(f"[{date}]\n{error}\n")
        logging.error(error)
    
    def edit(self):
        pass


def get_db():
    with open(os.path.join("files", "tokens.csv"), "r") as f:
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
    print("ALL DONE")

# inp = input()
# while inp != '0':
#     eval(f"db.{inp}")
#     inp = input()


