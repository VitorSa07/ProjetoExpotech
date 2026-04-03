from flask import Flask, request, render_template, url_for, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = '0'
@app.route('/')
def home():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    try:
        usuario = request.form['usuario']
        email = request.form['cremail']
        senha = request.form['crsenha']
        
        if not usuario or not email or not senha:
            return 'Todos os campos são obrigatórios!'
        
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='guriSQL_',
            database='expotech'
        )
        
        cursor = conexao.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE email_usuario = %s', (email,))
        existe = cursor.fetchone()
        
        if existe:
            cursor.close()
            conexao.close()
            return 'Usuário já cadastrado!'
        
        cursor.execute(
            'INSERT INTO usuarios (nome_usuario, email_usuario, senha_usuario) VALUES (%s, %s, %s)',
            (usuario, email, senha)
        )
        conexao.commit()
        cursor.close()
        conexao.close()
        session['usuario']= usuario
        return redirect(url_for('main'))
    except Exception as e:
        return f'Erro ao cadastrar: {str(e)}'

@app.route('/main')
def main():
    usuario= session.get('usuario')
    return render_template('main.html', usuario=usuario)
      

if __name__ == '__main__':
    app.run(debug=True)