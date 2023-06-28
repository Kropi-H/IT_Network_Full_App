from flask import Flask, render_template, session, request, g, redirect, url_for
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def get_current_user():
    user_result = None
    if 'user' in session:
        user = session['user']
        db = get_db()
        user_cur = db.execute('SELECT jmeno, password FROM uzivatele WHERE jmeno = ?', [user])
        user_result = user_cur.fetchone()
    return user_result

@app.route('/delete_pojisteni/<int:id>', methods=['POST', 'GET'])
def delete_pojisteni(id):
    db = get_db()
    if request.method == 'GET':
        cur = db.execute('SELECT * FROM pojistky WHERE id=?', [id])
        result = cur.fetchone()
        db.execute('DELETE FROM pojistky WHERE id=?', [id])
        db.commit()
        return redirect(url_for('pojistenci_detail', id = result['id_pojistence']))

@app.route('/uprava_pojisteni/<int:id>', methods=['POST', 'GET'])
def uprava_pojisteni(id):
    user = get_current_user()
    if not user:
        return redirect('/login')
    db = get_db()
    if request.method == 'GET':
        cur = db.execute('SELECT * FROM pojistky WHERE id=?', [id])
        result = cur.fetchone() # Vytažení uživatelovi pojistky

        pojistenec_cur = db.execute('SELECT * FROM pojistenci WHERE id=?', [result['id_pojistence']])
        result_pojistenec = pojistenec_cur.fetchone() # Uživatel pro kterého je pojistka sjednaná

        pojisteni_cur = db.execute('SELECT predmet_pojisteni FROM pojisteni')
        result_pojisteni = pojisteni_cur.fetchall() # List všech možných pojištění, které pojistitel nabízí

        return render_template('uprava_pojisteni.html', pojistka = result, pojisteni = result_pojisteni, pojistenec = result_pojistenec, user=user)

    elif request.method == 'POST':
        id_pojistky = id
        typ_pojisteni = request.form.get('pojisteni')
        hodnota_pojisteni = request.form['castka']
        predmet_pojisteni = request.form['predmet_pojisteni']
        platnost_od = request.form['platnost_od']
        platnost_do = request.form['platnost_do']
        """return '<h4>id: {}, typ pojisteni: {}, hodnota: {}, predmet: {}, od: {}, do: {}</h4>'.format(id_pojistky, typ_pojisteni, hodnota_pojisteni, predmet_pojisteni, platnost_od, platnost_do)"""

        db.execute('UPDATE pojistky SET predmet_pojisteni = ?, typ_pojisteni = ?, castka = ?, platnost_od = ?, platnost_do = ?  WHERE id = ?',
                   [predmet_pojisteni, typ_pojisteni, hodnota_pojisteni, platnost_od, platnost_do, id_pojistky])
        db.commit()

        cur = db.execute('SELECT * FROM pojistky WHERE id=?', [id_pojistky])
        result = cur.fetchone()

        return redirect(url_for('pojistenci_detail', id = result['id_pojistence']), user=user)

@app.route('/')
def index():
    user = get_current_user()
    return render_template('index.html', page_title = 'Hlavní stránka', user = user)

@app.route('/pojistenci', methods=['POST', 'GET'])
def pojistenci():
    user = get_current_user()
    if not user:
        return redirect('login')
    db = get_db()
    cur = db.execute('SELECT id, jmeno, prijmeni, mesto, adresa, psc FROM pojistenci')
    results = cur.fetchall()

    return render_template('pojistenci.html', page_title = 'Pojištěnci', pojistenci = results, user = user)

@app.route('/pojistenci/<int:id>', methods=['POST'])
def get_member(id):
    db = get_db()
    if request.method == 'POST':
        if request.form['submit'] == 'delete':
            db.execute('DELETE FROM pojistenci WHERE id=?', [id])
            db.execute('DELETE FROM pojistky WHERE id_pojistence=?', [id])
            db.commit()
            return redirect('/pojistenci')
        elif request.form['submit'] == 'edit':
            return redirect(url_for("pojistenec_update", id=id))
        elif request.form['submit'] == 'add_pojisteni':
            return redirect(url_for("pojisteni", id=id))

