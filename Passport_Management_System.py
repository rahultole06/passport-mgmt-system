import mysql.connector as mycon
import sys
import csv
from tabulate import tabulate
from mysql.connector.errors import Error
import matplotlib.pyplot as mpl
import pandas as pd
import warnings

# Connect sql to python
con = mycon.connect(host='localhost', user = 'root', password='enterpasswordhere')
if con.is_connected():
    print("Connection established, starting session...")

# Assigning cursor
cur = con.cursor()

# Creating main database and tables to be used
cur.execute("create database if not exists passport_mgmt_sys")
cur.execute("use passport_mgmt_sys")
cur.execute("create table if not exists staff(username varchar(20) primary key not null, name varchar(20), password varchar(20))")
cur.execute("create table if not exists passports(passpt_no varchar(8) primary key not null, user_name varchar(20), nationality varchar(10), sex char(1), dob date, exp_date date)")
cur.execute("create table if not exists users(username varchar(20) primary key not null, user_name varchar(20), password varchar(20))")

#Disabling startup warnings
warnings.filterwarnings("ignore")

#Main Functions


def nationality_csv():
    sql_query = pd.read_sql_query("select nationality from passport_mgmt_sys.passports",con)
    df = pd.DataFrame(sql_query)
    df.to_csv (r'nationality.csv', index = False)
    home()
    

# Used for invalid options throughout program
def invalid():
    print("")
    print("==========")
    print("Invalid Option")
    print("==========")
    print("")
    input("Enter any key to continue: ")
    
# Too many attempts
def max_attempts():
    print("")
    print("===============")
    print("You exeeded 3 tries!")
    print("===============")
    print("")
    print("Connection Terminated.")
    sys.exit()

# Home confirm option
def confirm():
    c = input("Confirm? y/n: ")
    if (c == "y"):
        print("Confirmed!")
    else:
        print("Cancelled!")
        home()

# Staff confirm option
def confirm_staff(): 
    cs = input("Confirm? y/n: ")
    if (cs == "y"):
        print("Confirmed!")
    else:
        print("Cancelled!")
        staff_home()

# User confirm option
def confirm_user(): 
    cu = input("Confirm? y/n: ")
    if (cu == "y"):
        print("Confirmed!")
    else:
        print("Cancelled!")
        user_home()


# Used when duplicate primary key
def insertionerror():
    print("")
    print("===================================")
    print("|         Username/Passport already exists!         |")
    print("===================================")



def issue_passport():
    print("")
    print("===================")
    print("ISSUE PASSPORT")
    print("===================")
    print("")
    while True:
        iss_pass_no = input("Enter Passport No: ")
        if (iss_pass_no == "" or len(iss_pass_no) != 8):
            print("Invalid Passport No!")
            continue
        break
    while True:
        iss_pass_user_name = input("Enter Name (like_this): ")
        if (iss_pass_user_name == "" or len(iss_pass_user_name) > 20):
            print("Invalid Passport Name!")
            continue
        break
    while True:
        iss_pass_nationality = input("Enter Nationality: ")
        if (iss_pass_nationality == "" or len(iss_pass_nationality) > 10):
            print("Invalid Passport Nationality!")
            continue
        break
    while True:
        iss_pass_sex = input("Enter Sex (M/F): ")
        if (iss_pass_sex == "M" or iss_pass_sex == "F"):
            break
        else:
            print("Invalid Passport Sex!")
            continue
    while True:
        iss_pass_dob = input("Input DOB (yyyy-MM-dd): ")
        if (iss_pass_dob == "" or len(iss_pass_dob) != 10):
            print("Invalid Passport DOB!")
            continue
        break
    while True:
        iss_pass_expdate = input("Enter Passport Expiration Date (yyyy-MM-dd): ")
        if (iss_pass_expdate == "" or len(iss_pass_expdate) != 10):
            print("Invalid Passport Expiration Date!")
            continue
        break
    print("")    
    print("Passport No: ", iss_pass_no)
    print("Name: ", iss_pass_user_name)
    print("Nationality: ", iss_pass_nationality)
    print("Sex: ", iss_pass_sex)
    print("DOB: ", iss_pass_dob)
    print("Expiry Date: ", iss_pass_expdate)
    print("")
    confirm_user()
    try:
        cur.execute("insert into passports values(%s,%s,%s,%s,%s,%s)", (iss_pass_no, iss_pass_user_name, iss_pass_nationality, iss_pass_sex, iss_pass_dob, iss_pass_expdate))
        con.commit()
    except mycon.IntegrityError:
        insertionerror()
        invalid()
        user_home()

    print("")
    print("======================")
    print("Created Passport Successfully!")
    print("======================")
    print("")
    input("Enter any key to return: ")
    user_home()



