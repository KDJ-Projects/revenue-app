import sqlite3 as sq
import ttkbootstrap as ttk
from tkinter import messagebox


class Vat:
    """Class for the VAT input window."""

    def __init__(self, main_window):
        """function to initialize the VAT input window."""
        self.vat = ttk.Toplevel()  # Create a new top-level window
        self.vat.geometry("+500+415")
        self.vat.title("Btw Ingave")
        self.main_window = main_window  # Store the MainWindow instance

        self.conn = sq.connect("KDJ-Projects.db")  # Database name
        self.curr = self.conn.cursor()  # Create a cursor

        # Create table
        self.curr.execute(
            """CREATE TABLE IF NOT EXISTS vat (vat_quarter TEXT, vat_amount BLOB)"""
        )
        self.conn.commit()

        # Input Quarter
        self.quarter_lbl = ttk.Label(self.vat, text="Kwartaal:")
        self.quarter_entry = ttk.Entry(self.vat, width=10)
        self.quarter_entry.focus()

        self.quarter_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.quarter_entry.grid(row=0, column=1, padx=(5, 10), pady=5)

        # Input Vat Amount
        self.vat_amount_lbl = ttk.Label(self.vat, text="Btw:")
        self.vat_amount_entry = ttk.Entry(self.vat, width=10)
        self.vat_amount_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.vat_amount_entry.grid(row=1, column=1, padx=(5, 10), pady=5)

        # Buttons
        self.enter_btn = ttk.Button(
            self.vat,
            text="Invoeren",
            bootstyle="success",
            command=self.input_vat,
        )
        self.enter_btn.grid(
            row=2, column=0, columnspan=3, padx=15, pady=10, sticky="WE"
        )

    def input_vat(self):
        """function to input the VAT data into the database."""
        input = (self.quarter_entry.get(), self.vat_amount_entry.get())

        if not input[0] or not input[1]:
            messagebox.showerror("Opgelet", "Vul alstublieft alle velden in.")
            self.quarter_entry.focus()  # Set focus back to the quarter entry field
            return

        self.curr.execute(
            """INSERT INTO vat (quarter, vat_amount) VALUES (?, ?)""",
            (input[0], input[1]),
        )
        self.conn.commit()

        self.total_quarter_vat()  # Call the function to get the total VAT amount for the quarter

        # Clearing the input fields
        self.quarter_entry.delete(0, "end")
        self.vat_amount_entry.delete(0, "end")

        self.vat.destroy()  # Close the VAT input window

    # Functions
    def total_quarter_vat(self):
        """function to get the total VAT amount for the quarter."""
        self.curr.execute("""SELECT SUM(vat_amount) FROM vat""")
        total_quarter_vat = self.curr.fetchone()[0]  # Fetch the first value
        if total_quarter_vat is None:
            total_quarter_vat = 0.0

        self.main_window.quarter_vat_info_lbl.config(
            text=f"Totaal Btw Ingave: {total_quarter_vat:,.2f}€"
        )

    def close_connection(self):
        """function to close the database connection."""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    """Main function to run the VAT input window."""
    vat = ttk.Window()
    style = ttk.Style(theme="darkly")
    app = Vat(vat)
    vat.protocol("WM_DELETE_WINDOW", lambda: (app.close_connection(), vat.destroy()))
    vat.mainloop()
