import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to request valid data from the user,
    which must be six comma separated integer values.
    Request will repeat until the data provided is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("e.g. 23,52,33,21,23,11\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(',')
        if validate_data(sales_data):
            print('Data is valid!')
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all values into integers.
    Raises ValueError if strings can't all be converted into int,
    or there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Required are 6 values, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.\n")
        return False

    return True


def update_worksheet(data, worksheet):
    """
    Receive a list of integers and inserts them into the worksheet.
    """
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated successfully.\n')


def calculate_surplus_data(sales_row):
    """
    Calculate sales with stock and calculate surplus for each item.
    """
    print('Calculating surplus data...\n')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]

    surplus_data = []
    for sales, stock in zip(sales_row, stock_row):
        surplus_data.append(int(stock) - sales)

    return surplus_data


def get_last_5_entries_from_sales():
    """
    Collects columns of data from the sales worksheet, collecting
    the last five entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet('sales')

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns


def main():
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')


print('Welcome to Love Sandwiches Data Automation!')
# main()
sales_columns = get_last_5_entries_from_sales()
