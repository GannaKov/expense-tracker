import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
from plot_transactions import plot_transactions


# Class to handle reading, writing, and analyzing finance data stored in a CSV file
class CSV:
    CSV_FILE = "finance_data.csv" # File name for storing data
    COLUMNS = ["date", "amount", "category", "description"] # Expected columns in the CSV file
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        # Checks if the CSV file exists; if not, creates it with the correct headers
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)


    @classmethod
    def add_entry(cls, date, amount, category, description):
        # Adds a new transaction to the CSV file
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")    


    @classmethod
    def get_transactions(cls, start_date, end_date):
        # Returns transactions within a specific date range
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT) # Convert to datetime
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

# Filter rows between start and end date
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

# Print transaction data or message if no data found
        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )   
            # Calculate and display summary statistics
            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expenses = filtered_df[filtered_df["category"] == "Expenses"][
                "amount"
            ].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expenses: ${total_expenses:.2f}")
            print(f"Net Savings: ${(total_income - total_expenses):.2f}") 
        
        return filtered_df    





def add():
    # Function to interactively add a new transaction
    CSV.initialize_csv() # Make sure CSV exists
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description) 


  
#01-01-2025 
#14-04-2025
def main():
    # Main loop for user interaction
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            # Ask for start and end dates and display filtered data
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            # Ask whether to show a plot for this data
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
               plot_transactions(df)
               print("Moment...")
               continue
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")

# Start the program if run directly
if __name__ == "__main__":
    main()