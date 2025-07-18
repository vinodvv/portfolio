from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3


app = Flask(__name__)
app.secret_key = "super_secret_key"  # Required for flash messages

DATABASE = 'projects.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Dummy credentials (you can store securely in a real app)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid credentials", "error")
    return render_template('admin_login.html')


@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        repo_link = request.form.get('repo_link')

        if title and description and repo_link:
            conn = get_db_connection()
            conn.execute("INSERT INTO projects (title, description, repo_link) VALUES (?, ?, ?)",
                         (title, description, repo_link))
            conn.commit()
            conn.close()
            flash("Project add successfully!", "success")
        else:
            flash("All fields are required.", "error")

    conn = get_db_connection()
    projects = conn.execute("SELECT * FROM projects").fetchall()
    conn.close()
    return render_template('admin_dashboard.html',  projects=projects)


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash("Logged out successfully", "info")
    return redirect(url_for('home'))


@app.route('/admin/delete/<int:project_id>')
def delete_project(project_id):
    if not session.get('admin'):
        return redirect(url_for('admin', 'login'))

    conn = get_db_connection()
    conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()
    conn.close()
    flash("Project deleted.", "info")
    return redirect(url_for('admin_dashboard'))


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
