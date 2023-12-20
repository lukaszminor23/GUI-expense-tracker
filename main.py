import sqlite3
from tkinter import *
from tkinter import ttk

from repository import Repository

FONT = ("Arial", 12, 'normal')
PADY = 2
PADX = 2


def init_db(conn):
    cursor = conn.cursor()
    sql = '''CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    amount REAL,
    date TEXT
    )'''
    cursor.execute(sql)
    conn.commit()


def create_table():
    table.heading('id', text='id')
    table.heading('category', text='Category')
    table.heading('amount', text='Amount')
    table.heading('date', text='Date')
    table.column('id', width=100)
    table.column('category', width=100)
    table.column('amount', width=100)
    table.column('date', width=100)
    table.pack(fill='both')


if __name__ == '__main__':
    with sqlite3.connect('expense_tracker.db') as connection:
        init_db(connection)

        window = Tk()
        window.title('Expense tracker')

        table = ttk.Treeview(columns=('id', 'category', 'amount', 'date'), show='headings')
        create_table()

        repo = Repository(connection, table)

        entry_frame = ttk.Frame(window)
        entry_frame.pack(expand=True, fill="both")

        button_frame = ttk.Frame(window)
        button_frame.pack(expand=True, fill="both")

# ------------------- Entries -----------------#
        category_entry = Entry(master=entry_frame, width=65)
        category_entry.grid(row=1, column=1, columnspan=2, sticky="snew", pady=PADY, padx=PADX)

        amount_entry = Entry(master=entry_frame)
        amount_entry.grid(row=2, column=1, columnspan=2, sticky="snew", pady=PADY, padx=PADX)

        date_entry = Entry(master=entry_frame)
        date_entry.grid(row=3, column=1, columnspan=2, sticky="snew", pady=PADY, padx=PADX)
        date_entry.insert(0, "YYYY-MM-DD")

# ------------------- Labels ------------------#

        category_label = Label(master=entry_frame, text="Category:", width=10, font=FONT)
        category_label.grid(row=1, column=0, sticky="snew", pady=PADY, padx=PADX)

        amount_label = Label(master=entry_frame, text="Amount:", font=FONT)
        amount_label.grid(row=2, column=0, sticky="snew", pady=PADY, padx=PADX)

        date_label = Label(master=entry_frame, text="Date:", font=FONT)
        date_label.grid(row=3, column=0, sticky="snew", pady=PADY, padx=PADX)

# -------------------- Buttons ----------------#
        add_button = ttk.Button(master=button_frame, width=30, text="Add item", command=lambda: repo.add_item(
            category_entry,
            amount_entry,
            date_entry
        ))
        add_button.grid(row=0, column=0, sticky="snew", pady=PADY,  padx=PADX, ipady=15)

        delete_button = ttk.Button(master=button_frame, width=30, text="Delete item", command=repo.delete_item)
        delete_button.grid(row=0, column=1, sticky="snew", pady=PADY,  padx=PADX, ipady=15)

        display_button = ttk.Button(master=button_frame, width=30, text="Display chart", command=repo.create_plot)
        display_button.grid(row=0, column=2, sticky="snew", pady=PADY,  padx=PADX, ipady=15)

        repo.list_items()

        window.mainloop()
