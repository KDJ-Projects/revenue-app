"""Revenue Overview Window for displaying revenue data in a Treeview."""

import sqlite3 as sq

import ttkbootstrap as ttk  # type: ignore


class RevenueOverview(ttk.Toplevel):
    """Class for the Revenue Overview window, displaying revenue data in a Treeview."""

    def __init__(self, main_window=None):
        super().__init__()
        self.title("Overzicht Inkomsten")
        self.main_window = main_window  # Store the MainWindow instance

        # Center the window on the screen
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2) - (width // 10)
        y = (self.winfo_screenheight() // 2) - (height // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")
        self.resizable(False, False)  # Disable resizing

        self.conn = sq.connect("./Database/project.db")
        self.curr = self.conn.cursor()

        # Fetch data first to determine height
        self.rows = self.fetch_revenue_overview()
        self.tree_height = max(5, len(self.rows))  # Minimum 5 rows for aesthetics

        # Create a style for the Treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # Create a Treeview widget
        self.tree = ttk.Treeview(
            self,
            columns=("Maand", "Bedrijf", "Bedrag"),
            show="headings",
            height=self.tree_height,
            bootstyle="dark",
            selectmode="browse",
            style="Treeview",
        )
        self.tree.column("Maand", anchor="center", width=100, stretch=True)
        self.tree.column("Bedrijf", anchor="center", width=100, stretch=True)
        self.tree.column("Bedrag", anchor="center", width=90, stretch=True)

        self.tree.heading("Maand", text="Maand", anchor="center")
        self.tree.heading("Bedrijf", text="Bedrijf", anchor="center")
        self.tree.heading("Bedrag", text="Bedrag", anchor="center")
        self.tree.pack(fill=ttk.BOTH, expand=True)

        # Populate the list view with data
        self.populate_list_view()

    def fetch_revenue_overview(self):
        """Fetch revenue data from the database."""
        self.curr.execute("SELECT month, company, amount FROM revenue")
        rows = self.curr.fetchall()
        return rows

    def populate_list_view(self):
        """Populate the Treeview with revenue data."""
        for row in self.fetch_revenue_overview():
            maand, bedrijf, bedrag = row
            bedrag = float(bedrag)
            bedrag_met_euro = (
                f"{bedrag:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                + " €"
            )
            self.tree.insert("", ttk.END, values=(maand, bedrijf, bedrag_met_euro))

    def close_connection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    revenue_overview = RevenueOverview()
    revenue_overview.protocol(
        "WM_DELETE_WINDOW",
        lambda: (revenue_overview.close_connection(), revenue_overview.destroy()),
    )  # close the connection and destroy the window
    revenue_overview.mainloop()
