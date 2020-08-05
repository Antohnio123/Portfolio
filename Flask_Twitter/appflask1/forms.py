from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from appflask1.models import User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class MessageForm(FlaskForm):
    message_text = StringField('Текст сообщения', validators=[DataRequired()])
    submit = SubmitField('Отправить сообщение')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    repassword = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
# , Email()  - валидатор, для которого пришлось pip install email_validator

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Имя занято. Выберите другое.')

    def validate_repassword(self, repassword):
        password = self.password
        if repassword.data != password.data:
            raise ValidationError('Пароли не совпадают!  Введите правильно.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Емейл-адрес некорректен или занят. Введите другой.')
    # так как эти два метода называются validate_<имя поля формы>, Flask автоматически
    # считатет их валидаторами для указанных полей и добавляет их в валидаторы