"""This module contains the Vat class, which is a Tkinter Toplevel window"""

import sqlite3 as sq
from tkinter import messagebox

import customtkinter as ctk  # type: ignore


class Vat(ctk.CTkToplevel):
    """Class for the VAT input window."""

    def __init__(self, main_window) -> None:
        super().__init__()
        self.title("Ingave Btw")
        self.main_window = main_window  # Store the MainWindow instance

        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        self.resizable(False, False)  # Disable resizing

        self.conn = sq.connect("./Database/project.db")  # Database name
        self.curr = self.conn.cursor()  # Create a cursor

        # Create table
        self.curr.execute(
            """CREATE TABLE IF NOT EXISTS vat (vat_quarter TEXT, vat_amount BLOB)"""
        )
        self.conn.commit()

        # Create labels for input fields
        self.vat_labels = {
            "quarter": ctk.CTkLabel(self, text="Kwartaal"),
            "vat": ctk.CTkLabel(self, text="Btw"),
        }
        self.vat_labels["quarter"].grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.vat_labels["vat"].grid(row=1, column=0, padx=5, pady=5, sticky="W")

        # Create input fields
        self.vat_entries = {
            "quarter": ctk.CTkEntry(self, width=100),
            "vat": ctk.CTkEntry(self, width=100),
        }
        self.vat_entries["quarter"].grid(row=0, column=1, padx=5, pady=5)
        self.vat_entries["quarter"].focus()  # Set focus to the quarter entry field
        self.vat_entries["vat"].grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        self.enter_btn = ctk.CTkButton(self, text="Invoeren", command=self.input_vat)
        self.enter_btn.grid(
            row=2, column=0, columnspan=2, padx=5, pady=10, sticky="NSEW"
        )
        self.enter_btn.columnconfigure(0, weight=1)
        self.enter_btn.configure(
            font=("Arial", 16, "bold"),
            anchor="center",
            fg_color="green",
            hover_color="darkgreen",
        )

    # FUNCTIONS
    def input_vat(self):
        """function to input the VAT data into the database."""
        input_vat = (
            self.vat_entries["quarter"].get(),
            self.vat_entries["vat"].get(),
        )

        if not all(input_vat):
            messagebox.showerror("Opgelet", "Vul alstublieft alle velden in.")
            self.vat_entries[
                "quarter"
            ].focus()  # Set focus back to the quarter entry field
            return

        try:
            self.curr.execute(
                """INSERT INTO vat (vat_quarter, vat_amount) VALUES (?, ?)""",
                input_vat,
            )
            self.conn.commit()

            # Update the MainWindow with the new VAT data
            self.update_total_paid_vat()
            self.update_total_difference_vat_amount()
            self.update_total_net_revenue_with_rest_vat()
            messagebox.showinfo("Succes", "Btw is succesvol ingevoerd.")
        except sq.Error as e:
            messagebox.showerror("Database Error", f"Er is een fout opgetreden: {e}")
            return
        finally:
            self.clear_entries()

    def clear_entries(self):
        """function to clear the input fields."""
        self.vat_entries["quarter"].delete(0, "end")
        self.vat_entries["vat"].delete(0, "end")

    # UPDATE FUNCTIONS FOR UPDATING MAIN WINDOW
    def update_total_paid_vat(self):
        """fetches the total VAT amount for the quarter from the MainWindow."""
        self.curr.execute("""SELECT SUM(vat_amount) FROM vat""")
        total_quarter_vat = self.curr.fetchone()[0]  # Fetch the first value
        if total_quarter_vat is None:
            total_quarter_vat = 0.0

        self.main_window.info_labels["paid_vat_info"].config(
            text=f"Btw Kwartaal: {total_quarter_vat:,.2f}€"
        )

    def update_total_difference_vat_amount(self):
        """
        fetches the difference between the VAT income
        and quarter VAT from the MainWindow.
        """
        self.main_window.calc_diff_vat_amount_vat_paid()

    def update_total_net_revenue_with_rest_vat(self):
        """fetches the net revenue with the remaining VAT from the MainWindow."""
        self.main_window.calc_net_revenue_with_rest_vat()

    def close_connection(self):
        """function to close the database connection."""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # For testing purposes, pass None as main_window
    vat = Vat(main_window=None)
    vat.protocol(
        "WM_DELETE_WINDOW", lambda: (vat.close_connection(), vat.destroy())
    )  # Handle closing window and connection
    vat.mainloop()
