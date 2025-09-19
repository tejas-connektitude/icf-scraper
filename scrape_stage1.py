import requests
from bs4 import BeautifulSoup
import mysql.connector

# Step 1: Scrape the data
url = "https://www.icf-core-sets.org/en/page1.php"
response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "html.parser")

select_box = soup.find("select", {"id": "cs_selection"})
options = select_box.find_all("option")

data = [
    option.get_text(strip=True).replace(u'\xa0', '')
    for option in options
    if "color:blue" not in option.get("style", "") and option.get_text(strip=True) != ""
]

# Step 2: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",      # Change if using remote DB  
    user="root",           # Your MySQL username
    password="root", # Your MySQL password
    database="icf_db_v1"      # Database you created
)

cursor = conn.cursor()

# # Step 3: Create table if not exists
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS core_set (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         name VARCHAR(255) NOT NULL
#     )
# """)

# Step 4: Insert data
for item in data:
    cursor.execute("INSERT INTO core_set (name) VALUES (%s)", (item,))

# Step 5: Commit and Close
conn.commit()
cursor.close()
conn.close()

print("✅ Data saved to MySQL database: icf_db.core_sets")
