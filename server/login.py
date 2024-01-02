from connection import connection


def insert_data_into_login(data):
    try:
        conn = connection()
        cursor = conn.cursor(buffered=True)

        # Check data in registration table
        query = "SELECT uid, firstname, email, password FROM registered_user WHERE email = %s and password = %s"
        data = (
            data['email'],
            data['password']
        )
        cursor.execute(query, data)
        row = cursor.fetchone()
        # Login table
        if row is None:
            result = {
                "success": 0,
                "message": "login unsuccessful"
            }
            return result
        else:
            query = "INSERT INTO login(uid, firstname, email, password) VALUES(%s, %s, %s, %s)"
            data = (
                row[0],  # uid
                row[1],  # firstName
                row[2],  # email
                row[3]   # password
            )
            cursor.execute(query, data)
            conn.commit()
            result = {
                "success": 1,
                "uid": row[0],
                "email": row[2]
            }
            return result
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()


# insert_data()
