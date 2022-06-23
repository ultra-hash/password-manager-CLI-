import app

db = app.db('cipherpass.db', 'key')
Display = True
Root = "\n[1] -> view , [2] -> ADD , [3] -> EDIT , [4] -> DELETE , [5] -> EXIT\n"

def view():
    # [s.no, website_max_len , username_max_len ,email_max_len, password_max_len ]
    max_len_list = [4,0,10,15,0]

    # fetching results from db
    result = db.selectall()

    # For counting max_lens for table creation
    for i in range(len(result)):
        for j in range(len(result[i])):
            if len(str(result[i][j])) > max_len_list[j]:
                max_len_list[j] = len(str(result[i][j]))

    # Printing as table
    print("".ljust((sum(max_len_list)+(6*3))//2, '-') + "".rjust((sum(max_len_list)+(6*3))//2, '-')) # decoration
    #print("| "+ "s.no".center(max_len_list[0]) + " | " + "website".center(max_len_list[1]) + " | " + "username".center(max_len_list[2]) + " | " + "email address".center(max_len_list[3]) + " | " + "password".center(max_len_list[4]) + " |" )
    print("| "+ "s.no".center(max_len_list[0]) + " | " + "website".center(max_len_list[1]) + " | " + "username".center(max_len_list[2]) + " | " + "email address".center(max_len_list[3]) + " | " + "For password".center(17) + " |" )
    print("".ljust((sum(max_len_list)+(6*3))//2, '-') + "".rjust((sum(max_len_list)+(6*3))//2, '-')) # decoration

    for i in result:
        #print("| " + str(i[0]).ljust(max_len_list[0]) + " | " + str(i[1]).ljust(max_len_list[1]) + " | " + str(i[2]).ljust(max_len_list[2]) + " | " + str(i[3]).ljust(max_len_list[3]) + " | " + str(i[4]).ljust(max_len_list[4]) + " |")        
        print("| " + str(i[0]).ljust(max_len_list[0]) + " | " + str(i[1]).ljust(max_len_list[1]) + " | " + str(i[2]).ljust(max_len_list[2]) + " | " + str(i[3]).ljust(max_len_list[3]) + " | " + f"Press {i[0]} and Enter" + " |")        

    print("".ljust((sum(max_len_list)+(6*3))//2, '-') + "".rjust((sum(max_len_list)+(6*3))//2, '-')) # decoration


while Display:
    try: 
        print(Root)
        x = int(input(f"Enter One of The Options : "))
    except ValueError:
        print("\n\ninvalid input you must use number\n\n")
        continue

    if x == 1:
        view()
        try:
            rowid = int(input('Enter the s.no to show password or 0 to skip: '))
            if rowid == 0:
                continue
            else:
                print('Password: ', db.show_password_with_rowid(rowid))
        except ValueError:
            print("\n\nInvalid Input you must use number\n\n")
            continue
    elif x == 2:
        db.add_entries_to_database()
        view()
    elif x == 3:
        view()
        rowid = int(input('Enter the s.no to edit : '))
        db.edit_entries_by_rowid(rowid)
    elif x == 4:
        view()
        rowid = int(input('Enter the s.no to delete : '))
        db.delete_entries_by_rowid(rowid)
    elif x == 5:
        exit()
    else:
        print("invalid input you must use number between 1 - 5")
