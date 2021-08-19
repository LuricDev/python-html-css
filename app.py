import sqlite3 
from flask import Flask, request, session, g, redirect, abort, render_template, flash

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
@app.route('/entradas')
def exibir_entradas():
    return render_template('exibir_entradas.html')

@app.route('/hello') #Rota inicial url
def pagina_inicial():
    return "Hello World"
