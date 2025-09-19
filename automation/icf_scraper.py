# automation/icf_scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.config import SELENIUM_CONFIG

class ICFScraper:
    def __init__(self, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def scrape_first_entry(self):
        self.driver.get(SELENIUM_CONFIG["base_url"])

        # Step 1: Select the first entry
        select_element = self.wait.until(EC.presence_of_element_located((By.ID, "cs_selection")))
        select = Select(select_element)
        select.select_by_index(0)

        # Submit
        submit_btn = self.driver.find_element(By.XPATH, "//input[@type='submit' and @value='Submit selection']")
        submit_btn.click()

        # Step 2: Extract codes
        self.wait.until(EC.presence_of_element_located((By.ID, "form")))
        all_selects = self.driver.find_elements(
            By.XPATH, "//form//select[not(@id='cat_selection') and not(@id='cs_sel2')]"
        )

        categories = []
        comprehensive = []
        has_comprehensive = False

        if len(all_selects) >= 1:
            # First block = ICF Categories
            for opt in all_selects[0].find_elements(By.TAG_NAME, "option"):
                text = opt.text.strip()
                if text:
                    categories.append(text.split()[0])

        if len(all_selects) > 1:
            # Second block = Comprehensive Set
            has_comprehensive = True
            for opt in all_selects[1].find_elements(By.TAG_NAME, "option"):
                text = opt.text.strip()
                if text:
                    comprehensive.append(text.split()[0])

        return categories, comprehensive, has_comprehensive


    def close(self):
        self.driver.quit()
