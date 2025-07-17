from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3


app = Flask(__name__)
app.secret_key = "super_secret_key"  # Required for flash messages

DATABASE = 'projects.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create projects table automatically if needed
def init_db():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            repo_link TEXT NOT NULL
            )
        ''')
        conn.commit()


init_db()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects')
def projects():
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects').fetchall()
    conn.close()
    return render_template('projects.html', projects=projects)


@app.route('/skills')
def skills():
    # Pass your skills list here; in real apps use db or config file
    tech_skills = ['Python', 'Flask', 'HTML', 'CSS', 'JavaScript', 'SQL']
    soft_skills = ['Problem Solving', 'Communication', 'Teamwork']
    return render_template('skills.html', tech_skills=tech_skills, soft_skills=soft_skills)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Real apps should implement email sending or contact logic
        flash('Thank you for reaching out! I will get back to you soon.')
        return redirect(url_for('contact'))
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
