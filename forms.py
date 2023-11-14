from flask_wtf import FlaskForm

# Field types to be used
from wtforms import StringField
from wtforms import IntegerField  # (more useful than number fields)

# Validators to be used
from wtforms.validators import DataRequired, NumberRange, Optional

import datetime as dt

class MovieEditForm(FlaskForm):
    title = StringField('Title', 
                        validators=[DataRequired()])
    
    year = IntegerField('Year', 
                        validators=[
                            Optional(),
                            NumberRange(min=1887, max=dt.datetime.now().year)
                        ])