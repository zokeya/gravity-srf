from dotenv import load_dotenv
import os

from config import settings


load_dotenv()

# Print the values of environment variables
print(settings.database_name)
print(os.getenv("DATABASE_URL"))
print(os.getenv("DATABASE_NAME"))