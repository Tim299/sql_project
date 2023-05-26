import mysqlx
from mysqlx.errors import DatabaseError
import tkinter as tk
from tkmacosx import Button
import tkinter.messagebox as messagebox

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


# Create a label for displaying the total sum
total_label = tk.Label(window, text="Total: $0.00")
total_label.grid(row=2, column=3)
total_label.configure(borderwidth=2, relief="solid", highlightthickness=2, highlightbackground="black")


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
    reset_table()


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


def update_total_sum(amount):
    current_text = total_label.cget("text")
    current_total = float(current_text.split(":")[1].strip().replace("$", ""))
    new_total = current_total + amount
    total_label["text"] = "Total: ${:.2f}".format(new_total)

def reset_table():
    insert_sql = [
        "TRUNCATE TABLE OrderItem"
    ]

    for query in insert_sql:
        try:
            print("SQL query {}: ".format(query), end='')
            text_widget.insert(tk.END, "------------ SELECTED ITEMS -----------\n\n")
            session.sql(query).execute()
        except DatabaseError as err:
            print(err.msg)
        else:
            print("OK")

def write_receipt_to_file(rows):
    receipt_info = ""  # Variable to store the receipt information

    for row in rows:
        order_id = row[0]
        order_date = row[1]
        total_quantity = row[5]
        item_id = row[3]
        item_price = row[4]
        subtotal = row[6]

        receipt_info += f"Order ID: {order_id}\n"
        receipt_info += f"Order Date: {order_date}\n"
        receipt_info += f"Total Quantity: {total_quantity}\n"
        receipt_info += f"Item: {item_id}\n"
        receipt_info += f"Item Price: {item_price}\n"
        receipt_info += f"Subtotal: {subtotal}\n\n"

    total_price = sum(row[6] for row in rows)
    receipt_info += f"Total Price: {total_price}\n"

    global OrderID
    temp = OrderID -1
    filename = f"receipt_order_{temp}.txt"  # Include OrderID in the file name

    # Write receipt information to a text file
    with open(filename, "w") as file:
        file.write(receipt_info)

def open_popup(rows):
    popup = tk.Toplevel(window)
    popup.title("Payment")

    label = tk.Label(popup, text="Please complete the purchase in the terminal and close this window when finished", font=("Verdana", 14))
    label.pack(pady=20)
   
    # Function to execute when the popup is closed
    def on_popup_close():
        print("Popup closed")
        global OrderID
        OrderID += 1
        print(OrderID)
        reset_table()
        total_label["text"] = "Total: $0.00"
        write_receipt_to_file(rows)  # Write the receipt information to a text file
        messagebox.showinfo("Purchase Complete", "Purchase completed successfully")  # Display a message box
        popup.destroy()

    # Bind the function to the pop-up window's close event
    popup.protocol("WM_DELETE_WINDOW", on_popup_close)

    # Add a button for indicating payment completion
    payment_button = tk.Button(popup, text="Payment Complete", width=15, command=on_popup_close)
    payment_button.pack(pady=10)

    # Calculate the desired width and height of the popup window based on label content
    label_width = 800
    label_height = 400
    padding = 20  # Padding around the label

    popup_width = label_width + padding
    popup_height = label_height + padding + payment_button.winfo_reqheight() + 10  # Additional height for the button

    # Set the size of the popup window
    popup.geometry(f"{popup_width}x{popup_height}")

    # Focus the pop-up window (optional)
    popup.focus_set()


def button1_click():
    try:
        query = "SELECT name, itemType,stock FROM Item;"
        result = session.sql(query).execute()

        # Iterate over the rows and display the data
        text_widget.insert(tk.END, "------------ CURRENT STOCK -----------\n\n")
        for row in result.fetch_all():
            print(row)
            text_widget.insert(tk.END, f"{row}\n")
        text_widget.insert(tk.END, "---------------------------------------\n\n")
      
    except DatabaseError as err:
        print(f"Error: {err}")

def button2_click():
    pass

def button3_click():
    #Insert Pizza into OrderItem
    # OrderId should be a global variable
    # itemID should be constant 1 s
    # quanity should be removed
    # subtotal should be constant 99
    insert_sql = [
        "INSERT INTO OrderItem (orderID, itemID,quantity,subtotal) VALUES ("+str(OrderID)+",1,1,0);",
        "Update Item Set stock = stock - 1 WHERE itemID = 1;" 
    ]
    text_widget.insert(tk.END, "1x Pizza 99;-\n")
    for query in insert_sql:
        try:
            print("SQL query {}: ".format(query), end='')
            
            session.sql(query).execute()
        except DatabaseError as err:
            print(err.msg)
        else:
            print("OK")
    update_total_sum(99.00)


