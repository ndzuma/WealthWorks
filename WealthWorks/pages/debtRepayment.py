import reflex as rx

from typing import List, Dict, Any
from WealthWorks.components import basic
from WealthWorks.workers.debtRepaymentCalculator import calculate_repayment, priority_payment


# State
class DebtState(rx.State):
    resources: list
    debts: list
    previousDebts: List[Dict[str, Any]]
    repaymentBalanceState: str
    minimumPaymentState: str
    interestRateState: str
    extraMonthlyPaymentState: str

    # Inputs
    name: str
    repaymentBalance: float
    minimumPayment: float
    interestRate: float
    extraMonthlyPayment: float
    inputState: str

    # Outputs
    months: int
    monthlyPayment: float
    priority: str
    totalPaid: float
    totalInterestPaid: float
    yearMonth: list

    def __init__(self, *args, **kwargs):
        # Initialize state
        super().__init__(*args, **kwargs)
        self.name = ""
        self.repaymentBalance = 0
        self.minimumPayment = 0
        self.interestRate = 0
        self.extraMonthlyPayment = 0
        self.months = 0
        self.monthlyPayment = 0
        self.priority = ""
        self.totalPaid = 0
        self.totalInterestPaid = 0
        self.resources = [{"name": "Principal", "value": 100}, {"name": "Interest", "value": 0}]
        self.debts = []
        self.previousDebts = []
        self.yearMonth = [0, 0]
        self.repaymentBalanceState = ""
        self.minimumPaymentState = ""
        self.interestRateState = ""
        self.extraMonthlyPaymentState = ""

    # Setters
    @staticmethod
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def set_extraMonthlyPayment(self, value: float):
        if self.is_float(value):
            self.extraMonthlyPayment = float(value)
            self.extraMonthlyPaymentState = f"{value}"

    def set_repaymentBalance(self, value: float):
        if self.is_float(value):
            self.repaymentBalance = float(value)
            self.repaymentBalanceState = f"{value}"

    def set_minimumPayment(self, value: float):
        if self.is_float(value):
            self.minimumPayment = float(value)
            self.minimumPaymentState = f"{value}"

    def set_interestRate(self, value: float):
        if self.is_float(value):
            self.interestRate = float(value)
            self.interestRateState = f"{value}"

    def add_debts(self):
        """
        Add the debts to the state from values already in the state
        """
        if not self.name == "" and not self.repaymentBalance == 0 and not self.minimumPayment == 0 and not self.interestRate == 0:
            # Add the debt to the list
            self.debts.append({"name": self.name, "amount": self.repaymentBalance, "interest_rate": self.interestRate, "min_payment": self.minimumPayment})

            # Clear the inputs
            self.name = ""
            self.repaymentBalance = 0
            self.minimumPayment = 0
            self.interestRate = 0

            # Clear the "state" inputs, so that the input fields are cleared
            self.repaymentBalanceState = ""
            self.minimumPaymentState = ""
            self.interestRateState = ""

    @staticmethod
    def convert_to_years(months: int):
        """
        Convert months to years and months
        :param months: Number of months
        :return: Years, Months
        """
        years = months // 12
        months = months % 12
        return [years, months]

    def save_debts(self):
        """
        Save the debts to the previous debts list, for future reference
        :return:
        """
        self.previousDebts = []
        dictionary = {"name": "", "amount": 0, "min_payment": 0, "interest_rate": 0}
        for i in self.debts:
            dictionary["name"] = i["name"]
            dictionary["amount"] = i["amount"]
            dictionary["min_payment"] = i["min_payment"]
            dictionary["interest_rate"] = i["interest_rate"]
            self.previousDebts.append(dictionary.copy())

    def calculate_repayment(self):
        """
        Calculate the debt repayment and priority payment, and set the results to the state
        """
        if len(self.debts) > 0:
            self.save_debts()
            # Calculate the repayment
            results = calculate_repayment(debts=self.debts, extra_payment=self.extraMonthlyPayment)
            # Calculate the priority
            priority = priority_payment(debts=self.debts)

            if results is not None:
                # Set the results
                self.months = results[0]
                self.monthlyPayment = results[1]
                self.totalPaid = results[2]
                self.totalInterestPaid = results[3]
                self.priority = priority
                self.yearMonth = self.convert_to_years(self.months)

                # Update the resources for the graph
                self.resources[0]["value"] = self.totalPaid - self.totalInterestPaid
                self.resources[1]["value"] = self.totalInterestPaid

            # Clearing the debts from memory
            self.debts = []


def graph() -> rx.Component:
    return rx.flex(
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=DebtState.resources,
                data_key="value",
                name_key="name",
                cx="50%",
                cy="50%",
                fill="#4662D5",
                label=True,
            ),
            rx.recharts.graphing_tooltip(),
            min_height=300,
            max_width=500,
            max_height=500
        ),
    )


