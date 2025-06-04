class Calculations:
    def __init__(self):
        super().__init__()

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

    def calc_diff_vat_amount_vat_paid(self) -> float:
        """function to fetch the difference between VAT income and quarter VAT."""
        self.total_vat = self.fetch_total_vat_revenue()
        self.total_paid_vat = self.fetch_total_paid_vat()

        if self.total_vat is None:
            self.total_vat = 0.0
        if self.total_paid_vat is None:
            self.total_paid_vat = 0.0

        self.diff_vat = self.total_vat - self.total_paid_vat
        # fmt: off
        self.diff_vat_info_lbl.config(
            text=f"{'Verschil Btw:':<10} {self.diff_vat:>20,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
            + " €"
        )
        # fmt: on
        return self.diff_vat

    def calc_net_revenue_with_rest_vat(self) -> float:
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
        # fmt: off
        self.net_revenue_with_rest_vat_lbl.config(
            text=f"Netto inkomsten: {self.total_net_revenue_with_rest_vat:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " €"
        )
        # fmt: on
        return self.total_net_revenue_with_rest_vat


if __name__ == "__main__":
    Calculations()
