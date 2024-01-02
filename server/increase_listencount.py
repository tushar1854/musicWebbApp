from connection import connection


def update_listen_count(data):
    try:
        conn = connection()
        cursor = conn.cursor(buffered=True)

        query = "UPDATE triplets SET listencount = listencount + 1 WHERE userid = %s AND songid= %s"
        send_data = (
            data['userid'],
            data['songid']
        )
        cursor.execute(
            query, send_data)
        # Check if any rows were affected
        if cursor.rowcount > 0:
            result = {"message": "update 1 successfully"}
        else:
            # print("User ID and/or Song ID not found")
            query = "INSERT INTO triplets(userid, songid, listencount) VALUES(%s, %s, %s)"
            send_data = (
                data['userid'],
                data['songid'],
                1
            )
            cursor.execute(query, send_data)

            result = {"message": "update 2 successfully"}
        conn.commit()
        return result
    except Exception as e:
        return f"Error: {e}"


# data = {
#     "userid": "fffe6d1d8500f1c1f31bd63abce35c0f975a86bf",
#     "songid": "SOYLAOB12A8C1342AE"
# }
# update_listen_count("data")