def view_passport():
    print("")
    print("===============")
    print("VIEW PASSPORT")
    print("===============")
    print("")
    viewpass_no = input("Enter Passport No: ")
    if (viewpass_no == "" or len(viewpass_no) != 8):
        print("Invalid Passport No!")
        user_home()
    cur.execute("select * from passports where passpt_no like %s", (viewpass_no,))
    vpi_fetch = cur.fetchall()
    if not(vpi_fetch):
        invalid()
        user_home()
    for i in vpi_fetch:
        print("")
        print("===============")
        print("PASSPORT INFO")
        print("===============")
        print("")
        print("Passport Number: ", i[0])
        print("Name: ", i[1])
        print("Nationality: ", i[2])
        print("Sex: ", i[3])
        print("DOB: ", i[4])
        print("Expiry Date: ", i[5])
        print("")
        input("Enter any key to return: ")
        user_home()

 # Main home page
def home(): 
    print("")
    print("==============================")
    print("PASSPORT MANAGEMENT SYSTEM")
    print("==============================")
    print("")
    print("1. USER REGISTER")
    print("2. STAFF REGISTER")
    print("3. USER LOGIN")
    print("4. STAFF LOGIN")
    print("5. PROGRAM INFO")
    print("6. EXIT")
    print("")
    home_menu = int(input("Enter: "))
    if (home_menu > 6):
        invalid()
        home()
    else:
        if (home_menu == 1):
            new_user()
        elif (home_menu == 2):
            new_staff()
        elif (home_menu == 3):
            user_login()
        elif (home_menu == 4):
            staff_login()
        elif (home_menu == 5):
            prog_info()
        elif (home_menu == 6):
            print("Connection Terminated.")
            sys.exit()
                    
          
# User registration
def new_user(): 
    print("")
    print("==================")
    print("USER REGISTRATION")
    print("==================")
    print("")
    while True:
        new_username = input("Enter your username (likethis): ")
        if (new_username == "" or len(new_username) > 20):
            print("Invalid username!")
            continue
        break
    while True:
        new_user_name = input("Enter your full name (first_middle_last): ")
        if (new_user_name == "" or len(new_user_name) > 20):
            print("Invalid Full Name!")
            continue
        break
    while True:
        new_user_password = input("Enter your password: ")
        if (new_user_password == "" or len(new_user_password) > 20):
            print("Invalid password!")
            continue
        break
    while True:
        new_user_confirm_password = input("Re-enter your password: ")
        if (new_user_password != new_user_confirm_password):
            print("Password does not match!")
            continue
        break
    print("")
    print("ID: ", new_username)
    print("Name: ", new_user_name)
    print("")
    confirm()
    try:
        cur.execute("insert into users values(%s, %s, %s)", (new_username, new_user_name, new_user_password))
        con.commit()
    except mycon.IntegrityError:
        insertionerror()
        invalid()
        home()
    print("")
    print("==========")
    print("User created!")
    print("==========")
    print("")
    print("========")
    print("Logging In")
    print("========")
    print("")
    user_home()
    

# Staff registration
def new_staff(): 
    print("")
    print("==================")
    print("STAFF REGISTRATION")
    print("==================")
    print("")
    while True:
        new_staff_username = input("Enter staff username: ")
        if (new_staff_username == "" or len(new_staff_username) > 20):
            print("Invalid username!")
            continue
        break
    while True:
        new_staff_name = input("Enter staff full name: ")
        if (new_staff_name == "" or len(new_staff_name) > 20):
            print("Invalid name!")
            continue
        break
    while True:
        new_staff_password = input("Enter staff password: ")
        if (new_staff_password == "" or len(new_staff_password) > 20):
            print("Invalid password!")
            continue
        break
    while True:
        new_staff_confirm_password = input("Re-enter staff password: ")
        if (new_staff_password != new_staff_confirm_password):
            print("Password does not match!")
            continue
        break
    print("")
    print("Username: ", new_staff_username)
    print("Name: ", new_staff_name)
    print("")
    confirm()
    try:
        cur.execute("insert into staff values(%s, %s, %s)", (new_staff_username, new_staff_name, new_staff_password))
        con.commit()
    except mycon.IntegrityError:
        insertionerror()
        invalid()
        home()
    print("")
    print("================")
    print("Staff account created!")
    print("================")
    print("")
    print("1. Create another staff account")
    print("2. Back")
    print("")
    c = int(input("Enter: "))
    if (c == 1):
        new_staff()
    elif (c == 2):
        home()



