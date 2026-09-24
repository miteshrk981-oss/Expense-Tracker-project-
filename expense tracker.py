import tkinter as tk
import sqlite3 as sql
import pandas as pd
from tkinter import messagebox, ttk
from datetime import datetime

con = sql.connect("expense.db")
cursor = con.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS expense (
        ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        MONTH TEXT NOT NULL, 
        EXPENSE REAL NOT NULL, 
        CATEGORY TEXT NOT NULL, 
        REMARKS TEXT, 
        DATE TEXT NOT NULL
    )
"""
)

def add_expense(): 
    try:
        expense_val = float(expense.get().strip())
        if expense_val <= 0:
            messagebox.showinfo("Alert", "Expense must be greater than 0")
            return
    except ValueError:
        messagebox.showinfo("Alert", "Expense must be a number!")
        return
    


    month_val = month.get()
    category_val = category.get()
    remarks_val = remarks.get()
    date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        "INSERT INTO expense (MONTH, EXPENSE, CATEGORY, REMARKS, DATE) VALUES(?, ?, ?, ?, ?)",
        (month_val, expense_val, category_val, remarks_val, date)
    )
        
    con.commit()

    messagebox.showinfo("Success", "Record inserted Successfully")

    show_expense()

    expense.delete(0, tk.END)
    remarks.delete(0, tk.END)
    month.current(0)
    category.current(0)

def clear_all():
    expense.delete(0, tk.END)
    remarks.delete(0, tk.END)
    month.current(0)
    category.current(0)

    messagebox.showinfo("Success", "Record Cleared Successfully")

def show_expense():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM expense ORDER BY DATE DESC")
    
    row = cursor.fetchall()

    total_val = 0

    for r in row:
        tree.insert("", "end", values=r)
        total_val += r[2]

    total_expense_lbl.config(text=f"Total Expenses (in RS.): {total_val}")

def delete_expense():
    selected_row = tree.selection()

    if not selected_row:
        messagebox.showinfo("Error","Please select a record to delete")
        return

    item = tree.item(selected_row[0])

    record_id = item['values'][0]

    cursor.execute("DELETE FROM expense WHERE ID = ?", (record_id,)
    )

    con.commit()

    messagebox.showinfo("Success", "Record Deleted Successfully")

    show_expense()

def export_to_csv():
    df = pd.read_sql_query("SELECT * FROM expense ORDER BY DATE ", con)
    df.to_csv('expense.csv', index=False)

    messagebox.showinfo("Success", "Records exported Successfully")
    
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x350")

frame1 = tk.Frame(root)
frame1.pack(pady=20)

lbl1 = tk.Label(frame1, text="Select Month", font=("Arial",12,"bold"))
lbl1.grid(row=0, column=0, pady=10)

all_month = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
month =ttk.Combobox(frame1, values=all_month, state="readonly", font=("Arial",12,))
month.grid(row=0, column=1, pady=10)
month.current(0)

lbl2 = tk.Label(frame1, text="Enter Expense(in Rs.)", font=("Arial",12,"bold"))
lbl2.grid(row=1, column=0, pady=10)

expense =ttk.Entry(frame1, width=20, font=("Arial",16))
expense.grid(row=1, column=1, pady=10)

lbl3 = tk.Label(frame1, text="Select Category", font=("Arial",12,"bold"))
lbl3.grid(row=2, column=0, pady=10)

all_categories = ["Food","Bills","Travel","Clothes","Others"]
category = ttk.Combobox(frame1, values=all_categories, state="readonly",font=("Arial",12,))
category.grid(row=2, column=1, pady=10)
category.current(0)

lbl4 = tk.Label(frame1, text="Select Remarks", font=("Arial",12,"bold"))
lbl4.grid(row=3, column=0, pady=10)

remarks = ttk.Entry(frame1, width=20, font=("Arial",16))
remarks.grid(row=3, column=1, pady=10)

add_btn = tk.Button(frame1, text="Submit", bg="black", fg="white", font=("Arial",12), command=add_expense)
add_btn.grid(row=4, column=0, pady=10)

clear_btn = tk.Button(frame1, text="Clear", bg="lightblue", fg="black", font=("Arial",12), command=clear_all)
clear_btn.grid(row=4, column=1, pady=10)

delete_btn = tk.Button(frame1, text="Delete", bg="yellow", fg="red", font=("Arial",12), command=delete_expense)
delete_btn.grid(row=5, column=0, pady=10)

export_btn = tk.Button(frame1, text="Export", bg="darkblue", fg="white", font=("Arial",12), command=export_to_csv)
export_btn.grid(row=5, column=1, pady=10)

total_expense_lbl = tk.Label(frame1 ,text="Total Expense(in RS.): 0", font=("Arial",12,"bold"))
total_expense_lbl.grid(row=6, column=0, columnspan=2, pady=10)

frame2 = tk.Frame(root)
frame2.pack(pady=20)

tree = ttk.Treeview(frame2, columns=("ID","MONTH","EXPENSE","CATEGORY","REMARKS","DATE"), show="headings")

tree.heading("ID", text="ID", anchor="center")
tree.heading("MONTH", text="MONTH", anchor="center")
tree.heading("EXPENSE", text="EXPENSE", anchor="center")
tree.heading("CATEGORY", text="CATEGORY", anchor="center")
tree.heading("REMARKS", text="REMARKS", anchor="center")
tree.heading("DATE", text="DATE", anchor="center")

tree.column("ID", width=50)
tree.column("MONTH", width=100)
tree.column("EXPENSE", width=100)
tree.column("CATEGORY", width=100)
tree.column("REMARKS", width=200)
tree.column("DATE", width=120)

tree.pack()

show_expense()

root.mainloop()

con.close()




 