def button4_click():
    # Perform some other functionality
    insert_sql = [
        "INSERT INTO OrderItem (orderID, itemID,quantity,subtotal) VALUES ("+str(OrderID)+",2,1,0);",
        "Update Item Set stock = stock - 1 WHERE itemID = 2;" 

    ]
    text_widget.insert(tk.END, "1x Cola 19;-\n")
    for query in insert_sql:
        try:
            print("SQL query {}: ".format(query), end='')
            
            session.sql(query).execute()
        except DatabaseError as err:
            print(err.msg)
        else:
            print("OK")
    
    
    update_total_sum(19.00)

def button5_click():
    #update total price in orders
    #take sum of all prices in OrderItem
    #print all items, prices, sum of prices, date and orderid
   
    try:
        query = "SELECT o.orderID, o.orderDate, oi.itemID, i.name, i.price, oi.quantity, oi.subtotal " \
                "FROM Orders o " \
                "JOIN OrderItem oi ON o.orderID = oi.orderID " \
                "JOIN Item i ON oi.itemID = i.itemID " \
                "WHERE o.orderID = (SELECT MAX(orderID) FROM Orders);"
        result = session.sql(query).execute()

        # Retrieve all rows of data
        rows = result.fetch_all()

        # Open the popup and pass the retrieved data as a parameter
        open_popup(rows)
      
    except DatabaseError as err:
        print(f"Error: {err}")

  

def button6_click():
    try:
        query = "SELECT SUM(totalPrice) FROM Orders WHERE orderDate = CURDATE();"
        result = session.sql(query).execute()
        total_sales = result.fetch_one()[0] or 0

        messagebox.showinfo("Total Sales Today", "Total Sales Today: ${:.2f}".format(total_sales))
    except DatabaseError as err:
        print(f"Error: {err}")


def button7_click():
    try:
        # SQL query to join Orders and Items tables and count the number of times each item appears in Orders
        query = "SELECT i.itemID, i.name, COUNT(*) AS sold_count FROM Orders o JOIN OrderItem oi ON o.orderID = oi.orderID JOIN Item i ON oi.itemID = i.itemID GROUP BY oi.itemID, i.itemID, i.name;"
        result = session.sql(query).execute()

        # Retrieve the item sales data
        item_sales = result.fetch_all()

        # Display the item sales
        messagebox.showinfo("Item Sales", "Item Sales:\n\n{}".format('\n'.join([f"Item ID: {row[0]}, Item Name: {row[1]}, Sold Count: {row[2]}" for row in item_sales])))
      
    except DatabaseError as err:
        print(f"Error: {err}")


def main():
    select_database(session)

    # Create the main window
    

    

    # Create buttons
    button1 = Button(window, text="Show stock", font=("Verdana", 40), width=300, height=200, command=button1_click)
    button1.configure(background="red", fg="white")
    button1.grid(row=0, column=0, padx=10, pady=10)

    button2 = Button(window, text="Add items", font=("Verdana", 40), width=300, height=200, command=button2_click)
    button2.configure(background="green", fg="white")
    button2.grid(row=1, column=0, padx=10, pady=10)

    button3 = Button(window, text="Pizza", font=("Verdana", 40), width=300, height=200, command=button3_click)
    button3.configure(background="#001f3f", fg="white")
    button3.grid(row=0, column=1, padx=10, pady=10)

    button4 = Button(window, text="Cola", font=("Verdana", 40), width=300, height=200, command=button4_click)
    button4.configure(background="#0a4275", fg="white")
    button4.grid(row=1, column=1, padx=10, pady=10)

    button5 = Button(window, text="Card", font=("Verdana", 40),borderless=1, width=300, height=200, command=button5_click)
    button5.configure(background="#d3d3d3", fg="white")
    button5.grid(row=2, column=0, padx=10, pady=10)

    button6 = Button(window, text="View Total Sales Today", font=("Verdana", 20), width=300, height=100, command=button6_click)
    button6.configure(background="black", fg="white")
    button6.grid(row=3, column=0, padx=10, pady=10)

    button7 = Button(window, text="View Item Sales", font=("Verdana", 20), width=300, height=100, command=button7_click)
    button7.configure(background="black", fg="white")
    button7.grid(row=3, column=1, padx=10, pady=10)
    # Start the GUI event loop
    window.mainloop()

    session.close()

if __name__ == "__main__":
    main()
