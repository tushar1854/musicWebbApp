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
    return jsonify(lst)


@app.route("/api/contentbased")
def content_based():
    songname = request.args.get('songname').lower()
    artist = request.args.get('artist').lower()
    lst = content_api_result(songname, artist)
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



if __name__ == '__main__':
    app.run(port=5000, debug=True)
