# Python Expense Tracker

This Python Expense Tracker manages daily expenses with add, list, update, delete operations and monthly summaries. It supports real-time currency conversion from USD (Assuming Expenses are in USD) to other currencies via an external API. Built with simplicity in mind, the project leverages Colorama for colored output and python-dotenv for secure API key management, offering an extensible, modular solution for expense tracking with robust functionality.


This project is inspired by [Roadmap.sh Expense Tracker](https://roadmap.sh/projects/expense-tracker). It extends the basic functionality by adding features like **currency conversion**.

## Features

- **Add, list, update, and delete expenses**  
- **Monthly expense summaries**  
- **Currency conversion (USD to other currencies)**  
- **Color-coded output** using [Colorama](https://pypi.org/project/colorama/)  
- **Securely store API keys** with [python-dotenv](https://pypi.org/project/python-dotenv/)

## Installation

1. **Clone this repository** or download the source code.
2. *(Optional)* Create a virtual environment:
   ```bash
   python -m venv expense_env
   source expense_env/bin/activate  # or expense_env\Scripts\activate on Windows
   ```
3. **Install dependencies:**
   ```bash
      pip install -r requirements.txt
   ```
4. (Optional) Create a .env file for using API that requires a key:
   ```bash
      EXCHANGE_API_KEY=your_api_key_here
   ```
5. **Run the application:**
   ```bash
      python main.py
   ```
## Usage

When you run main.py, you can use the following commands:

- help – Show available commands
- add – Add a new expense
- list – List all expenses
- upd – Update an existing expense
- del – Delete an expense
- sum – Show overall expense summary
- month – Show monthly expense summary
- con – Convert expenses from USD to another currency
- exit – Exit the application


## Contributing

Contributions are always welcome!

Feel free to submit issues and pull requests. Any improvements are welcome!

