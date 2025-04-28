from decouple import config

# Load the token from the environment variables
TELEGRAM_TOKEN = config("TELEGRAM_TOKEN")
