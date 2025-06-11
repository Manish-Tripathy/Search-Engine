# import requests
# import time
#
# url = "https://www.codechef.com/api/list/problems"
# headers = {
#     "User-Agent": "Mozilla/5.0"
# }
#
# # Prepare files
# id_file = open("codechef_id.txt", "w", encoding="utf-8")
# code_file = open("codechef_code.txt", "w", encoding="utf-8")
# name_file = open("codechef_name.txt", "w", encoding="utf-8")
# diff_file = open("codechef_difficulty.txt", "w", encoding="utf-8")
# url_file = open("codechef_url.txt", "w", encoding="utf-8")
#
# # Iterate rating ranges
# for start in range(500, 2800, 100):
#     end = start + 100
#     params = {
#         "page": 1,
#         "limit": 50,
#         "sort_by": "difficulty_rating",
#         "sort_order": "asc",
#         "search": "",
#         "category": "rated",
#         "start_rating": start,
#         "end_rating": end,
#         "topic": "",
#         "tags": "",
#         "group": "unattempted"
#     }
#
#     print(f"Fetching {start}-{end}...")
#     response = requests.get(url, params=params, headers=headers)
#
#     if response.status_code == 200:
#         problems = response.json().get("data", [])
#         for p in problems:
#             pid = p.get("id", "")
#             code = p.get("code", "")
#             name = p.get("name", "").replace("\n", " ").replace(",", " ")
#             rating = p.get("difficulty_rating", "")
#             prob_url = f"https://www.codechef.com/problems/{code}"
#
#             id_file.write(f"{pid}\n")
#             code_file.write(f"{code}\n")
#             name_file.write(f"{name}\n")
#             diff_file.write(f"{rating}\n")
#             url_file.write(f"{prob_url}\n")
#     else:
#         print(f"Failed to fetch {start}-{end}, status: {response.status_code}")
#
#     time.sleep(1)
#
# # Close files
# id_file.close()
# code_file.close()
# name_file.close()
# diff_file.close()
# url_file.close()
#
# print("\nSaved all data in separate .txt files.")



import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Load URLs and codes
with open("codechef_url.txt", "r", encoding="utf-8") as f:
    urls = f.read().splitlines()

with open("codechef_code.txt", "r", encoding="utf-8") as f:
    codes = f.read().splitlines()

# Ensure directory exists
folder = "codechef_problems_txt"
os.makedirs(folder, exist_ok=True)

# Loop over URLs and save to corresponding file
for i, (url, code) in enumerate(zip(urls, codes)):
    print(f"[{i+1}/{len(urls)}] Scraping: {code} -> {url}")
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_problemBody_1llav_33"))
        )
        div = driver.find_element(By.CLASS_NAME, "_problemBody_1llav_33")
        content = div.text.strip()

        with open(os.path.join(folder, f"{code}.txt"), "w", encoding="utf-8") as f_out:
            f_out.write(content)

    except Exception as e:
        print(f"❌ Error for {code}: {e}")
        with open(os.path.join(folder, f"{code}.txt"), "w", encoding="utf-8") as f_out:
            f_out.write("ERROR: " + str(e))

    time.sleep(1)  # to be gentle with server

driver.quit()
print("✅ All problem bodies saved to codechef_problems_txt/")
