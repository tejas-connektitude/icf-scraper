import re
import mysql.connector
from bs4 import BeautifulSoup

# ---------- Step 1: Parse the local HTML file ----------
with open("whole_icf.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Find the select element with id="cat_selection"
select = soup.find("select", {"id": "cat_selection"})

data = []
if select:
    for option in select.find_all("option"):
        text = option.get_text(" ", strip=True)  # preserve spaces
    
        # Regex: capture code (letters+digits + optional 1 uppercase letter), then name
        m = re.match(r"^([a-z]\d+[A-Z]?)\s+(.+)$", text, re.IGNORECASE)
        if m:
            code = m.group(1).strip()
            name = m.group(2).strip()
            data.append((code, name))
        else:
            # fallback if no match (e.g. group ranges like b110-b139)
            parts = text.split(None, 1)
            if len(parts) == 2:
                code, name = parts
            else:
                code, name = text, ""
            data.append((code, name))

# ---------- Step 2: Insert into MySQL ----------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",           # change if your username is different
        password="root",   # replace with your MySQL password
        database="icf_db_v1"
    )
    cursor = conn.cursor()

    for code, name in data:
        try:
            cursor.execute(
                "INSERT IGNORE INTO icf_category (code, description) VALUES (%s, %s)",
                (code, name)
            )
        except Exception as e:
            print(f"Error inserting {code}: {e}")

    conn.commit()
    print("✅ Data inserted successfully.")

except mysql.connector.Error as err:
    print("MySQL Error:", err)

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals() and conn.is_connected():
        conn.close()
