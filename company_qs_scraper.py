from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

driver = webdriver.Chrome()  # Make sure ChromeDriver is installed and in your PATH

# Navigate to the GitHub README
url = "https://github.com/hxu296/leetcode-company-wise-problems-2022?tab=readme-ov-file#deutsche-bank"
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Adjust the sleep time as needed

# Initialize a list to store the scraped data
data = []

# Find all the tables in the README
tables = driver.find_elements(By.TAG_NAME, "table")

# Skip the first few irrelevant tables
start_index = 2  # Adjust this based on the number of irrelevant tables
relevant_tables = tables[start_index:]

# Iterate through each relevant table
for table in relevant_tables:
    try:
        # Find the company name (from the nearest preceding heading)
        company_heading = table.find_element(By.XPATH, "./preceding::h2[1]")
        company_name = company_heading.text.strip()
    except Exception as e:
        print(f"Could not find company name for table: {e}")
        company_name = "Unknown"  # Assign a default value

    # Find all rows in the table
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Iterate through each row
    for row in rows:
        # Skip header rows
        if row.find_elements(By.TAG_NAME, "th"):
            continue

        # Find all columns in the row
        cols = row.find_elements(By.TAG_NAME, "td")

        # Skip rows with insufficient columns
        if len(cols) < 4:
            print(f"Skipping row with insufficient columns: {row.text}")  # Debugging line
            continue

        # Extract the text from each column
        occurrence = cols[0].text
        problem = cols[1].text
        difficulty = cols[2].text
        solution = cols[3].text

        # Format the problem URL
        problem_url = f"https://leetcode.com/problems/{problem.lower().replace(' ', '-')}/"

        # Append the data to the list
        print(company_name, occurrence, problem, problem_url, difficulty, solution)
        data.append([company_name, occurrence, problem, problem_url, difficulty, solution])

# Close the WebDriver
driver.quit()

# Print the scraped data
for entry in data:
    print(
        f"Company: {entry[0]}, Occurrence: {entry[1]}, Problem: {entry[2]}, Problem URL: {entry[3]}, Difficulty: {entry[4]}, Solution: {entry[5]}")

# Save the data to a CSV file
with open('leetcode_problems.csv', 'w', newline = '', encoding = 'utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Company", "Occurrence", "Problem", "Problem URL", "Difficulty", "Solution"])
    writer.writerows(data)