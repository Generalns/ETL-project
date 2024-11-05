
import json
import psycopg2
import redis
from infra.postgresql_connector import connect_postgresql
from infra.redis_connector import connect_redis
from datetime import datetime


class PostgreSQLPipeline:
    dummy = "dummy value"

    def __init__(self):

        self.connection = connect_postgresql()

        self.cur = self.connection.cursor()

        self.cur.execute("""DROP TABLE IF EXISTS raw_table""")
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS raw_table (
                         id SERIAL PRIMARY KEY,
                         slug TEXT,
                         req_id TEXT,
                         title VARCHAR(255),
                         description TEXT,
                         street_address TEXT,
                         city TEXT,
                         state TEXT,
                         country_code TEXT,
                         postal_code TEXT,
                         location_type TEXT,
                         latitude TEXT,
                         longitude TEXT,
                         categories TEXT,
                         tags TEXT,
                         brand TEXT,
                         promotion_value TEXT,
                         salary_currency TEXT,
                         salary_value TEXT,
                         salary_min_value TEXT,
                         salary_max_value TEXT,
                         benefits TEXT,
                         employment_type TEXT,
                         hiring_organization TEXT,
                         source TEXT,
                         apply_url TEXT,
                         internal TEXT,
                         searchable TEXT,
                         applyable TEXT,
                         li_easy_applyable TEXT,
                         ats_code TEXT,
                         meta_data TEXT,
                         update_date TEXT,
                         create_date TEXT,
                         category TEXT,
                         full_location TEXT,
                         short_location TEXT,
                         location_name TEXT,
                         department TEXT,
                         recruiter_id TEXT,
                         posted_date TEXT,
                         posting_expiry_date TEXT,
                         work_hours TEXT,
                         salary_frequency TEXT
                         )""")
        self.connection.commit()

    def list2string(self, lst):
        return ", ".join(str(l) for l in lst)

    def process_item(self, item, spider):
        try:
            insert_query = f"""INSERT INTO raw_table (
                slug, title, description, street_address, city, state, country_code, 
                postal_code, location_type, latitude, longitude, categories, tags, brand, promotion_value,
                salary_currency, salary_value, salary_min_value, salary_max_value, benefits, employment_type,
                hiring_organization, source, apply_url, internal, searchable, applyable,
                li_easy_applyable, ats_code, meta_data, update_date, create_date, category, full_location,
                short_location, location_name, department, recruiter_id, posted_date, posting_expiry_date,
                work_hours, salary_frequency
                ) VALUES (
                '{item['slug']}',
                '{item['title']}',
                '{item['description']}',
                '{item['street_address']}',
                '{item['city']}',
                '{item['state']}',
                '{item['country_code']}',
                '{item['postal_code']}',
                '{item['location_type']}',
                '{item['latitude']}',
                '{item['longitude']}',
                '{item['categories']}',
                '{item['tags']}',
                '{item['brand']}',
                '{item['promotion_value']}',
                '{item.get('salary_currency', "NA")}',
                '{item.get('salary_value', "NA")}',
                '{item.get('salary_min_value', "NA")}',
                '{item.get('salary_max_value', "NA")}',
                '{item.get('benefits', "NA")}',
                '{item.get('employment_type', "NA")}',
                '{item.get('hiring_organization', "NA")}',
                '{item.get('source', "NA")}',
                '{item.get('apply_url', "NA")}',
                '{item.get('internal', "NA")}',
                '{item.get('searchable', "NA")}',
                '{item.get('applyable', "NA")}',
                '{item.get('li_easy_applyable', "NA")}',
                '{item.get('ats_code', "NA")}',
                '{item.get('meta_data', "NA")}',
                '{item.get('update_date', "NA")}',
                '{item.get('create_date', "NA")}',
                '{item.get('category', "NA")}',
                '{item.get('full_location', "NA")}',
                '{item.get('short_location', "NA")}',
                '{item.get('location_name', "NA")}',
                '{item.get('department', "NA")}',
                '{item.get('recruiter_id', "NA")}',
                '{item.get('posted_date', "NA")}',
                '{item.get('posting_expiry_date', "NA")}',
                '{item.get('work_hours', "NA")}',
                '{item.get('salary_frequency', "NA")}'
                 )"""
            self.cur.execute(insert_query)
            self.connection.commit()
        except:
            self.connection.rollback()
            raise
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.connection.close()
        self.cur.close()


class RedisPipeline:
    def open_spider(self, spider):
        self.redis_client = connect_redis()

    def process_item(self, item, spider):
        item_key = f"{item['slug']}_{item['req_id']}"

        # Check if the item is already cached
        if not self.redis_client.exists(item_key):
            # Cache the item
            self.redis_client.set(item_key, json.dumps(dict(item)))
            return item
        else:
            spider.logger.info(f"Item already cached: {item_key}")
            return None
