import reflex as rx

from typing import List, Dict
from WealthWorks.components import basic
from WealthWorks.workers.pdfWrapper import create_pdf
from WealthWorks.workers import consoleStatements as Display


# State
class BudgetState(rx.State):
    service: str
    resources: list
    resources_list: Dict[str, List[List[str]]]
    category: str

    # Inputs from the user
    name: str
    amount: int
    budget: int

    # Outputs from the calculations
    current_total: int
    true_total: int
    available: int
    saved: int
    Emergency_fund: int

    def __init__(self, *args, **kwargs):
        # initialize state
        super().__init__(*args, **kwargs)
        self.service = "Budget page"
        self.resources = [{"name": "Available", "value": 100}]
        self.resources_list = {}
        self.category = "Rent"
        self.budget = 0
        self.current_total = 0

    # Methods
    def add_expense(self):
        """
        Adds an expense to the list
        """
        if self.name != "" and self.amount != 0:
            # add to list
            if self.name not in self.resources_list:
                self.resources_list.update({self.name: [[self.category], [self.amount]]})

                # update category list
                self.resources = self.sum_categories(self.resources_list)
                self.find_total()
                self.find_available()
                self.find_saved()
                self.resources = self.sum_categories(self.resources_list)

                # Displaying in the console
                Display.message(self.service, "Added expense")

    def sum_categories(self, dictionary):
        """
        Sums the categories in the dictionary
        :param dictionary: The current list of resources
        :return: A list of categories and their values
        """
        category_list = [
            {"name": "Investing", "value": 0},
            {"name": "Savings", "value": 0},
            {"name": "Emergency fund", "value": 0},
            {"name": "Debt repayment", "value": 0},
            {"name": "Utilities", "value": 0},
            {"name": "Mortgage", "value": 0},
            {"name": "Rent", "value": 0},
            {"name": "Other", "value": 0},
            {"name": "Transport", "value": 0},
            {"name": "Entertainment", "value": 0},
            {"name": "Available", "value": self.available}
        ]
        for i in dictionary:
            j = (dictionary[i][0])
            for k in category_list:
                if k["name"] == j[0]:
                    k["value"] += dictionary[i][1][0]

        return category_list

    def find_saved(self):
        """
        Finds the amount saved or invested and the amount in the emergency fund
        """
        saved = 0
        ef = 0
        for l in self.resources:
            if l["name"] == "Investing" or l["name"] == "Savings":
                saved += l["value"]
            elif l["name"] == "Emergency fund":
                ef += l["value"]
        self.saved = saved
        self.Emergency_fund = ef

    def find_total(self):
        """
        Finds the total amount of money spent
        """
        no_fly_list = ["Investing", "Savings", "Emergency fund", "Available"]
        total = 0
        real_total = 0
        for l in self.resources:
            if l["name"] not in no_fly_list:
                total += l["value"]
            else:
                real_total += l["value"]

        self.current_total = total
        self.true_total = real_total + total - self.budget

    def find_available(self):
        """
        Finds the amount of money available from your budget after expenses
        """
        if self.budget != 0:
            self.available = int(self.budget) - self.current_total

    def set_budget(self, value):
        try:
            self.budget = int(value)
            self.find_available()
        except ValueError:
            print("Not a number")

    def download_pdf(self):
        """
        Downloads the budget as a PDF, by creating a PDF and downloading it
        :return: A PDF file
        """
        # format expense data
        expense_data = [["Category", "Item", "Amount"]]
        for i in self.resources_list:
            if self.resources_list[i][0][0] not in ["Investing", "Savings", "Emergency fund", "Available"]:
                expense_data.append([str(self.resources_list[i][0][0]), i, str(self.resources_list[i][1][0])])
        expense_data.append(["Total", "", str(self.current_total)])

        # format savings data
        savings_data = [["Category", "", "Amount"]]
        for i in self.resources:
            if i["name"] == "Investing" or i["name"] == "Savings" or i["name"] == "Emergency fund":
                savings_data.append([i["name"], "", str(i["value"])])

        # format summary data
        summary_data = [["Category", "", "Amount"], ["Spend", "", str(self.current_total)],
                        ["Saved/Invested", "", str(self.saved)], ["Emergency fund", "", str(self.Emergency_fund)],
                        ["Total", "", str(self.true_total)]]

        return rx.download(
            data=create_pdf(expense_data, savings_data, summary_data),
            filename="Budget.pdf",
        )


