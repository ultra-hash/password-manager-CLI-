import sqlite3, os
from cryptography.fernet import Fernet

class db:

    def __init__(self, dbname, key):
        self.database = dbname
        self.db_path = os.getcwd()
        self.key = ciphertext(key)

        if not os.path.exists(f"{self.database}"):
            self.createTablePassword()
            self.commit()
            self.close()

    def connect(self):
        self.conn = sqlite3.connect(self.database)
        self.curser = self.conn.cursor()

    def exec(self, queryString):
        execresult = self.curser.execute(queryString)
        return execresult

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


    def createTablePassword(self):
        self.connect()
        self.curser.execute(f"""CREATE TABLE passwords(
            website_name text,
            username text,
            email text,
            password text
        );
        """)

    def selectall(self):
        self.connect()
        result = self.exec(f"SELECT rowid,* from passwords")
        result = result.fetchall()
        self.close()
        return result

    def select_by_rowid(self, rowid):
        self.connect()
        result = self.exec(f"SELECT * from passwords WHERE rowid={rowid}")
        result = result.fetchall()
        self.close()
        return result

    def add_entries_to_database(self):
        website = input("Enter The website name : ").strip()
        username = input("Enter The usename : ").strip()
        email = input("Enter The email address : ").strip()
        password = input("Enter The password :").strip()
        
        allgood = True
        #check entries given:
        if website != "":
            if username != "" or email != "":
                if password != "":
                    pass
                else:
                    print("Please enter a valid password")
                    allgood = False
            else:
                print("Please enter atleast one valid username or email")
                allgood = False
        else:
            print("Please enter a valid website")
            allgood = False
        
        if not allgood:
            return 

        # encrypt password
        password = self.key.encrypt(password)

        password = str(password)[2:-1] # simple fix to work around quotation problem during submiting code high risk to leave this code

        #connecting to DB and sending to DB
        self.connect()
        self.exec(f"INSERT INTO passwords VALUES ('{website}', '{username}', '{email}', '{password}')")
        self.commit()
        self.close()

    def delete_entries_by_rowid(self, rowid):
        self.connect()
        self.exec(f"DELETE FROM passwords WHERE rowid={rowid}")
        self.commit()
        self.close()

    def edit_entries_by_rowid(self, rowid):
        # Retreving data from database
        [(website, username, email, password)] = self.select_by_rowid(rowid)
        
        # Decrypting password to show to user for editing password
        password = bytes(password, 'utf-8')
        password = self.key.decrypt(password)

        #Taking input to update
        print("Press Enter to leave as previous")
        edit_website = input(f"webiste -> {website} : ")
        edit_username = input(f"username -> {username} : ")
        edit_email = input(f"email -> {email} : ")
        edit_password = input(f"password -> {password} : ")

        #checking and updating variables before updating database
        edit_website = website if edit_website == "" else edit_website
        edit_username = username if edit_username == "" else edit_username
        edit_email = email if edit_email == "" else edit_email

        #Also encrypting password before sending into DB
        if edit_password == "":
            edit_password = password
        else:
            edit_password = self.key.encrypt(edit_password)
            edit_password = str(edit_password)[2:-1]


        self.connect()
        self.exec(f"""UPDATE passwords
            SET website_name = '{edit_website}',
            username = '{edit_username}',
            email = '{edit_email}',
            password = '{edit_password}'
            WHERE rowid = {rowid}
            """)
        self.commit()
        self.close()
    
    def show_password_with_rowid(self, rowid):
        [(website, username, email, password)] = self.select_by_rowid(rowid)
        
        # Decrypting password to show to user for editing password
        password = bytes(password, 'utf-8')
        password = self.key.decrypt(password)
        return password

class ciphertext:
    
    def __init__(self,keyname):
        self.name = keyname
        
        if not os.path.exists(self.name):
            self.generate_key()

    def generate_key(self):
        f = Fernet.generate_key()
        with open(self.name, 'wb') as file:
            file.write(f)
        
    def encrypt(self, token):
        with open(self.name, 'rb') as file:
            key = file.read()
        token = Fernet(key).encrypt(bytes(token,'utf-8'))
        return token

    def decrypt(self, token):
        with open(self.name, 'rb') as file:
            key = file.read()
        token = Fernet(key).decrypt(token)
        return token.decode('utf-8')

if __name__ == "__main__":
    #data = db('pass.db')
    #print(data.selectall())
    #data.add_entries_to_database()
    #data.delete_entries_by_rowid(2)
    #data.edit_entries_by_rowid(1)
    #print(data.selectall())

    # Put this somewhere safe!

    '''key = Fernet.generate_key()

    f = Fernet(key)

    with open('key', 'wb') as file:
        file.write(f)

    token = f.encrypt(b"A really secret message. Not for prying eyes.")

    print(token)

    token = f.decrypt(token)

    print(token)'''

    key = ciphertext('key')
    #name = input("enter your name : ")
    name = "swamy"
    e = key.encrypt(name)
    print(e, key.decrypt(e))
    b = e.strip()
    c = str(e)[2:-1]
    print(c,b)
    again = bytes(c, "utf-8")
    print(again, key.decrypt(again))