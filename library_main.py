

import tkinter
from tkinter import *
from tkinter import ttk
import mysql.connector
from datetime import datetime
from tkinter import Toplevel, Label
from tkinter import simpledialog, messagebox, Toplevel
from PIL import Image, ImageTk
import barcode
from barcode.writer import ImageWriter
import os


m = Tk()
m.geometry("550x850")
m.title("Library management")
m.configure(bg="Light yellow")
m.state('zoomed')
m.maxsize(760, 500)

conobj=mysql.connector.connect(host='localhost',database='library',user='root',password='pass')
cur = conobj.cursor()



page1=Frame(m,bg="#274c77")
page2=Frame(m,bg="#34a0a4")
page3=Frame(m,bg="#cdb4db")
page4=Frame(m,bg="#778da9")
page5=Frame(m,bg="honeydew")
page6=Frame(m,bg="honeydew")
page7=Frame(m,bg="khaki")

for p in (page1, page2, page3, page4, page5, page6, page7):
    p.grid(row=0, column=0, sticky="nsew")

lbl1=Label(page1, text=" Library Management ", font="Castellar 40", anchor="center", bg="#6096ba", fg="Black")
lbl1.grid(row=0, column=0, columnspan=5, rowspan=1, pady=40, padx=5)
btn_student = Button(page1, text="Admin\nlogin", font="vardana 20", height=2, width=12, fg="black", bg="#a3cef1",command=lambda:page2.tkraise())
btn_student.grid(row=1, column=1, pady=40, padx=15)
btn_book = Button(page1, text="Student \nlogin", font="vardana 20", height=2, width=12, fg="black", bg="#a3cef1",command=lambda:page3.tkraise())
btn_book.grid(row=1, column=3, pady=40, padx=15)
btn_exit = Button(page1, text="Exit", font="vardana 15", height=1, width=14, fg="black", bg="#8b8c89",command=m.destroy)
btn_exit.grid(row=2, column=2, pady=40, padx=5)

