from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page_title = 'Hlavní stránka')

@app.route('/pojistenci')
def pojistenci():
    return render_template('pojistenci.html', page_title = 'Pojištěnci')

@app.route('/pojisteni')
def pojisteni():
    return render_template('pojisteni.html', page_title = 'Pojištění')

@app.route('/oaplikaci')
def oaplikaci():
    return render_template('oaplikaci.html', page_title = 'O aplikaci')

@app.route('/pojistenci/detail/<id>', methods = ['POST', 'GET'])
def pojistenci_detail(id):
    if request.method == 'POST':
        return '<h1>request methods is working!</h1>'
    return render_template('pojistenec_detail.html', page_title='Pojištěnec {}'.format(id))

@app.route('/pojistenci/novy')
def pojistenci_novy():
    return render_template('novy_pojistenec.html', page_title = 'Nový pojištěnec')


if __name__ == '__main__':
    app.run(debug=True)