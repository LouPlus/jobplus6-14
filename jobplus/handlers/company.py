from flask import Blueprint, redirect, flash, render_template, url_for
from flask_login import current_user
from jobplus.decorators import company_required
from jobplus.forms import CompanyProfileForm

company = Blueprint('company', __name__, url_prefix='/company')


@company.route('/admin/profile', methods=['GET', 'POST'])
@company_required
def profile():

    form = CompanyProfileForm(obj=current_user.company)
    action = 'company.profile'
    title = '编辑公司信息'

    if form.validate_on_submit():
        form.update_profile(current_user.company)
        flash('信息更新成功', 'success')
        return redirect(url_for('company.profile'))

    return render_template('justform.html', form=form, action=action, title=title, upload=True)