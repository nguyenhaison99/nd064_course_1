import sqlite3
import logging
from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO  # Set the logging level to INFO
)

# Function to get a database connection.
# This function connects to a database with the name 'database.db'
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define a logger for the Flask app
app.logger.addHandler(logging.StreamHandler())  # Log to STDOUT
app.logger.setLevel(logging.INFO)  # Set the logger level to INFO

# Define a before_request function to log incoming requests
@app.before_request
def log_request_info():
    app.logger.info(f'Incoming request: {request.method} {request.url}')

# Define an after_request function to log responses
@app.after_request
def log_response_info(response):
    app.logger.info(f'Response: {response.status} - {response.status_code}')
    return response

# Define the main route of the web application
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.info(f'Article with ID {post_id} not found - 404 page displayed')
        return render_template('404.html'), 404
    else:
        app.logger.info(f'Article "{post["title"]}" retrieved')
        return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About Us page accessed')
    return render_template('about.html')

# Define the post creation functionality
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            app.logger.info(f'New article created with title "{title}"')
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
            connection.commit()
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/healthz')
def status():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    return response

@app.route('/metrics')
def metrics():
    connection = get_db_connection()
    post  = connection.execute('SELECT COUNT(*) FROM posts').fetchone()
    count = post[0]
    connection.close()
    response = app.response_class(            
            response=json.dumps({"status":"success","code":200,"data":{"db_connection_count": count, "post_count": count}}),
            status=200,
            mimetype='application/json'
    )
    return response  

# Start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
