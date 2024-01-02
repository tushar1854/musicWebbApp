from connection import connection
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def collaborative_api_result(song_name, artist):
    # Establish connection
    conn = connection()
    cursor = conn.cursor(buffered=True)

    try:
        # Get genre and danceability
        if artist == "not_present":
            query = "SELECT songid, genre, danceability FROM song_info WHERE trackname=%s"
            cursor.execute(query, (song_name,))
        else:
            query = "SELECT songid, genre, danceability FROM song_info WHERE trackname=%s and artist = %s"
            cursor.execute(query, (song_name, artist))
        get_song_id = cursor.fetchone()

        # Get all triplets data
        # triplets_query = "SELECT userid, songid, listencount FROM triplets ORDER BY songid DESC LIMIT 2000"
        # cursor.execute(triplets_query)
        # all_rows = cursor.fetchall()
        # all_distinct = "SELECT DISTINCT songid FROM triplets"
        # cursor.execute(all_distinct)
        # all_distinct_rows = cursor.fetchall()
        # print(len(all_distinct_rows))

        triplets_query = '''SELECT userid, songid, listencount
                        FROM triplets
                        WHERE userid IN (
                            SELECT userid
                            FROM triplets
                            WHERE songid = %s
                        )
                        '''
        cursor.execute(triplets_query, (get_song_id[0],))
        all_rows = cursor.fetchall()
        # print(all_rows)

        # Convert all_rows to df
        column_names = [desc[0] for desc in cursor.description]
        triplets_df = pd.DataFrame(all_rows, columns=column_names)

        # Convert it into pivot table
        pt = triplets_df.pivot_table(
            index='songid', columns='userid', values='listencount')
        pt.fillna(0, inplace=True)

        # Calculate cosine_similarity
        similarity_score = cosine_similarity(pt)
        similarity_df = pd.DataFrame(
            similarity_score, columns=pt.index, index=pt.index)

        # Sort on the bases of songid
        sorted_df = similarity_df.sort_values(get_song_id[0], ascending=False)

        # Get first 8 sorted songs (remove the searched song here )
        sorted_df = sorted_df.index[1:8]
        sorted_tuple = tuple(sorted_df)

        # Get all song detail related to that song_id
        query = "SELECT songid, trackname, artist, album, genre, img FROM song_info WHERE songid in (%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, sorted_tuple)
        recommended_song_lst = cursor.fetchall()

        result_lst = []
        for song in recommended_song_lst:
            # Calculate Views
            views_query = '''
                SELECT SUM(listencount) as views FROM triplets
                WHERE songid = %s
                GROUP BY songid
                '''

            cursor.execute(views_query, (song[0],))
            views_present = cursor.fetchone()
            if views_present:
                views = views_present[0]
            else:
                views = 0

            result_dict = {
                'songid': song[0],
                'trackname': song[1],
                'artist': song[2],
                'album': song[3],
                'genre': song[4].title(),
                'img': song[5],
                'views': views
            }
            result_lst.append(result_dict)
    except:
        return None
    conn.close()
    return result_lst


# print(collaborative_api_result("so high", "sidhu moose wala"))
