from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, InputRequired, StopValidation
from jobplus.models import db, User


class UserRegForm(FlaskForm):

    username = StringField('用户名', validators=[InputRequired(message='用户名长度应在3~24个字符之间'), Length(3, 24, message='用户名长度应在3~24个字符之间')])
    email = StringField('邮箱', validators=[InputRequired(message='请输入合法的Email地址'), Email(message='请输入合法的Email地址')])
    password = PasswordField('密码', validators=[InputRequired(message='密码长度应在6~24个字符之间'), Length(6, 24, message='密码长度应在6~24个字符之间')])
    repeat_password = PasswordField('重复密码', validators=[InputRequired(message='两次输入的密码不一致'), EqualTo('password', message='两次输入的密码不一致')])
    submit = SubmitField('提交')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


class LoginForm(FlaskForm):

    userauth = StringField('用户名/邮箱', validators=[InputRequired(message='请输入合法的用户名或Email地址'), Length(3, 24, message='请输入合法的用户名或Email地址')])
    password = PasswordField('密码', validators=[InputRequired(message='密码不正确'), Length(6, 24, message='密码不正确')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_userauth(self, field):
        if not User.query.filter_by(username=field.data).first() and not User.query.filter_by(email=field.data).first():
            raise StopValidation('用户不存在')

    def validate_password(self, field):
        user = User.query.filter_by(username=self.userauth.data).first() or User.query.filter_by(email=self.userauth.data).first()
        if user and not user.check_password(field.data):
            raise ValueError('密码不正确')




