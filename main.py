import json
from datetime import datetime
import os
from colorama import init, Fore, Back, Style


EXP_FILE = "expenses.json"  # json file defination


# Initialize Colorama
init(autoreset=True)  


# Help Menu
def show_help():
    print()
    print("-"*50)
    print(Fore.RED+"\nAvalaible Commands ")
    print(Back.YELLOW + Fore.RED + Style.BRIGHT + "\thelp - For This Menu")
    print(Back.YELLOW + Fore.RED + Style.BRIGHT + "\tadd - To Add A Expence")
    print(Back.YELLOW + Fore.RED + Style.BRIGHT + "\tlist - To List All The Expenses")
    print(Back.YELLOW + Fore.RED + Style.BRIGHT + "\tupdate - To Update A Expence")
    print(Back.YELLOW + Fore.RED + Style.BRIGHT + "\tdelete - To Delete A Expence")
    print(Back.YELLOW + Fore.RED + Style.BRIGHT + "\texit -To Exit Program")
    print()
    print("-"*50)


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
    for expense in expenses:
        print()
        print(Style.RESET_ALL+"+"*50)
        print(Fore.GREEN+"ID : ",expense["id"])
        print(Fore.GREEN+"Description : ",expense["description"])
        print(Fore.GREEN+"Amount : ",expense["amount"])
        print(Fore.GREEN+"EntryTime : ",expense["entryTime"])
        print(Fore.GREEN+"UpdationTime : ",expense["updationTime"])
        print("+"*50)
        print()


# find expense by id for updation and deletion
def find_expense_by_id(expenses, expense_id):
    """Return the expense with the matching id, or None if not found."""
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    return None


# show expense other than list used in update_expenses and delete_expenses
def display_expenses(expenses):
    """Display expenses in a neat tabular format."""
    header = f"{'ID':<5}{'Description':<30}{'Amount':<10}"
    print(Fore.BLUE + header + Style.RESET_ALL)
    print(Fore.BLUE + "-" * len(header) + Style.RESET_ALL)
    for expense in expenses:
        print(Fore.GREEN + f"{expense['id']:<5}{expense['description']:<30}{expense['amount']:<10}" + Style.RESET_ALL)


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
        elif command == "update":
            update_expenses()
        elif command == "delete":
            delete_expenses()
        elif command == "exit":
            print("GoodBye User!")
            break
        else:
            print(Back.RED+"Please Enter Valid Command")
            show_help()

if __name__ == "__main__":
    main()