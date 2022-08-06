
import re
from os import system
import mysql.connector


# make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
# for validating an Phone Number
Pattern = re.compile("(0|91)?[7-9][0-9]{9}")



connect = mysql.connector.connect( host = 'localhost', user = 'root', password = 'root' )
cursor = connect.cursor()

cursor.execute('USE EmployeeManagementGUI;')


def add_emp():
    
    print("{:>60}".format("---Add An Employee Record---\n"))
    
    ID = input('Enter an Employee ID: ')

    if check_employee_ID(ID)==True:
        print('Employee ID already Exists\nPlease Try Again...')
        press = input('Press Any Key To Continue...')
        add_emp()
    Name = input('Enter Employee Name')
    if check_employee_name(Name) == True:
        print('Employee Name Already Exists\nPlease Try Again...')
        press
        add_emp()
    Email = input('Please enter an Email: ')
    if re.fullmatch(regex,Email):
        print('Valid Email')
    else:
        print('Invalid Email\nPlease Try Again...')
        press
        add_emp()
    PhoneNumber = input('Please Enter Employee Phone Number: ')
    if Pattern.match(PhoneNumber):
        print('Valid Phone Number')
    else:
        print('Invalid Phone Number\nPlease Try Again...')
        press
        add_emp()
    Address = input('Pleae Enter Employee Address: ')
    Position = input('Please Enter The Employee Position: ')
    Salary = input('Enter Employee Salary: ')
    data = (ID,Name,Email,PhoneNumber,Address,Position,Salary)

    sql = 'insert into employeeData values(%s,%s,%s,%s,%s,%s,%s)'
    c = connect.cursor()

    c.execute(sql,data)

    connect.commit()
    print("[Successfully Added Record]")
    press
    menu()

#Checking if Employee name is in the Database
def check_employee_name(employee_name):
    #making query in SQL to select all from table
    sql = 'SELECT *FROM employeeData WHERE Name=%s'
    #configuring cursor to buffered to make rowcount work
    c = connect.cursor(buffered=True)
    data = (employee_name,)
    #execute query
    c.execute(sql,data)
    #Counting rows to find if any duplicates exist
    row = c.rowcount
    if row ==1:
        return True
    else:
        return False


def check_employee_ID(ID):
    #creating SQL query to execute
    sql = 'SELECT *FROM employeeData WHERE ID=%d'

    c = connect.cursor(buffered=True)
    data = (ID)

    c.execute(sql)

    row = c.rowcount
    if row ==1:
        return True
    else:
        return False

def display_employee():

    print('{:>60}'.format('---Display Employee Record---\n'))

    sql = 'SELECT *FROM employeeData'
    c = connect.cursor()

    c.execute(sql,)

    row = c.fetchall()

    for i in row:
        print('Employee ID: ',i[0])
        print('Employee Name: ',i[1])
        print('Employee Email: ',i[2])
        print('Employee Phone Number: ',i[3])
        print('Employee Address: ',i[4])
        print('Employee Position: ',i[5])
        print('Employee Salary: ',i[6])
        print('\n')
    press = input('Press Any Key To Continue...')
    menu()

def update_employee():
    print('{:>60}'.format('---Update Employee Record---\n'))
    ID = input('Please Enter The Employee ID: ')

    if (check_employee_ID(ID)==False):
        print('Employee Record Does Not Exist\nPlease Try Again...')
        press = input('Press Any Key To Continue...')
        menu()
    else:
        Email = input('Please Enter The Employee Email: ')
        if re.fullmatch(regex,Email):
            print('Valid Email')
        else:
            print('Invalid Email\nPlease Try Again...')
            press= input('Press Any Key To Continue...')
            update_employee()
        PhoneNumber = input('Please Enter The Employee Phone Number: ')
        if Pattern.match(PhoneNumber):
            print('Valid Phone Number')
        else:
            print('Invalid Phone Number\nPlease Try Again...')
            press = input('Press Any Key To Continue...')
            update_employee()
        Address = input('Please Enter The Employee Address')

        sql = 'UPDATE employeeData SET Email = %s, PhoneNumber = %s, Address = %s, WHERE ID = %s'
        data = (Email,PhoneNumber,Address,ID)
        c = connect.cursor()

        c.execute(sql,data)

        connect.commit()
        print('[Updated Employee Record]')
        menu()


