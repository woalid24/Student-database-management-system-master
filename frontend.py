
from tkinter import *
import backend
import sqlite3  


def get_selected_row(event):
    '''Get content of the selected row.'''
    global selected_tuple
    if lb1.curselection() != ():
        index = lb1.curselection()[0]
        selected_tuple = lb1.get(index)
        clear_entries()
        e1.insert(END, selected_tuple[1])
        e2.insert(END, selected_tuple[2])
        e3.insert(END, selected_tuple[3])
        e4.insert(END, selected_tuple[4])


def view_command():
    '''Show the content of the database.'''
    lb1.delete(0, END)
    for row in backend.view():
        lb1.insert(END, row)


def view_high_gpa_command():
    '''Show students with GPA > 3.0.'''
    lb1.delete(0, END)
    for row in backend.view_high_gpa_students():
        lb1.insert(END, row)


def view_log_command():
    '''Show the log of updates from data1_log table.'''
    conn = sqlite3.connect("Students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM data1_log")
    rows = cur.fetchall()
    conn.close()
    lb1.delete(0, END)
    for row in rows:
        lb1.insert(END, row)


def search_command():
    '''Search the database for a specific student.'''
    lb1.delete(0, END)
    for row in backend.search(fn.get(), ln.get(), term.get(), gpa.get()):
        lb1.insert(END, row)
    clear_entries()


def add_command():
    '''Add a new student to the database.'''
    backend.insert(fn.get(), ln.get(), term.get(), gpa.get())
    clear_entries()
    view_command()


def update_command():
    '''Update the data of a specific student.'''
    backend.update(selected_tuple[0], fn.get(), ln.get(), term.get(), gpa.get())
    clear_entries()
    view_command()


def delete_command():
    '''Delete a specific student.'''
    index = lb1.curselection()[0]
    selected_tuple = lb1.get(index)
    backend.delete(selected_tuple[0])
    clear_entries()
    view_command()


def delete_data_command():
    '''Delete all students from the database.'''
    backend.delete_data()
    view_command()


def clear_entries():
    '''Clear all entry fields.'''
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)


def clear_command():
    '''Clear the content of the Listbox.'''
    lb1.delete(0, END)
    clear_entries()


wind = Tk()

fn = StringVar()
ln = StringVar()
term = StringVar()
gpa = StringVar()

l0 = Label(wind, text="Students", width="10", fg="blue")
l0.config(font=("Courier", 15))

l00 = Label(wind, text="Database", width="10", fg="blue")
l00.config(font=("Courier", 15))

l1 = Label(wind, text="First Name", width="10")
l2 = Label(wind, text="Last Name", width="10")
l3 = Label(wind, text="Term", width="10")
l4 = Label(wind, text="GPA", width="10")

e1 = Entry(wind, textvariable=fn)
e2 = Entry(wind, textvariable=ln)
e3 = Entry(wind, textvariable=term)
e4 = Entry(wind, textvariable=gpa)

b1 = Button(wind, text="View all", width="15", command=view_command)
b2 = Button(wind, text="Search", width="15", command=search_command)
b3 = Button(wind, text="Add New", width="15", command=add_command)
b4 = Button(wind, text="Update", width="15", command=update_command)
b5 = Button(wind, text="Delete", width="15", command=delete_command)
b6 = Button(wind, text="Clear", width="15", command=clear_command)
b7 = Button(wind, text="Delete all Students", width="15", command=delete_data_command)
b8 = Button(wind, text="High GPA Students", width="15", command=view_high_gpa_command)  # New button
b9 = Button(wind, text="View Logs", width="15", command=view_log_command)  # New button
b10 = Button(wind, text="Exit", width="15", command=wind.destroy)

lb1 = Listbox(wind, height=6, width=35)
lb1.bind('<<ListboxSelect>>', get_selected_row)

sc = Scrollbar(wind)

l0.grid(row=0, column=1)
l00.grid(row=0, column=2)
l1.grid(row=1, column=0)
l2.grid(row=1, column=2)
l3.grid(row=2, column=0)
l4.grid(row=2, column=2)

e1.grid(row=1, column=1)
e2.grid(row=1, column=3)
e3.grid(row=2, column=1)
e4.grid(row=2, column=3)

b1.grid(row=3, column=3)
b2.grid(row=4, column=3)
b3.grid(row=5, column=3)
b4.grid(row=6, column=3)
b5.grid(row=7, column=3)
b6.grid(row=8, column=3)
b7.grid(row=9, column=3)
b8.grid(row=10, column=3)  # High GPA button
b9.grid(row=11, column=3)  # Logs button
b10.grid(row=12, column=3)

lb1.grid(row=4, column=0, rowspan=8, columnspan=2)

sc.grid(row=4, column=2, rowspan=8)

lb1.configure(yscrollcommand=sc.set)
sc.configure(command=lb1.yview)

wind.mainloop()