@app.route('/pojistenec_update/<int:id>', methods=['POST', 'GET'])
def pojistenec_update(id):
    user = get_current_user()
    if not user:
        return redirect('/login')
    db = get_db()
    cur = db.execute('SELECT * FROM pojistenci WHERE id=?', [id])
    result = cur.fetchone()
    header = 'Úprava dat pojištěnce {}'.format(result['prijmeni'])

    if request.method == 'POST':
        id_user = id
        jmeno = request.form['first_name']
        prijmeni = request.form['second_name']
        email = request.form['email']
        telefon = request.form['telephone']
        adresa = request.form['street']
        mesto = request.form['town']
        psc = request.form['psc']
        db.execute('UPDATE pojistenci SET jmeno = ?, prijmeni = ?, email = ?, telefon = ?, adresa = ?, mesto = ?, psc = ?  WHERE id = ?',[jmeno, prijmeni, email, telefon, adresa, mesto, psc, id_user])
        db.commit()
        return redirect(url_for('pojistenci_detail', id = id_user))

    return render_template('novy_pojistenec.html', page_title = 'Pojistenec {} úprava'.format(result['prijmeni']), edit_data = result, header=header, user=user)


@app.route('/pojisteni/<int:id>', methods=['POST', 'GET'])
def pojisteni(id):
    user = get_current_user()
    if not user:
        return redirect('/login')
    db = get_db()

    cur = db.execute('SELECT predmet_pojisteni FROM pojisteni')
    result = cur.fetchall()

    cur_pojistenec = db.execute('SELECT id, jmeno, prijmeni FROM pojistenci WHERE id=?', [id])
    result_pojistenec = cur_pojistenec.fetchone()

    if request.method == 'POST':
        id_pojistence = id
        typ_pojisteni = request.form.get('pojisteni')
        hodnota_pojisteni = request.form['castka']
        predmet_pojisteni = request.form['predmet_pojisteni']
        platnost_od = request.form['platnost_od']
        platnost_do = request.form['platnost_do']


        db.execute('INSERT INTO pojistky (id_pojistence, predmet_pojisteni, typ_pojisteni, castka, platnost_od, platnost_do ) VALUES (?,?,?,?,?,?)',
                   [id_pojistence, predmet_pojisteni, typ_pojisteni,  hodnota_pojisteni, platnost_od, platnost_do ])
        db.commit()

        return redirect(url_for('pojistenci_detail', id = id_pojistence))

    return render_template('pojisteni.html', page_title = 'Pojištění', pojisteni = result, pojistenec=result_pojistenec, user=user)

@app.route('/oaplikaci')
def oaplikaci():
    return render_template('oaplikaci.html', page_title = 'O aplikaci')

@app.route('/pojistenci/detail/<int:id>', methods = ['POST', 'GET'])
def pojistenci_detail(id):
    user = get_current_user()
    if not user:
        return redirect('/login')
    db=get_db()
    cur = db.execute('SELECT * FROM pojistenci WHERE id=?', [id])
    result = cur.fetchone()
    pojisteni_cur = db.execute('SELECT * FROM pojistky WHERE id_pojistence=?', [id])
    pojisteni_result = pojisteni_cur.fetchall()

    return render_template('pojistenec_detail.html', page_title='Pojištěnec {}'.format(result['prijmeni']), data = result, pojisteni = pojisteni_result, user=user)

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
        return redirect(url_for('pojistenci'))

    return render_template('novy_pojistenec.html', page_title = 'Nový pojištěnec', header = 'Nový pojištěnec')


@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        db = get_db()
        user_cur = db.execute('SELECT id, jmeno, password FROM uzivatele WHERE jmeno=?', [name])
        user_result = user_cur.fetchone()
        if user_result:
            if check_password_hash(user_result['password'], password):
                session['user'] = user_result['jmeno']
                return redirect(url_for('pojistenci'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html', page_title = 'Přihlášení')
@app.route('/register', methods=['POST', 'get'])
def register():
    db = get_db()
    if request.method == 'POST':
        name = request.form['name']
        password = generate_password_hash(request.form['password'],method='sha256')
        db.execute('INSERT INTO uzivatele (jmeno, password, user, admin) VALUES (?,?,?,?)',[name, password, '0', '0'])
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html', page_title = 'Registerace')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)