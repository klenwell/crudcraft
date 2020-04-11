"""
# Cruds Controller
"""
from controllers import (app, render_template, g, authenticated_only, redirect_on_cancel,
                         request, redirect, url_for)
from models.crud import Crud
from forms.crud import CrudForm


#
# Cruds
#
@app.route('/cruds/', methods=['GET'])
def cruds_index():
    cruds = Crud.s_recently_created(25)
    return render_template('cruds/index.html',
                           cruds=cruds,
                           table='cruds/_table.html')


@app.route('/cruds/new/', methods=['GET'])
@authenticated_only()
def cruds_new():
    form = CrudForm()
    return render_template('cruds/new.html', form=form)


@app.route('/cruds/create/', methods=['POST'])
@authenticated_only()
@redirect_on_cancel()
def cruds_create():
    form = CrudForm(request.form)
    creator = g.uest

    if form.validate():
        created_crud = Crud.create(creator, form.message.data)
        return redirect(url_for('cruds_show', public_id=created_crud.public_id))
    else:
        return render_template('cruds/new.html', form=form)
