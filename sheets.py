import os
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# =========================
# GOOGLE SHEETS SETUP
# =========================

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    os.environ.get("GOOGLE_SHEETS_CREDENTIALS_FILE", "credentials.json"),
    scopes=scope
)

client = gspread.authorize(creds)

sheet_name = os.environ.get("GOOGLE_SHEET_NAME", "My_Expenses_2026")
sheet = client.open(sheet_name).sheet1

def categorize_expense(description):
    description = description.lower()

    if any(word in description for word in ["lunch", "dinner", "food", "tea", "coffee", "snacks"]):
        return "Food"
    elif any(word in description for word in ["uber", "bus", "train", "petrol", "fuel"]):
        return "Travel"
    elif any(word in description for word in ["rent", "house"]):
        return "Rent"
    elif any(word in description for word in ["electricity", "bill", "internet"]):
        return "Bills"
    else:
        return "Other"


def add_expense(user, description, amount):
    category = categorize_expense(description)

    print(">>> Inside add_expense")

    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d"),
        user,
        description,
        category,
        amount
    ])

    print(">>> Row inserted successfully")

from datetime import datetime

def get_user_summary(user):
    records = sheet.get_all_records()

    total = 0
    category_totals = {}

    current_month = datetime.now().strftime("%Y-%m")

    for row in records:
        if str(row["User"]) == str(user):
            if row["Date"].startswith(current_month):
                amount = int(row["Amount"])
                category = row["Category"]

                total += amount

                if category in category_totals:
                    category_totals[category] += amount
                else:
                    category_totals[category] = amount

    return total, category_totals