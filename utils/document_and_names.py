"""Main class for documents and paths"""


# pylint: disable=too-few-public-methods
class DocumentsAndPaths:
    """Main class for documents and paths"""
    url = "https://judu.lt/"

    column_hours = "Hours"
    column_minutes = "Minutes"

    file_path_excel = "./project_files/judu_4g_timetable.xlsx"
    file_path_json = "./project_files/duplicate_data.json"

    mongo_client = "mongodb://localhost:27017"
    mongodb = 'judu'
    mongodb_collection = 'timetables'
