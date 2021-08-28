import sqlite3 
from flask import Flask, request, url_for, session, g, redirect, abort, render_template, flash

# configuração
DATABASE = "blog.db"
SECRET_KEY = "pudim"

app = Flask(__name__)
app.config.from_object(__name__)

def conectar_bd():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request #Antes da requisição
def antes_requisicao():
    g.bd = conectar_bd() #Deixa o bd globalmente com a variável g do flask

@app.teardown_request #Depois da requisição
def depois_request(exc):
    g.bd.close() #Fecha a conexão

@app.route('/') 
@app.route('/entradas') #Rota que mostra os posts
def exibir_entradas():
    sql = "SELECT titulo, texto FROM entradas ORDER BY id DESC" #Pega o titulo e texto da tabela entradas em ordem decrescente
    cur = g.bd.execute(sql) #executando o sql e armazenando na variável cur
    entradas = [] #Lista que vai armazenar o resultado que retornou da tabela
    for titulo, texto in cur.fetchall(): #fetchall traz todos os resultados com o titulo e texto
        entradas.append({'titulo': titulo, 'texto': texto}) #Dicionario do python com o titulo e texto
    return render_template('exibir_entradas.html', entradas=entradas)

@app.route('/inserir', methods=['POST']) #Rota para inserir posts
def inserir_entrada():
    if not session.get('logado'):
        abort(401)
    sql = "INSERT INTO entradas(titulo, texto) VALUES (?,?)"
    g.bd.execute(sql, request.form['campoTitulo', request.form['campoTexto']]) #Enviando os valores pegando direto do formulário
    g.bd.commit() #Se tiver tudo certo com a inserção, salvar no banco de dados
    return redirect(url_for('exibir_entradas')) #Redirecionando para a página entradas

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('exibir_entradas'))

@app.route('/login', methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        if request.form['campoUsuario'] != 'admin' \
        or request.form['campoSenha'] != 'admin':
            erro = "Senha ou Usuário Inválidos"
        else:
            session['logado'] = True
            return redirect(url_for('exibir_entradas'))

    return render_template('login.html', erro=erro)