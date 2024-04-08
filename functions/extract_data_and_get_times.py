"""Extract data from web"""
import datetime
import json

from bs4 import BeautifulSoup
import pandas
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from requests import RequestException

from utils.base_class import BaseClass
from utils.document_and_names import DocumentsAndPaths


class ExtractDataAndGetTimes:
    """Extract data from web"""
    def __init__(self, driver, logger):
        self.driver = driver
        self.base_class = BaseClass(self.driver)
        self.logger = logger

    def extract_data(self):
        """Full steps to extract data"""
        time_sheet = self.scrap_data()
        self.insert_data_to_mongodb(time_sheet, DocumentsAndPaths.mongodb_collection)
        self.insert_data_to_excel(time_sheet, DocumentsAndPaths.file_path_excel)
        hours_time_tables = self.get_timetables_list()
        duplicate_hours = self.duplicate_hours(hours_time_tables)
        self.format_to_json_if_duplicates(duplicate_hours,
                                          hours_time_tables, DocumentsAndPaths.file_path_json)

    def scrap_data(self):
        """Insert data to DataFrame"""
        try:
            page_content = self.driver.page_source
            soup = BeautifulSoup(page_content, "html.parser")
            scraped_data = ((soup.find('div', class_='timetable-container'))
                            .find('table', class_='table-bordered').find_all('tr'))
            time_tables = []

            # Skip first line from scraped_data (Darbo diena/Sestadienis/Sekmadienis)
            for row in scraped_data[1:]:
                content = {
                    # Find all th and insert text to row, strip.True removes
                    # any whitespaces from text
                    DocumentsAndPaths.column_hours: row.find('th').get_text(strip=True),
                    # Adding all 'a' elements to a list as text removing all
                    # the whitespaces from text
                    DocumentsAndPaths.column_minutes: list(
                        map(lambda a: a.get_text(strip=True), row.find_all('a')))
                }
                time_tables.append(content)
            # Insert time_table to data frame
            return pandas.DataFrame(time_tables)
        # Exception raised if http request failed (bs4 exception)
        except RequestException as e:
            self.logger.error(f"Time table data was not scrapped: {e}")
            return None

    def insert_data_to_excel(self, df, file_path):
        """Create/overwrite and insert data to excel"""
        # Creates/ overwrites excel and inserts data to excel
        # naming sheet 'Timetables', index false remove index numbers
        try:
            with pandas.ExcelWriter(file_path, engine='xlsxwriter', ) as writer:
                df.to_excel(writer, index=False, sheet_name='Timetables')
        except FileNotFoundError as e:
            self.logger.error(f"Excel create failed {e}")

    def insert_data_to_mongodb(self, df, collection_name):
        """Create/overwrite and insert data to MongoDB"""
        try:
            # Insert data to dictionary
            time_tables = df.to_dict(orient='records')
            # connect to mongoDB database client
            client = MongoClient(DocumentsAndPaths.mongo_client)
            db = client[DocumentsAndPaths.mongodb]
            collection = db[collection_name]
            # drop old collection
            collection.drop()
            # insert to database the newest collection
            collection.insert_many(time_tables)
            self.logger.info("Data inserted to MongoDB database")
        # Exception occurs if data will not be inserted to Mongo DB (MongoBD exception)
        except PyMongoError as e:
            self.logger.error(f"Data was not inserted into the MongoDB database: {e}")

    def get_timetables_list(self):
        """Create timetable lists"""
        # Takes current hour
        current_hour = int(datetime.datetime.now().strftime('%H'))
        # Set needed hours to a list -1 0 +1
        all_hours = [current_hour - 1, current_hour, current_hour + 1]

        # Connect to mongoDB
        # pylint: disable=line-too-long
        col = MongoClient(DocumentsAndPaths.mongo_client)[DocumentsAndPaths.mongodb][DocumentsAndPaths.mongodb_collection]

        hour_data = []

        for row in col.find():
            hour = int(row.get('Hours'))
            minutes = row.get('Minutes')
            if hour in all_hours and minutes:
                # Format minutes to int to add 00
                minute_list = []
                for minute in minutes:
                    minute_list.append(f"{hour:02}:{int(minute):02}")
                # Append the hour and minute list as a tuple
                hour_data.append((hour, minute_list))

        # Check if hours in the database print or return the hour_data list
        for hour in all_hours:
            hour_minutes = []
            for entry in hour_data:
                if entry[0] == hour:
                    hour_minutes = entry[1]
                    break
            if hour_minutes:
                self.logger.info(f"Data for {hour:02} hour: {hour_minutes}")
        return hour_data

    def duplicate_hours(self, hour_data):
        """Check duplicate minutes in lists"""
        # Find duplicate minutes across three lists
        # Store minutes and hours
        all_minutes = {}
        duplicates = []

        # Iterate over hour_data to find duplicate minutes and their corresponding hours
        for data in hour_data:
            hour, minute_list = data
            for minute_str in minute_list:
                minute = minute_str.split(":")[1]
                if minute in all_minutes:
                    if minute not in duplicates:
                        duplicates.append(minute)
                    all_minutes[minute].append(hour)
                else:
                    all_minutes[minute] = [hour]

        duplicate_hours = []
        if duplicates:
            for minute in duplicates:
                duplicate_hours.append(all_minutes[minute])
            self.logger.info(f"Hours that have the same minutes: {duplicate_hours} ")
        else:
            self.logger.info("There were no hours with the same minutes.")
        # Return all hours that have duplicate minutes
        return duplicate_hours

    def format_to_json_if_duplicates(self, duplicate_hours, hour_data, path_to_json):
        """Create/overwrite and insert data to JSON"""
        result_json = {}

        # Create set for duplicate hours(now if hour is the same it will be eliminated)
        duplicate_set = set()
        for sublist in duplicate_hours:
            for hour in sublist:
                duplicate_set.add(hour)

        # Convert data of hours that have duplicate minutes to JSON
        for hour, minute_list in hour_data:
            if hour in duplicate_set:
                bus_schedule = {}
                bus_index = 1
                for minute in minute_list:
                    minute_without_hour = minute.split(":")[1]
                    bus_schedule[f"Bus-{bus_index} at minute"] = minute_without_hour
                    bus_index += 1
                if "Time_table" not in result_json:
                    result_json["Time_table"] = {}
                result_json["Time_table"][f"{hour} hours"] = bus_schedule

        if result_json:
            with open(path_to_json, "w", encoding='utf-8') as json_file:
                json.dump(result_json, json_file, indent=4)
            self.logger.info("JSON was created")
        else:
            with open(path_to_json, "w", encoding='utf-8') as json_file:
                json.dump({"Time_tables": result_json}, json_file, indent=4)
            self.logger.info("No times found, JSON is empty")