def promote_employee():
    print("{:>60}".format("---Promote Employee Record---\n"))
    ID = input("Enter The Employee ID: ")
    # checking If Employee Id is Exit Or Not
    if(check_employee_ID(ID) == False):
        print("Employee Record Not exists\nTry Again")
        press = input("Press Any Key To Continue...")
        menu()
    else:
        Amount  = int(input("Enter The Salary Increase: "))
        #query to fetch salary of Employee with given data
        sql = 'SELECT Salary FROM employeeData WHERE ID=%s'
        data = (ID,)
        c = connect.cursor()
        
        #executing the sql query
        c.execute(sql, data)
        
        #fetching salary of Employee with given Id
        row = c.fetchone()
        table = row[0]+Amount
        
        #query to update salary of Employee with given id
        sql = 'UPDATE employeeData SET Salary = %s WHERE ID = %s'
        d = (table, ID)

        #executing the sql query
        c.execute(sql, d)

        #commit() method to make changes in the table 
        connect.commit()
        print("[Employee Promoted]")
        press = input("Press Any key To Continue..")
        menu()


# Function to Remove_Employee
def remove_employee():
    print("{:>60}".format("--Remove Employee Record--\n"))
    ID = input("Enter The Employee ID: ")
    # checking If Employee Id is False Or Not
    if(check_employee_ID(ID) == False):
        print("Employee Record Does Not Exist\nPlease Try Again...")
        press = input("Press Any Key To Continue..")
        menu()
    else:
        #query to delete Employee from empdata table
        sql = 'DELETE FROM employeeData WHERE ID = %s'
        data = (ID,)
        c = connect.cursor()

        #executing the sql query
        c.execute(sql, data)

        #commit() method to make changes in the empdata table
        connect.commit()
        print("[Employee Removed]")
        press = input("Press Any key To Continue..")
        menu()

# Function to search for employee
def find_employee():
    print("{:>60}".format("---Search Employee Record---\n"))
    ID = input("Enter Employee ID: ")
    # checking If Employee Id is Exit Or Not
    if(check_employee_ID(ID) == False):
        print("Employee Record Not exists\nPlease Try Again...")
        press = input("Press Any Key To Continue..")
        menu()
    else:
        #query to search Employee from empdata table
        sql = 'SELECT *FROM employeeData WHERE ID = %s'
        data = (ID,)
        c = connect.cursor()
        
        #executing the sql query
        c.execute(sql, data)

        #fetching all details of all the employee
        row = c.fetchall()
        for i in row:
            print("Employee ID: ", i[0])
            print("Employee Name: ", i[1])
            print("Employee Email: ", i[2])
            print("Employee Phone Number: ", i[3])
            print("Employee Address: ", i[4])
            print("Employee Position: ", i[5])
            print("Employee Salary: ", i[6])
            print("\n")
        press = input("Press Any key To Continue..")
        menu()


def menu():
    system("cls")
    print("{:>60}".format("------------------------------------"))
    print("{:>60}".format("--- Employee Management System ---"))
    print("{:>60}".format("------------------------------------"))
    print("1. Add Employee")
    print("2. Display Employee Record")
    print("3. Update Employee Record")
    print("4. Promote Employee Record")
    print("5. Remove Employee Record")
    print("6. Search Employee Record")
    print("7. Exit\n")
    print("{:>60}".format("-->> Choice Options: [1/2/3/4/5/6/7] <<--"))

    ch = int(input("Enter your Choice: "))
    if ch == 1:
        system("cls")
        add_emp()
    elif ch == 2:
        system("cls")
        display_employee()
    elif ch == 3:
        system("cls")
        update_employee()
    elif ch == 4:
        system("cls")
        promote_employee()
    elif ch == 5:
        system("cls")
        remove_employee()
    elif ch == 6:
        system("cls")
        find_employee()
    elif ch == 7:
        system("cls")
        print("{:>60}7".format("Have A NIce Day :)"))
        exit(0)
    else:
        print("Invalid Choice!")
        press = input("Press Any key To Continue..")
        menu()


menu()