def generate_barcode():
    code = simpledialog.askstring("Create Barcode", "Enter the barcode number:", parent=page2)
    if not code:
        return

    try:
        barcode_cls = barcode.get_barcode_class('code128')
        bc_obj = barcode_cls(code, writer=ImageWriter())

        folder = "barcodes"
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = os.path.join(folder, f"barcode_{code}")
        saved_file = bc_obj.save(filename)
        if not os.path.isfile(saved_file ):
            raise FileNotFoundError(f"{saved_file}.png not found after saving.")

        img = Image.open(saved_file)
        img = img.resize((400, 120), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        win = Toplevel(page2)
        win.title(f"Barcode Preview – {code}")
        Label(win, text=f"Saved to {saved_file}.png", font="BookAntiqua 12").pack(pady=5)
        Label(win, image=img_tk).pack(padx=10, pady=10)
        win.image = img_tk

    except Exception as e:
        messagebox.showerror("Error", f"Could not generate barcode:\n{e}", parent=page2)
        print("Barcode generation failed:", e)

lbl2=Label(page2,text="Admin \nlogin",bg="honeydew")
lbl2.grid(row=0, column=0)
btn_report = Button(page2, text="Student\nlist", font="vardana 20", height=2, width=12, fg="black", bg="#52b69a",command=lambda:page5.tkraise())
btn_report.grid(row=2, column=4, pady=65,padx=20)
btn_bookcat = Button(page2, text="Add new book\n(Barcode)", font="vardana 20", height=2, width=12, fg="black", bg="#52b69a",command=generate_barcode)
btn_bookcat.grid(row=2, column=2, pady=65, padx=20)
#btn_suggest = Button(page2, text="Issue\nbook", font="vardana 20", height=2, width=12, fg="black", bg="light blue")
#btn_suggest.grid(row=4, column=2, pady=10, padx=25)
btn_back = Button(page2, text="Back", font="vardana 20", height=1, width=8, fg="black", bg="#a3b18a",command=lambda:page1.tkraise())
btn_back.grid(row=4, column=3, pady=0, padx=5)


def find_barcode(page7):
    code = simpledialog.askstring(
        "Search Barcode",
        "Enter / scan the student book barcode:",
        parent=page7
    )
    if not code:
        return

    cur = conobj.cursor()

    cur.execute(
        "SELECT S_ID, F_Name, M_Name, L_Name, Class, Book_title, Borrow_Date, Return_Date "
        "FROM student_data WHERE Barcode = %s",
        (code,)
    )
    row = cur.fetchone()

    if row is None:
        messagebox.showinfo("Not found",
                            f"No student record with barcode {code} found.",
                            parent=page7)
    else:
        sid, fname, mname, lname, sclass, title, bdate, rdate = row
        msg = (
            f"Student ID   : {sid}\n"
            f"Name         : {fname} {mname} {lname}\n"
            f"Class        : {sclass}\n"
            f"Book title   : {title}\n"
            f"Borrowed on  : {bdate}\n"
            f"Return by    : {rdate}"
        )

        win = Toplevel(page7)
        win.title(f"Student Book Info – Barcode: {code}")
        Label(win, text=msg, font="BookAntiqua 12", justify="left").pack(padx=14, pady=14)

    cur.close()


def rec():
    if not conobj.is_connected():
        messagebox.showerror("DB error", "Not connected to database")
        return

    curobj.execute("SELECT * FROM student_data")
    rows = curobj.fetchall()

    if not rows:
        messagebox.showinfo("Records", "No records found.")
        return
    win = Toplevel(page3)  
    win.title("All student records")


    columns = (
        "S_ID", "F_Name", "M_Name", "L_Name",
        "Class", "Book_title", "Barcode",
        "Borrow_Date", "Return_Date"
    )

    tree = ttk.Treeview(win, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=110, anchor="center")


    for r in rows:
        tree.insert("", "end", values=r)

    tree.pack(fill="both", expand=True)

SUGGESTION_FILE = "library_suggestions.txt"
def library_suggestions():

    win = Toplevel(page3)
    win.title("Library Suggestions")
    win.grab_set()

    Label(win, text="Student ID:", font="BookAntiqua 12").grid(
        row=0, column=0, padx=10, pady=6, sticky="e")
    sid_var = StringVar()
    Entry(win, textvariable=sid_var, font="BookAntiqua 12").grid(
        row=0, column=1, padx=10, pady=6)

    Label(win, text="Your suggestion (2‑3 lines):",
          font="BookAntiqua 12").grid(row=1, column=0,
                                      columnspan=2, sticky="w", padx=10)
    txt = Text(win, height=3, width=38, font="BookAntiqua 12")
    txt.grid(row=2, column=0, columnspan=2, padx=10, pady=6)

    def save_suggestion():
        sid = sid_var.get().strip()
        suggestion = txt.get("1.0", "end").strip()
        if not sid or not suggestion:
            messagebox.showwarning("Missing data",
                                   "Please enter both Student ID and suggestion.",
                                   parent=win)
            return
        try:
            with open(SUGGESTION_FILE, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp}, {sid}, {suggestion}\n")
            messagebox.showinfo("Saved!",
                                "Suggestion saved to file.",
                                parent=win)
            win.destroy()
        except Exception as e:
            messagebox.showerror("Error",
                                 f"Could not save suggestion:\n{e}",
                                 parent=win)

    Button(win, text="Save", font="vardana 12",
           bg="light blue", command=save_suggestion).grid(
        row=3, column=0, padx=10, pady=10)
    Button(win, text="Cancel", font="vardana 12",
           bg="Burlywood", command=win.destroy).grid(
        row=3, column=1, padx=10, pady=10)

btn_bookcat = Button(page3, text="Records", font="vardana 20", height=2, width=12, fg="black", bg="#ffafcc",command=rec)
btn_bookcat.grid(row=2, column=2, pady=40, padx=25)
btn_suggest = Button(page3, text="library\nsuggestions", font="vardana 20", height=2, width=12, fg="black", bg="#ffafcc",command=library_suggestions)
btn_suggest.grid(row=2, column=3, pady=40, padx=25)
btn_student = Button(page3, text="Search\nBarcode", font="vardana 20", height=2, width=12, fg="black", bg="#ffafcc",command=lambda: find_barcode(page7))
btn_student.grid(row=2, column=1, pady=40, padx=15)
btn_back = Button(page3, text="Back", font="vardana 20", height=1, width=10, fg="black", bg="#da627d",command=lambda:page1.tkraise())
btn_back.grid(row=4, column=2, pady=40, padx=5)

#lbl4=Label(page4,text="Generate\nReport",bg="honeydew")
#lbl4.grid(row=3, column=1)
btn_back = Button(page4, text="Back", font="vardana 20", height=1, width=10, fg="black", bg="#d5bdaf",command=lambda:page1.tkraise())
btn_back.grid(row=6, column=3, pady=40, padx=5)

lbl5=Label(page5, text="Student list ", font="vardana 20", anchor="center",bg="dark salmon",fg="black")
lbl5.grid(row=0, column=0, columnspan=5, rowspan=2)
curobj=conobj.cursor()

sid_var=IntVar()
fname_var=StringVar()
Mname_var=StringVar()
Lname_var=StringVar()
sclass_var=StringVar()
btitle_var=StringVar()
bcode_var=IntVar()
bdate_var=StringVar()
rdate_var=StringVar()


lb4=Label(page5,text="\tEnter student ID:",font="BookAntiqua 13",bg="alice blue")
lb4.grid(row=2,column=0)
sid=Entry(page5,font="BookAntiqua 13",textvariable=sid_var)
sid.grid(row=2,column=2,columnspan=3,pady=10)

lb1=Label(page5,text="\tEnter First name:",font="BookAntiqua 13",bg="alice blue")
lb1.grid(row=3,column=0)
fname=Entry(page5,font="BookAntiqua 13",textvariable=fname_var)
fname.grid(row=3,column=2,columnspan=2,pady=10)

lb2=Label(page5,text="\tEnter Middle name:",font="BookAntiqua 13",bg="alice blue")
lb2.grid(row=4,column=0)
Mname=Entry(page5,font="BookAntiqua 13",textvariable=Mname_var)
Mname.grid(row=4,column=2,columnspan=2,pady=10)

lb3=Label(page5,text="\tEnter Last name:",font="BookAntiqua 13",bg="alice blue")
lb3.grid(row=5,column=0)
Lname=Entry(page5,font="BookAntiqua 13",textvariable=Lname_var)
Lname.grid(row=5,column=2,columnspan=3,pady=10)

lb5=Label(page5,text="\tEnter Class:",font="BookAntiqua 13",bg="alice blue")
lb5.grid(row=6,column=0)
sclass=Entry(page5,font="BookAntiqua 13",textvariable=sclass_var)
sclass.grid(row=6,column=2,columnspan=3,pady=10)

lb6=Label(page5,text="\tEnter Book title:",font="BookAntiqua 13",bg="alice blue")
lb6.grid(row=7,column=0)
btitle=Entry(page5,font="BookAntiqua 13",textvariable=btitle_var)
btitle.grid(row=7,column=2,columnspan=3,pady=10)

lb7=Label(page5,text="\tEnter Barcode:",font="BookAntiqua 13",bg="alice blue")
lb7.grid(row=8,column=0)
bcode=Entry(page5,font="BookAntiqua 13",textvariable=bcode_var)
bcode.grid(row=8,column=2,columnspan=3,pady=10)

lb8=Label(page5,text="\tEnter date of borrow(mm/dd/yy):",font="BookAntiqua 13",bg="alice blue")
lb8.grid(row=9,column=0)
bdate=Entry(page5,font="BookAntiqua 13",textvariable=bdate_var)
bdate.grid(row=9,column=2,columnspan=3,pady=10)

lb9=Label(page5,text="\tEnter Return date(mm/dd/yy):",font="BookAntiqua 13",bg="alice blue")
lb9.grid(row=10,column=0)
rdate=Entry(page5,font="BookAntiqua 13",textvariable=rdate_var)
rdate.grid(row=10,column=2,columnspan=3,pady=10)

def sadd():
    if conobj.is_connected():

        if not sid_var.get() or not fname_var.get() or not Lname_var.get() or not sclass_var.get() or not btitle_var.get() or not bcode_var.get():
            messagebox.showwarning("Validation Error", "Please fill in all required fields.")
            return

        try:
            b_date = datetime.strptime(bdate_var.get(), "%m/%d/%y").date()
            r_date = datetime.strptime(rdate_var.get(), "%m/%d/%y").date()
        except ValueError:
            messagebox.showerror("Date Error", "Please enter valid dates in MM/DD/YY format.")
            return

        try:
            qry = """INSERT INTO student_data
            (S_ID,F_Name,M_Name,L_Name,Class,Book_title ,Barcode,Borrow_Date,Return_Date)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            values = (
                sid_var.get(),
                fname_var.get(),
                Mname_var.get(),
                Lname_var.get(),
                sclass_var.get(),
                btitle_var.get(),
                bcode_var.get(),
                b_date,
                r_date
            )

            curobj.execute(qry, values)
            conobj.commit()
            messagebox.showinfo("Success", "Student data inserted successfully")
            clr()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            print("MySQL Error:", err)

        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
            print("Unexpected Error:", e)
    else:
        messagebox.showerror("Database Error", "Connection to database failed")


def remove_student():
    sid = sid_var.get()
    if sid == "":
        messagebox.showerror("Error", "Please enter a Student ID to remove.")
        return
    curobj.execute("DELETE FROM student_data WHERE S_ID = %s", (sid,))
    conobj.commit()
    messagebox.showinfo("Success", "Student record removed.")
    clr()
    if not fname_var.get() or not sclass_var.get() or not btitle_var.get():
        messagebox.showwarning("Validation Error", "Please fill in all required fields.")
        return

def clr():
    sid_var.set("")
    fname_var.set("")
    Mname_var.set("")
    Lname_var.set("")
    sclass_var.set("")
    btitle_var.set("")
    bcode_var.set("")
    bdate_var.set("")
    rdate_var.set("")


btn_back = Button(page5, text="Back", font="vardana 15", height=1, width=10, fg="black", bg="Burlywood",command=lambda:page1.tkraise())
btn_back.grid(row=11, column=0, pady=2, padx=10)
btn_add= Button(page5, text="Add Student", font="vardana 15", height=1, width=10, fg="black", bg="Burlywood",command=sadd)
btn_add.grid(row=11, column=2, pady=2,ipadx=10,padx=10)
btn_remove = Button(page5, text="Remove student", font="vardana 15", height=1, width=10, fg="black", bg="Burlywood",command=remove_student)
btn_remove.grid(row=11, column=3, pady=2,ipadx=13,padx=10)



page1.tkraise()
m.mainloop()