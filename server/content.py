from connection import connection
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


def content_api_result(song_name, artist):
    # Establish connection
    conn = connection()
    cursor = conn.cursor(buffered=True)

    try:
        # Get genre and danceability
        if artist == "not_present":
            query = "SELECT genre, danceability FROM song_info WHERE trackname=%s"
            cursor.execute(query, (song_name,))
        else:
            query = "SELECT genre, danceability FROM song_info WHERE trackname=%s and artist = %s"
            cursor.execute(query, (song_name, artist))
        genre_and_danceability = cursor.fetchone()
        # Get filtered data
        query = "SELECT songid, trackname, artist, album, genre, tags, img FROM song_info WHERE genre = %s and danceability = %s"
        cursor.execute(
            query, (genre_and_danceability[0], genre_and_danceability[1]))
        rows = cursor.fetchall()
        # Convert the result into a DataFrame
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=column_names)

        # Convert all to lower case
        df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)

        # vectorizer
        # print(df)
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(df['tags'])

        similarities = cosine_similarity(tfidf_matrix)
        # print(tfidf_matrix)

        song_index = df[df['trackname'] == song_name].index[0]

        distance = similarities[song_index]
        recommended_song_index = sorted(list(enumerate(distance)),
                                        reverse=True, key=lambda x: x[1])[:8]

        result_lst = []
        for i in recommended_song_index:
            views_query = '''
                SELECT SUM(listencount) as views FROM triplets 
                WHERE songid = %s
                GROUP BY songid
                '''
            cursor.execute(views_query, (df.iloc[i[0]]['songid'],))
            views_present = cursor.fetchone()
            if views_present:
                views = views_present[0]
            else:
                views = 0

            result_dict = {
                'songid': df.iloc[i[0]]['songid'],
                'trackname': df.iloc[i[0]]['trackname'],
                'artist': df.iloc[i[0]]['artist'],
                'album': df.iloc[i[0]]['album'],
                'genre': df.iloc[i[0]]['genre'],
                'img': df.iloc[i[0]]['img'],
                'views': views
            }
            result_lst.append(result_dict)
    except:
        return None
    # print(result_lst)
    # print(song_index)
    # print(distance)
    # print(recommended_song_index)
    conn.close()
    return result_lst


# print(content_api_result("kryptonite", "not_present"))
