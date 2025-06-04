import sqlite3 as sq
from tkinter import messagebox

import ttkbootstrap as ttk


class Expenses(ttk.Toplevel):
    """Class for the expenses input window."""

    def __init__(self, main_window):
        super().__init__()
        """function to initialize the expenses input window."""
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

        # Input label and entry for Month
        self.month_lbl = ttk.Label(self, text="Maand:")
        self.month_entry = ttk.Entry(self, width=10)
        self.month_entry.focus()
        self.month_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.month_entry.grid(row=0, column=1, padx=(5, 10), pady=5)

        # Input label and entry for Vendor
        self.vendor_lbl = ttk.Label(self, text="Leverancier:")
        self.vendor_entry = ttk.Entry(self, width=10)
        self.vendor_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.vendor_entry.grid(row=1, column=1, padx=(5, 10), pady=5)
        # Input label and entry for Amount
        self.gross_amount_lbl = ttk.Label(self, text="Brutto bedrag:")
        self.gross_amount_entry = ttk.Entry(self, width=10)
        self.gross_amount_lbl.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.gross_amount_entry.grid(row=2, column=1, padx=(5, 10), pady=5)

        # Input label and entry for Vat
        self.nett_amount_lbl = ttk.Label(self, text="Netto bedrag:")
        self.nett_amount_entry = ttk.Entry(self, width=10)
        self.nett_amount_lbl.grid(row=3, column=0, padx=5, pady=5, sticky="W")
        self.nett_amount_entry.grid(row=3, column=1, padx=(5, 10), pady=5)

        # Input label and entry for Description
        self.description_lbl = ttk.Label(self, text="Omschrijving:")
        self.description_entry = ttk.Entry(self, width=10)
        self.description_lbl.grid(row=4, column=0, padx=5, pady=5, sticky="W")
        self.description_entry.grid(row=4, column=1, padx=(5, 10), pady=5)

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
            self.month_entry.get(),
            self.vendor_entry.get(),
            self.gross_amount_entry.get(),
            self.nett_amount_entry.get(),
            self.description_entry.get(),
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
            self.month_entry.focus()

    def clear_entries(self):
        """function to clear the input fields."""
        self.month_entry.delete(0, "end")
        self.vendor_entry.delete(0, "end")
        self.gross_amount_entry.delete(0, "end")
        self.nett_amount_entry.delete(0, "end")
        self.description_entry.delete(0, "end")


if __name__ == "__main__":
    root = ttk.Window(title="Expenses Input Window")
    app = Expenses(root)
    root.mainloop()
