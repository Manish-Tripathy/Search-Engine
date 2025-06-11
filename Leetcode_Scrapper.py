# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# import time
# from bs4 import BeautifulSoup
# from webdriver_manager.chrome import ChromeDriverManager
#
# # Setup Selenium WebDriver for Google Chrome
# options = Options()
# # options.add_argument('--headless')  # Optional: run Chrome in headless mode
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#
# # Navigate to the page
# url = 'https://leetcode.com/problemset/all/?page='  # Replace with the URL of the page you want to visit
#
# def get_a_tags(url):
#     driver.get(url)
#     time.sleep(8)  # Wait for page to load
#     links = driver.find_elements(By.TAG_NAME, "a")
#     ans = []
#     pattern = "/problems"
#     for i in links:
#         try:
#             if pattern in i.get_attribute("href"):
#                 ans.append(i.get_attribute("href"))
#         except:
#             pass
#     ans = list(set(ans))  # Remove duplicates
#     return ans
#
# final_ans = []
#
# for i in range(1, 3):  # Loop through page numbers
#     final_ans += get_a_tags(url + str(i))
#
# final_ans = list(set(final_ans))  # Final deduplication
#
# # Write results to a file
# with open('lc.txt', 'a') as f:
#     for j in final_ans:
#         f.write(j + '\n')
#
# print(len(final_ans))
#
# driver.quit()

##saving problem statements in folder
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import re

# Setup Selenium WebDriver
options = Options()
# options.add_argument('--headless')  # Uncomment to run in headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Prepare output folder
output_folder = 'leetcode_problems_txt'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load already saved problem names
existing_files = {f[:-4] for f in os.listdir(output_folder) if f.endswith(".txt")}

# Load problem URLs
with open("lc.txt", "r") as f:
    urls = [line.strip() for line in f if line.strip()]

# Extract problem name from URL
def get_problem_name(url):
    match = re.search(r'/problems/([^/]+)/', url)
    return match.group(1) if match else None

# Main scraping loop
for url in urls:
    problem_name = get_problem_name(url)
    if not problem_name:
        print(f"Invalid URL format: {url}")
        continue

    if problem_name in existing_files:
        print(f"Skipping {problem_name}, already scraped.")
        continue

    print(f"Scraping: {problem_name}")
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'elfjS'))
        )
        div = driver.find_element(By.CLASS_NAME, 'elfjS')
        content = div.text.strip()

        with open(os.path.join(output_folder, f"{problem_name}.txt"), "w", encoding="utf-8") as out_file:
            out_file.write(content)
        print(f"Saved {problem_name}.txt")

    except Exception as e:
        print(f"Failed to scrape {problem_name}: {e}")

driver.quit()

