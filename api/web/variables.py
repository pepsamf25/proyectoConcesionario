import os
def cargarvariables():
    return {
         "DB_USERNAME": os.getenv("DB_USER"),
        "DB_PASSWORD": os.getenv("DB_PASSWORD"),
        "DB_DATABASE": os.getenv("DB_NAME"),
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "PORT": os.getenv("PORT"),
        "HOST": os.getenv("HOST")
    }
