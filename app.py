from flask import Flask, render_template, request, redirect, Response
import sqlite3
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table

app = Flask(__name__)

# ---------------- DATABASE SETUP ----------------
def init_db():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rank TEXT NOT NULL,
            email TEXT,
            phone TEXT
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS duty (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_name TEXT,
            rank TEXT,
            shift TEXT,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    duty = conn.execute("SELECT * FROM duty").fetchall()
    conn.close()
    return render_template('index.html', duty=duty)

# ---------------- STAFF ----------------
@app.route('/staff')
def staff():
    conn = sqlite3.connect('database.db')
    data = conn.execute("SELECT * FROM staff").fetchall()
    conn.close()
    return render_template('staff.html', staff=data)

# ADD STAFF
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        rank = request.form['rank']
        email = request.form['email']
        phone = request.form['phone']

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO staff (name, rank, email, phone) VALUES (?, ?, ?, ?)", (name, rank, email, phone))
        conn.commit()
        conn.close()

        return redirect('/staff')

    return render_template('add_staff.html')

# EDIT STAFF
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('database.db')
    if request.method == 'POST':
        name = request.form['name']
        rank = request.form['rank']
        email = request.form['email']
        phone = request.form['phone']

        conn.execute("UPDATE staff SET name=?, rank=?, email=?, phone=? WHERE id=?", (name, rank, email, phone, id))
        conn.commit()
        conn.close()
        return redirect('/staff')

    staff = conn.execute("SELECT * FROM staff WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template('edit_staff.html', staff=staff)

# DELETE STAFF
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    
    # delete staff
    conn.execute("DELETE FROM staff WHERE id=?", (id,))
    
    # ALSO clear duty (important)
    conn.execute("DELETE FROM duty")
    
    conn.commit()
    conn.close()
    
    return redirect('/staff')

# ---------------- DUTY GENERATION ----------------
@app.route('/generate')
def generate():
    conn = sqlite3.connect('database.db')
    staff = conn.execute("SELECT * FROM staff").fetchall()

    shifts = ['Morning', 'Evening', 'Night']

    conn.execute("DELETE FROM duty")

    today = datetime.now().strftime("%Y-%m-%d")

    for i, person in enumerate(staff):
        shift = shifts[i % 3]
        conn.execute(
            "INSERT INTO duty (staff_name, rank, shift, date) VALUES (?, ?, ?, ?)",
            (person[1], person[2], shift, today)
        )

    conn.commit()
    conn.close()

    return redirect('/')

# ---------------- DOWNLOAD PDF ----------------
@app.route('/download_pdf')
def download_pdf():
    conn = sqlite3.connect('database.db')
    duty = conn.execute("SELECT staff_name, rank, shift, date FROM duty").fetchall()
    conn.close()

    file_path = "duty_chart.pdf"
    doc = SimpleDocTemplate(file_path)

    data = [['Name', 'Rank', 'Shift', 'Date']]
    data.extend(duty)

    table = Table(data)
    doc.build([table])

    with open(file_path, "rb") as f:
        pdf = f.read()

    return Response(
        pdf,
        mimetype='application/pdf',
        headers={"Content-Disposition": "attachment;filename=duty_chart.pdf"}
    )
@app.route('/duty')
def duty():
    conn = sqlite3.connect('database.db')
    data = conn.execute("SELECT * FROM duty").fetchall()
    conn.close()
    return render_template('duty.html', duty=data)
# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)