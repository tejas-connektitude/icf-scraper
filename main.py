from automation.icf_scraper import ICFScraper
from database.db import Database

def main():
    scraper = ICFScraper(headless=False)
    db = Database()

    try:
        categories, comprehensive, has_comprehensive = scraper.scrape_first_entry()
        print("ICF Categories:", categories)
        print("Comprehensive:", comprehensive)
        print("Has Comprehensive?", has_comprehensive)

        core_set_id = 1  # Example: first entry in DB is ID=1

        # Insert into mapping tables
        db.insert_core_set_category(core_set_id, categories)
        if comprehensive:
            db.insert_comp_core_set_category(core_set_id, comprehensive)

        # Update has_comprehensive flag in core_set
        db.update_has_comprehensive(core_set_id, has_comprehensive)

    finally:
        scraper.close()
        db.close()

if __name__ == "__main__":
    main()