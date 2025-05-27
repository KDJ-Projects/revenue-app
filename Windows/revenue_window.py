import sqlite3 as sq
from tkinter import messagebox

import ttkbootstrap as ttk


class Revenue(ttk.Toplevel):
    """Class for the revenue input window."""

    def __init__(self, main_window):
        super().__init__()
        """function to initialize the revenue input window."""
        self.title("Ingave inkomsten")
        self.main_window = main_window  # Store the MainWindow instance

        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2) - (width // 10)
        y = (self.winfo_screenheight() // 2) - (height // 2) - height
        self.geometry(f"+{x}+{y}")

        self.conn = sq.connect("project.db")  # Database name
        self.curr = self.conn.cursor()  # Create a cursor

        # Create table
        self.curr.execute(
            """CREATE TABLE
            IF NOT EXISTS revenue (
            month TEXT, company TEXT, amount BLOB, tax BLOB)
            """
        )
        self.conn.commit()

        # Input Date
        self.month_lbl = ttk.Label(self, text="Maand:")
        self.month_entry = ttk.Entry(self, width=10)
        self.month_entry.focus()

        self.month_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.month_entry.grid(row=0, column=1, padx=(5, 10), pady=5)

        # Input Company
        self.company_lbl = ttk.Label(self, text="Bedrijf:")
        self.company_entry = ttk.Entry(self, width=10)

        self.company_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.company_entry.grid(row=1, column=1, padx=(5, 10), pady=5)

        # Input Amount
        self.amount_lbl = ttk.Label(self, text="Bedrag:")
        self.amount_entry = ttk.Entry(self, width=10)

        self.amount_lbl.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.amount_entry.grid(row=2, column=1, padx=(5, 10), pady=5)

        # Input Vat
        self.vat_lbl = ttk.Label(self, text="Btw:")
        self.vat_entry = ttk.Entry(self, width=10)

        self.vat_lbl.grid(row=3, column=0, padx=5, pady=5, sticky="W")
        self.vat_entry.grid(row=3, column=1, padx=(5, 10), pady=5)

        # BUTTONS
        self.enter_revenue_btn = ttk.Button(
            self,
            text="Invoeren",
            bootstyle="success",
            command=self.input_revenue,
        )
        self.enter_revenue_btn.grid(
            row=4, column=0, columnspan=3, pady=10, padx=15, sticky="WE"
        )

        self.find_revenue_btn = ttk.Button(
            self,
            text="Zoek",
            bootstyle="success",
            command=self.find_revenue,
        )
        self.find_revenue_btn.grid(
            row=5, column=0, columnspan=3, pady=10, padx=15, sticky="WE"
        )

    # FUNCTIONS
    def input_revenue(self):
        """inserts the input data into the database."""
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

        # Fetching the data from MainWindow
        self.update_total_revenue_amount()
        self.update_total_vat_revenue()
        self.update_total_gross_revenue()
        self.update_total_difference_vat_amount()
        self.update_total_nett_revenue_with_rest_vat()

        # clears all input fields
        self.month_entry.delete(0, ttk.END)
        self.company_entry.delete(0, ttk.END)
        self.amount_entry.delete(0, ttk.END)
        self.vat_entry.delete(0, ttk.END)

        self.destroy()  # Close the revenue window

    # FIND FUNCTIONS
    def find_revenue(self):
        """function to find revenue in the database."""
        input = self.month_entry.get()

        if not input:
            messagebox.showwarning("Opgelet", "Voer alstublieft een maand in.")
            self.month_entry.focus()
            return
        self.curr.execute("SELECT * FROM revenue WHERE month = ?", (input,))
        result = self.curr.fetchall()

        if not result:
            messagebox.showinfo("Resultaat", "Geen gegevens gevonden.")
        else:
            result_str = "\n".join(
                [
                    (
                        f"Maand: {row[0]}\n"
                        f"Bedrijf: {row[1]}\n"
                        f"Bedrag: {row[2]}€\n"
                        f"Btw: {row[3]}€"
                    )
                    for row in result
                ]
            )
            messagebox.showinfo("Resultaat", result_str)

        self.month_entry.delete(0, ttk.END)
        self.month_entry.focus()
        # self.destroy()  # Close the revenue window

    # UPDATE FUNCTIONS FOR UPDATING MAIN WINDOW
    def update_total_revenue_amount(self):
        """fetches the total revenue from the MainWindow."""
        total_revenue_amount = self.main_window.fetch_total_revenue()
        self.main_window.revenue_info_lbl.config(
            text=f"Netto Inkomsten: {total_revenue_amount:,.2f}€"
        )

    def update_total_vat_revenue(self):
        """fetches the total VAT from the MainWindow."""
        total_vat_amount = self.main_window.fetch_total_vat_revenue()
        self.main_window.vat_info_lbl.config(
            text=f"Btw Inkomsten: {total_vat_amount:,.2f}€"
        )

    def update_total_gross_revenue(self):
        """fetches the gross revenue from the MainWindow."""
        self.main_window.calc_gross_revenue()

    def update_total_difference_vat_amount(self):
        """fetches the difference between income VAT
        and quarter VAT from the MainWindow."""
        self.main_window.calc_diff_vat_amount_vat_paid()

    def update_total_nett_revenue_with_rest_vat(self):
        """fetches the nett revenue with the remaining VAT from the MainWindow."""
        self.main_window.calc_net_revenue_with_rest_vat()

    def close_connection(self):
        """function to close the database connection."""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    """Main function to run the Revenue class."""
    revenue = Revenue()
    revenue.protocol(
        "WM_DELETE_WINDOW", lambda: (revenue.close_connection(), revenue.destroy())
    )  # Close the database connection when the window is closed
    revenue.mainloop()
