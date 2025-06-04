#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "ttkbootstrap",
# ]
# ///

import sqlite3 as sq

import ttkbootstrap as ttk

from Database.revenue_calculations import Calculations


class MainWindow(ttk.Window, Calculations):
    """Main window class for KDJ-Projects."""

    def __init__(self):
        super().__init__()
        """function to initialize the main window."""
        self.title("KDJ - Projects")

        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2) - width
        y = (self.winfo_screenheight() // 2) - (height // 2) - height
        self.geometry(f"+{x}+{y}")
        self.resizable(False, False)  # Disable resizing

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # DATABASE
        self.conn = sq.connect("./Database/project.db")
        self.curr = self.conn.cursor()

        # MAIN WINDOW
        # Creating frames
        self.total_frame = ttk.Frame(self)
        self.info_frame = ttk.Frame(self)

        # Creating panels
        self.button_panel = ttk.Frame(self)

        # Layout frames
        self.total_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.info_frame.grid(row=1, column=1, padx=5, pady=10)

        # Layout panels
        self.button_panel.grid(row=1, column=0, padx=10, pady=10)

        # Top total income label
        self.net_revenue_with_rest_vat_lbl = ttk.Label(
            master=self.total_frame,
            text="",
            bootstyle="success",
            font=("Helvetica", 20, "bold"),
        )
        self.net_revenue_with_rest_vat_lbl.grid(
            row=0, column=0, columnspan=3, padx=5, pady=5, sticky="N"
        )

        # Create button panel items
        self.revenue_btn = ttk.Button(
            master=self.button_panel,
            text="Inkomsten Ingave",
            width=14,
            bootstyle="success",
            command=self.rev_input,
        )

        self.vat_btn = ttk.Button(
            master=self.button_panel,
            text="Btw Ingave",
            width=14,
            bootstyle="success",
            command=self.vat_input,
        )

        self.social_security_btn = ttk.Button(
            master=self.button_panel,
            text="RSZ Ingave",
            width=14,
            bootstyle="success",
            command=self.social_input,
        )

        self.overview_revenue_btn = ttk.Button(
            master=self.button_panel,
            text="Overzicht Inkomsten",
            width=14,
            bootstyle="success",
            command=self.show_revenue_overview,
        )

        self.expense_btn = ttk.Button(
            master=self.button_panel,
            text="Uitgaven Ingave",
            width=14,
            bootstyle="success",
            command=self.expense_input,
        )

        # Layout for button frame items
        self.revenue_btn.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            ipady=10,
            sticky="W",
        )

        self.vat_btn.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            ipady=10,
            sticky="W",
        )

        self.social_security_btn.grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            ipady=10,
            sticky="W",
        )

        self.overview_revenue_btn.grid(
            row=3,
            column=0,
            padx=10,
            pady=5,
            ipady=10,
            sticky="W",
        )

        self.expense_btn.grid(
            row=4,
            column=0,
            padx=10,
            pady=5,
            ipady=10,
            sticky="W",
        )

        # Info frame items
        self.gross_revenue_lbl = ttk.Label(
            master=self.info_frame,
            text="Bruto Inkomsten: €",
            bootstyle="primary",
            font=("Arial", 12, "bold"),
        )
        self.revenue_info_lbl = ttk.Label(
            master=self.info_frame,
            text="",
            bootstyle="primary",
            font=("Arial", 12, "bold"),
        )
        self.vat_info_lbl = ttk.Label(
            master=self.info_frame,
            text="",
            bootstyle="primary",
            font=("Arial", 12, "bold"),
        )
        self.seprator = ttk.Separator(
            master=self.info_frame,
            orient="horizontal",
            bootstyle="primary",
        )
        self.paid_vat_info_lbl = ttk.Label(
            master=self.info_frame,
            text="",
            bootstyle="primary",
            font=("Arial", 12, "bold"),
        )
        self.diff_vat_info_lbl = ttk.Label(
            master=self.info_frame,
            text="",
            bootstyle="primary",
            font=("Arial", 12, "bold"),
        )
        self.social_security_lbl = ttk.Label(
            master=self.info_frame,
            text="",
            bootstyle="primary",
            font=("Arial", 12, "bold"),
        )

        # Layout info frame items
        self.gross_revenue_lbl.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="E",
        )
        self.revenue_info_lbl.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="E",
        )
        self.vat_info_lbl.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky="E",
        )
        self.seprator.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky="EW",
        )
        self.paid_vat_info_lbl.grid(
            row=4,
            column=0,
            padx=5,
            pady=5,
            sticky="E",
        )
        self.diff_vat_info_lbl.grid(
            row=5,
            column=0,
            padx=5,
            pady=5,
            sticky="E",
        )
        self.social_security_lbl.grid(
            row=6,
            column=0,
            padx=5,
            pady=5,
            sticky="E",
        )

        # Fetch Values
        self.fetch_total_revenue()
        self.fetch_total_vat_revenue()
        self.fetch_total_paid_vat()
        self.fetch_total_social_security()

        # Calculate Values
        Calculations.calc_gross_revenue(self)
        Calculations.calc_diff_vat_amount_vat_paid(self)
        Calculations.calc_net_revenue_with_rest_vat(self)
        Calculations.calc_diff_vat_amount_vat_paid(self)

    # INPUT FUNCTIONS
    def rev_input(self):
        """function to open the revenue input window."""
        from PopupWindows.revenue_window import Revenue

        Revenue(self)

    def vat_input(self):
        """function to open the vat input window."""
        from PopupWindows.vat_window import Vat

        Vat(self)

    def social_input(self):
        """function to open the social security input window."""
        from PopupWindows.social_security_window import SocialSecurity

        SocialSecurity(self)

    def expense_input(self):
        """function to open the expense input window."""
        from PopupWindows.expenses_window import Expenses

        Expenses(self)

    # OVERVIEW FUNCTIONS
    def show_revenue_overview(self):
        """function to show the revenue overview."""
        from PopupWindows.revenue_overview_window import RevenueOverview

        RevenueOverview(self)

    # FETCHING DATA FROM DATABASE FUNCTIONS
    def fetch_total_revenue(self):
        """function to fetch the total revenue from the database."""
        self.curr.execute("SELECT SUM(amount) FROM revenue")
        self.total_revenue = self.curr.fetchone()[0]  # Fetch the first value

        if self.total_revenue is None:
            self.total_revenue = 0.0
            return self.total_revenue

        # fmt: off
        self.revenue_info_lbl.config(
            text=f"{'Netto Inkomsten:':10} {self.total_revenue:>20,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " €"
        )
        # fmt: on
        return self.total_revenue

    def fetch_total_vat_revenue(self):
        """function to fetch the total vat from the database."""
        self.curr.execute("SELECT SUM(vat) FROM revenue")
        self.total_vat = self.curr.fetchone()[0]  # Fetch the first value

        if self.total_vat is None:
            self.total_vat = 0.0
            return self.total_vat
        # fmt: off
        self.vat_info_lbl.config(
            text=f"{'Btw Inkomsten:':<15} {self.total_vat:>20,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " €"
        )

        return self.total_vat

    def fetch_total_paid_vat(self):
        """function to fetch the total quarterly VAT from the database."""
        self.curr.execute("SELECT SUM(vat_amount) FROM vat")
        self.total_quarter_vat = self.curr.fetchone()[0]  # Fetchfirst value
        # fmt: off
        if self.total_quarter_vat is None:
            self.total_quarter_vat = 0.0
            return self.paid_vat_info_lbl.config(
                text=f"{'Btw betaald:':<16} {self.total_quarter_vat:>20,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                    + " €"
            )

        self.paid_vat_info_lbl.config(
            text=f"{'Btw betaald:':<10} {self.total_quarter_vat:>20,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " €"
        )
        # fmt: on
        return self.total_quarter_vat

    def fetch_total_social_security(self):
        """function to fetch the total social security from the database."""
        self.curr.execute("SELECT SUM(amount) FROM social")
        self.total_social_security = self.curr.fetchone()[0]

        # fmt: off
        if self.total_social_security is None:
            self.total_social_security = 0.0
            return self.social_security_lbl.config(
                text=f"{'Sociale Zekerheid:':<10} {self.total_social_security:>20,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                    + " €"
            )

        self.social_security_lbl.config(
            text=f"{'Sociale Zekerheid:':<10} {self.total_social_security:>20,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " €"
        )
        # fmt: on
        return self.total_social_security


if __name__ == "__main__":
    """Main function to run the application."""
    app = MainWindow()
    style = ttk.Style(theme="superhero")
    # style = ttk.Style(theme="morph")
    app.mainloop()
