import sqlite3 as sq
import ttkbootstrap as ttk
from tkinter import messagebox


class SocialSecurity(ttk.Toplevel):
    """Class for the social security input window."""

    def __init__(self, main_window):
        super().__init__()
        """function to initialize the social security input window."""
        self.title("Ingave Sociale Zekerheid")
        self.main_window = main_window  # Store the MainWindow instance

        self.conn = sq.connect("project.db")  # Database name
        self.curr = self.conn.cursor()  # Create a cursor

        # Create table
        self.curr.execute(
            """CREATE TABLE IF NOT EXISTS social (quarter TEXT, amount BLOB)"""
        )
        self.conn.commit()

        # Input Month
        self.quarter_lbl = ttk.Label(self, text="Kwartaal:")
        self.quarter_entry = ttk.Entry(self, width=10)
        self.quarter_entry.focus()

        self.quarter_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.quarter_entry.grid(row=0, column=1, padx=(5, 10), pady=5)

        # Input Amount
        self.amount_lbl = ttk.Label(self, text="Bedrag:")
        self.amount_entry = ttk.Entry(self, width=10)

        self.amount_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.amount_entry.grid(row=1, column=1, padx=(5, 10), pady=5)

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
        input = (self.quarter_entry.get(), self.amount_entry.get())

        if not input[0] or not input[1]:
            messagebox.showerror("Opgelet", "Vul alstublieft alle velden in.")
            self.quarter_entry.focus()
            return
        self.curr.execute(
            """INSERT INTO social (quarter, amount) VALUES (?, ?)""",
            (input[0], input[1]),
        )
        self.conn.commit()

        self.update_social_security()  # call the function to update the social security data in the main window
        self.destroy()  # Close the social security window

    # UPDATE FUNCTIONS FOR UPDATING MAIN WINDOW
    def update_social_security(self):
        """fetch the total social security from the database and update the main window."""
        self.main_window.fetch_total_social_security()
        self.main_window.calc_net_revenue_with_rest_vat()

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    """Main function to test the SocialSecurity class."""
    SocialSecurity = SocialSecurity()
    SocialSecurity.protocol(
        "WM_DELETE_WINDOW",
        lambda: SocialSecurity.close_connection(),
        SocialSecurity.destroy(),
    )  # Close the database connection when the window is closed
    SocialSecurity.mainloop()
