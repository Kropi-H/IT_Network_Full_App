from flask import Flask, render_template, request, g, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to the database
def connect_db():
    sql = sqlite3.connect('/home/honza/Dokumenty/Python_Flask_Udemy/IT_Network_ZP_Plna_verze/pojisteni.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def index():
    return render_template('index.html', page_title = 'Hlavní stránka')

@app.route('/pojistenci', methods=['POST', 'GET'])
def pojistenci():
    db = get_db()
    cur = db.execute('SELECT id, jmeno, prijmeni, mesto, adresa, psc FROM pojistenci')
    results = cur.fetchall()

    return render_template('pojistenci.html', page_title = 'Pojištěnci', pojistenci = results)

@app.route('/pojistenci/<int:id>', methods=['POST'])
def get_member(id):
    db = get_db()
    if request.method == 'POST':
        if request.form['submit'] == 'delete':
            db.execute('DELETE FROM pojistenci WHERE id=?', [id])
            db.commit()
            return redirect('/pojistenci')
        elif request.form['submit'] == 'edit':
            return redirect(url_for("pojistenec_update", id=id))
        elif request.form['submit'] == 'add_pojisteni':
            return redirect(url_for("pojisteni", id=id))

@app.route('/pojistenec_update/<int:id>', methods=['POST', 'GET'])
def pojistenec_update(id):
    db = connect_db()
    cur = db.execute('SELECT * FROM pojistenci WHERE id=?', [id])
    result = cur.fetchone()
    header = 'Úprava dat pojištěnce {}'.format(result['prijmeni'])

    if request.method == 'POST':
        id = id
        jmeno = request.form['first_name']
        prijmeni = request.form['second_name']
        email = request.form['email']
        telefon = request.form['telephone']
        adresa = request.form['street']
        mesto = request.form['town']
        psc = request.form['psc']
        db.execute('UPDATE pojistenci SET jmeno = ?, prijmeni = ?, email = ?, telefon = ?, adresa = ?, mesto = ?, psc = ?  WHERE id = ?',[jmeno, prijmeni, email, telefon, adresa, mesto, psc, id])
        db.commit()
        return redirect('/pojistenci')

    return render_template('novy_pojistenec.html', page_title = 'Pojistenec {} úprava'.format(result['prijmeni']), edit_data = result, header=header)


@app.route('/pojisteni/<int:id>', methods=['POST', 'GET'])
def pojisteni(id):
    db = connect_db()
    cur = db.execute('SELECT pojisteni FROM typ_pojisteni')
    result = cur.fetchall()

    cur_pojistenec = db.execute('SELECT id, jmeno, prijmeni FROM pojistenci WHERE id=?', [id])
    result_pojistenec = cur_pojistenec.fetchone()

    return render_template('pojisteni.html', page_title = 'Pojištění', pojisteni = result, pojistenec=result_pojistenec)

@app.route('/oaplikaci')
def oaplikaci():
    return render_template('oaplikaci.html', page_title = 'O aplikaci')

@app.route('/pojistenci/detail/<int:id>', methods = ['POST', 'GET'])
def pojistenci_detail(id):
    db=get_db()
    cur = db.execute('SELECT * FROM pojistenci WHERE id=?', [id])
    result = cur.fetchone()
    return render_template('pojistenec_detail.html', page_title='Pojištěnec {}'.format(result['prijmeni']), data = result)

@app.route('/pojistenci/novy', methods = ['POST','GET'])
def pojistenci_novy():
    db = get_db()
    if request.method == 'POST':

        jmeno = request.form['first_name']
        prijmeni = request.form['second_name']
        email = request.form['email']
        telefon = request.form['telephone']
        adresa = request.form['street']
        mesto = request.form['town']
        psc = request.form['psc']
        db.execute('INSERT INTO pojistenci (jmeno, prijmeni, email, adresa, mesto, psc, telefon, email) VALUES (?,?,?,?,?,?,?,?)',
                [jmeno, prijmeni, email, adresa, mesto, psc, telefon, email])
        db.commit()

    return render_template('novy_pojistenec.html', page_title = 'Nový pojištěnec', header = 'Nový pojištěnec')


if __name__ == '__main__':
    app.run(debug=True)