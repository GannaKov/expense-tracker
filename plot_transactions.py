import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def plot_transactions(df):
    # Font styles for labels and titles
    font1 = {'family':'sans-serif','color':'darkred','size':12}
    font2 = {'family':'sans-serif','size':16,'weight':'bold'}
     # Convert the "date" column to datetime and sort the DataFrame
    df["date"] = pd.to_datetime(df["date"])  # transform date column to datetime
    df = df.sort_values("date")              # sort by date

    # Set "date" as index for resampling
    df.set_index("date", inplace=True)

# Resample and sum up income data by day
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
       
    )

# Resample and sum up expenses data by day
    expenses_df = (
        df[df["category"] == "Expenses"]
        .resample("D")
        .sum()
        
    )

 # Create figure and define layout: 1 row, 2 columns with 2:1 width ratio
    fig =plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])  # 2/3 and 1/3
    
    

     # -------- Left Plot: Time Series of Income and Expenses --------
    ax1 = fig.add_subplot(gs[0, 0])  # First subplot (2/3 of the figure)
    # Line and scatter plot for expenses
    ax1.plot(income_df.index, income_df["amount"], label="Income", color="g")
    ax1.scatter(
        income_df[income_df["amount"] > 0].index,
        income_df[income_df["amount"] > 0]["amount"],
        color="g",
        #marker="o"
        marker = '*',
        s=100,  # Size of the marker
       
    )
    # Line and scatter plot for expenses
    ax1.plot(expenses_df.index, expenses_df["amount"], label="Expenses", color="r", linestyle="--")
    ax1.scatter(
        expenses_df[expenses_df["amount"] > 0].index,
        expenses_df[expenses_df["amount"] > 0]["amount"],
        color="r",
        marker="o"
    )
    # Customize axis and appearance
    ax1.set_xlabel("Date", fontdict = font1)
    ax1.tick_params(axis='x', rotation=-45)
    ax1.set_ylabel("Amount", fontdict = font1)
    ax1.set_title("Income and Expenses Over Time", fontdict = font2)
    ax1.legend()
    ax1.grid(True)
    
    # -------- Right Plot: Total Income vs Expenses Bar Chart --------
    ax2 = fig.add_subplot(gs[0, 1])   # Second subplot takes 1/3 of space
     # Calculate total values for income and expenses
    total_expenses = df[df["category"] == "Expenses"]["amount"].sum()
    total_income = df[df["category"] == "Income"]["amount"].sum()

    # Bar chart comparing totals
    labels = ["Income", "Expenses"]
    values = [total_income, total_expenses]
    colors = ["green", "red"]
    ax2.bar(labels, values, color=colors)
    # Customize bar chart appearance
    ax2.set_title("Total Income vs Expenses", fontdict = font2)
    ax2.set_ylabel("Amount", fontdict = font1)
    ax2.grid(axis="y", linestyle="--", alpha=0.5)
    

    # Automatically adjust layout to prevent overlap
    plt.tight_layout()
    plt.show()