from openpyxl import load_workbook, Workbook

JOB_EXCEL_FILE = "job_data.xlsx"
ELIGIBILITY_FILE = "job_eligibility.xlsx"

MIN_CGPA = 7.0  # You can change this threshold

# Load existing job data
wb = load_workbook(JOB_EXCEL_FILE)
ws = wb.active

# Create new workbook for eligibility
new_wb = Workbook()
new_ws = new_wb.active

# Copy headers and add new "Eligibility" column
headers = [cell.value for cell in ws[1]]
headers.append("Eligibility")
new_ws.append(headers)

# Iterate through data rows
for row in ws.iter_rows(min_row=2, values_only=True):
    cgpa = float(row[4])  # assuming CGPA is at column index 4
    eligibility = "Eligible" if cgpa >= MIN_CGPA else "Not Eligible"
    new_ws.append(list(row) + [eligibility])

# Save to new file
new_wb.save(ELIGIBILITY_FILE)
print(f"Eligibility data saved to {ELIGIBILITY_FILE}")
