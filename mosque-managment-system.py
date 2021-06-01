from tkinter import *
import sqlite3
from tkinter import messagebox


class Mosque:
    def __init__(self, id, n, t, a, c, i):
        self.id = id
        self.name = n
        self.type = t
        self.address = a
        self.coordinates = c
        self.imam_name = i


class Db:
    def __init__(self):
        con = sqlite3.connect('mosque.db')
        cur = con.cursor()

        cur.execute("""

        CREATE TABLE IF NOT EXISTS mosque(
            id int PRIMARY KEY NOT NULL,
            name text, 
            type text,
            address text,
            coordinates text,
            imam_name text
        )
                """)
        con.commit()
        con.close()

    def display(self):
        con = sqlite3.connect('mosque.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM mosque ")
        records = cur.fetchall()
        con.commit()
        con.close()
        return records

    def insert(self, id, n, t, a, c, i):
        con = sqlite3.connect('mosque.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM mosque WHERE id=?", (id,))
        pkcheck = cur.fetchall()
        if len(pkcheck) != 0 or id == '':
            return 0
        cur.execute("INSERT INTO mosque VALUES (?,?,?,?,?,? )", (id, n, t, a, c, i))
        con.commit()
        con.close()
        return 1

    def search(self, sname):
        con = sqlite3.connect('mosque.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM mosque WHERE name=?", (sname,))
        qr = cur.fetchall()
        con.commit()
        con.close()
        return qr

    def delete(self, id):
        con = sqlite3.connect('mosque.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM mosque WHERE id=?", (id,))
        delcheck = cur.fetchall()
        if len(delcheck) == 0 or id == '':
            return 0
        cur.execute("DELETE FROM mosque WHERE id=?", (id,))
        con.commit()
        con.close()

    def update(self, imam, idd):
        con = sqlite3.connect('mosque.db')
        cur = con.cursor()
        cur.execute("UPDATE mosque SET imam_name=? WHERE id = ? ", (imam, idd))
        con.commit()
        con.close()


def manage(op):
    listing.delete(0, 'end')
    id = Identry.get()
    n = Nameentry.get()
    t = type
    a = Addressentry.get()
    c = Coorentry.get()
    i = Imamentry.get()
    Identry.delete(0, END)
    Nameentry.delete(0, END)
    Addressentry.delete(0, END)
    Coorentry.delete(0, END)
    Imamentry.delete(0, END)

    if op == 0:
        report = database.display()
        listing.insert(END, "Report as follows: ")
        listing.insert(END, 'ID, Name , Type, Address, Coordinates, Imam_name ')
        listing.insert(END, '')
        for i in report:
            listing.insert(END, i)
    elif op == 1:
        primarykeycheck = database.insert(id, n, t, a, c, i)
        if primarykeycheck == 0:
            messagebox.showinfo('Insertion Error', 'ID Empty / Used')
            return
        Mosque(id, n, t, a, c, i)
        listing.insert(END, "Record for ID: " + id + ' created successfully')
    elif op == 2:
        searchres = database.search(n)
        listing.insert(END, "Report as follows: ")
        listing.insert(END, 'ID, Name , Type, Address, Coordinates, Imam_name ')
        listing.insert(END, '')
        if len(searchres) == 0:
            listing.insert(END, " No result for " + n)
        else:
            listing.insert(END, 'Found ' + str(len(searchres)) + ' result(s)')
            for i in searchres:
                listing.insert(END, i)
    elif op == 3:
        delcheck = database.delete(id)
        if delcheck == 0:
            messagebox.showinfo('Deletion Error', 'ID not found')
            return
        listing.insert(END, "Record for ID: " + id + ' deleted successfully')
    elif op == 4:
        if id == "" or i == "":
            messagebox.showinfo('Updating Error',
                                'Enter ID and the new Imam_name to update, search for ID using Search by name button')
        else:
            database.update(i, id)
            listing.insert(END, "Record for ID: " + id + ' Updated successfully')


def menuchoice(event):
    global type
    type = optionvar.get()


database = Db()
root = Tk()
root.title("Mosque Management System")
mainframe = Frame(root)
mainframe.grid(row=0, column=0)
sideframe = Frame(root)
sideframe.grid(row=0, column=1)
part1 = Frame(mainframe)
part2 = Frame(sideframe)
part3 = Frame(mainframe)
part1.grid(row=0, column=0)
part2.grid()
part3.grid(row=1, column=0, padx=20, pady=20)

Idlabel = Label(part1, text="ID")
Idlabel.grid(row=0, column=0)
Identry = Entry(part1)
Identry.grid(row=0, column=1, pady=4, padx=10)
Namelabel = Label(part1, text="Name")
Namelabel.grid(row=0, column=2)
Nameentry = Entry(part1)
Nameentry.grid(row=0, column=3, padx=10)

Typelabel = Label(part1, text="Type")
Typelabel.grid(row=1, column=0)
optionvar = StringVar(value="select an option")
options = ['Mosque', 'Jame']
Menuentry = OptionMenu(part1, optionvar, *options, command=menuchoice)
Menuentry.grid(row=1, column=1)
Addresslabel = Label(part1, text="Address")
Addresslabel.grid(row=1, column=2)
Addressentry = Entry(part1)
Addressentry.grid(row=1, column=3)

Coorlabel = Label(part1, text="Coordinates")
Coorlabel.grid(row=2, column=0)
Coorentry = Entry(part1)
Coorentry.grid(row=2, column=1, pady=4)
Imamlabel = Label(part1, text="Imam_name")
Imamlabel.grid(row=2, column=2)
Imamentry = Entry(part1)
Imamentry.grid(row=2, column=3)

listing = Listbox(part2, width=65)
listing.grid()

button = {}
button[0] = Button(part3, text='Display All', width=12, command=lambda: manage(0))
button[1] = Button(part3, text='Search by Name', width=12, command=lambda: manage(2))
button[2] = Button(part3, text='Update Entry', width=12, command=lambda: manage(4))
button[3] = Button(part3, text='Add Entry', width=12, command=lambda: manage(1))
button[4] = Button(part3, text='Delete Entry', width=12, command=lambda: manage(3))
button[5] = Button(part3, text='Display on Map', width=12)

button[0].grid(row=0, column=0, padx=8, pady=4)
button[1].grid(row=0, column=1, padx=8, pady=4)
button[2].grid(row=0, column=2, padx=8, pady=4)
button[3].grid(row=1, column=0, padx=8, pady=4)
button[4].grid(row=1, column=1, padx=8, pady=4)
button[5].grid(row=1, column=2, padx=8, pady=4)
root.mainloop()

