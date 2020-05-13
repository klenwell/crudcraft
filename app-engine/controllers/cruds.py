"""
# Cruds Controller
"""
from controllers import (app, render_template, g, authenticated_only, admin_only,
                         redirect_on_cancel, request, redirect, url_for)
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
@admin_only()
@redirect_on_cancel()
def cruds_create():
    form = CrudForm(request.form)
    creator = g.uest

    if form.validate():
        created_crud = Crud.create(creator, form.content.data)
        return redirect(url_for('cruds_show', public_id=created_crud.public_id))
    else:
        return render_template('cruds/new.html', form=form)


@app.route('/cruds/<public_id>/', methods=['GET'])
def cruds_show(public_id):
    crud = Crud.read(public_id)

    if not crud:
        return abort(404, 'Crud not found.')

    return render_template('cruds/show.html', crud=crud)
