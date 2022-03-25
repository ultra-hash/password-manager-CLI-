import sqlite3, os


class db:

    def __init__(self, dbname) -> None:
        self.database = dbname
        self.db_path = os.getcwd()

        if not os.fspath(f"{os.getcwd()}+/{self.database}"):
            self.createTablePassword()

    def connect(self):
        self.conn = sqlite3.connect(self.database)
        self.curser = self.conn.cursor()

    def exec(self, queryString):
        execresult = self.conn.execute(queryString)
        return execresult
    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


    def createTablePassword(self):
        self.connect()
        self.conn.execute(f"""CREATE TABLE passwords(
            website_name text,
            username text,
            email text,
            password text
        );
        """)

    def select(self):
        self.connect()
        result = self.exec(f"SELECT rowid,* from passwords")
        result = result.fetchall()
        self.close()
        return result

    def add_entries_to_database(self):
        website = input("Enter The website name : ")
        username = input("Enter The usename : ")
        email = input("Enter The email address : ")
        password = input("Enter The password :")
        
        allgood = True
        #check entries given:
        if website and website != "":
            if username and username != "":
                if email and email != "":
                    if password and password != "":
                        pass
                    else:
                        print("Please enter a valid password")
                        allgood = False
                else:
                    print("Please enter a valid email address")
                    allgood = False
            else:
                print("Please enter a valid username")
                allgood = False
        else:
            print("Please enter a valid website")
            allgood = False
        
        if not allgood:
            return 

        self.connect()
        self.exec(f"INSERT INTO passwords VALUES ('{website}', '{username}', '{email}', '{password}')")
        self.commit()
        self.close()

    def delete_entries_by_rowid(self, rowid):
        self.connect()
        self.exec(f"DELETE FROM passwords WHERE rowid={rowid}")
        self.commit()
        self.close()

if __name__ == "__main__":
    data = db('dbpass.db')
    #data.add_entries_to_database()
    print(data.select())
    #data.delete_entries_by_rowid(3)
    