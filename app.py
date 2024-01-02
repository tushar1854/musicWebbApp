from flask import Flask, render_template, redirect, request, url_for, flash, session, jsonify
import requests
from flask_bootstrap import Bootstrap
import threading
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
Bootstrap(app)


# API call functions

result1 = None
result2 = None
# URL = "http://ec2-16-16-58-122.eu-north-1.compute.amazonaws.com"
URL = "http://127.0.0.1:5000"


def content_fetch_data_get_api(songname, artist):
    global result1
    result1 = None

    url = f"{URL}/api/contentbased"
    params = {
        "songname": songname,
        "artist": artist
    }
    response = requests.get(url, params=params)
    result1 = response.json()
    # Make result data to title case
    for element in result1:
        element['trackname'] = element['trackname'].title()
        element['album'] = element['album'].title()
        element['artist'] = element['artist'].title()
        element['genre'] = element['genre'].title()


def collaborative_fetch_data_get_api(songname, artist):

    global result2
    result2 = None
    url = f"{URL}/api/collaborative"
    params = {
        "songname": songname,
        "artist": artist
    }
    response = requests.get(url, params=params)
    result2 = response.json()


def send_data_for_registration(form_data):
    url = f"{URL}/api/registration"
    response = requests.post(url, json=form_data)
    result = response.json()
    return result


def send_data_for_login(form_data):
    url = f"{URL}/api/login"
    response = requests.post(url, json=form_data)
    result = response.json()
    return result


def get_history(userid):
    url = f"{URL}/api/history"
    params = {
        "userid": userid
    }
    response = requests.get(url, params=params)
    result = response.json()
    return result


@app.route('/logout')
def logout():
    session.pop('uid', None)
    return redirect(url_for('home'))


# session['uid'] = False


@app.route("/")
def home():
    url = f"{URL}/api/top50"
    response = requests.get(url)
    result = response.json()
    if "uid" in session:
        return render_template("index.html", top_30=result, current_user=session['uid'])
    else:
        return render_template("index.html", top_30=result, current_user=False)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form_data = {
            "firstname": request.form['first_name'],
            "lastname": request.form['last_name'],
            "country": request.form['country'],
            "email": request.form['email'],
            "password": request.form['pass']
        }
        send_data_for_registration(form_data)
        return redirect(url_for('login'))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form_data = {
            "email": request.form['email'],
            "password": request.form['pass']
        }
        result = send_data_for_login(form_data)
        if result['success'] == 0:
            flash("Incorrect Credentials, Try Again")
            return redirect(url_for('login'))
        elif result['success'] == 1:
            session['uid'] = result['uid']
            return redirect(url_for('home'))
    return render_template("login.html")


@app.route("/recommend", methods=["POST"])
def recommend():

    if request.method == "POST":
        song_text = request.form['song_text']

        if "play" in song_text:
            songtext = song_text.split('by')
            songname = songtext[0].strip()
            artist = songtext[1].strip()
            # thread_one = threading.Thread(
            #     target=song_play, args=(artist.title(), songname.title()))
            # thread_one.start()
            # song_play(artist.title(),songname.title())

        elif "by" in song_text:
            songtext = song_text.split('by')
            songname = songtext[0].strip()
            artist = songtext[1].strip()
        else:
            songname = song_text.strip()
            artist = "not_present"

        # URL content based
        # content_based_lst = content_fetch_data_get_api(songname,artist)
        thread_two = threading.Thread(
            target=content_fetch_data_get_api, args=(songname, artist))
        thread_two.start()

        # URL collaboarative based
        # collaborative_based_lst = collaborative_fetch_data_get_api(songname, artist)
        thread_three = threading.Thread(
            target=collaborative_fetch_data_get_api, args=(songname, artist))
        thread_three.start()

        # Join to complete threading
        thread_two.join()
        thread_three.join()

        content_based_lst = result1
        collaborative_based_lst = result2
        # Increase listen_count
        if "play" in song_text:
            if 'uid' in session:
                url = f"{URL}/api/update_listencount"
                params = {
                    "userid": session['uid'],
                    "songid": content_based_lst[0]['songid']
                }
                requests.post(url, json=params)
        if "uid" in session:
            return render_template("reco.html", content_based_lst=content_based_lst, collaborative_based_lst=collaborative_based_lst, current_user=session['uid'])
        else:
            return render_template("reco.html", content_based_lst=content_based_lst, collaborative_based_lst=collaborative_based_lst, current_user=False)


@app.route("/history")
def history():
    if "uid" in session:
        userid = session['uid']
        history_data = get_history(userid)
        return render_template('history.html', history_data=history_data, current_user=session['uid'])
    return "You Have To Login First"


if __name__ == '__main__':
    app.run(port=8000, debug=True)