def graph() -> rx.Component:
    return rx.flex(
        rx.recharts.pie_chart(
            rx.recharts.pie(
                data=BudgetState.resources,
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


def amount_input() -> rx.Component:
    category = ["Groceries", "Transport", "Entertainment", "Utilities", "Mortgage", "Rent", "Debt repayment",
                "Other", "Investing", "Savings", "Emergency fund"]
    placeholder = category[3]
    return rx.flex(
        rx.flex(
            rx.chakra.input(placeholder="Budget", on_change=BudgetState.set_budget, border_color="#CDCED6", size="sm", border_radius="8"),
            justify="start",
            width="100%",
            spacing="2",
        ),
        rx.flex(
            rx.chakra.select(
                category,
                default_value=placeholder,
                on_change=BudgetState.set_category,
                is_required=True,
                border_color="#CDCED6",
                border_radius="8",
                size="sm"
            ),
            rx.chakra.input(placeholder="Name", on_change=BudgetState.set_name, is_required=True, border_color="#CDCED6", size="sm", border_radius="8"),
            rx.chakra.input(placeholder="Amount", on_change=BudgetState.set_amount, is_required=True, border_color="#CDCED6", size="sm", border_radius="8"),
            rx.chakra.button("Enter", on_click=BudgetState.add_expense, bg="#4662D5", color="white", size="sm", width="15em", border_radius="8"),
            justify="start",
            spacing="2",
        ),
        direction="column",
        spacing="2",
    )


def get_info(text) -> rx.Component:
    explanation = "X means Y"
    return rx.popover.root(
        rx.popover.trigger(
            rx.link(text),
        ),
        rx.popover.content(
            rx.flex(
                rx.text(explanation),
                rx.popover.close(
                    rx.link("Close"),
                ),
                direction="column",
                spacing="3",
            ),
        ),
    )


def get_budget(item) -> rx.Component:
    return rx.table.row(
        rx.table.cell(rx.avatar(fallback=f"WW")),
        rx.table.row_header_cell(
            get_info(item[0])
        ),
        rx.table.cell(item[1][1]),
        align="center",
    )


def budget_list() -> rx.Component:
    return rx.flex(
        rx.card(
            rx.text("Category", size="4", weight="medium", align="center"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Icon"),
                        rx.table.column_header_cell("Items"),
                        rx.table.column_header_cell("Amount"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(
                        BudgetState.resources_list,
                        get_budget
                    )
                ),
            ),
            width="100%",
        ),
        width="100%"
    )


def budget_summary() -> rx.Component:
    return rx.flex(
        rx.card(
            rx.text("Summary", size="4", weight="medium", align="center"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Category"),
                        rx.table.column_header_cell("Amount"),
                    ),
                ),
                rx.table.body(
                    rx.table.row(
                        rx.table.cell("Spend"),
                        rx.table.cell(BudgetState.current_total),
                        align="center",
                    ),
                    rx.table.row(
                        rx.table.cell("Saved/Invested"),
                        rx.table.cell(BudgetState.saved),
                        align="center",
                    ),
                    rx.table.row(
                        rx.table.cell("Emergency Fund"),
                        rx.table.cell(BudgetState.Emergency_fund),
                        align="center",
                    ),
                    rx.table.row(
                        rx.table.cell("Available"),
                        rx.table.cell(BudgetState.available),
                        align="center",
                    ),
                ),
            ),
            rx.box(height="10px"),
            rx.button(
                "Download as PDF",
                on_click=BudgetState.download_pdf,
            ),
            width="100%",
        ),
        width="100%"
    )


# Main section
def planner() -> rx.Component:
    return rx.flex(
        rx.theme_panel(default_open=False),
        rx.spacer(min_width="10px"),
        rx.flex(
            basic.header("/"),
            graph(),
            amount_input(),
            budget_list(),
            budget_summary(),
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
