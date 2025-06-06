"""Calculations for revenue, VAT, and net revenue with rest VAT."""

from typing import Any, cast


# pylint: disable=no-member
# pylint: disable=too-many-instance-attributes
class Calculations:
    """Class to perform calculations related to revenue, VAT, and net revenue."""

    def __init__(self):
        self.gross_revenue = 0.0
        self.total_vat = 0.0
        self.total_paid_vat = 0.0
        self.diff_vat = 0.0
        self.total_social_security = 0.0
        self.net_revenue = 0.0
        self.total_vat_revenue = 0.0
        self.total_net_revenue_with_rest_vat = 0.0

    def calc_gross_revenue(self) -> float:
        """function to fetch the gross revenue from the database."""
        main_window = cast(Any, self)
        main_window.gross_revenue = (
            main_window.fetch_total_revenue() + main_window.fetch_total_vat_revenue()
        )
        main_window.info_labels["gross_revenue_info"].config(
            text=f"{'Bruto Inkomsten:':<16} {main_window.gross_revenue:>20,.2f}".replace(
                ",", "X"
            )
            .replace(".", ",")
            .replace("X", ".")
            + " €"
        )
        return main_window.gross_revenue

    def calc_diff_vat_amount_vat_paid(self) -> float:
        """function to fetch the difference between VAT income and quarter VAT."""
        main_window = cast(Any, self)
        main_window.total_vat = main_window.fetch_total_vat_revenue()
        main_window.total_paid_vat = main_window.fetch_total_paid_vat()

        if main_window.total_vat is None:
            main_window.total_vat = 0.0
        if main_window.total_paid_vat is None:
            main_window.total_paid_vat = 0.0

        main_window.diff_vat = main_window.total_vat - main_window.total_paid_vat
        # fmt: off
        main_window.info_labels["diff_vat_info"].config(
            text=f"{'Verschil Btw:':<10} {main_window.diff_vat:>20,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
            + " €"
        )
        # fmt: on
        return main_window.diff_vat

    def calc_net_revenue_with_rest_vat(self) -> float:
        """function to fetch the net revenue with the rest vat."""
        main_window = cast(Any, self)
        main_window.total_social_security = main_window.fetch_total_social_security()
        main_window.net_revenue = main_window.fetch_total_revenue()
        main_window.diff_vat = main_window.calc_diff_vat_amount_vat_paid()
        main_window.total_vat_revenue = main_window.fetch_total_vat_revenue()

        main_window.total_net_revenue_with_rest_vat = (
            main_window.net_revenue + main_window.diff_vat
        )

        if main_window.total_social_security is None:
            main_window.total_social_security = 0.0
        if main_window.net_revenue is None:
            main_window.net_revenue = 0.0
        if main_window.diff_vat is None:
            main_window.diff_vat = 0.0
        if main_window.total_vat_revenue is None:
            main_window.total_vat_revenue = 0.0

        if main_window.diff_vat < main_window.total_vat_revenue:
            main_window.total_net_revenue_with_rest_vat = (
                main_window.total_net_revenue_with_rest_vat
                - main_window.total_social_security
            )
        else:
            main_window.total_net_revenue_with_rest_vat = (
                main_window.net_revenue - main_window.total_social_security
            )
        # fmt: off
        main_window.net_revenue_with_rest_vat_lbl.config(
            text=f"Netto inkomsten: {main_window.total_net_revenue_with_rest_vat:,.2f}"
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
                + " €"
        )
        # fmt: on
        return main_window.total_net_revenue_with_rest_vat
