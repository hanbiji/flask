'''
nginx + flash 部署
https://www.oschina.net/translate/serving-flask-with-nginx-on-ubuntu
'''
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class NameForm(FlaskForm):
    name = TextAreaField('广告内容?', validators=[DataRequired()])
    submit = SubmitField('开始生成')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DsdflIsdf89'

@app.route('/', methods=['GET', 'POST'])
def index():
    name = "用英语为以下产品编写创意广告，在 Facebook 上针对滑雪爱好者投放，要求简短：\n\n产品：印花滑雪服套装，适合单双板，雪地摩托"
    form = NameForm()
    form.name.data = name
    if form.validate_on_submit():
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=form.name.data,
            temperature=0.5,
            max_tokens=60,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        name = response
        form.name.data = ''
    return render_template('index.html', form=form, name=name)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')