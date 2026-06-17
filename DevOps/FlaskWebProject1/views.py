from datetime import datetime
from flask import render_template, jsonify
from FlaskWebProject1 import app
import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "mysql"),
        port=3306,
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", "root123"),
        database=os.environ.get("MYSQL_DB", "mysql")
    )

@app.route('/')
def root():
    return jsonify({
        "instance": os.environ.get("INSTANCE_NAME", "flask-app"),
        "version": os.environ.get("APP_VERSION", "1.0")
    })

@app.route('/home')
def home():
    return render_template('index.html', title='Home Page', year=datetime.now().year)

@app.route('/about')
def about():
    return render_template('about.html', title='About', year=datetime.now().year, message='About page.')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact', year=datetime.now().year, message='Contact page.')

@app.route('/db-check')
def db_check():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify(status="connected", mysql_version=version, host="mysql")
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500