'''
nginx + flash 部署
https://www.oschina.net/translate/serving-flask-with-nginx-on-ubuntu
'''
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

import os
import openai
from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'DsdflIsdf89'

class NameForm(FlaskForm):
    name = TextAreaField('内容?', validators=[DataRequired()])
    submit = SubmitField('开始生成')

class AdsForm(FlaskForm):
    platform = SelectField('广告平台', choices=[('Facebook', 'Facebook'), ('Google', 'Google')])
    age = SelectField('年龄', choices=[('<18', '<18'), ('18-30', '18-30'), ('30-45', '30-45'), ('45-65', '45-65'), ('65+', '65+')])
    gender = SelectField('性别', choices=[('', '不限'), ('women', '女性'), ('men', '男性'), ('young adults', '年轻人'), ('kids', '儿童')])
    body = TextAreaField('内容?', validators=[DataRequired()])
    submit = SubmitField('开始生成')

class AmazonForm(FlaskForm):
    product = StringField('产品?', validators=[DataRequired()])
    body = TextAreaField('关键词?', validators=[DataRequired()])
    submit = SubmitField('开始生成')

class MailForm(FlaskForm):
    body = TextAreaField('邮件内容?', validators=[DataRequired()])
    submit = SubmitField('开始生成')

class TranslateForm(FlaskForm):
    body = TextAreaField('需要翻译的内容?', validators=[DataRequired()])
    language = SelectField('语言', choices=[('English', '英语'), ('Japanese', '日语'), ('French', '法语')])
    submit = SubmitField('开始翻译')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.route('/facebook/ads', methods=['GET', 'POST'])
def facebook_ads():
    form = AdsForm()
    name = None
    ai_data = None
    response = None
    if form.validate_on_submit():
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="I want you to act as an advertiser. Please create a creative advertisement for the following product to be placed on Facebook targeting %s aged %s, adding appropriate emojis, and keeping it brief:\n\n%s" % (form.gender.data, form.age.data, form.body.data),
            temperature=0.5,
            max_tokens=300,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        ai_data = response
        name = ai_data['choices'][0]['text']

    if name is None:
        # name = "用英语为以下产品编写创意广告, 在 Facebook 上投放, 要求简短:\n\nProduct: Ski Jacket Coat Waterproof Windproof Warm Winter Snow Coat Hooded Outdoor Skiing Rain Jacket 20% Off Coupon over $199"
        form.body.data = "Women's Plus Size Tankini Bandeau Swimsuit Two Piece Bathing Suit Tummy Control Swimwear with Shorts 20% OFF Coupon over $99 and Free Shipping over $69"
    return render_template('facebook_ads.html', form=form, name=name, response=response)

@app.route('/correct', methods=['GET', 'POST'])
def correct():
    """
    英语语法修改
    Returns:
        _type_: _description_
    """
    form = NameForm()
    name = None
    ai_data = None
    response = None
    if form.validate_on_submit():
        # response = openai.Edit.create(
        #     model="text-davinci-edit-001",
        #     input=form.name.data,
        #     instruction="Correct this to standard English"
        # )
        
        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt="I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. I want you to replace my simplified A0-level words and sentences with more beautiful and elegant, upper level English words and sentences. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations. My first sentence is:\n\n" + form.name.data,
        #     temperature=0,
        #     max_tokens=2048,
        #     top_p=1.0,
        #     frequency_penalty=0.0,
        #     presence_penalty=0.0
        # )

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="Correct this to standard English:\n\n" + form.name.data,
            temperature=0,
            max_tokens=2048,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        ai_data = response
        name = ai_data['choices'][0]['text']

    return render_template('correct.html', form=form, name=name, response=response)

@app.route('/mail', methods=['GET', 'POST'])
def email():
    """
    邮件回复
    Returns:
        _type_: _description_
    """
    form = MailForm()
    body = None
    ai_data = None
    response = None
    if form.validate_on_submit():
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=form.body.data,
            temperature=0.5,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        ai_data = response
        body = ai_data['choices'][0]['text']
    
    if body is None:
        form.body.data = "回复下面的邮件, 询问客户部分退款能不能接受:\n\nHello.\nI need to return all three items from order GS14573. They are too big.\nPlease find attached the receipt with the items and let me know how to proceed.\nThanks!"

    return render_template('mail.html', form=form, body=body, response=response)

@app.route('/translate', methods=['GET', 'POST'])
def translate():
    """
    翻译
    Returns:
        _type_: _description_
    """
    form = TranslateForm()
    body = None
    ai_data = None
    response = None
    if form.validate_on_submit():
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt='Translate this into %s:\n\n%s' % (form.language.data, form.body.data),
            temperature=0,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        ai_data = response
        body = ai_data['choices'][0]['text']

    return render_template('translate.html', form=form, body=body, response=response)

@app.route('/amazon', methods=['GET', 'POST'])
def amazon():
    """
    亚马逊
    Returns:
        _type_: _description_
    """
    form = AmazonForm()
    body = None
    ai_data = None
    response = None
    if form.validate_on_submit():
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt='I sell %s on Amazon, please help me write a title, 5-point description and related keywords with keywords:\n\n%s' % (form.product.data, form.body.data),
            temperature=0,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        ai_data = response
        body = ai_data['choices'][0]['text']

    return render_template('amazon.html', form=form, body=body, response=response)

@app.route('/image', methods=['GET', 'POST'])
def image():
    """
    图片生成
    """
    return 'Hello world.'
    form = NameForm()
    api_data = None
    image_url = None
    if form.validate_on_submit():
        response = openai.Image.create(
            prompt=form.name.data,
            n=1,
            size="1024x1024"
        )
        api_data = response
        image_url = response['data'][0]['url']

    return render_template('image.html', form=form, api_data=api_data, image_url=image_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')