

import os

# Base directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Directories
DATA_DIR = os.path.join(BASE_DIR, "data")
SCRAPED_DATA_DIR = os.path.join(DATA_DIR, "scraped_data")
ID_MEMORY_DIR = os.path.join(DATA_DIR, "id_memory")
ID_STATE_DIR = os.path.join(DATA_DIR, "id_state")
SPREADSHEETS_DIR = os.path.join(DATA_DIR, "Spreadsheets")
SCRIPTS_DIR = os.path.join(DATA_DIR, "scripts")
APP_DIR = os.path.join(BASE_DIR, "app")

# Files
excel_file_name = "Wesco Inventory All 250324.xls"
TEST_WEBSITE_DATA_PATH = os.path.join(SCRAPED_DATA_DIR, "test_website_data.txt")
INVENTORY_XLS_PATH = os.path.join(SPREADSHEETS_DIR, excel_file_name)
ALL_LINKS_PATH = os.path.join(SCRIPTS_DIR, "all_links.txt")