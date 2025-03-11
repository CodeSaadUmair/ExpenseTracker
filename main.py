import requests
import json
from datetime import datetime
import os
from colorama import init, Fore, Back, Style
from dotenv import load_dotenv

load_dotenv() # Loads .env into os.environ


EXP_FILE = "expenses.json"  # json file defination


# Initialize Colorama
init(autoreset=True)  


# Help Menu
def show_help():
     
    print("\n" + Fore.RED + Style.BRIGHT + " AVAILABLE COMMANDS ".center(50, "-"))
    
    commands = [
        ("help", "For This Menu"),
        ("add", "To Add an Expense"),
        ("list", "To List All Expenses"),
        ("upd", "To Update an Expense"),
        ("del", "To Delete an Expense"),
        ("sum", "To Summarize Expenses [Current Listed]"),
        ("month", "To View Summary for a Specific Month (current year)"),
        ("con", "To Convert Expenses Currency From USD To Other Types"),
        ("exit", "To Exit the Program")
    ]
    
    for cmd, desc in commands:
        print(f"{Back.YELLOW}{Fore.BLACK}{Style.BRIGHT} {cmd.ljust(10)} {Style.RESET_ALL} {desc}")

    print("-" * 50)


# load json data
def load_json():
    '''
    load data from the EXP_FILE and returns it in case of no file found starts with empty file/list
    '''
    if os.path.exists(EXP_FILE):
        try:
            with open(EXP_FILE, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError:
            print(Fore.YELLOW + "Warning: Unable to read existing Expenses. Starting with an empty list." + Style.RESET_ALL)
    return []


# save he json
def save_json(expenses):
    '''
    Dumps i.e saves data to json file 
    '''
    with open(EXP_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


# Global expense counter which returns next available expense id
def get_next_expense_id(expenses):
    """Return the next available expense id."""
    if expenses:
        # Compute the next id as max(current id's) + 1
        return max(expense["id"] for expense in expenses) + 1
    else:
        return 1


# add Expenses Function
def add_expense():
    '''
        adds expense to the list and saves by calling save_json function
    '''
    description = input(Fore.WHITE + "Enter Expense description : " + Style.RESET_ALL).strip()
    if not description:
        print(Fore.RED + "Expense Description Cannot Be Empty." + Style.RESET_ALL)
        return

    raw_amount = input(Fore.WHITE + "Enter Amount: " + Style.RESET_ALL).strip()
    # this try exceptblock is to handle int and float data from user after taking a string as a amount
    try:
        amount = float(raw_amount)
        if amount.is_integer():
            amount = int(amount)
    except ValueError:
        print(Fore.RED + "Invalid amount. Please enter a numeric value." + Style.RESET_ALL)
        return

    time = datetime.now().isoformat()

    # Load the existing expenses
    expenses = load_json()
    # Determine the next id based on existing expenses
    expense_id = get_next_expense_id(expenses)

    expense = {
        "id": expense_id,
        "description": description,
        "amount": amount,
        "entryTime": time,
        "updationTime": time
    }

    # append expense to expenses List
    expenses.append(expense)
    #save expenses to json file
    save_json(expenses)
    print(Fore.GREEN + f"Expense added with ID {expense_id}" + Style.RESET_ALL)


# list the Expense
def list_expenses():
    '''
    Called when user inputs list to list all the avilable expense handles no expense also
    '''
    expenses = load_json()
    if not expenses:
        print(Fore.RED + "No expenses available to List!" + Style.RESET_ALL)
        return
    display_expenses(expenses)
    # for expense in expenses:
    #     print()
    #     print(Style.RESET_ALL+"+"*50)
    #     print(Fore.GREEN+"ID : ",expense["id"])
    #     print(Fore.GREEN+"Description : ",expense["description"])
    #     print(Fore.GREEN+"Amount : ",expense["amount"])
    #     print(Fore.GREEN+"EntryTime : ",expense["entryTime"])
    #     print(Fore.GREEN+"UpdationTime : ",expense["updationTime"])
    #     print("+"*50)
    #     print()


# find expense by id for updation and deletion
def find_expense_by_id(expenses, expense_id):
    """Return the expense with the matching id, or None if not found."""
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    return None


#update Expenses
def update_expenses():
    '''
    to update existing expense by id handles all cases
    '''
    expenses = load_json()
    if not expenses:
        print(Fore.RED + "No expenses available to update!" + Style.RESET_ALL)
        return

    #function called to show available options to update
    display_expenses(expenses)
    
    try:
        update_id = int(input("Enter Id of The Expense You Want To Update : "))
    except ValueError:
        print(Fore.RED + "Invalid ID. Please enter a valid number from the list." + Style.RESET_ALL)
        return
    except Exception as e:
        print(e)
        return

    selected_expense = find_expense_by_id(expenses, update_id)#function called to find the id given by user in the expenses 
    if selected_expense is None:
        print(Fore.RED + "Expense with the given ID not found!" + Style.RESET_ALL)
        return

    print(Fore.CYAN + "Current Description:" + Style.RESET_ALL, selected_expense["description"])
    new_description = input(Fore.WHITE + "Enter new description (press enter to keep current): " + Style.RESET_ALL).strip()
    if new_description:
        selected_expense["description"] = new_description

    print(Fore.CYAN + "Current Amount:" + Style.RESET_ALL, selected_expense["amount"])

    # this try exceptblock is to handle int and float data from user after taking a string as a amount
    raw_amount = input(Fore.WHITE + "Enter new Amount (press enter to keep current): " + Style.RESET_ALL).strip()
    if raw_amount:
        try:
            new_amount = float(raw_amount)
            if new_amount.is_integer():
                new_amount = int(new_amount)
            selected_expense["amount"] = new_amount
        except ValueError:
            print(Fore.RED + "Invalid amount entered. Update aborted." + Style.RESET_ALL)
            return

    new_uptime = datetime.now().isoformat() # update the updation time field
    selected_expense["updationTime"] = new_uptime
    save_json(expenses)
    print(Fore.GREEN + "Expense updated successfully!" + Style.RESET_ALL)


# Delete Expence
def delete_expenses():
    '''
    to Delete existing expense by id handles all cases
    '''
    expenses = load_json()
    if not expenses:
        print(Fore.RED + "No expenses available to Delete!" + Style.RESET_ALL)
        return

     #function called to show available options to Delete
    display_expenses(expenses)
    
    try:
        delete_id = int(input(Fore.WHITE + "Enter Expense Id To Delete: " + Style.RESET_ALL))
    except ValueError:
        print(Fore.RED + "Invalid input! Please enter a valid number." + Style.RESET_ALL)
        return

    expense_to_delete = find_expense_by_id(expenses,delete_id)#function called to find the id given by user in the expenses 
    if expense_to_delete is None:
        print(Fore.RED + "Expense with the given ID not found!" + Style.RESET_ALL)
        return

    expenses.remove(expense_to_delete)
    save_json(expenses)
    print(Fore.GREEN + f"Expense '{expense_to_delete['description']}' deleted successfully!" + Style.RESET_ALL)


# show expense used in update_expenses and delete_expenses list_Expenses
def display_expenses(expenses):
    """Display expenses in a neat tabular format."""
    header = f"{'ID':<5}{'Description':<30}{'Amount':<10}{'Date':<15}"
    print(Fore.BLUE + header + Style.RESET_ALL)
    print(Fore.BLUE + "-" * len(header) + Style.RESET_ALL)
    for expense in expenses:
        date_str = expense["entryTime"].split("T")[0]
        print(Fore.GREEN + f"{expense['id']:<5}{expense['description']:<30}{expense['amount']:<10}{date_str:<15}" + Style.RESET_ALL)


#show summary of Expenses All
def show_summary():
    expenses = load_json()
    header = f"{'ID':<5}{'Description':<30}{'Amount':<10}{'Date':<15}"
    print(Fore.BLUE + header + Style.RESET_ALL)
    print(Fore.BLUE + "-" * len(header) + Style.RESET_ALL)
    summary = []
    for expense in expenses:
        date_str = expense["entryTime"].split("T")[0]
        print(Fore.GREEN + f"{expense['id']:<5}{expense['description']:<30}{expense['amount']:<10}{date_str:<15}" + Style.RESET_ALL)
        summary.append(expense['amount'])
    print(Fore.BLUE + "-" * len(header) + Style.RESET_ALL)
    total = sum(summary)
    print(Fore.GREEN + f"{'':<5}{'Total':<30}{total:<10}" + Style.RESET_ALL)


# Specific month summary
def show_monthly_summary():
    try:
        month_input = input(Fore.WHITE + "Enter month (1-12): " + Style.RESET_ALL).strip()
        month = int(month_input)
        if month < 1 or month > 12:
            print(Fore.RED + "Invalid month. Please enter a number between 1 and 12." + Style.RESET_ALL)
            return
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a valid number for the month." + Style.RESET_ALL)
        return

    current_year = datetime.now().year

    expenses = load_json()# function called

    filtered_expenses = []

    for expense in expenses:
        try:
            entry_date = datetime.fromisoformat(expense["entryTime"])
        except ValueError:
            continue  # skip any expense with an invalid date format
        if entry_date.year == current_year and entry_date.month == month:
            filtered_expenses.append(expense)

    if not filtered_expenses:
        print(Fore.YELLOW + f"No expenses found for {current_year}-{month:02d}." + Style.RESET_ALL)
        return

    # Display header with an extra Date column
    header = f"{'ID':<5}{'Description':<30}{'Amount':<10}{'Date':<15}"
    print(Fore.BLUE + header + Style.RESET_ALL)
    print(Fore.BLUE + "-" * len(header) + Style.RESET_ALL)

    total = 0
    for expense in filtered_expenses:
        total += expense["amount"]
        # Extract only the date portion from the entryTime
        date_str = expense["entryTime"].split("T")[0]
        print(Fore.GREEN + f"{expense['id']:<5}{expense['description']:<30}{expense['amount']:<10}{date_str:<15}" + Style.RESET_ALL)

    print(Fore.BLUE + "-" * len(header) + Style.RESET_ALL)
    print(Fore.GREEN + f"{'':<5}{'Total':<30}{total:<10}" + Style.RESET_ALL)


# convert_currency Function
def convert_currency(amount, from_currency="USD", to_currency="EUR"):
    api_key = os.environ.get('EXCHANGE_API_KEY')

    if not api_key:
        print("API key not found. Please set the EXCHANGE_API_KEY environment variable.")
        return None
    
    url = f"https://api.exchangerate.host/convert?access_key={api_key}&from={from_currency}&to={to_currency}&amount={amount}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("result")
    except requests.RequestException as e:
        print("Error retrieving conversion rate:", e)
        return None


# Conert_Expenses Function
def convert_expenses():
    target_currency = input("Enter the target currency code (e.g., EUR, GBP, INR): ").upper().strip()
    expenses = load_json()
    if not expenses:
        print("No expenses available for conversion.")
        return
    
    header = f"{'ID':<5}{'Description':<30}{'Original (USD)':<15}{'Converted (' + target_currency + ')':<20}"
    print(header)
    print("-" * len(header))

    for expense in expenses:
        original_amount = expense['amount']
        converted_amount = convert_currency(original_amount, "USD", target_currency) # Function Called
        if converted_amount is not None:
            print(f"{expense['id']:<5}{expense['description']:<30}{original_amount:<15}{converted_amount:<20}")
        else:
            print(f"Conversion failed for Expense ID {expense['id']}")


# Main Function
def main():
    init(autoreset=True)  
    print("*"*50)
    print(Fore.RED+"\n-- Welcome To Your Own Expense Tracker --\n")
    print("*"*50)
    show_help()

    while True:
        command = input(Fore.GREEN+">>>>> ").lower().strip()
        if command == "help":
            show_help()
        elif command == "add":
            add_expense()
        elif command == "list":
            list_expenses()
        elif command == "upd":
            update_expenses()
        elif command == "del":
            delete_expenses()
        elif command == "sum":
            show_summary()
        elif command == "month":
            show_monthly_summary()
        elif command == "con":
            convert_expenses()
        elif command == "exit":
            print("GoodBye User!")
            break
        else:
            print(Back.RED+"Please Enter Valid Command")
            show_help()


if __name__ == "__main__":
    main()