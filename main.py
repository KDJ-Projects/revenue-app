import sqlite3 as sq
from tkinter import messagebox

import ttkbootstrap as tb


class Revenue:
    def __init__(self, root):
        self.root = root
        self.root.title("KDJ-Projects")

        # Create a database
        self.conn = sq.connect("KDJ-Projects.db")
        self.curr = self.conn.cursor()

        # Create table
        self.curr.execute(
            """CREATE TABLE IF NOT EXISTS revenue (month TEXT, company TEXT, amount BLOB, tax BLOB)"""
        )
        self.conn.commit()

        # Date
        self.month_lbl = tb.Label(root, text="Maand:")
        self.month_entry = tb.Entry(root, width=10)
        self.month_entry.focus()

        self.month_lbl.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="W")
        self.month_entry.grid(row=0, column=1, padx=5, pady=(5, 10), sticky="E")

        # Company
        self.company_lbl = tb.Label(root, text="Bedrijf:")
        self.company_entry = tb.Entry(root, width=10)

        self.company_lbl.grid(row=1, column=0, padx=5, pady=(10, 5), sticky="W")
        self.company_entry.grid(row=1, column=1, padx=5, pady=(5, 10), sticky="E")

        # Amount
        self.amount_lbl = tb.Label(root, text="Bedrag:")
        self.amount_entry = tb.Entry(root, width=10)

        self.amount_lbl.grid(row=2, column=0, padx=5, pady=(10, 5), sticky="W")
        self.amount_entry.grid(row=2, column=1, padx=5, pady=(5, 10), sticky="E")

        # Total amount
        self.total_amount_lbl = tb.Label(
            root, text=f"Totaal inkomsten: {self.total_revenue()}€"
        )
        self.total_amount_lbl.grid(row=3, columnspan=3, pady=5, padx=5)

        # Tax
        self.total_tax_lbl = tb.Label(
            root, text=f"Totaal btw: {self.total_revenue() * 0.21}€"
        )
        self.total_tax_lbl.grid(row=4, columnspan=3, pady=5, padx=5)

        # Buttons
        self.enter_btn = tb.Button(
            root, text="Invoeren", bootstyle="success", command=self.input_revenue
        )
        self.enter_btn.grid(row=5, column=0, columnspan=3, pady=5, padx=(10, 5))

        # self.total_rev_btn = tb.Button(
        #     root, text="Totaal", bootstyle="", command=self.total_revenue
        # )
        # self.total_rev_btn.grid(row=4, column=1, pady=5, padx=(5, 10), sticky="E")

    def input_revenue(self):
        input = (
            self.month_entry.get()
            and self.company_entry.get()
            and self.amount_entry.get()
        )
        if input:
            self.curr.execute(
                "INSERT INTO revenue (month, company, amount) VALUES (?,?,?)",
                (
                    self.month_entry.get(),
                    self.company_entry.get(),
                    self.amount_entry.get(),
                ),
            )
            self.conn.commit()
            self.total_revenue()
            self.conn.close()

            # clear input fields
            self.month_entry.delete(0, tb.END)
            self.company_entry.delete(0, tb.END)
            self.amount_entry.delete(0, tb.END)
        else:
            messagebox.showwarning("Opgelet", "Voer ingave in!")

    def total_revenue(self):
        self.curr.execute("SELECT SUM(amount) FROM revenue")
        total_amount = self.curr.fetchall()
        for amount in total_amount:
            for x in amount:
                return x
                # print(f"Totaal inkomsten: {x}€")


if __name__ == "__main__":
    root = tb.Window()
    root.geometry("+3000+300")
    style = tb.Style(theme="superhero")
    app = Revenue(root)
    root.mainloop()
