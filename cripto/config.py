import os
from dotenv import load_dotenv
load_dotenv()


apikey = os.getenv('API_IO')
path_database = os.getenv('PATH_SQLITE')