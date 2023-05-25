import mysqlx
from mysqlx.errors import DatabaseError
import tkinter as tk

OrderID = 1
## IDE ##
## Varje knapp lägger till en viss item i en vanlig lista.Om 

# Connect to server on localhost
session = mysqlx.get_session({
    "host": "localhost",
    "port": 33060,
    "user": "root",
    "password": "12345678"
})
window = tk.Tk()
text_widget = tk.Text(window, width=40, height=30)
text_widget.grid(row=0, column=3,rowspan=2)

DB_NAME = 'pos_system'

def select_database(session):
    try:
        session.sql("USE {}".format(DB_NAME)).execute()
        
    except DatabaseError as de:
        if de.errno == 1049:
            print("Error: Database '{}' does not exist.".format(DB_NAME))
            session.sql("USE {}".format(DB_NAME)).execute()
        else:
            print("Error executing SQL command: {}".format(de))
            raise


    ## RESET ORDERITEM
    insert_sql = [
        "TRUNCATE TABLE OrderItem"
    ]

    for query in insert_sql:
        try:
            print("SQL query {}: ".format(query), end='')
            text_widget.insert(tk.END, "1x Pizza 150;-")
            session.sql(query).execute()
        except DatabaseError as err:
            print(err.msg)
        else:
            print("OK")


def insert_into_table(session,table,OrderID):
    
    insert_sql = [
        "INSERT INTO "+table+" (orderID, item_id) VALUES ("+OrderID+",itemID""," +  str(test2) + ");"
    ]

    for query in insert_sql:
        try:
            print("SQL query {}: ".format(query), end='')
            text_widget.insert(tk.END, "1x Pizza 150;-")
            session.sql(query).execute()
        except DatabaseError as err:
            print(err.msg)
        else:
            print("OK")

def retrieve_from_database(session):
    try:
        query = "SELECT orderID, item_id FROM Orders;"
        result = session.sql(query).execute()

        # Iterate over the rows and display the data
        for row in result.fetch_all():
            print(row)
            text_widget.insert(tk.END, f"{row}\n")
      
    except DatabaseError as err:
        print(f"Error: {err}")

def button1_click():
    retrieve_from_database(session)

def button2_click():
    pass

def button3_click():
    #Insert Pizza into OrderItem
    # OrderId should be a global variable
    # itemID should be constant 1
    # quanity should be removed
    # subtotal should be constant 99
    insert_sql = [
        "INSERT INTO OrderItem (orderID, itemID,quantity,subtotal) VALUES ("+OrderID+",1,1,20);"
    ]

    for query in insert_sql:
        try:
            print("SQL query {}: ".format(query), end='')
            text_widget.insert(tk.END, "1x Pizza 150;-")
            session.sql(query).execute()
        except DatabaseError as err:
            print(err.msg)
        else:
            print("OK")

def button4_click():
    # Perform some other functionality
    pass

def button5_click():
    # Perform some other functionality
    pass
def main():
    select_database(session)

    # Create the main window
    

    

    # Create buttons
    button1 = tk.Button(window, text="Show items", font=("Arial", 16), width=30, height=10, command=button1_click)
    button1.configure(background="red", fg="white")
    button1.grid(row=0, column=0, padx=10, pady=10)

    button2 = tk.Button(window, text="Add items", font=("Arial", 16), width=30, height=10, command=button2_click)
    button2.configure(background="green", fg="white")
    button2.grid(row=1, column=0, padx=10, pady=10)

    button3 = tk.Button(window, text="Pizza", font=("Arial", 16), width=30, height=10, command=button3_click)
    button3.configure(background="blue", fg="white")
    button3.grid(row=0, column=1, padx=10, pady=10)

    button4 = tk.Button(window, text="Cola", font=("Arial", 16), width=30, height=10, command=button4_click)
    button4.configure(background="yellow", fg="white")
    button4.grid(row=1, column=1, padx=10, pady=10)

    button5 = tk.Button(window, text="Card", font=("Arial", 16), width=30, height=10, command=button4_click)
    button5.configure(background="yellow", fg="white")
    button5.grid(row=2, column=0, padx=10, pady=10)

    # Start the GUI event loop
    window.mainloop()

    session.close()

if __name__ == "__main__":
    main()