# User login
def user_login():
    max_attempt = 0
    while True:
        print("")
        print("===========")
        print("USER LOGIN")
        print("===========")
        print("")
        while True:
            user_login_username = input("Enter your username: ")
            if (user_login_username == ""):
                print("Invalid username!")
                continue
            break
        while True:
            user_login_password = input("Enter your password: ")
            if (user_login_password == ""):
                print("Invalid password!")
                continue
            break
        cur.execute("select username,password from users where username like %s", (user_login_username,))
        unc_fetch = cur.fetchall()
        if not(unc_fetch):
            invalid()
            home()
        for i in unc_fetch:
            if (i[0] == user_login_username and i[1] == user_login_password):
                print("")
                print("=================")
                print("Successfully logged in!")
                print("=================")
                print("")
                user_home()
            print("")
            print("=====")
            print("Invalid!")
            print("=====")
            max_attempt += 1
            if (max_attempt == 3):
                max_attempts()
            continue
        
        

# User home
def user_home(): 
    print("")
    print("=========================")
    print("PASSPORT USER HOME PAGE")
    print("=========================")
    print("")
    print("1. ISSUE PASSPORT")
    print("2. VIEW PASSPORT")
    print("3. LOGOUT")
    print("")
    usr_home_page = int(input("Enter: "))
    if (usr_home_page > 3):
        invalid()
        user_home()
    elif (usr_home_page == 1):
        issue_passport()
    elif (usr_home_page == 2):
        view_passport()
    elif (usr_home_page == 3):
        home()



# Staff login 
def staff_login():
    max_attempt = 0
    while True:
        print("")
        print("===========")
        print("STAFF LOGIN")
        print("===========")
        print("")
        while True:
            staff_login_username = input("Enter your username: ")
            if (staff_login_username == ""):
                print("Invalid username!")
                continue
            break
        while True:
            staff_login_password = input("Enter your password: ")
            if (staff_login_password == ""):
                print("Invalid password!")
                continue
            break
        cur.execute("select username,password from staff where username like %s", (staff_login_username,))
        snc_fetch = cur.fetchall()
        if not(snc_fetch):
            invalid()
            home()
        for i in snc_fetch:
            if (i[0] == staff_login_username and i[1] == staff_login_password):
                print("")
                print("=================")
                print("Successfully logged in!")
                print("=================")
                print("")
                staff_home()
            print("")
            print("=====")
            print("Invalid!")
            print("=====")
            max_attempt += 1
            if (max_attempt == 3):
                max_attempts()
            continue
                

# Staff home screen                
def staff_home(): 
    print("")
    print("=========================")
    print("PASSPORT STAFF HOME PAGE")
    print("=========================")
    print("")
    print("1. UPDATE PASSPORTS")
    print("2. DELETE PASSPORTS")
    print("3. VIEW NATIONALITIES")
    print("4. LOGOUT")
    print("")
    staff_home_page = int(input("Enter: "))
    if (staff_home_page > 5):
        invalid()
        staff_home()
    elif (staff_home_page == 1):
        update_passport()
    elif (staff_home_page == 2):
        delete_passport()
    elif (staff_home_page == 3):
        display_nationalities()
    elif (staff_home_page == 4):
        home()
    



