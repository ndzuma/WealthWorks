import time
from WealthWorks.workers import consoleStatements as Display


service = "Repayment Calculator"


def calculate_repayment(debts: list, extra_payment=0):
    """
    Calculate the repayment of debts
    :param debts: List of debts
    :param extra_payment:
    :return: months, monthly_payment, total_paid, total_interest_paid
    """
    # Displaying in the console
    Display.start(service)

    # cleaning the data, making sure the interest rate is in decimal
    debts = perc_to_dec(debts)

    # checking if the minimum payment is enough to cover the interest
    min_pay_bool = check_min_payment(debts)

    # changing the minimum payment to cover the interest, if necessary
    for i in range(len(min_pay_bool)):
        if not min_pay_bool[i]:
            debts[i] = change_min_payment(debts[i])

    # checking if it is possible to pay off the debts at all
    if not check_if_possible(debts, extra_payment):
        Display.message(service, "It is not possible to pay off the debts")
        return None

    # setting main variables
    total_debt = sum(debt['amount'] for debt in debts)
    monthly_payment = sum(debt['min_payment'] for debt in debts)
    total_payment = monthly_payment + extra_payment
    total_paid = total_debt
    total_interest_paid = 0
    months = 0

    # calculating the repayment
    while total_debt > 0:
        months += 1
        interest = 0
        for debt in debts:
            if debt['amount'] <= 0:  # Skip if debt amount is zero or negative
                continue

            interest += debt['amount'] * (debt['interest_rate'] / 12)
            debt['amount'] += debt['amount'] * (debt['interest_rate'] / 12)
            if debt['amount'] < debt['min_payment']:
                total_payment -= (debt['min_payment'] - debt['amount'])
                debt['amount'] = 0
            else:
                debt['amount'] -= debt['min_payment']

        total_interest_paid += interest
        total_debt += interest
        total_debt -= total_payment

        if total_debt <= 0:
            break

    # Displaying in the console
    Display.completed(service)
    return months, monthly_payment, round(total_paid, 2), round(total_interest_paid, 2)


def priority_payment(debts: list):
    """
    Finds the debt to prioritize
    :param debts: List of debts
    :return: The name of the debt to prioritize
    """
    sorted_debts = sorted(debts, key=lambda x: x['interest_rate'])

    # Displaying in the console
    Display.message(service, "Priority payment found")
    return sorted_debts[-1]['name']


def perc_to_dec(debts: list):
    """
    Change the interest rate from percentage to decimal
    :param debts: List of debts
    :return: List of debts with interest rate in decimal
    """
    final_debts = []
    for debt in debts:
        debt['interest_rate'] = debt['interest_rate'] * (10**(-2))
        final_debts.append(debt)

    # Displaying in the console
    Display.message(service, "Interest rates converted to decimal")
    return final_debts


def check_min_payment(debts: list):
    """
    Check if the minimum payment is enough to cover the interest
    :param debts: List of debts
    :return: List of booleans per debt
    """
    results = []
    for debt in debts:
        if debt['min_payment'] < (debt['amount'] * (debt['interest_rate'] / 12)):
            results.append(False)
        else:
            results.append(True)

    # Displaying in the console
    if all(results):
        Display.message(service, "Minimum payments are enough to cover interest")
    else:
        Display.message(service, "Minimum payments not enough to cover interest")
    return results


def change_min_payment(debt: dict):
    """
    Change the minimum payment to cover the interest
    :param debt: dict of debt
    :return: Dict of debt with the minimum payment changed
    """
    name = debt['name']
    current_min_payment = debt['min_payment']

    # The amount of the debt that goes to interest
    min_payment = (debt['amount'] * (debt['interest_rate'] / 12))
    debt['min_payment'] = min_payment

    # Displaying in the console
    Display.message(service, f"{name}'s minimum payment changed. From: {current_min_payment} to: {min_payment}")
    return debt


def check_if_possible(debts: list, extra_payment: float):
    """
    Check if it is possible to pay off the debts at all
    :param debts: List of debts
    :param extra_payment: Additional payment
    :return: Boolean
    """
    total_payment = 0 + extra_payment
    total_interest = 0
    for debt in debts:
        if not debt["amount"] > 0:
            return False
        if not debt["min_payment"] > 0:
            return False
        if not debt["interest_rate"] > 0:
            return False
        total_payment += debt["min_payment"]
        total_interest += debt["amount"] * (debt["interest_rate"] / 12)

    if total_payment <= total_interest:
        return False
    return True
