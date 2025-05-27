from flask import Flask, render_template, request, redirect, url_for, flash, session
from passlib.hash import bcrypt  # Incluído para segurança no hash de senhas

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura'  # Para sessões e mensagens flash

# Simulação de "banco de dados" em memória
usuarios = {}
dispositivos = []

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in usuarios and bcrypt.verify(password, usuarios[username]):
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
    aceita_politica = request.form.get('acceptPrivacy')

    if not aceita_politica:
        flash('Você deve aceitar a Política de Privacidade para se cadastrar.', 'warning')
        return redirect(url_for('cadastro'))
    
    if username in usuarios:
        flash('Usuário já existe.', 'warning')
        return redirect(url_for('cadastro'))
    else:
        usuarios[username] = bcrypt.hash(password)
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

@app.route('/cadastrar_dispositivo', methods=['GET', 'POST'])
def cadastrar_dispositivo():
    if 'username' not in session:
        flash('Faça login para cadastrar dispositivos.', 'warning')
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
        flash('Dispositivo cadastrado com sucesso!', 'success')
        return redirect(url_for('consultar_dispositivos'))
    return render_template('cadastrar_dispositivo.html')

@app.route('/consultar_dispositivos')
def consultar_dispositivos():
    if 'username' not in session:
        flash('Faça login para acessar os dispositivos.', 'warning')
        return redirect(url_for('index'))
    
    return render_template('consultar_dispositivos.html', dispositivos=dispositivos)

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/perfil')
def perfil():
    if 'username' not in session:
        flash('Faça login para acessar seu perfil.', 'warning')
        return redirect(url_for('index'))

    username = session['username']
    return render_template('perfil.html', username=username)

@app.route('/excluir_conta', methods=['POST'])
def excluir_conta():
    if 'username' not in session:
        flash('Faça login para excluir sua conta.', 'warning')
        return redirect(url_for('index'))

    username = session['username']
    usuarios.pop(username, None)
    session.pop('username', None)
    flash('Sua conta foi excluída com sucesso.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
