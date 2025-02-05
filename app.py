import os
import psycopg2
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configurações do banco de dados
DATABASE_URL = os.getenv('DATABASE_URL')  # URL do banco de dados no Render

# Função para conectar ao banco de dados
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# Função para criar a tabela de registros
def criar_banco():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            data TEXT NOT NULL,
            entrada TEXT NOT NULL,
            saida TEXT,
            comentario TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para registrar entrada
@app.route('/registrar_entrada', methods=['POST'])
def registrar_entrada():
    nome = request.form['nome']
    data = datetime.now().strftime("%Y-%m-%d")
    entrada = datetime.now().strftime("%H:%M:%S")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO registros (nome, data, entrada) VALUES (%s, %s, %s)
    ''', (nome, data, entrada))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Rota para registrar saída e comentário
@app.route('/registrar_saida/<int:id>', methods=['POST'])
def registrar_saida(id):
    saida = datetime.now().strftime("%H:%M:%S")
    comentario = request.form['comentario']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE registros SET saida = %s, comentario = %s WHERE id = %s
    ''', (saida, comentario, id))
    conn.commit()
    conn.close()
    
    return redirect(url_for('registros'))

# Rota para visualizar registros
@app.route('/registros')
def registros():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registros')
    registros = cursor.fetchall()
    conn.close()
    
    return render_template('registros.html', registros=registros)

# Rota para editar registro
@app.route('/editar_registro/<int:id>', methods=['GET', 'POST'])
def editar_registro(id):
    if request.method == 'POST':
        comentario = request.form['comentario']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE registros SET comentario = %s WHERE id = %s
        ''', (comentario, id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('registros'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registros WHERE id = %s', (id,))
    registro = cursor.fetchone()
    conn.close()
    
    return render_template('editar.html', registro=registro)

# Rota para excluir registro
@app.route('/excluir_registro/<int:id>')
def excluir_registro(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM registros WHERE id = %s', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('registros'))

if __name__ == '__main__':
    criar_banco()
    app.run(host='0.0.0.0', port=10000)  # Use uma porta específica
