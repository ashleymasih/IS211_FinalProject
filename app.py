from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'thekeyforblog'


conn = sqlite3.connect('blogs.db', check_same_thread=False)
c = conn.cursor()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    else:
        error = request.args.get('error')
        return render_template('login.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
      
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        
        if user is None:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
        
      
        if password == user[2]: 
            session['authenticated'] = True
            session['user_id'] = user[0] 
            session['username'] = user[1]
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    c.execute('SELECT * FROM posts WHERE author_id = ?', (session['user_id'],))
    posts = c.fetchall()
    
    return render_template('dashboard.html', posts=posts)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    c.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
    post = c.fetchone()
    
    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        
        c.execute('UPDATE posts SET title = ?, content = ? WHERE id = ?', (new_title, new_content, post_id))
        conn.commit()
        
        return redirect(url_for('dashboard'))
    else:
        return render_template('edit_post.html', post=post)
    
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    c.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()

    return redirect(url_for('dashboard'))

@app.route('/post/<int:post_id>')
def view_post(post_id):
    c.execute('SELECT title, content, published_date, author_id FROM posts WHERE id = ?', (post_id,))
    post = c.fetchone()

    c.execute('SELECT username FROM users WHERE id = ?', (post[3],))
    author = c.fetchone()[0]

    post_dict = {
        'title': post[0],
        'content': post[1],
        'published_date': post[2],
        'author': author
    }

    return render_template('view_post.html', post=post_dict)
    
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author_id = session['user_id']
        
        published_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        c.execute('INSERT INTO posts (title, content, published_date, author_id) VALUES (?, ?, ?, ?)', 
                  (title, content, published_date, author_id))
        conn.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('add_post.html')

if __name__ == '__main__':
    app.run()