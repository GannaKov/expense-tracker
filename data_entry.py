from datetime import datetime

# Define the expected date format for input/output
date_format = "%d-%m-%Y"
# Dictionary to map short category input to full names
CATEGORIES = {"I": "Income", "E": "Expenses"}


# Function to get a valid date from the user
def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    # If allowed and input is empty, return today's date
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)

    try:
        # Try converting the input string into a datetime object
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        # If the format is wrong, notify the user and retry
        print("Invalid date format. Please enter the date in dd-mm-yyyy format")
        return get_date(prompt, allow_default)
    

# Function to get a valid amount from the user
def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative non-zero value.")
        return amount
    except ValueError as e:
        # If input is invalid, show error and retry
        print(e)
        return get_amount()  


# Function to get a valid category from the user
def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expenses): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]  # Return full category name

# If invalid input, notify and retry
    print("Invalid category. Please enter 'I' for Income or 'E' for Expenses.")
    return get_category()     


# Function to get an optional description from the user
def get_description():
    # Capitalize the input, use default placeholder if empty
    return input("Enter a description (optional): ").capitalize() or "--------"