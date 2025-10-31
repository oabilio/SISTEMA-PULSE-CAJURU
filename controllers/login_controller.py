# controllers/login_controller.py
from flask import Blueprint, request, render_template, redirect
from flask_login import login_user, logout_user, login_required, UserMixin
from data import users

login_bp = Blueprint("login", __name__, template_folder="../views")

class User(UserMixin):
    def __init__(self, username):
        self.id = username

    def get_id(self):
        return self.id
    
@login_bp.route('/login', methods=['GET'])
def index():
    return render_template('login.html')

@login_bp.route('/validated_user', methods=['GET', 'POST'])
def validated_user():
    if request.method == 'POST':
        user = request.form['email']
        password = request.form['password']

        if user in users and users[user] == password:
            user_obj = User(user)
            login_user(user_obj)
            return redirect('/home')
        else:
            return '<h1>Informações erradas...</h1>'

@login_bp.route('/logoff')
@login_required
def logout():
    logout_user()
    return redirect('/login')
