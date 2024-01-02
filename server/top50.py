from connection import connection


def get_top_50_song():
    # Establish connection
    try:
        conn = connection()
        cursor = conn.cursor()
        # Get most viewd songs
        query = ''' WITH most_viewed AS(
                        SELECT songid, SUM(listencount) as views
                        FROM triplets GROUP BY songid
                        ORDER BY views DESC LIMIT 50
                        )
                    SELECT mv.songid, mv.views, si.trackname, si.artist, si.album, si.genre,si.img
                    FROM most_viewed as mv
                    INNER JOIN song_info as si ON mv.songid = si.songid ORDER BY mv.views DESC
                    '''
        # query = "SELECT songid, SUM(listencount) as views FROM triplets GROUP BY songid ORDER BY views DESC LIMIT 50"
        cursor.execute(query)
        rows = cursor.fetchall()
        lst = []
        for row in rows:
            dicts = {"songid": row[0],
                     "views": row[1],
                     "trackname": row[2],
                     "artist": row[3],
                     "album": row[4],
                     "genre": row[5],
                     "img": row[6]
                     }
            lst.append(dicts)
        return lst
    except Exception as e:
        return f"Error: {e}"

# print(get_top_50_song())
