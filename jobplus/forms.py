import os
from hashlib import md5
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, Email, EqualTo, InputRequired, StopValidation, ValidationError
from flask_wtf.file import FileField, FileAllowed
from jobplus.models import db, User, Company


class UserRegForm(FlaskForm):
    username = StringField('用户名', validators=[InputRequired(message='用户名长度应在3~24个字符之间'),
                                              Length(3, 24, message='用户名长度应在3~24个字符之间')])
    email = StringField('邮箱', validators=[InputRequired(message='请输入合法的Email地址'), Email(message='请输入合法的Email地址')])
    password = PasswordField('密码', validators=[InputRequired(message='密码长度应在6~24个字符之间'),
                                               Length(6, 24, message='密码长度应在6~24个字符之间')])
    repeat_password = PasswordField('重复密码', validators=[InputRequired(message='两次输入的密码不一致'),
                                                        EqualTo('password', message='两次输入的密码不一致')])
    submit = SubmitField('提交')

    def create_user(self, company_id=-1):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        if company_id != -1:
            user.company_id = company_id
            user.role = user.ROLE_COMPANY
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经存在')


class UserProfileForm(FlaskForm):
    username = StringField('用户名', render_kw={'readonly': True})
    realname = StringField('真实姓名')
    email = StringField('邮箱', validators=[InputRequired(message='请输入合法的Email地址'), Email(message='请输入合法的Email地址')])
    password = PasswordField('密码')
    phone = StringField('电话')
    resume = FileField('上传简历', validators=[FileAllowed(['pdf'], message='只接受pdf格式简历!')])
    submit = SubmitField('提交')

    def update_profile(self, user):
        user.realname = self.realname.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        print(self.resume.data)
        if self.resume.data:
            filename = md5(user.username.encode("utf-8")).hexdigest() + '_resume.pdf'
            self.resume.data.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                               'static',
                                               'resumes',
                                               filename))
            user.resume_url = url_for('static', filename=os.path.join('resumes', filename))

        db.session.add(user)
        db.session.commit()
        return user

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已关联其他用户')


class CompanyRegForm(UserRegForm):
    company = StringField('企业名称', validators=[InputRequired(message='企业名长度应在3~24个字符之间'),
                                              Length(3, 24, message='企业名长度应在3~24个字符之间')])

    def __init__(self):
        super(CompanyRegForm, self).__init__()
        self._fields.move_to_end('company', False)

    def create_company(self):
        company = Company()
        company.name = self.company.data
        db.session.add(company)
        db.session.commit()
        self.create_user(company.id)

        return company

    def validate_company(self, field):
        if Company.query.filter_by(name=field.data).first():
            raise ValidationError('企业名已经存在')


class CompanyProfileForm(FlaskForm):
    name = StringField('企业名称', validators=[InputRequired(message='企业名长度应在3~24个字符之间'),
                                           Length(3, 24, message='企业名长度应在3~24个字符之间')])
    site = StringField('企业网址', validators=[Length(0, 50, message='长度应在3~50个字符之间')])
    location = StringField('城市', validators=[Length(0, 24, message='长度应在1~24个字符之间')])
    description = StringField('一句话简介', validators=[Length(0, 50, message='长度应在1~50个字符之间')])
    about = StringField('公司详情', validators=[Length(0, 50, message='长度应在1~50个字符之间')])
    tags = StringField('标签', validators=[Length(0, 50, message='长度应在1~50个字符之间')], description='用|隔开')
    stack = StringField('技术栈', validators=[Length(0, 50, message='长度应在1~50个字符之间')], description='用|隔开')
    field = StringField('公司领域', validators=[Length(0, 50, message='长度应在1~50个字符之间')])
    finance = StringField('融资情况', validators=[Length(0, 50, message='长度应在1~50个字符之间')])
    logo_upload = FileField('上传logo', validators=[FileAllowed(['jpg', 'jpeg', 'png'], message='只接受图片格式!')])
    submit = SubmitField('提交')

    def update_profile(self, company):

        for key in ['name', 'site', 'location', 'description', 'about', 'tags', 'stack', 'field', 'finance']:
            setattr(company, key, getattr(self, key).data)

        if self.logo_upload.data:
            filename = md5(str(company.id).encode("utf-8")).hexdigest() + os.path.splitext(self.logo.data.filename)[1]
            self.logo_upload.data.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                               'static',
                                               'logos',
                                               filename))
            company.logo = url_for('static', filename=os.path.join('logos', filename))

        db.session.add(company)
        db.session.commit()
        return company



class LoginForm(FlaskForm):
    userauth = StringField('用户名/邮箱', validators=[InputRequired(message='请输入合法的用户名或Email地址'),
                                                 Length(3, 24, message='请输入合法的用户名或Email地址')])
    password = PasswordField('密码', validators=[InputRequired(message='密码不正确'), Length(6, 24, message='密码不正确')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

    def validate_userauth(self, field):
        if not User.query.filter_by(username=field.data).first() and not User.query.filter_by(email=field.data).first():
            raise StopValidation('用户不存在')

    def validate_password(self, field):
        user = User.query.filter_by(username=self.userauth.data).first() or User.query.filter_by(
            email=self.userauth.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('密码不正确')