# Update any passport
def update_passport():
    # Fuctions for updation
    def up_pass_name():
        while True:
            upf_name = input("Enter new Passport Name: ")
            if (upf_name == "" or len(upf_name) > 20):
                print("Invalid Passport Name!")
                continue
            break
        print("")
        print("New Passport Name:", upf_name)
        print("")
        confirm_staff()
        cur.execute("update passports set user_name = %s where passpt_no = %s", (upf_name, up_no))
        con.commit()
        print("")
        print("=====================")
        print("Passport has been updated!")
        print("=====================")
        print("")
        print("1. Update another field")
        print("2. Return Home")
        print("")
        upfn_exit = int(input("Enter: "))
        if (upfn_exit > 2):
            invalid()
            staff_home()
        elif (upfn_exit == 1):
            update_passport()
        elif (upfn_exit == 2):
            staff_home()



    def up_pass_nationality():
        while True:
            upf_nationality = input("Enter new Passport Nationality: ")
            if (upf_nationality == "" or len(upf_nationality) > 10):
                print("Invalid Passport Nationality!")
                continue
            break
        print("")
        print("New Passport Nationality:", upf_nationality)
        print("")
        confirm_staff()
        cur.execute("update passports set nationality = %s where passpt_no = %s", (upf_nationality, up_no))
        con.commit()
        print("")
        print("=====================")
        print("Passport has been updated!")
        print("=====================")
        print("")
        print("1. Update another field")
        print("2. Return Home")
        print("")
        upfna_exit = int(input("Enter: "))
        if (upfna_exit > 2):
            invalid()
            staff_home()
        elif (upfna_exit == 1):
            update_passport()
        elif (upfna_exit == 2):
            staff_home()



    def up_pass_sex():
        while True:
            upf_sex = input("Enter new Passport Sex: ")
            if (upf_sex == "" or len(upf_sex) != 1):
                print("Invalid Passport Sex!")
                continue
            break
        print("")
        print("New Passport Sex:", upf_sex)
        print("")
        confirm_staff()
        cur.execute("update passports set sex = %s where passpt_no = %s", (upf_sex, up_no))
        con.commit()
        print("")
        print("=====================")
        print("Passport has been updated!")
        print("=====================")
        print("")
        print("1. Update another field")
        print("2. Return Home")
        print("")
        upfp_exit = int(input("Enter: "))
        if (upfp_exit > 2):
            invalid()
            staff_home()
        elif (upfp_exit == 1):
            update_passport()
        elif (upfp_exit == 2):
            staff_home()



    def up_pass_dob():
        while True:
            upf_dob = input("Enter new Passport DOB: ")
            if (upf_dob == "" or len(upf_dob) != 10):
                print("Invalid Passport DOB!")
                continue
            break
        print("")
        print("New Passport DOB:", upf_dob)
        print("")
        confirm_staff()
        cur.execute("update passports set dob = %s where passpt_no = %s", (upf_dob, up_no))
        con.commit()
        print("")
        print("=====================")
        print("Passport has been updated!")
        print("=====================")
        print("")
        print("1. Update another field")
        print("2. Return Home")
        print("")
        upfd_exit = int(input("Enter: "))
        if (upfd_exit > 2):
            invalid()
            staff_home()
        elif (upfd_exit == 1):
            update_passport()
        elif (upfd_exit == 2):
            staff_home() 



    def up_pass_exp():
        while True:
            upf_expd = input("Enter new Passport Expiry Date: ")
            if (upf_expd == "" or len(upf_expd) != 10):
                print("Invalid Passport Expiry Date!")
                continue
            break
        print("")
        print("New Passport Expiry Date:", upf_expd)
        print("")
        confirm_staff()
        cur.execute("update passports set exp_date = %s where passpt_no = %s", (upf_expd, up_no))
        con.commit()
        print("")
        print("=====================")
        print("Passport has been updated!")
        print("=====================")
        print("")
        print("1. Update another field")
        print("2. Return Home")
        print("")
        upfed_exit = int(input("Enter: "))
        if (upfed_exit > 2):
            invalid()
            staff_home()
        elif (upfed_exit == 1):
            update_passport()
        elif (upfed_exit == 2):
            staff_home()



    def up_pass_all():
        while True:
            upf_all_name = input("Enter new Passport Name: ")
            if (upf_all_name == "" or len(upf_all_name) > 20):
                print("Invalid Passport Name!")
                continue
            break
        while True:
            upf_all_nationality = input("Enter new Passport Nationality: ")
            if (upf_all_nationality == "" or len(upf_all_nationality) > 10):
                print("Invalid Passport Nationality!")
                continue
            break
        while True:
            upf_all_sex = input("Enter new Passport Sex: ")
            if (upf_all_sex == "" or len(upf_all_sex) != 1):
                print("Invalid Passport Sex!")
                continue
            break
        while True:
            upf_all_dob = input("Enter new Passport DOB: ")
            if (upf_all_dob == "" or len(upf_all_dob) != 10):
                print("Invalid Passport DOB!")
                continue
            break
        while True:
            upf_all_expd = input("Enter new Passport Expiry Date: ")
            if (upf_all_expd == "" or len(upf_all_expd) != 10):
                print("Invalid Passport Expiry Date!")
                continue
            break
        print("")
        print("New Passport Name:", upf_all_name)
        print("New Passport Nationality:", upf_all_nationality)
        print("New Passport Sex:", upf_all_sex)
        print("New Passport DOB:", upf_all_dob)
        print("New Passport Expiry Date:", upf_all_expd)
        print("")
        confirm_staff()
        try:
            cur.execute("update passports set user_name = %s where passpt_no = %s", (upf_all_name, up_no))
            cur.execute("update passports set nationality = %s where passpt_no = %s", (upf_all_nationality, up_no))
            cur.execute("update passports set sex = %s where passpt_no = %s", (upf_all_sex, up_no))
            cur.execute("update passports set dob = %s where passpt_no = %s", (upf_all_dob, up_no))
            cur.execute("update passports set exp_date = %s where passpt_no = %s", (upf_all_expd, up_no))
            con.commit()
        except mycon.IntegrityError:
            insertionerror()
            invalid()
            staff_home()
        print("")
        print("Passport has been updated!")
        print("")
        print("1. Update another field")
        print("2. Return Home")
        print("")
        upfa_exit = int(input("Enter: "))
        if (upfa_exit > 2):
            invalid()
            staff_home()
        elif (upfa_exit == 1):
            update_passport()
        elif (upfa_exit == 2):
            staff_home()
    
    
    
    print("")
    print("===============")
    print("UPDATE PASSPORT")
    print("===============")
    print("")
    while True:
        up_no = input("Enter the Passport No: ")
        if (up_no == "" or len(up_no) != 8):
            print("Invalid Passport No.!")
            continue
        break
    cur.execute("select * from passports where passpt_no like %s", (up_no,))
    up_fetch = cur.fetchall()
    if not(up_fetch):
        invalid()
        staff_home()
    for row in up_fetch:
        print("")
        print("Choose which field to update: ")
        print("1. Name: ", row[1])
        print("2. Nationality: ", row[2])
        print("3. Sex: ", row[3])
        print("4. DOB: ", row[4])
        print("5. Expiry Date: ", row[5])
        print("6. All of them")
        print("7. Return Home")
        print("")
        up_field = int(input("Enter: "))
        if (up_field > 7):
            invalid()
            staff_home()
        elif (up_field == 1):
            up_pass_name()
        elif (up_field == 2):
            up_pass_nationality()
        elif (up_field == 3):
            up_pass_sex()
        elif (up_field == 4):
            up_pass_dob()
        elif (up_field == 5):
            up_pass_exp()
        elif (up_field == 6):
            up_pass_all()
        elif (up_field == 7):
            staff_home()
    
    

