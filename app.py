#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "ttkbootstrap",
# ]
# ///

import sqlite3 as sq

import ttkbootstrap as ttk


class MainWindow(ttk.Window):
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

        # DATABASE
        self.conn = sq.connect("project.db")
        self.curr = self.conn.cursor()

        # MAIN WINDOW
        # Creating frames
        self.total_frame = ttk.Frame(self)
        self.button_frame = ttk.Frame(self)
        self.info_frame = ttk.Frame(self)

        # Layout frames
        self.total_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.button_frame.grid(row=1, column=0, padx=10, pady=10)
        self.info_frame.grid(row=1, column=1, padx=5, pady=10)

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

        # Create button frame items
        self.revenue_btn = ttk.Button(
            master=self.button_frame,
            text="Inkomsten Ingave",
            width=14,
            bootstyle="success",
            command=self.rev_input,
        )

        self.vat_btn = ttk.Button(
            master=self.button_frame,
            text="Btw Ingave",
            width=14,
            bootstyle="success",
            command=self.vat_input,
        )

        self.social_security_btn = ttk.Button(
            master=self.button_frame,
            text="RSZ Ingave",
            width=14,
            bootstyle="success",
            command=self.social_input,
        )

        self.overview_revenue_btn = ttk.Button(
            master=self.button_frame,
            text="Overzicht Inkomsten",
            width=14,
            bootstyle="success",
            command=self.show_revenue_overview,
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

        # Fetch and calculate values
        self.fetch_total_revenue()
        self.fetch_total_vat_revenue()
        self.fetch_total_paid_vat()
        self.fetch_total_social_security()

        self.calc_gross_revenue()
        self.calc_diff_vat_amount_vat_paid()
        self.calc_net_revenue_with_rest_vat()

    # INPUT FUNCTIONS
    def rev_input(self):
        """function to open the revenue input window."""
        from Windows.revenue_window import Revenue

        Revenue(self)

    def vat_input(self):
        """function to open the vat input window."""
        from Windows.vat_window import Vat

        Vat(self)

    def social_input(self):
        """function to open the social security input window."""
        from Windows.social_security_window import SocialSecurity

        SocialSecurity(self)

    # OVERVIEW FUNCTIONS
    def show_revenue_overview(self):
        """function to show the revenue overview."""
        from Windows.revenue_overview import RevenueOverview

        RevenueOverview(self)

    # FETCHING DATA FROM DATABASE FUNCTIONS
    def fetch_total_revenue(self):
        """function to fetch the total revenue from the database."""
        self.curr.execute("SELECT SUM(amount) FROM revenue")
        self.total_revenue = self.curr.fetchone()[0]  # Fetch the first value

        if self.total_revenue is None:
            self.total_revenue = 0.0
            return self.total_revenue

        self.revenue_info_lbl.config(
            text=f"{'Netto Inkomsten:':10} {self.total_revenue:>20,.2f}".replace(
                ",", "X"
            )
            .replace(".", ",")
            .replace("X", ".")
            + " €"
        )
        return self.total_revenue

    def fetch_total_vat_revenue(self):
        """function to fetch the total vat from the database."""
        self.curr.execute("SELECT SUM(vat) FROM revenue")
        self.total_vat = self.curr.fetchone()[0]  # Fetch the first value

        if self.total_vat is None:
            self.total_vat = 0.0
            return self.total_vat

        self.vat_info_lbl.config(
            text=f"{'Btw Inkomsten:':<15} {self.total_vat:>20,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
            + " €"
        )
        return self.total_vat

    def fetch_total_paid_vat(self):
        """function to fetch the total quarterly VAT from the database."""
        self.curr.execute("SELECT SUM(vat_amount) FROM vat")
        self.total_quarter_vat = self.curr.fetchone()[0]  # Fetchfirst value

        if self.total_quarter_vat is None:
            self.total_quarter_vat = 0.0
            return self.paid_vat_info_lbl.config(
                text=f"{'Btw betaald:':<16} {self.total_quarter_vat:>20,.2f}".replace(
                    ",", "X"
                )
                .replace(".", ",")
                .replace("X", ".")
                + " €"
            )

        self.paid_vat_info_lbl.config(
            text=f"{'Btw betaald:':<16} {self.total_quarter_vat:>20,.2f}".replace(
                ",", "X"
            )
            .replace(".", ",")
            .replace("X", ".")
            + " €"
        )
        return self.total_quarter_vat

    def fetch_total_social_security(self):
        """function to fetch the total social security from the database."""
        self.curr.execute("SELECT SUM(amount) FROM social")
        self.total_social_security = self.curr.fetchone()[0]

        if self.total_social_security is None:
            self.total_social_security = 0.0
            return self.social_security_lbl.config(
                text=f"{'Sociale Zekerheid:':<10}"
                "{self.total_social_security:>20,.2f}".replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " €"
            )

        self.social_security_lbl.config(
            text=f"{'Sociale Zekerheid:':<10} {self.total_social_security:>20,.2f}".replace(
                ",", "X"
            )
            .replace(".", ",")
            .replace("X", ".")
            + " €"
        )
        return self.total_social_security

    # CALCULATIONS FUNCTIONS
    def calc_gross_revenue(self) -> float:
        """function to fetch the gross revenue from the database."""
        self.gross_revenue = self.fetch_total_revenue() + self.fetch_total_vat_revenue()
        self.gross_revenue_lbl.config(
            text=f"{'Bruto Inkomsten:':<16} {self.gross_revenue:>20,.2f}".replace(
                ",", "X"
            )
            .replace(".", ",")
            .replace("X", ".")
            + " €"
        )
        return self.gross_revenue

    def calc_diff_vat_amount_vat_paid(self):
        """function to fetch the difference between VAT income and quarter VAT."""
        self.total_vat = self.fetch_total_vat_revenue()
        self.total_paid_vat = self.fetch_total_paid_vat()

        if self.total_vat is None:
            self.total_vat = 0.0
        if self.total_paid_vat is None:
            self.total_paid_vat = 0.0

        self.diff_vat = self.total_vat - self.total_paid_vat

        self.diff_vat_info_lbl.config(
            text=f"{'Verschil Btw:':<14} {self.diff_vat:>20,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
            + " €"
        )
        return self.diff_vat

    def calc_net_revenue_with_rest_vat(self):
        """function to fetch the net revenue with the rest vat."""
        self.total_social_security = self.fetch_total_social_security()
        self.net_revenue = self.fetch_total_revenue()
        self.diff_vat = self.calc_diff_vat_amount_vat_paid()
        self.total_vat_revenue = self.fetch_total_vat_revenue()

        self.total_net_revenue_with_rest_vat = self.net_revenue + self.diff_vat

        if self.total_social_security is None:
            self.total_social_security = 0.0
        if self.net_revenue is None:
            self.net_revenue = 0.0
        if self.diff_vat is None:
            self.diff_vat = 0.0
        if self.total_vat_revenue is None:
            self.total_vat_revenue = 0.0

        if self.diff_vat < self.total_vat_revenue:
            self.total_net_revenue_with_rest_vat = (
                self.total_net_revenue_with_rest_vat - self.total_social_security
            )
        else:
            self.total_net_revenue_with_rest_vat = (
                self.net_revenue - self.total_social_security
            )

        self.net_revenue_with_rest_vat_lbl.config(
            text=f"Netto inkomsten: {self.total_net_revenue_with_rest_vat:,.2f}".replace(
                ",", "X"
            )
            .replace(".", ",")
            .replace("X", ".")
            + " €"
        )

        return self.total_net_revenue_with_rest_vat


if __name__ == "__main__":
    """Main function to run the application."""
    app = MainWindow()
    style = ttk.Style(theme="superhero")
    app.mainloop()
