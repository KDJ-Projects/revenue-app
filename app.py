#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "customtkinter",
# ]
# ///


"""
Application for managing projects, revenue, expenses, and social security contributions.
"""

import sqlite3 as sq

import customtkinter as ctk  # type: ignore

from Calculations.revenue_calculations import Calculations
from PopupWindows.expenses_window import Expenses
from PopupWindows.revenue_overview_window import RevenueOverview
from PopupWindows.revenue_window import Revenue
from PopupWindows.social_security_window import SocialSecurity
from PopupWindows.vat_window import Vat


# pylint: disable=too-many-instance-attributes
class MainWindow(ctk.CTk, Calculations):
    """Main window class for KDJ-Projects."""

    def __init__(self) -> None:
        """function to initialize the main window."""
        super().__init__()
        self.setup_window()
        self.setup_database()
        self.create_frames()

        # Fetching Data from Database
        self.fetch_total_revenue()
        self.fetch_total_vat_revenue()
        self.fetch_total_paid_vat()
        self.fetch_total_social_security()

        # Calculate Values
        Calculations.calc_gross_revenue(self)
        Calculations.calc_diff_vat_amount_vat_paid(self)
        Calculations.calc_net_revenue_with_rest_vat(self)
        Calculations.calc_diff_vat_amount_vat_paid(self)

    def setup_window(self) -> None:
        """function to set up the main window."""
        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2) - width
        y = (self.winfo_screenheight() // 2) - (height // 2) - height
        self.title("KDJ - Projects")
        self.geometry(f"+{x}+{y}")
        self.resizable(False, False)  # Disable resizing

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    def setup_database(self) -> None:
        """function to set up the database connection."""
        # DATABASE
        self.conn = sq.connect("./Database/project.db")
        self.curr = self.conn.cursor()

    def create_frames(self) -> None:
        """function to create the main window layout."""
        self.main_win_fr = {
            "total": ctk.CTkFrame(self),
            "info": ctk.CTkFrame(self),
            "button": ctk.CTkFrame(self),
        }
        # Layout frames in main window
        self.main_win_fr["total"].grid(
            row=0, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW"
        )
        self.main_win_fr["button"].grid(
            row=1, column=0, padx=(10, 5), pady=10, sticky="NSEW"
        )
        self.main_win_fr["info"].grid(
            row=1, column=1, padx=(5, 10), pady=10, sticky="NSEW"
        )

        # configure frames in main window
        self.main_win_fr["total"].configure(border_width=2)
        self.main_win_fr["info"].configure(border_width=2)
        self.main_win_fr["button"].configure(border_width=2)

        # Grid configuration for frames in main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Top total net income label with rest VAT
        self.main_win_fr["total"].columnconfigure(0, weight=1)
        self.net_revenue_with_rest_vat_lbl = ctk.CTkLabel(
            master=self.main_win_fr["total"],
            text="",
            font=("Helvetica", 24, "bold"),
            text_color="#708A58",
        )
        self.net_revenue_with_rest_vat_lbl.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky="WE"
        )

        # Create buttons in the info frames
        self.info_buttons = {
            "revenue_btn": ctk.CTkButton(
                master=self.main_win_fr["button"],
                text="Inkomsten Ingave",
                command=self.rev_input,
            ),
            "vat_btn": ctk.CTkButton(
                master=self.main_win_fr["button"],
                text="Btw Ingave",
                command=self.vat_input,
            ),
            "social_security_btn": ctk.CTkButton(
                master=self.main_win_fr["button"],
                text="RSZ Ingave",
                command=self.social_input,
            ),
            "overview_revenue_btn": ctk.CTkButton(
                master=self.main_win_fr["button"],
                text="Overzicht Inkomsten",
                command=self.show_revenue_overview,
            ),
            "expense_btn": ctk.CTkButton(
                master=self.main_win_fr["button"],
                text="Uitgaven Ingave",
                command=self.expense_input,
            ),
        }

        self.font_btn = ("Arial", 16, "bold")

        # Layout for button frame items
        self.info_buttons["revenue_btn"].grid(
            row=0, column=0, padx=10, pady=5, ipady=10, sticky="NSEW"
        )

        self.info_buttons["vat_btn"].grid(
            row=1, column=0, padx=10, pady=5, ipady=10, sticky="NSEW"
        )

        self.info_buttons["social_security_btn"].grid(
            row=2, column=0, padx=10, pady=5, ipady=10, sticky="NSEW"
        )

        self.info_buttons["overview_revenue_btn"].grid(
            row=3, column=0, padx=10, pady=5, ipady=10, sticky="NSEW"
        )

        self.info_buttons["expense_btn"].grid(
            row=4, column=0, padx=10, pady=5, ipady=10, sticky="NSEW"
        )

        # Configure button styles
        self.info_buttons["revenue_btn"].configure(
            font=self.font_btn, fg_color="green", hover_color="darkgreen"
        )
        self.info_buttons["vat_btn"].configure(
            font=self.font_btn, fg_color="green", hover_color="darkgreen"
        )
        self.info_buttons["social_security_btn"].configure(
            font=self.font_btn, fg_color="green", hover_color="darkgreen"
        )
        self.info_buttons["overview_revenue_btn"].configure(
            font=self.font_btn, fg_color="green", hover_color="darkgreen"
        )
        self.info_buttons["expense_btn"].configure(
            font=self.font_btn, fg_color="green", hover_color="darkgreen"
        )

        # Create info labels in the info frames
        self.info_labels = {
            "gross_revenue_info": ctk.CTkLabel(
                master=self.main_win_fr["info"],
                text="Bruto Inkomsten: €",
                font=("Arial", 14, "bold"),
            ),
            "revenue_info": ctk.CTkLabel(
                master=self.main_win_fr["info"],
                text="",
                font=("Arial", 14, "bold"),
            ),
            "vat_info": ctk.CTkLabel(
                master=self.main_win_fr["info"],
                text="",
                font=("Arial", 14, "bold"),
            ),
            "paid_vat_info": ctk.CTkLabel(
                master=self.main_win_fr["info"],
                text="",
                font=("Arial", 14, "bold"),
            ),
            "diff_vat_info": ctk.CTkLabel(
                master=self.main_win_fr["info"],
                text="",
                font=("Arial", 14, "bold"),
            ),
            "social_security": ctk.CTkLabel(
                master=self.main_win_fr["info"],
                text="",
                font=("Arial", 14, "bold"),
            ),
        }

        # Layout info frame items
        self.info_labels["gross_revenue_info"].grid(
            row=0, column=0, padx=5, pady=10, sticky="W"
        )
        self.info_labels["revenue_info"].grid(
            row=1, column=0, padx=5, pady=10, sticky="W"
        )
        self.info_labels["vat_info"].grid(row=2, column=0, padx=5, pady=10, sticky="W")

        self.info_labels["paid_vat_info"].grid(
            row=4, column=0, padx=5, pady=10, sticky="W"
        )
        self.info_labels["diff_vat_info"].grid(
            row=5, column=0, padx=5, pady=10, sticky="W"
        )
        self.info_labels["social_security"].grid(
            row=6, column=0, padx=5, pady=10, sticky="W"
        )

    # INPUT FUNCTIONS
    def rev_input(self) -> None:
        """function to open the revenue input window."""
        Revenue(self)

    def vat_input(self) -> None:
        """function to open the vat input window."""
        Vat(self)

    def social_input(self) -> None:
        """function to open the social security input window."""
        SocialSecurity(self)

    def expense_input(self) -> None:
        """function to open the expense input window."""
        Expenses(self)

    # OVERVIEW FUNCTIONS
    def show_revenue_overview(self) -> None:
        """function to show the revenue overview."""
        RevenueOverview(self)

    # FETCHING DATA FROM DATABASE FUNCTIONS
    def fetch_total_revenue(self) -> float:
        """function to fetch the total revenue from the database."""
        self.curr.execute("SELECT SUM(amount) FROM revenue")
        self.total_revenue = self.curr.fetchone()[0]  # Fetch the first value

        if self.total_revenue is None:
            self.total_revenue = 0.0
            return self.total_revenue

        # fmt: off
        self.info_labels["revenue_info"].configure(
            text=f"{'Netto Inkomsten:':10} {self.total_revenue:>20,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
            + " €"
        )
        # fmt: on
        return self.total_revenue

    def fetch_total_vat_revenue(self) -> float:
        """function to fetch the total vat from the database."""
        self.curr.execute("SELECT SUM(vat) FROM revenue")
        self.total_vat = self.curr.fetchone()[0]  # Fetch the first value

        if self.total_vat is None:
            self.total_vat = 0.0
            return self.total_vat
        # fmt: off
        self.info_labels["vat_info"].configure(
            text=f"{'Btw Inkomsten:':<18} {self.total_vat:>20,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " €"
        )

        return self.total_vat

    def fetch_total_paid_vat(self) -> float:
        """function to fetch the total quarterly VAT from the database."""
        self.curr.execute("SELECT SUM(vat_amount) FROM vat")
        self.total_quarter_vat = self.curr.fetchone()[0]  # Fetchfirst value
        # fmt: off
        if self.total_quarter_vat is None:
            self.total_quarter_vat = 0.0
            return self.info_labels["paid_vat_info"].configure(
                text=f"{'Btw betaald:':<21} {self.total_quarter_vat:>20,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " €"
            )

        self.info_labels["paid_vat_info"].configure(
            text=f"{'Btw betaald:':<21} {self.total_quarter_vat:>20,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " €"
        )
        # fmt: on
        return self.total_quarter_vat

    def fetch_total_social_security(self) -> float:
        """function to fetch the total social security from the database."""
        self.curr.execute("SELECT SUM(amount) FROM social")
        self.total_social_security = self.curr.fetchone()[0]

        # fmt: off
        if self.total_social_security is None:
            self.total_social_security = 0.0
            return self.info_labels["social_security"].configure(
                text=f"{'Sociale Zekerheid:':<0} {self.total_social_security:>20,.2f}"
                    .replace(",", "X")
                    .replace(".", ",")
                    .replace("X", ".")
                    + " €"
            )

        self.info_labels["social_security"].configure(
            text=f"{'Sociale Zekerheid:':<0} {self.total_social_security:>20,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " €"
        )
        # fmt: on
        return self.total_social_security


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
