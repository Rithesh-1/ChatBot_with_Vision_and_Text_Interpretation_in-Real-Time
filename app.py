#backed/app.py
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager,create_access_token,jwt_required
from transformers import pipeline
from config import config
from models import db,Query
from extractors import extract_text_from_pdf,extract_text_from_csv,extract_text_from_url
from ocr import extract_text_from_image
import ssl
import re

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
CORS(app)
jwt = JWTManager(app)

qa_pipeline = pipeline('question-answering',model= 'distribution-base-uncased-distilled-squad')

def sanitize_input(input_string):
    return re.sub(r'[^\w\s]','',input_string)

@app.route('/login',methods=['POST'])

def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username == 'test' and password =='test': #implement Your User Verification login
        access_token = create_access_token(identity={'username':username})
        return jsonify(access_token =access_token),200
    else:
        return jsonify({'error':'Invalid credentials'}),401
@app.route('/ask',methods=['POST'])
@jwt_required()

def ask():
    data = request.json
    question = sanitize_input(data['question'])
    context_type = sanitize_input(data['context_type'])
    context_source = sanitize_input(data['context_source'])
    
    if context_type == 'pdf':
        context = extract_text_from_pdf(context_source)
    elif context_type == 'csv':
        context = extract_text_from_csv(context_source)
    elif context_source == 'url':
        context = extract_text_from_url(context_source)
    else:
        return jsonify({'error':'Invalid Context type'}),400
    
    answer = qa_pipeline({'question':question,'context':context})['answer']
    new_query = Query(question=question,context_type=context_type,context_source=context_source,answer=answer)
    db.session.add(new_query)
    db.session.commit()
    return jsonify({'answer':answer})
@app.route('/upload-image',methods=['POST'])
@jwt_required()

def upload_image():
    if 'image' not in request.files:
        return jsonify({'error':'No Image file Provided'}),400
    
    image = request.files['image']
    image_bytes = image.read()
    context = extract_text_from_image(image_bytes)
    return jsonify({'context':context})

if __name__=='__main__':
    context = ('cert.pem','key.pem')
    app.run(ssl_context=context,debug=True)
        