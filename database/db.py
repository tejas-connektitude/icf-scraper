# database/db.py

import mysql.connector
from config.config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()

    def insert_core_set_category(self, core_set_id, category_codes):
        """
        Insert codes into core_set_category table
        """
        for code in category_codes:
            # Find category_id from icf_category
            self.cursor.execute("SELECT category_id FROM icf_category WHERE code = %s", (code,))
            result = self.cursor.fetchone()
            if result:
                category_id = result[0]
                self.cursor.execute(
                    "INSERT IGNORE INTO core_set_category (core_set_id, category_id) VALUES (%s, %s)",
                    (core_set_id, category_id)
                )
        self.conn.commit()

    def insert_comp_core_set_category(self, core_set_id, category_codes):
        """
        Insert codes into comp_core_set_category table
        """
        for code in category_codes:
            self.cursor.execute("SELECT category_id FROM icf_category WHERE code = %s", (code,))
            result = self.cursor.fetchone()
            if result:
                category_id = result[0]
                self.cursor.execute(
                    "INSERT IGNORE INTO comp_core_set_category (core_set_id, category_id) VALUES (%s, %s)",
                    (core_set_id, category_id)
                )
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def update_has_comprehensive(self, core_set_id, flag):
        """
        Update has_comprehensive flag in core_set table
        """
        self.cursor.execute(
            "UPDATE core_set SET has_comprehensive = %s WHERE core_set_id = %s",
            (1 if flag else 0, core_set_id)
        )
        self.conn.commit()
