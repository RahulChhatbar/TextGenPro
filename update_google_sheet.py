import json
import gspread
from google.oauth2.service_account import Credentials

# Define the required Google Sheets API scope
scopes = ['https://www.googleapis.com/auth/spreadsheets']

# Authenticate and authorize with the provided credentials JSON file
creds = Credentials.from_service_account_file("cred.json", scopes=scopes)
client = gspread.authorize(creds)

# Define product information
product_name = "textgenpro"
claimed_ports = "11111 - 11120"

# Open the Google Sheet by its ID
sheet_id = "1mZu6w649saioKTaXiqYJw4ohCOpk_XSiVD4h3vQ15FA"
sheet1 = client.open_by_key(sheet_id).sheet1

# Load IP address information from 'ip.txt' file
with open('ip.txt') as f:
    data = json.load(f)

# Extract the IP address from JSON data
ip_address = data[0]["NetworkSettings"]["Networks"]["monitoring"]["IPAddress"]

group_column_index = None
row_1_values = sheet1.row_values(1)  # Row 1 is the first row
for index, value in enumerate(row_1_values):
    if "group" in value.lower():
        group_column_index = index + 1
        break

# Update the IP address in the Google Sheet
if group_column_index is None:
    exit("Error: 'group' column not found")

column_a_values = sheet1.col_values(group_column_index)  # Column A is the first column
for index, value in enumerate(column_a_values):
    if "16" in value:
        sheet1.update_cell(index + 1, 2, "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIM9P6aOKIW6dho3pvCSKVbrAajy4BZKg2so1Ie1KsTGp rahul-chhatbar@IK4k")

column_b_values = sheet1.col_values(2)  # Column B is the second column
row_1_values = sheet1.row_values(1)  # Row 1 is the first row
row_index = None
claimed_port_column_index = None
product_name_column_index = None
ngrok_url_column_index = None
ngrok_url = None

with open("ngrok_log.txt", "r") as f:
    for line in f:
        if "started tunnel" in line:
            parts = line.split(" ")
            for part in parts:
                if part.startswith("url"):
                    ngrok_url = part[4:]
                    break

for index, value in enumerate(row_1_values):
    if "Claimed port" in value:
        claimed_port_column_index = index + 1
        break

for index, value in enumerate(row_1_values):
    if "Product CONTAINER NAME" in value:
        product_name_column_index = index + 1
        break

for index, value in enumerate(row_1_values):
    if "ngrok URL 1" in value:
        ngrok_url_column_index = index + 1
        break

for index, value in enumerate(column_b_values):
    if "rahul-chhatbar" in value:
        row_index = index + 1
        break

if row_index and claimed_port_column_index and product_name_column_index and ngrok_url_column_index and ngrok_url:
    sheet1.update_cell(row_index, claimed_port_column_index, claimed_ports)
    sheet1.update_cell(row_index, product_name_column_index, product_name)
    sheet1.update_cell(row_index, ngrok_url_column_index, ngrok_url)
    print("Row updated successfully!")
else:
    print('"rahul-chhatbar" not found in column B. No updates made.')
