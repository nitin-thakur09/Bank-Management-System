import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# Establish connection to the MySQL database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='',    #name of the database
            user='root',
            password=''  #password of mysql(root)
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Login Page
def login_page():
    def authenticate():
        username = username_entry.get()
        password = password_entry.get()
        
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            if user:
                messagebox.showinfo("Login Successful", "Welcome to the Bank Management System!")
                main_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials, try again.")
            connection.close()
    
    # Set up the login window
    login_window = tk.Tk()
    login_window.attributes('-fullscreen', True)
    login_window.configure(bg='lightblue')
    login_window.title("Login Page")
    tk.Label(login_window, text="USERNAME",pady=20,font="Times 20 bold",bg='lightblue').pack(pady=15)
    username_entry = tk.Entry(login_window,font="Times 25 bold" )
    username_entry.pack()
    
    tk.Label(login_window, text="PASSWORD",font="Times 20 bold",bg='lightblue',pady=20).pack(pady=15)
    password_entry = tk.Entry(login_window, show="*",font="Times 25 bold" )
    password_entry.pack()
    
    login_button = tk.Button(login_window, text="Login",
bg = "green",fg="white",
font = 'Times 18 bold',
activebackground ="#7209b7",
activeforeground ="#ced4da",
height = 0,
bd = 5,
width = 5,command=authenticate)
    login_button.pack(pady=20)
    
    login_window.mainloop()

# Main Dashboard Page
def main_dashboard():
    dashboard_window = tk.Tk()
    dashboard_window.configure(bg='lightblue')
    dashboard_window.attributes('-fullscreen', True)
    dashboard_window.title("Bank Management Dashboard")

    # Functions for different operations
    def manage_accounts():
        manage_accounts_page()

    def handle_transactions():
        transaction_page()

    def view_transactions():
        view_transactions_page()

    def logout():
        dashboard_window.destroy()
        login_page()

    tk.Button(dashboard_window, text="Manage Accounts",bg = "#03045E",fg="white",font = 'Times 18 bold',activebackground ="#7209b7",activeforeground ="#ced4da",height = 0,bd = 5,width = 15, command=manage_accounts).pack(pady='20')
    tk.Button(dashboard_window, text="Transactions",bg = "#03045E",fg="white",font = 'Times 18 bold',activebackground ="#7209b7",activeforeground ="#ced4da",height = 0,bd = 5,width = 15, command=handle_transactions).pack(pady='20')
    tk.Button(dashboard_window, text="View Transactions",bg = "#03045E",fg="white",font = 'Times 18 bold',activebackground ="#7209b7",activeforeground ="#ced4da",height = 0,bd = 5,width = 15, command=view_transactions).pack(pady='20')
    tk.Button(dashboard_window, text="Logout",bg = "#03045E",fg="white",font = 'Times 18 bold',activebackground ="#7209b7",activeforeground ="#ced4da",height = 0,bd = 5,width = 15, command=logout).pack(pady='20')
    
    dashboard_window.mainloop()

# Manage Accounts Page
def manage_accounts_page():
    def add_account():
        def save_account():
            customer_name = name_entry.get()
            initial_balance = balance_entry.get()
            customer_password=password_entry.get()

            connection = connect_to_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO accounts (customer_name, balance) VALUES (%s, %s)", 
                               (customer_name, initial_balance))
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", 
                               (customer_name, customer_password))
                connection.commit()
                messagebox.showinfo("Success", "Account created successfully!")
                add_account_window.destroy()
                connection.close()

        add_account_window = tk.Tk()
        add_account_window.configure(bg='lightblue')
        add_account_window.attributes('-fullscreen', True)
        add_account_window.title("Add Account")
        
        tk.Label(add_account_window, text="Customer Name",pady=20,font="Times 20 bold",bg='lightblue').pack(pady=20)
        name_entry = tk.Entry(add_account_window,font="Times 25 bold")
        name_entry.pack()

        tk.Label(add_account_window, text="Initial Balance",pady=20,font="Times 20 bold",bg='lightblue').pack(pady=20)
        balance_entry = tk.Entry(add_account_window,font="Times 25 bold")
        balance_entry.pack()

        tk.Label(add_account_window, text="Password",pady=20,font="Times 20 bold",bg='lightblue').pack(pady=20)
        password_entry = tk.Entry(add_account_window,font="Times 25 bold")
        password_entry.pack()

        tk.Button(add_account_window, text="Save",bg = "#03045E",fg="white",font = 'Times 18 bold',activebackground ="#7209b7",activeforeground ="#ced4da",height = 0,bd = 5,width = 15, command=save_account).pack(pady='20')
        add_account_window.mainloop()
    
    manage_window = tk.Tk()
    manage_window.configure(bg='lightblue')
    manage_window.attributes('-fullscreen', True)
    manage_window.title("Manage Accounts")
    tk.Button(manage_window, text="Add Account",bg = "#03045E",fg="white",font = 'Times 25 bold',activebackground ="#7209b7",activeforeground ="#ced4da",height = 0,bd = 10,width = 30, command=add_account).pack(pady='100')
    manage_window.mainloop()

