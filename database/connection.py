
# ==========================================
# LIBRARY MANAGEMENT SYSTEM
# MYSQL DATABASE CONNECTION
# ==========================================

import mysql.connector
from mysql.connector import Error
import configparser
import os

# Read database configuration
config = configparser.ConfigParser()

config_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "config.ini"
)

config.read(config_path)


def connect_database():

    try:

        connection = mysql.connector.connect(

            host=config.get("mysql", "host"),

            port=config.getint("mysql", "port"),

            user=config.get("mysql", "user"),

            password=config.get("mysql", "password"),

            database=config.get("mysql", "database")

        )

        if connection.is_connected():

            return connection

    except Error as e:

        print("Database Connection Error:", e)

    except (configparser.Error, OSError) as e:

        print("Configuration Error:", e)

    return None
