'''
nginx + flash 部署
https://www.oschina.net/translate/serving-flask-with-nginx-on-ubuntu
'''
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = TextAreaField('广告内容?', validators=[DataRequired()])
    submit = SubmitField('开始生成')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DsdflIsdf89'

@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')