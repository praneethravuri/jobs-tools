import requests
from bs4 import BeautifulSoup
import csv

url = "https://h1bdata.info/topcompanies.php"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
table = soup.find('table', {'class': 'table'})

# Get all table rows including the header
rows = table.find_all("tr")

# Extract the header using th tags
header = [i.get_text(strip=True) for i in rows[0].find_all("th")]

# Extract the data using td tags, skipping the first row which is the header
data = [[i.get_text(strip=True) for i in row.find_all("td")] for row in rows[1:]]

# Combine header and data
table_data = [header] + data

with open("companies.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(table_data)
