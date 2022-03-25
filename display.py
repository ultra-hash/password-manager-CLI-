import app

db = app.db('pass.db')
Display = True
Root = "\n[1] -> view , [2] -> ADD , [3] -> EDIT , [4] -> DELETE , [5] -> EXIT\n"

def view():
    # [s.no, website_max_len , username_max_len ,email_max_len, password_max_len ]
    max_len_list = [4,0,0,0,0]

    # fetching results from db
    result = db.selectall()

    # For counting max_lens for table creation
    for i in range(len(result)):
        for j in range(len(result[i])):
            if len(str(result[i][j])) > max_len_list[j]:
                max_len_list[j] = len(str(result[i][j]))

    # Printing as table
    for i in result:
        print("| " + str(i[0]).ljust(max_len_list[0]) + " | " + str(i[1]).ljust(max_len_list[1]) + " | " + str(i[2]).ljust(max_len_list[2]) + " | " + str(i[3]).ljust(max_len_list[3]) + " | " + str(i[4]).ljust(max_len_list[4]) + " |")        

