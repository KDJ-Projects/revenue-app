"""Revenue input window for entering income data."""

import sqlite3 as sq
from tkinter import messagebox

import ttkbootstrap as ttk  # type: ignore


class Revenue(ttk.Toplevel):
    """This class allows users to input revenue data into a database."""

    def __init__(self, main_window):
        super().__init__()
        self.title("Ingave inkomsten")
        self.main_window = main_window  # Store the MainWindow instance

        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2) - (width // 10)
        y = (self.winfo_screenheight() // 2) - (height // 2) - height
        self.geometry(f"+{x}+{y}")
        self.resizable(False, False)  # Disable resizing

        self.conn = sq.connect("./Database/project.db")  # Database name
        self.curr = self.conn.cursor()  # Create a cursor

        # Create table
        self.curr.execute(
            """CREATE TABLE
            IF NOT EXISTS revenue (
            month TEXT, company TEXT, amount BLOB, tax BLOB)
            """
        )
        self.conn.commit()

        # Create labels for input fields
        self.revenue_labels = {
            "month": ttk.Label(self, text="Maand:"),
            "company": ttk.Label(self, text="Bedrijf:"),
            "amount": ttk.Label(self, text="Bedrag:"),
            "vat": ttk.Label(self, text="Btw:"),
        }
        self.revenue_labels["month"].grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.revenue_labels["company"].grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.revenue_labels["amount"].grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.revenue_labels["vat"].grid(row=3, column=0, padx=5, pady=5, sticky="W")

        # Create input fields
        self.revenue_entries = {
            "month": ttk.Entry(self, width=10),
            "company": ttk.Entry(self, width=10),
            "amount": ttk.Entry(self, width=10),
            "vat": ttk.Entry(self, width=10),
        }
        self.revenue_entries["month"].grid(row=0, column=1, padx=(5, 10), pady=5)
        self.revenue_entries["month"].focus()
        self.revenue_entries["company"].grid(row=1, column=1, padx=(5, 10), pady=5)
        self.revenue_entries["amount"].grid(row=2, column=1, padx=(5, 10), pady=5)
        self.revenue_entries["vat"].grid(row=3, column=1, padx=(5, 10), pady=5)

        # Create buttons for input and search
        self.revenue_buttons = {
            "enter_revenue": ttk.Button(
                self, text="Invoeren", bootstyle="primary", command=self.input_revenue
            ),
            "find_revenue": ttk.Button(
                self, text="Zoek", bootstyle="info", command=self.find_revenue
            ),
        }
        self.revenue_buttons["enter_revenue"].grid(
            row=4, column=0, columnspan=3, pady=10, padx=15, sticky="WE"
        )
        self.revenue_buttons["find_revenue"].grid(
            row=5, column=0, columnspan=3, pady=10, padx=15, sticky="WE"
        )

    # FUNCTIONS
    def input_revenue(self):
        """inserts the input data into the database."""
        input_revenue = (
            self.revenue_entries["month"].get(),
            self.revenue_entries["company"].get(),
            self.revenue_entries["amount"].get(),
            self.revenue_entries["vat"].get(),
        )
        if not all(input_revenue):
            messagebox.showwarning("Opgelet", "Voer alstublieft alle velden in.")
            return

        try:
            self.curr.execute(
                """INSERT INTO revenue (
                    month, company, amount, vat) VALUES (?,?,?,?)""",
                input_revenue,
            )
            self.conn.commit()

            # Fetching the data from MainWindow
            self.update_total_revenue_amount()
            self.update_total_vat_revenue()
            self.update_total_gross_revenue()
            self.update_total_difference_vat_amount()
            self.update_total_nett_revenue_with_rest_vat()
            messagebox.showinfo("Succes", "Inkomsten succesvol ingevoerd.")
        except sq.Error as e:
            messagebox.showerror("Fout", f"Er is een fout opgetreden: {e}")
            return
        finally:
            self.clear_entries()

    def clear_entries(self):
        """function to clear the input fields."""
        self.revenue_entries["month"].delete(0, "end")
        self.revenue_entries["company"].delete(0, "end")
        self.revenue_entries["amount"].delete(0, "end")
        self.revenue_entries["vat"].delete(0, "end")

        self.destroy()  # Close the revenue window

    # FIND FUNCTIONS
    def find_revenue(self):
        """function to find revenue in the database."""
        rev_input = self.revenue_entries["month"].get()

        if not rev_input:
            messagebox.showwarning("Opgelet", "Voer alstublieft een maand in.")
            self.revenue_entries["month"].focus()
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

        self.revenue_entries["month"].delete(0, ttk.END)
        self.revenue_entries["month"].focus()

    # UPDATE FUNCTIONS TO UPDATE THE MAIN WINDOW
    def update_total_revenue_amount(self):
        """fetches the total revenue from the MainWindow."""
        total_revenue_amount = self.main_window.fetch_total_revenue()
        self.main_window.info_labels["revenue_info"].config(
            text=f"Netto Inkomsten: {total_revenue_amount:,.2f}€"
        )

    def update_total_vat_revenue(self):
        """fetches the total VAT from the MainWindow."""
        total_vat_amount = self.main_window.fetch_total_vat_revenue()
        self.main_window.info_labels["vat_info"].config(
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
    revenue = Revenue(main_window=None)
    revenue.protocol(
        "WM_DELETE_WINDOW", lambda: (revenue.close_connection(), revenue.destroy())
    )  # Handle closing window and connection
    revenue.mainloop()
