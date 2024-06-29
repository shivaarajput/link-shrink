from flask import Flask, request, jsonify, redirect, render_template
import random
import string
import os
import redis

app = Flask(__name__)

# Connect to Vercel KV (Redis)
redis_url = os.environ.get('KV_URL')
db = redis.from_url(redis_url)

def generate_short_key(length=6):
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    short_key = generate_short_key()
    db.set(short_key, long_url)
    return jsonify({'short_url': f"{request.host_url}?{short_key}"})

@app.route('/<short_key>')
def redirect_url(short_key):
    long_url = db.get(short_key)
    if long_url:
        return redirect(long_url.decode('utf-8'))
    else:
        return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
