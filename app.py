from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

login_manager = LoginManager()
login_manager.init_app(app)

# Kullanıcı modeli


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


users = [
    User(1, 'admin', generate_password_hash('admin'))  # Örnek kullanıcı
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/movies')
@login_required
def movies():
    return render_template('movie_list.html')


@login_manager.user_loader
def load_user(user_id):
    return next((user for user in users if user.id == int(user_id)), None)

# SQLite veritabanına bağlanma


def connect_db():
    return sqlite3.connect('movies.db')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((user for user in users if user.username ==
                    username and check_password_hash(user.password, password)), None)
        if user:
            login_user(user)
            return redirect(url_for('admin_panel'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin_panel')
@login_required
def admin_panel():
    return render_template('admin_panel.html')


@app.route('/films', methods=['GET'])
def get_films():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM films')
    films = cursor.fetchall()

    conn.close()

    return jsonify(films)


@app.route('/films/<int:id>', methods=['GET'])
def get_film(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM films WHERE id = ?', (id,))
    film = cursor.fetchone()

    conn.close()

    return jsonify(film)


@app.route('/adddfilms', methods=['POST'])
@login_required
def add_film():
    title = request.form['title']
    director = request.form['director']
    genre = request.form['genre']
    review = request.form['review']
    movie_img = request.form['movie_img']

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO films (title, director, genre, review, movie_img) VALUES (?, ?, ?, ?, ?)',
                   (title, director, genre, review, movie_img))
    conn.commit()

    conn.close()

    return "Film added successfully"


@app.route('/editfilm/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_film(id):
    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        genre = request.form['genre']
        review = request.form['review']
        movie_img = request.form['movie_img']

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute('UPDATE films SET title=?, director=?, genre=?, review=?, movie_img=? WHERE id=?',
                       (title, director, genre, review, movie_img, id))
        conn.commit()

        conn.close()

        return "Film updated successfully"


@app.route('/removefilm/<int:id>', methods=['DELETE'])
@login_required
def remove_film(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM films WHERE id = ?', (id,))
    conn.commit()

    conn.close()

    return "Film removed successfully"


if __name__ == '__main__':
    app.run(debug=True)
