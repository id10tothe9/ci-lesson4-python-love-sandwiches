import gspread
from google.oauth2.service_account import Credentials

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
    Get sales figures input from the user
    """
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("e.g. 23,52,33,21,23,11\n")

    data_str = input("Enter your data here: ")

    sales_data = data_str.split(',')
    validate_data(sales_data)

def validate_data(values):
    """
    Inside the try, converts all values into integers.
    Raises ValueError if strings can't all be converted into int,
    or there aren't exactly 6 values.
    """
    try:
        if len(values) != 6:
            raise ValueError(f"Required are 6 values, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}. Please try again.\n")

get_sales_data()