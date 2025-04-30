import sqlite3 as sq
import ttkbootstrap as ttk


class MainWindow:
    """Main window class for KDJ-Projects."""

    def __init__(self, parent):
        """function to initialize the main window."""
        self.parent = parent
        self.parent.title("KDJ - Projects")

        # Database
        self.conn = sq.connect("KDJ-Projects.db")
        self.curr = self.conn.cursor()

        # Frames
        self.button_frm = ttk.Frame(parent)
        self.button_frm.grid(row=0, column=0, padx=5, pady=10)

        self.info_frm = ttk.Frame(parent)
        self.info_frm.grid(row=0, column=1, padx=5, pady=10)

        # Button frame itmes
        self.revenue_btn = ttk.Button(
            self.button_frm,
            text="Inkomsten",
            width=10,
            bootstyle="success",
            command=self.rev_input,
        )
        self.revenue_btn.grid(row=0, column=0, padx=10, pady=5, sticky="W")

        self.vat_btn = ttk.Button(
            self.button_frm,
            text="Btw Ingave",
            width=10,
            bootstyle="success",
            command=self.vat_input,
        )
        self.vat_btn.grid(row=1, column=0, padx=10, pady=5, sticky="W")

        # Info frame items
        self.revenue_info_lbl = ttk.Label(self.info_frm, text="")
        self.revenue_info_lbl.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.vat_info_lbl = ttk.Label(self.info_frm, text="")
        self.vat_info_lbl.grid(row=1, column=0, padx=5, pady=5, sticky="W")

        self.quarter_vat_info_lbl = ttk.Label(self.info_frm, text="")
        self.quarter_vat_info_lbl.grid(row=2, column=0, padx=5, pady=5, sticky="W")

        # Fetch data for info frame
        self.fetch_total_revenue()
        self.fetch_total_vat()
        self.fetch_total_quarter_vat()

    # Functions
    def rev_input(self):
        """function to open the revenue input window."""
        from Windows.revenue_window import Revenue

        Revenue(self)

    def vat_input(self):
        """function to open the vat input window."""
        from Windows.vat_window import Vat

        Vat(self)

    def fetch_total_revenue(self):
        """function to fetch the total revenue from the database."""
        self.curr.execute("SELECT SUM(amount) FROM revenue")
        total_revenue = self.curr.fetchone()[0]  # Fetch the first value
        if total_revenue is None:
            total_revenue = 0.0

        self.revenue_info_lbl.config(text=f"Totaal inkomsten: {total_revenue:,.2f}€")

    def fetch_total_vat(self):
        """function to fetch the total vat from the database."""
        self.curr.execute("SELECT SUM(vat) FROM revenue")
        total_vat = self.curr.fetchone()[0]  # Fetch the first value
        if total_vat is None:
            total_vat = 0.0

        self.vat_info_lbl.config(text=f"Totaal Btw: {total_vat:,.2f}€")

    def fetch_total_quarter_vat(self):
        """function to fetch the total quarterly VAT from the database."""
        self.curr.execute("SELECT SUM(vat_amount) FROM vat")
        total_quarter_vat = self.curr.fetchone()[0]  # Fetch the first value
        if total_quarter_vat is None:
            total_quarter_vat = 0.0

        self.quarter_vat_info_lbl.config(
            text=f"Totaal Kwartaal Ingave: {total_quarter_vat:,.2f}€"
        )


if __name__ == "__main__":
    """Main function to run the application."""
    parent = ttk.Window()
    parent.geometry("+430+280")
    style = ttk.Style(theme="superhero")
    app = MainWindow(parent)
    parent.mainloop()
