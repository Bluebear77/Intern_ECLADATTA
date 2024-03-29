import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = ["pandas", "xlsxwriter", "openpyxl"]

# Install the required packages
for package in required_packages:
    install(package)
    
import pandas as pd

# List of CSV files to be included in the spreadsheet
csv_files = [
    'Invalid-ToTTo-Page-ID-URLs.csv',
    'LOGICNLG-Title-Format-URLs.csv',
    'ToTTO-Page-ID-URLs.csv',
    'LOGICNLG-Original-URLs.csv',
    'Skipped-LOGICNLG-URLs.csv',
    'ToTTo-Orignial-URLs.csv'
]

# Name of the output Excel file
output_excel_file = 'LOGICNLG & ToTTo Overview.xlsx'

# Create a Pandas Excel writer using XlsxWriter as the engine
with pd.ExcelWriter(output_excel_file, engine='xlsxwriter') as writer:
    # Loop through the list of CSV files
    for csv_file in csv_files:
        # Read each CSV file into a DataFrame
        df = pd.read_csv(csv_file)
        # Extract the filename without the extension to use as the sheet name
        sheet_name = csv_file.replace('.csv', '')
        # Write the DataFrame to a specific sheet
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f'All CSV files have been successfully combined into {output_excel_file}.')
