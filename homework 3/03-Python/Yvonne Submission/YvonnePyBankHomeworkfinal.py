# Module for reading CSV files
import csv
from os import write

#Set path for file, make sure to chnage backslashes 
csvpath = "03-Python/Yvonne Submission/budget_data.csv"


#set my variable for 1st line of data for summary table
total_months = 0
total_profit = 0
# month changes to be outputted as a list 
month_change = []
# profit changes to be outputted as a list 
profit_change = []
# keep track of previous profit
previous_profit = 0

# Open the CSV
with open(csvpath, "r") as file:

    # CSV reader specifies delimiter and variable that holds contents
    csvreader = csv.reader(file, delimiter=',')

    # Looking at data set we know the first row is the Header and I want to skip it
    csvheader = next(csvreader)

    # This prints just the header
    print(csvheader)
    print()

    # Print our table minus the header
    #for row in csvreader:
        #print(row)


    # start my loops
    for row in csvreader:
        # Calculate total months = total number of lines within the budget data. Adding one after each line
        total_months = total_months + 1

        # Calculate total profit = the sum of row two, but in python we count at 0 so 1. Changed it to integer since our data has it as a string '  '. adding line after line
        total_profit = total_profit + int(row[1]) + 1
        
        # Calculate Average Change
        # Do not want to include the first line. 
        if total_months > 1:
        # start by calculating the 85 changes. (current line of profit - previous line of profit)
            change = int(row[1]) - previous_profit
            change2 = row[0]
            # add to change list
            profit_change.append(change)
            month_change.append(change2)
        # Reset. update previous profit to be my new profit 
        previous_profit = int(row[1])
        print(row)

    
print(total_months)
print(total_profit)
# Used for sanity check
print(profit_change)
print(month_change)

# Calculate for average change
#86 months but only 85 changes
print(sum(profit_change)/ 85)
average_change = (sum(profit_change)/ 85)

# Calculate Greatest increase in profit change
print(max(profit_change))
greatest_pincrease = (max(profit_change))

# Calculate Greatest decrease in profit change
print(min(profit_change))
greatest_pdecrease = (min(profit_change))

# Calculate Greatest month increase in profit change
greatest_month_index = profit_change.index(max(profit_change))
greatest_month_increase = month_change[greatest_month_index]
print(greatest_month_increase)

# Calculate Greatest month decrease in profit change
lowest_month_index = profit_change.index(min(profit_change))
greatest_month_decrease = month_change[lowest_month_index]
print(greatest_month_decrease)


#creating my summary analysis    
print("Profit/Losses Summary Analysis")
print("----------------------------")
print(f"Total Months: {total_months}")
print(f"Total: ${total_profit}")
print(f"Average Change: ${round(sum(profit_change)/(85),2)}")
print(f"Greatest Increase in Profits: {greatest_month_increase} (${greatest_pincrease})")
print(f"Greatest Decrease in Profits: {greatest_month_decrease} (${greatest_pdecrease})")



# making it print to .txt  
summary = f"""Profit/Losses Summary Analysis
----------------------------
Total Months: {total_months}
Total: ${total_profit}
Average  Change: ${round(sum(profit_change)/(85),2)}
Greatest Increase in Profits: {greatest_month_increase} (${greatest_pincrease})
Greatest Decrease in Profits:  {greatest_month_decrease} (${greatest_pdecrease})"""

#Check it prints correctly
#print(summary)

with open("PYBANK_Financial_Analysis.txt","w") as file:
    file.write(summary)