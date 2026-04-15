import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

DB_URL = os.getenv("DATABASE_URL")

def conectar():
    return psycopg2.connect(DB_URL, sslmode='require')

# Criar tabela ao iniciar
def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            cidade TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY id ASC")
    clientes = cursor.fetchall()
    conn.close()
    return render_template('index.html', clientes=clientes)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form.get('nome')
    email = request.form.get('email')
    tel = request.form.get('telefone')
    cid = request.form.get('cidade')
    
    if nome and email:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nome, email, telefone, cidade) VALUES (%s, %s, %s, %s)", 
                       (nome, email, tel, cid))
        conn.commit()
        conn.close()
    
    return redirect(url_for('index')) # Sempre retorna algo agora!

@app.route('/editar', methods=['POST'])
def editar():
    id_cliente = request.form.get('id')
    nome = request.form.get('nome')
    email = request.form.get('email')
    tel = request.form.get('telefone')
    cid = request.form.get('cidade')
    
    if id_cliente:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clientes 
            SET nome=%s, email=%s, cidade=%s, telefone=%s 
            WHERE id=%s
        """, (nome, email, cid, tel, id_cliente))
        conn.commit()
        conn.close()
        
    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)