"""This module contains the SocialSecurity class, which is a popup window"""

import sqlite3 as sq
from tkinter import messagebox

import ttkbootstrap as ttk  # type: ignore


class SocialSecurity(ttk.Toplevel):
    """Class for the social security input window."""

    def __init__(self, main_window):
        super().__init__()
        self.title("Ingave Sociale Zekerheid")
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
            """CREATE TABLE IF NOT EXISTS social (quarter TEXT, amount BLOB)"""
        )
        self.conn.commit()

        self.social_labels = {
            "quarter": ttk.Label(self, text="Kwartaal:"),
            "amount": ttk.Label(self, text="Bedrag:"),
        }
        self.social_labels["quarter"].grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.social_labels["amount"].grid(row=1, column=0, padx=5, pady=5, sticky="W")

        self.social_entries = {
            "quarter": ttk.Entry(self, width=10),
            "amount": ttk.Entry(self, width=10),
        }
        self.social_entries["quarter"].grid(row=0, column=1, padx=(5, 10), pady=5)
        self.social_entries["quarter"].focus()
        self.social_entries["amount"].grid(row=1, column=1, padx=(5, 10), pady=5)

        # BUTTONS
        self.enter_social_security_btn = ttk.Button(
            self,
            text="Invoeren",
            bootstyle="success",
            command=self.input_social_security,
        )
        self.enter_social_security_btn.grid(
            row=2, column=0, columnspan=3, padx=15, pady=10, sticky="WE"
        )

    # INPUT FUNCTIONS
    def input_social_security(self):
        """function to input the social security data into the database."""
        input_social = (
            self.social_entries["quarter"].get(),
            self.social_entries["amount"].get(),
        )

        if not all(input_social):
            messagebox.showerror("Opgelet", "Vul alstublieft alle velden in.")
            self.social_entries["quarter"].focus()  # Focus on the first empty field
            return
        try:
            self.curr.execute(
                """INSERT INTO social (quarter, amount) VALUES (?, ?)""",
                input_social,
            )
            self.conn.commit()

            self.update_social_security()  # Update data in the main window
            messagebox.showinfo(
                "Succes", "De sociale zekerheid is succesvol ingevoerd."
            )
        except sq.Error as e:
            messagebox.showerror("Fout", f"Er is een fout opgetreden: {e}")
        finally:
            self.clear_entries()  # Clear the input fields after successful entry
            self.social_entries[
                "quarter"
            ].focus()  # Set focus back to the quarter entry field

    def clear_entries(self):
        """function to clear the input fields."""
        self.social_entries["quarter"].delete(0, "end")
        self.social_entries["amount"].delete(0, "end")
        self.social_entries["quarter"].focus()

    # UPDATE FUNCTIONS FOR UPDATING MAIN WINDOW
    def update_social_security(self):
        """fetch the total social security from the
        database and update the main window."""
        self.main_window.fetch_total_social_security()
        self.main_window.calc_net_revenue_with_rest_vat()

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    social = SocialSecurity(main_window=None)
    social.protocol(
        "WM_DELETE_WINDOW", lambda: (social.close_connection(), social.destroy())
    )  # Handle closing window and connection
    social.mainloop()