# Transaction Page (Deposit, Withdraw, Transfer)
def transaction_page():
    def deposit():
        account_id = account_entry.get()
        amount = float(amount_entry.get())
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", 
                           (amount, account_id))
            cursor.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Deposit', %s)", 
                           (account_id, amount))
            connection.commit()
            messagebox.showinfo("Success", f"Deposited {amount} to account {account_id}")
            connection.close()
    
    def withdraw():
        account_id = account_entry.get()
        amount = float(amount_entry.get())
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", 
                           (amount, account_id))
            cursor.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Withdrawal', %s)", 
                           (account_id, amount))
            connection.commit()
            messagebox.showinfo("Success", f"Withdrawn {amount} from account {account_id}")
            connection.close()

    def transfer():
        from_account = from_account_entry.get()
        to_account = to_account_entry.get()
        amount = float(transfer_amount_entry.get())
        
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", 
                           (amount, from_account))
            cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", 
                           (amount, to_account))
            cursor.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Transfer', %s)", 
                           (from_account, amount))
            cursor.execute("INSERT INTO transactions (account_id, transaction_type, amount) VALUES (%s, 'Transfer', %s)", 
                           (to_account, amount))
            connection.commit()
            messagebox.showinfo("Success", f"Transferred {amount} from account {from_account} to {to_account}")
            connection.close()

    # Set up transaction window
    transaction_window = tk.Tk()
    transaction_window.configure(bg='lightblue')
    transaction_window.attributes('-fullscreen', True)
    transaction_window.title("Transaction Operations")
    
    tk.Label(transaction_window, text="Account ID",pady=20,font="Times 20 bold",bg='lightblue').pack(pady='10')
    account_entry = tk.Entry(transaction_window,font="Times 25 bold" )
    account_entry.pack()

    tk.Label(transaction_window, text="Amount",pady=20,font="Times 20 bold",bg='lightblue').pack(pady='5')
    amount_entry = tk.Entry(transaction_window,font="Times 25 bold")
    amount_entry.pack()

    tk.Button(transaction_window, text="Deposit",bg = "#03045E",fg="white",font = 'Times 18 bold',activebackground ="#7209b7",activeforeground ="#ced4da",height = 0,bd = 5,width = 15, command=deposit).pack(pady='20')
    tk.Button(transaction_window, text="Withdraw",bg = "#03045E",fg="white",font = 'Times 18 bold',activebackground ="#7209b7",activeforeground ="#ced4da",height = 0,bd = 5,width = 15, command=withdraw).pack(pady='5')

    # For transfer
    tk.Label(transaction_window, text="From Account",pady=20,font="Times 20 bold",bg='lightblue').pack(pady='10')
    from_account_entry = tk.Entry(transaction_window,font="Times 25 bold")
    from_account_entry.pack()

    tk.Label(transaction_window, text="To Account",pady=20,font="Times 20 bold",bg='lightblue').pack(pady='5')
    to_account_entry = tk.Entry(transaction_window,font="Times 25 bold")
    to_account_entry.pack()

    tk.Label(transaction_window, text="Transfer Amount",pady=20,font="Times 20 bold",bg='lightblue').pack(pady='5')
    transfer_amount_entry = tk.Entry(transaction_window,font="Times 25 bold")
    transfer_amount_entry.pack()

    tk.Button(transaction_window, text="Transfer",bg = "#03045E",fg="white",font = 'Times 18 bold',activebackground ="#7209b7",activeforeground ="#ced4da",height = 0,bd = 5,width = 15, command=transfer).pack(pady='20')

    transaction_window.mainloop()

# View Transactions Page
def view_transactions_page():
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM transactions")
        transactions = cursor.fetchall()
        
        view_window = tk.Tk()
        view_window.configure(bg='lightblue')
        view_window.title("Transaction History")
        
        for transaction in transactions:
            transaction_details = f"ID: {transaction[0]} | Account ID: {transaction[1]} | Type: {transaction[2]} | Amount: {transaction[3]} | Date: {transaction[4]}"
            tk.Label(view_window, text=transaction_details,pady=10,font="Times 15 bold",bg='lightblue').pack(pady='10')
        
        view_window.mainloop()
        connection.close()

# Start the application
login_page()
