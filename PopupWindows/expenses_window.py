"""
This module defines the Expenses class, which creates a window
for inputting expenses data into a database.
"""

import sqlite3 as sq
from tkinter import messagebox

import ttkbootstrap as ttk  # type: ignore


class Expenses(ttk.Toplevel):
    """Class for the expenses input window."""

    def __init__(self, main_window):
        super().__init__()
        self.title("Uitgaven Invoeren")
        self.main_window = main_window
        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        self.resizable(False, False)

        self.conn = sq.connect("./Database/project.db")  # Database name
        self.curr = self.conn.cursor()  # Create a cursor

        # Create table
        self.curr.execute(
            """CREATE TABLE
            IF NOT EXISTS expenses (
            month TEXT, company TEXT,
            gross_amount BLOB,
            nett_amount BLOB, description TEXT)
            """
        )
        self.conn.commit()

        # Create labels and entries for input fields
        self.expense_labels = {
            "month": ttk.Label(self, text="Maand:"),
            "vendor": ttk.Label(self, text="Leverancier:"),
            "grosst": ttk.Label(self, text="Brutto bedrag:"),
            "nett": ttk.Label(self, text="Netto bedrag:"),
            "descr": ttk.Label(self, text="Omschrijving:"),
        }
        self.expense_labels["month"].grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.expense_labels["vendor"].grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.expense_labels["gross"].grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.expense_labels["nett"].grid(row=3, column=0, padx=5, pady=5, sticky="W")
        self.expense_labels["descr"].grid(row=4, column=0, padx=5, pady=5, sticky="W")

        # Create input fields
        self.expense_entries = {
            "month": ttk.Entry(self, width=10),
            "vendor": ttk.Entry(self, width=10),
            "gross": ttk.Entry(self, width=10),
            "nett": ttk.Entry(self, width=10),
            "descr": ttk.Entry(self, width=10),
        }
        self.expense_entries["month"].grid(
            row=0, column=1, padx=(5, 10), pady=5
        ).focus()
        # self.month_entry.focus()
        self.expense_entries["vendor"].grid(row=1, column=1, padx=(5, 10), pady=5)
        self.expense_entries["gross"].grid(row=2, column=1, padx=(5, 10), pady=5)
        self.expense_entries["nett"].grid(row=3, column=1, padx=(5, 10), pady=5)
        self.expense_entries["descr"].grid(row=4, column=1, padx=(5, 10), pady=5)

        # Buttons
        self.enter_btn = ttk.Button(
            self,
            text="Invoeren",
            bootstyle="success",
            command=self.input_expenses,
        )
        self.enter_btn.grid(
            row=5, column=0, columnspan=2, padx=15, pady=10, sticky="WE"
        )

    # INPUT FUNCTIONS
    def input_expenses(self):
        """function to input the expenses data into the database."""
        input_data = (
            self.expense_entries["month"].get(),
            self.expense_entries["vendor"].get(),
            self.expense_entries["gross"].get(),
            self.expense_entries["nett"].get(),
            self.expense_entries["descr"].get(),
        )

        if not all(input_data):
            messagebox.showerror("Fout", "Vul alle velden in.")
            return

        try:
            self.curr.execute(
                """INSERT INTO expenses (
                    month, company, gross_amount, nett_amount, description)
                VALUES (?, ?, ?, ?, ?)""",
                input_data,
            )
            self.conn.commit()
            messagebox.showinfo("Succes", "Uitgaven succesvol ingevoerd.")
        except sq.Error as e:
            messagebox.showerror("Fout", f"Er is een fout opgetreden: {e}")
        finally:
            self.clear_entries()
            self.expense_entries["month"].focus()

    def clear_entries(self):
        """function to clear the input fields."""
        self.expense_entries["month"].delete(0, "end")
        self.expense_entries["vendor"].delete(0, "end")
        self.expense_entries["gross"].delete(0, "end")
        self.expense_entries["nett"].delete(0, "end")
        self.expense_entries["descr"].delete(0, "end")

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
        self.destroy()


if __name__ == "__main__":
    expenses = Expenses(main_window=None)
    expenses.protocol(
        "WM_DELETE_WINDOW", lambda: (expenses.close_connection(), expenses.destroy())
    )  # Handle closing window and connection
    expenses.mainloop()
