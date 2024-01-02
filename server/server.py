from flask import Flask, request, jsonify, session
# import fcntl
# Other modules
from registration import insert_data_into_registration
from login import insert_data_into_login
from top50 import get_top_50_song
from increase_listencount import update_listen_count
# from spotify import get_access_token, get_images_lst
from content import content_api_result
from collaborative import collaborative_api_result
from history import history_result

# Your Spotify API credentials
CLIENT_ID = "c8500a3536794491ad7987729b8b5dc0"
CLIENT_SECRET = "59cf177d543c49929c094ec1393c047e"
ACCESS_TOKEN_URL = "https://accounts.spotify.com/api/token"
BASE_URL = "https://api.spotify.com/v1/search"


app = Flask(__name__)


@app.route("/api/registration", methods=['POST'])
def registration():
    data = request.json
    result = insert_data_into_registration(data)
    return jsonify(result)


@app.route("/api/login", methods=['POST'])
def login():
    data = request.json
    result = insert_data_into_login(data)
    return jsonify(result)


@app.route("/api/top50")
def top50():
    lst = get_top_50_song()
    # access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN_URL)
    # for i in range(len(lst)):
    #     # Exception
    #     if lst[i]["artist"] == "Florence + The Machine":
    #         artist = "The Machine"
    #     else:
    #         artist = lst[i]["artist"]
    #     img = get_images_lst(lst[i]["trackname"],
    #                          artist, BASE_URL, access_token)
    #     lst[i]["img"] = img

    return jsonify(lst)


@app.route("/api/contentbased")
def content_based():
    songname = request.args.get('songname').lower()
    artist = request.args.get('artist').lower()
    lst = content_api_result(songname, artist)
    # For fetching img
    # access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN_URL)
    # for i in range(len(lst)):
    #     img = get_images_lst(lst[i]['trackname'],
    #                          lst[i]['artist'], BASE_URL, access_token)
    #     lst[i]["img"] = img

    return lst


@app.route("/api/collaborative")
def collaboarative_based():
    songname = request.args.get('songname').lower()
    artist = request.args.get('artist').lower()
    lst = collaborative_api_result(songname, artist)
    return lst


@app.route("/api/update_listencount", methods=["POST"])
def listen_count_update():
    data = request.json
    result = update_listen_count(data)
    return jsonify(result)


@app.route("/api/history")
def history():
    userid = request.args.get('userid')
    print(userid)
    result = history_result(userid)
    return jsonify(result)


# if __name__ == '__main__':
#     app.run(host="0.0.0.0")
if __name__ == '__main__':
    app.run(port=5000, debug=True)
