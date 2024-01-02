from connection import connection
import uuid

# Generate UID


def generate_uid():
    return str(uuid.uuid4())


def insert_data_into_registration(data):
    try:
        # Connect to DB
        conn = connection()
        cursor = conn.cursor()

        query = "INSERT INTO registered_user(uid, firstname, lastname,country, email, password) VALUES (%s,%s, %s, %s, %s, %s)"
        uid = generate_uid()
        send_data = (uid,
                     data['firstname'],
                     data['lastname'],
                     data['country'],
                     data['email'],
                     data['password']
                     )
        cursor.execute(query, send_data)
        conn.commit()
        result = {
            "uid": uid,
            "email": data['email']
        }
        return result
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()
