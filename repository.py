from tkinter import messagebox
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib import style


class Repository:
    def __init__(self, connection, table):
        self.conn = connection
        self.table = table

    def add_item(self, category, amount, date):
        if len(category.get()) == 0 or len(amount.get()) == 0 or len(date.get()) == 0:
            messagebox.showinfo("Error", "Please dont leave any field empty")
        else:
            sql = '''INSERT INTO expenses VALUES(null, ?, ?, ?)'''
            cursor = self.conn.cursor()
            cursor.execute(sql, (category.get(), amount.get(), date.get()))
            self.conn.commit()
            self.list_items()
            messagebox.showinfo("Item added", 'Item has been added to the database')
            category.delete(0, tk.END)
            amount.delete(0, tk.END)
            date.delete(0, tk.END)

    def create_plot(self):
        plot_dict = {}
        sql = '''SELECT category, amount FROM expenses'''
        cursor = self.conn.cursor()
        for record in cursor.execute(sql):
            plot_dict[record[0]] = plot_dict.get(record[0], 0) + record[1]

        style.use('fivethirtyeight')
        plt.bar(plot_dict.keys(), plot_dict.values())
        plt.title('Amount of money spent by category')
        plt.xlabel('Categories')
        plt.ylabel('Amount')
        plt.show()

    def list_items(self):
        sql = '''SELECT * FROM expenses'''
        cursor = self.conn.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        for item in self.table.get_children():
            self.table.delete(item)

        for record in records:
            id = record[0]
            category = record[1]
            amount = record[2]
            date = record[3]
            data = (id, category, amount, date)
            self.table.insert(parent='', index=tk.END, values=data)

    def delete_item(self):
        try:
            selected_item = self.table.focus()
            item_id = self.table.item(selected_item)['values'][0]
        except IndexError:
            messagebox.showinfo("Error", "No item selected")
        else:
            proceed = messagebox.askyesno(title="How do you want to proceed?",
                                          message="Are yo sure that you want to delete this item?")
            if proceed:
                sql = '''DELETE from expenses WHERE id=?'''
                cursor = self.conn.cursor()
                cursor.execute(sql, [str(item_id)])
                self.conn.commit()

                self.table.delete(selected_item)
                messagebox.showinfo("Item deleted", 'Item has been deleted from the database')
            else:
                pass
