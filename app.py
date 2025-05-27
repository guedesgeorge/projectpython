from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura'  # Para sessões e mensagens flash

# Simulação de "banco de dados" em memória
usuarios = {}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in usuarios and usuarios[username] == password:
        session['username'] = username
        flash('Login bem-sucedido!', 'success')
        return redirect(url_for('home'))
    else:
        flash('Usuário ou senha incorretos.', 'danger')
        return redirect(url_for('index'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    username = request.form['username']
    password = request.form['password']
    
    if username in usuarios:
        flash('Usuário já existe.', 'warning')
        return redirect(url_for('cadastro'))
    else:
        usuarios[username] = password
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        flash('Você precisa fazer login primeiro.', 'warning')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Você saiu com sucesso.', 'info')
    return redirect(url_for('index'))

# ...existing code...

dispositivos = []

@app.route('/cadastrar_dispositivo', methods=['GET', 'POST'])
def cadastrar_dispositivo():
    if 'username' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        nome = request.form['nome']
        horas = request.form['horas']
        potencia = request.form['potencia']
        dispositivos.append({
            'nome': nome,
            'horas': horas,
            'potencia': potencia
        })
        flash('Dispositivo cadastrado com sucesso!')
        return redirect(url_for('consultar_dispositivos'))
    return render_template('cadastrar_dispositivo.html')

@app.route('/consultar_dispositivos')
def consultar_dispositivos():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('consultar_dispositivos.html', dispositivos=dispositivos)
# ...existing code...

if __name__ == '__main__':
    app.run(debug=True)
