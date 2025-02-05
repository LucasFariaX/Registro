from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Função para criar o banco de dados
def criar_banco():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO registros (nome, data, entrada) VALUES (?, ?, ?)
    ''', (nome, data, entrada))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))

# Rota para registrar saída e comentário
@app.route('/registrar_saida/<int:id>', methods=['POST'])
def registrar_saida(id):
    saida = datetime.now().strftime("%H:%M:%S")
    comentario = request.form['comentario']
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE registros SET saida = ?, comentario = ? WHERE id = ?
    ''', (saida, comentario, id))
    conn.commit()
    conn.close()
    
    return redirect(url_for('registros'))

# Rota para visualizar registros
@app.route('/registros')
def registros():
    conn = sqlite3.connect('database.db')
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
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE registros SET comentario = ? WHERE id = ?
        ''', (comentario, id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('registros'))
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM registros WHERE id = ?', (id,))
    registro = cursor.fetchone()
    conn.close()
    
    return render_template('editar.html', registro=registro)

# Rota para excluir registro
@app.route('/excluir_registro/<int:id>')
def excluir_registro(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM registros WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('registros'))

if __name__ == '__main__':
    criar_banco()
    app.run(debug=True, host='0.0.0.0')  # Rodar em todos os IPs da rede local