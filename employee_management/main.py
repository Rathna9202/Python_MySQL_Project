import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

def GetValue(event):
    try:
        e1.delete(0, tk.END)
        e2.delete(0, tk.END)
        e3.delete(0, tk.END)
        e4.delete(0, tk.END)
        row_id = listBox.selection()[0]
        select = listBox.item(row_id, 'values')
        e1.insert(0, select[0])
        e2.insert(0, select[1])
        e3.insert(0, select[2])
        e4.insert(0, select[3])
    except Exception as e:
        messagebox.showerror("Error", str(e))

def Add():
    studid = e1.get()
    studname = e2.get()
    mobile = e3.get()
    salary = e4.get()

    try:
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="payroll")
        mycursor = mysqldb.cursor()
        sql = "INSERT INTO registation (id, empname, mobile, salary) VALUES (%s, %s, %s, %s)"
        val = (studid, studname, mobile, salary)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Employee inserted successfully...")
        ClearEntries()
        ShowRecords()
    except Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if mysqldb.is_connected():
            mycursor.close()
            mysqldb.close()

def Update():
    studid = e1.get()
    studname = e2.get()
    mobile = e3.get()
    salary = e4.get()

    try:
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="payroll")
        mycursor = mysqldb.cursor()
        sql = "UPDATE registation SET empname=%s, mobile=%s, salary=%s WHERE id=%s"
        val = (studname, mobile, salary, studid)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Record updated successfully...")
        ClearEntries()
        ShowRecords()
    except Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if mysqldb.is_connected():
            mycursor.close()
            mysqldb.close()

def Delete():
    studid = e1.get()

    try:
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="payroll")
        mycursor = mysqldb.cursor()
        sql = "DELETE FROM registation WHERE id=%s"
        val = (studid,)
        mycursor.execute(sql, val)
        mysqldb.commit()
        messagebox.showinfo("Information", "Record deleted successfully...")
        ClearEntries()
        ShowRecords()
    except Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        if mysqldb.is_connected():
            mycursor.close()
            mysqldb.close()

def ShowRecords():
    try:
        mysqldb = mysql.connector.connect(host="localhost", user="root", password="", database="payroll")
        mycursor = mysqldb.cursor()
        mycursor.execute("SELECT id, empname, mobile, salary FROM registation")
        records = mycursor.fetchall()
        listBox.delete(*listBox.get_children())
        for record in records:
            listBox.insert("", "end", values=record)
    except Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        try:
            if mysqldb.is_connected():
                mycursor.close()
                mysqldb.close()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to close connection: {str(e)}")

def ClearEntries():
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)
    e4.delete(0, tk.END)
    e1.focus_set()

root = tk.Tk()
root.geometry("800x500")

tk.Label(root, text="Employee Registration", fg="red", font=(None, 30)).place(x=300, y=5)

tk.Label(root, text="Employee ID").place(x=10, y=10)
tk.Label(root, text="Employee Name").place(x=10, y=40)
tk.Label(root, text="Mobile").place(x=10, y=70)
tk.Label(root, text="Salary").place(x=10, y=100)

e1 = tk.Entry(root)
e1.place(x=140, y=10)

e2 = tk.Entry(root)
e2.place(x=140, y=40)

e3 = tk.Entry(root)
e3.place(x=140, y=70)

e4 = tk.Entry(root)
e4.place(x=140, y=100)

tk.Button(root, text="Add", command=Add, height=3, width=13).place(x=30, y=130)
tk.Button(root, text="Update", command=Update, height=3, width=13).place(x=140, y=130)
tk.Button(root, text="Delete", command=Delete, height=3, width=13).place(x=250, y=130)

cols = ('id', 'empname', 'mobile', 'salary')
listBox = ttk.Treeview(root, columns=cols, show='headings')

for col in cols:
    listBox.heading(col, text=col)

listBox.grid(row=1, column=0, columnspan=2)
listBox.place(x=10, y=200)

ShowRecords()
listBox.bind('<Double-Button-1>', GetValue)

root.mainloop()
