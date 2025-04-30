import sqlite3 as sq
import ttkbootstrap as ttk
from tkinter import messagebox


class Revenue:
    """Class for the revenue input window."""

    def __init__(self, main_window):
        """function to initialize the revenue input window."""
        self.revenue = ttk.Toplevel()  # Create a new top-level window
        self.revenue.geometry("+500+415")
        self.revenue.title("Ingave")
        self.main_window = main_window  # Store the MainWindow instance

        self.conn = sq.connect("KDJ-Projects.db")  # Database name
        self.curr = self.conn.cursor()  # Create a cursor

        # Create table
        self.curr.execute(
            """CREATE TABLE IF NOT EXISTS revenue (month TEXT, company TEXT, amount BLOB, tax BLOB)"""
        )
        self.conn.commit()

        # Input Date
        self.month_lbl = ttk.Label(self.revenue, text="Maand:")
        self.month_entry = ttk.Entry(self.revenue, width=10)
        self.month_entry.focus()

        self.month_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.month_entry.grid(row=0, column=1, padx=(5, 10), pady=5)

        # Input Company
        self.company_lbl = ttk.Label(self.revenue, text="Bedrijf:")
        self.company_entry = ttk.Entry(self.revenue, width=10)

        self.company_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.company_entry.grid(row=1, column=1, padx=(5, 10), pady=5)

        # Input Amount
        self.amount_lbl = ttk.Label(self.revenue, text="Bedrag:")
        self.amount_entry = ttk.Entry(self.revenue, width=10)

        self.amount_lbl.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.amount_entry.grid(row=2, column=1, padx=(5, 10), pady=5)

        # Input Vat
        self.vat_lbl = ttk.Label(self.revenue, text="Btw:")
        self.vat_entry = ttk.Entry(self.revenue, width=10)

        self.vat_lbl.grid(row=3, column=0, padx=5, pady=5, sticky="W")
        self.vat_entry.grid(row=3, column=1, padx=(5, 10), pady=5)

        # Buttons
        self.enter_revenue_btn = ttk.Button(
            self.revenue,
            text="Invoeren",
            bootstyle="success",
            command=self.input_revenue,
        )
        self.enter_revenue_btn.grid(
            row=4, column=0, columnspan=3, pady=10, padx=15, sticky="WE"
        )

        self.total_revenue()  # Gets the total revenue amount
        self.total_vat()  # Gets the total vat amount

    def input_revenue(self):
        """Inserts the input data into the database."""
        input = (
            self.month_entry.get(),
            self.company_entry.get(),
            self.amount_entry.get(),
            self.vat_entry.get(),
        )
        if not input[0] or not input[1] or not input[2] or not input[3]:
            messagebox.showwarning("Opgelet", "Voer alstublieft alle velden in.")
            self.month_entry.focus()  # Set focus back to the month entry field
            return

        self.curr.execute(
            "INSERT INTO revenue (month, company, amount, vat) VALUES (?,?,?,?)",
            (input[0], input[1], input[2], input[3]),
        )
        self.conn.commit()

        self.total_revenue()  # Gets the total revenue amount
        self.total_vat()  # Gets the total vat amount

        # clears all input fields
        self.month_entry.delete(0, ttk.END)
        self.company_entry.delete(0, ttk.END)
        self.amount_entry.delete(0, ttk.END)
        self.vat_entry.delete(0, ttk.END)

        self.revenue.destroy()  # Close the revenue window

    # Functions
    def total_revenue(self):
        """Calculates the total revenue from the database and updates the label."""
        self.curr.execute("SELECT SUM(amount) FROM revenue")
        total_amount = self.curr.fetchone()[0]  # Fetch the first value
        if total_amount is None:
            total_amount = 0.0  # Set to 0.0 if no data is found

        self.main_window.revenue_info_lbl.config(
            text=f"Totaal inkomsten: {total_amount:,.2f}€"
        )

    def total_vat(self):
        """Calculates the total VAT from the database and updates the label."""
        self.curr.execute("SELECT SUM(vat) FROM revenue")
        total_vat = self.curr.fetchone()[0]  # Fetch the first value
        if total_vat is None:
            total_vat = 0.0

        self.main_window.vat_info_lbl.config(text=f"Totaal Btw: {total_vat:,.2f}€")

    def close_connection(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    """Main function to run the Revenue class."""
    revenue = ttk.Window()
    style = ttk.Style(theme="superhero")
    app = Revenue(revenue)
    revenue.protocol(
        "WM_DELETE_WINDOW", lambda: (app.close_connection(), revenue.destroy())
    )
    revenue.mainloop()