def debt_input() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.chakra.input(
                value=DebtState.name,
                placeholder="Debt Name",
                on_change=DebtState.set_name,
                is_required=True,
                border_color="#CDCED6",
                size="sm",
                border_radius="8"
            ),
            rx.chakra.input(
                value=DebtState.repaymentBalanceState,
                placeholder="Repayment balance",
                on_change=DebtState.set_repaymentBalance,
                is_required=True,
                border_color="#CDCED6",
                size="sm",
                border_radius="8"
            ),

            justify="start",
            width="100%",
            spacing="2",
        ),
        rx.flex(
            rx.chakra.input(
                value=DebtState.minimumPaymentState,
                placeholder="Minimum payments",
                on_change=DebtState.set_minimumPayment,
                is_required=True,
                border_color="#CDCED6",
                size="sm",
                border_radius="8"
            ),
            rx.chakra.input(
                value=DebtState.interestRateState,
                placeholder="Interest rate in %",
                on_change=DebtState.set_interestRate,
                is_required=True,
                border_color="#CDCED6",
                size="sm",
                border_radius="8"
            ),

            justify="start",
            spacing="2",
        ),
        rx.chakra.button("Add debt",
                         on_click=DebtState.add_debts,
                         bg="#4662D5",
                         color="white",
                         size="sm",
                         border_radius="8"),
        direction="column",
        spacing="2",
    )


def other_input() -> rx.Component:
    return rx.flex(
        rx.flex(
            rx.chakra.input(
                value=DebtState.extraMonthlyPaymentState,
                placeholder="Extra monthly payment",
                on_change=DebtState.set_extraMonthlyPayment,
                is_required=True,
                border_color="#CDCED6",
                size="sm",
                border_radius="8"
            ),
            justify="start",
            width="100%",
            spacing="2",
        ),
        rx.chakra.button("Calculate",
                         on_click=DebtState.calculate_repayment,
                         bg="#4662D5",
                         color="white",
                         size="sm",
                         border_radius="8"),
        direction="column",
        spacing="2",
    )


def debt_summary() -> rx.Component:
    return rx.flex(
        rx.card(
            rx.text("Summary", size="4", weight="medium", align="center"),
            rx.text(
                f"You can pay off your debts in {DebtState.months} months "
                f"({DebtState.yearMonth[0]} years and {DebtState.yearMonth[1]} months). ",
                size="4",
                weight="regular",
                align="center"
            ),
            rx.text(
                f"We recommend you pay off '{DebtState.priority}' first.",
                size="4",
                weight="regular",
                align="center"
            ),
            rx.box(height="10px"),
            width="100%",
        ),
        width="100%"
    )


def debt_summary_table() -> rx.Component:
    return rx.flex(
        rx.card(
            rx.text("Table", size="4", weight="medium", align="center"),
            rx.table.root(
                rx.table.body(
                    rx.table.row(
                        rx.table.cell("Monthly Payment"),
                        rx.table.cell(DebtState.monthlyPayment),
                        align="center",
                    ),
                    rx.table.row(
                        rx.table.cell("Total Paid"),
                        rx.table.cell(DebtState.totalPaid),
                        align="center",
                    ),
                    rx.table.row(
                        rx.table.cell("Total Interest Paid"),
                        rx.table.cell(DebtState.totalInterestPaid),
                        align="center",
                    ),
                ),
            ),
            rx.box(height="10px"),
            width="100%",
        ),
        width="100%"
    )


def get_debt(item) -> rx.Component:
    return rx.table.row(
        rx.table.cell(item["name"]),
        rx.table.cell(item["amount"]),
        rx.table.cell(item["min_payment"]),
        rx.table.cell(item["interest_rate"]),
        align="center"
    )


def debt_table() -> rx.Component:
    return rx.flex(
        rx.card(
            rx.text("Debt Table", size="4", weight="medium", align="center"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Name of debt"),
                        rx.table.column_header_cell("Amount"),
                        rx.table.column_header_cell("Minimum Payment"),
                        rx.table.column_header_cell("Interest Rate"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        DebtState.previousDebts,
                        get_debt
                    )
                ),
            ),
            rx.box(height="10px"),
            width="100%",
        ),
        width="100%"
    )


# Main section
def debt_repayment() -> rx.Component:
    return rx.flex(
        rx.spacer(min_width="10px"),
        rx.flex(
            basic.header("/debt-repayment"),
            graph(),
            debt_input(),
            other_input(),
            debt_summary(),
            debt_summary_table(),
            debt_table(),
            rx.chakra.divider(border_color="lightgrey"),
            basic.footer(),
            rx.box(min_height="10px"),
            direction="column",
            width="100%",
            max_width="50em",
            spacing="5",
        ),
        rx.spacer(min_width="10px"),
        justify="center",
        direction="row",
        width="100vw",
        height="100vh",
    )
