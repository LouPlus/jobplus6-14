from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from jobplus.forms import UserRegForm, LoginForm, CompanyRegForm
from jobplus.models import User

front = Blueprint('front', __name__)


@front.route('/')
def index():
    return render_template('index.html')


@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    action = 'front.login'
    title = '用户登录'

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.userauth.data).first() or User.query.filter_by(email=form.userauth.data).first()
        login_user(user, form.remember_me.data)
        flash('登录成功！', 'success')
        return redirect(url_for('.index'))
    return render_template('justform.html', form=form, action=action, title=title)


@front.route('/userreg', methods=['GET', 'POST'])
def userreg():
    form = UserRegForm()
    action = 'front.userreg'
    title = '用户注册'

    if form.validate_on_submit():
        form.create_user()
        flash('注册成功，请登录!', 'success')
        return redirect(url_for('.login'))
    return render_template('justform.html', form=form, action=action, title=title)


@front.route('/companyreg', methods=['GET', 'POST'])
def companyreg():
    form = CompanyRegForm()
    action = 'front.companyreg'
    title = '企业注册'

    if form.validate_on_submit():
        form.create_company()
        flash('注册成功，请登录!', 'success')
        return redirect(url_for('.login'))
    return render_template('justform.html', form=form, action=action, title=title)


@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录', 'success')
    return redirect(url_for('.index'))
