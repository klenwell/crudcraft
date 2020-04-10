"""
# Cruds Controller
"""
from datetime import datetime, timedelta

from controllers import app, render_template, g
from models.crud import Crud


#
# Guests
#
@app.route('/cruds/', methods=['GET'])
def cruds_index():
    cruds = Crud.s_recently_created(25)
    return render_template('cruds/index.html',
                           cruds=cruds,
                           table='cruds/_table.html')
