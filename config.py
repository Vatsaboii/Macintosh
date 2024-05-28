import mysql.connector


# database connection
def db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        passwd="password",
        database="macintosh"
    )


db = db_connection()

# upload directory
UPLOAD_DIR = "uploads"