# Delete any users passport
def delete_passport():
    print("")
    print("===============")
    print("DELETE PASSPORT")
    print("===============")
    print("")
    while True:
        del_pass_no = input("Enter the Passport Number: ")
        if (del_pass_no == "" or len(del_pass_no) != 8):
            print("Invalid Passport Number!")
            continue
        break
    cur.execute("select * from passports where passpt_no like %s", (del_pass_no,))
    dpc_fetch = cur.fetchall()
    if not(dpc_fetch):
        invalid()
        staff_home()
    for dpf in dpc_fetch:
        print("")
        print("==============")
        print("PASSPORT INFO")
        print("==============")
        print("")
        print("Passport Number: ", dpf[0])
        print("Name: ", dpf[1])
        print("Nationality: ", dpf[2])
        print("Sex: ", dpf[3])
        print("DOB: ", dpf[4])
        print("Expiry Date: ", dpf[5])
        print("")
        confirm_staff()
        cur.execute("delete from passports where passpt_no like %s", (del_pass_no,))
        con.commit()
        print("")
        print("=======================")
        print("Passport Successfully Deleted!")
        print("=======================")
        print("")
        print("1. Delete another Passport")
        print("2. Return Home")
        print("")
        dps_ret = int(input("Enter: "))
        if (dps_ret > 2):
            invalid()
            staff_home()
        elif (dps_ret == 1):
            delete_passport()
        elif (dps_ret == 2):
            staff_home()

def display_nationalities():
    n_list = []
    n_label = []
    n_explode = []
    cur.execute("select nationality,count(*) from passports group by nationality order by count(*) desc")
    dn_fetch = cur.fetchall()
    if not(dn_fetch):
        invalid()
        staff_home()
    for i in dn_fetch:
        n_list.append(i[1])
        n_label.append(i[0])
        n_explode.append(0)
    n_explode[0] = 0.2
    mpl.pie(n_list, labels = n_label, explode = n_explode, shadow = True)
    mpl.legend(title = "Nationalities: ")
    mpl.show()
    input("Press any key to continue: ")
    staff_home()

def prog_info():
    with open("info.txt", "w") as proginfo:
        lines = ["============", "SYSTEM INFO", "============", "Guests can register and login as a user or staff.", "Users can issue and view their passport.", "Staff are able to update and delete passports", "============================"]
        for i in lines:
            proginfo.write(i)
            proginfo.write('\n')
    with open("info.txt") as progread:
        print("")
        content = progread.read()
        print(content)
        print("")
        pe_exit = input("Enter any key to return: ")
        home()


# Executing first function

nationality_csv()

