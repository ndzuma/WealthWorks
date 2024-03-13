import reflex as rx

from WealthWorks.components import basic
from WealthWorks.workers.debtRepaymentCalculator import calculate_repayment


# State
class DebtState(rx.State):
    resources: list
    debts: list

    # Inputs
    name: str
    repaymentBalance: float
    minimumPayment: float
    interestRate: float
    extraMonthlyPayment: float

    # Outputs
    months: int
    monthlyPayment: float
    priority: str
    totalPaid: float
    totalInterestPaid: float

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

    def set_repaymentBalance(self, value: float):
        if self.is_float(value):
            self.repaymentBalance = float(value)

    def set_minimumPayment(self, value: float):
        if self.is_float(value):
            self.minimumPayment = float(value)

    def set_interestRate(self, value: float):
        if self.is_float(value):
            self.interestRate = float(value)

    def add_debts(self):
        self.debts.append({"name": self.name, "amount": self.repaymentBalance, "interest_rate": self.interestRate, "min_payment": self.minimumPayment})
        self.name = ""
        self.repaymentBalance = 0
        self.minimumPayment = 0
        self.interestRate = 0
        print(self.debts)

    def calculate_repayment(self):
        results = calculate_repayment(debts=self.debts, extra_payment=self.extraMonthlyPayment)
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
            rx.chakra.input(placeholder="Debt Name",
                            on_change=DebtState.set_name,
                            is_required=True,
                            border_color="#CDCED6",
                            size="sm",
                            border_radius="8"),
            rx.chakra.input(placeholder="Repayment balance",
                            on_change=DebtState.set_repaymentBalance,
                            is_required=True,
                            border_color="#CDCED6",
                            size="sm",
                            border_radius="8"),

            justify="start",
            width="100%",
            spacing="2",
        ),
        rx.flex(
            rx.chakra.input(placeholder="Minimum payments",
                            on_change=DebtState.set_minimumPayment,
                            is_required=True,
                            border_color="#CDCED6",
                            size="sm",
                            border_radius="8"),
            rx.chakra.input(placeholder="Interest rate in %",
                            on_change=DebtState.set_interestRate,
                            is_required=True,
                            border_color="#CDCED6",
                            size="sm",
                            border_radius="8"),

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
            rx.chakra.input(placeholder="Extra monthly payment",
                            on_change=DebtState.set_extraMonthlyPayment,
                            is_required=True,
                            border_color="#CDCED6",
                            size="sm",
                            border_radius="8"),
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


# Main section
def debt_repayment() -> rx.Component:
    return rx.flex(
        rx.spacer(min_width="10px"),
        rx.flex(
            basic.header("/debt-repayment"),
            graph(),
            debt_input(),
            other_input(),
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
