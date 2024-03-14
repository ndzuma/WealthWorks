def start(service: str = "WealthWorks"):
    """
    Print a message to the console when a service starts
    :param service: The name of the service starting
    """
    print(f"\nStarting {service}...")


def completed(service: str = "WealthWorks"):
    """
    Print a message to the console when a service completes
    :param service: The name of the service being completed
    """
    print(service, "completed.")


def message(service: str, text: str):
    """
    Print a message to the console
    :param service: The name of the service displaying a message
    :param text: The message to be displayed
    """
    print(f"{service}: {text}")
