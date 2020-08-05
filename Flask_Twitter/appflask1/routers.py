from flask import render_template, flash, redirect, url_for, request
# Cookie файлы хранятся на стороне пользователя, а session-информация - на сервере
from appflask1 import app, db
from appflask1.forms import LoginForm, RegistrationForm, MessageForm
from flask_login import current_user, login_user, logout_user, login_required
from appflask1.models import User, Posts
from werkzeug.urls import url_parse
from flask import make_response, session


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    # if 'username' in session:
    #     return '<h1>Session: {}</h1>'.format(session['username'])
    # return '<h1>No session</h1>'
    # Дальнейший код функции индекс не используем для проверки сессий!

    # user={'username': 'Anton'}
    # Mock-кусок, пользователь-вставка на время, пока нет регистрации пользователей
    form = MessageForm()
    posts = db.session.query(Posts).order_by(Posts.timestamp.desc()).limit(30)
    # Выводим посты из БАЗЫ ДАННЫХ в обратном порядке!
    if form.validate_on_submit():
        post = Posts(body=form.message_text.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Вы оставили своё сообщение.')
        return redirect(url_for('index'))
    # posts = [
    #     {'author': {'username': 'Алексей'}, 'body': 'Привет!'},
    #     {'author': {'username': 'Елена'}, 'body': 'Отличный день сегодня!'},
    #     {'author': {'username': 'Саня'}, 'body': 'Кто хочет погулять?'},
    # ]
    return render_template('index.html', title='Домашняя страница', user=current_user, posts=posts, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Тут лектор прописал date вместо data
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный пользователь или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        # flash('Вход запрошен для пользователя {}, запомнить = {}'.format(form.username.data, form.remember_me.data))
        # Сюда вставить валидацию ??
        # return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Вы уже авторизованы. Чтобы зарегистрировать другого пользователя, выйдите из текущего аккаунта.')
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Если форма засубмичена и прошла валидацию...
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы зарегистрировались удачно.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация пользователя', form=form)
#  -----------------------------------------------------------------------------
# @app.route('/setsession', methods= ['GET', 'POST'])
# def setsession():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#     <form action="" method="post">
#     <p><input type="text" name="username">
#      <p><input type="submit" value="Логин">'''
# # Почему-то работает ТОЛЬКО с незакрытыми тегами.  С закрытыми выдаёт форму, но не сабмитит.
#
#
# @app.route('/unsettsession')
# def unsetsession():
#     session.pop('username', None)
#     return redirect(url_for('index'))
#
# app.secret_key = 'SOME_SECRET'
#  -----------------------------------------------------------------------------
# @app.route('/setcookie')
# def setcookie():
#     resp = make_response(redirect(url_for('index')))
#     resp.set_cookie('flask_cookie', 'cookie_value')
#     return resp
#
#
# @app.route('/getcookie')
# def getcookie():
#     flask_cookie = request.cookies.get('flask_cookie')
#     # Если куков не будет, выйдет значение None, ошибки не будет
#     return '<h1>Cookie: ' + flask_cookie +'</h1>'
#  -----------------------------------------------------------------------------
