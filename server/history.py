from connection import connection


def history_result(userid):
    # Establish connection
    conn = connection()
    cursor = conn.cursor(buffered=True)

    try:
        query = '''
                WITH filtered_triplets AS(
                    SELECT * FROM triplets
                    WHERE userid = %s 
                )
                SELECT t.songid, t.listencount, si.trackname, si.artist, si.album, si.genre, si.img
                FROM filtered_triplets as t
                JOIN song_info as si 
                ON t.songid = si.songid ORDER BY t.listencount DESC;
                '''
        cursor.execute(query, (userid,))
        rows = cursor.fetchall()
        lst = []
        for row in rows:
            dicts = {"songid": row[0],
                     "listencount": row[1],
                     "trackname": row[2],
                     "artist": row[3],
                     "album": row[4],
                     "genre": row[5],
                     "img": row[6]
                     }
            lst.append(dicts)
    except:
        return None

    return lst


# print(history("199d78ba-60b0-4609-9b96-4eb1963f0faa"))
