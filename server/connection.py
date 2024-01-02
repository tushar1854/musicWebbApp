import mysql.connector


def connection():
    try:

        conn = mysql.connector.connect(
            host="YOUR_HOST_NAME",
            user="YOUR_USERNAME",
            password="YOUR_PASSWORD",
            database="YOUR_USERNAME"
        )

        return conn
    except Exception as e:
        return f"Error: {e}"
