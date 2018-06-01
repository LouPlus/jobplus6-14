from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from jobplus.forms import UserProfileForm

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    form = UserProfileForm(obj=current_user)
    action = 'user.profile'
    title = '编辑个人信息'

    if form.validate_on_submit():
        form.update_profile(current_user)
        flash('个人信息更新成功', 'success')
        return redirect(url_for('user.profile'))

    return render_template('justform.html', form=form, action=action, title=title, upload=True)