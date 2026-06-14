import sqlite3
import os

class ConexaoDB:
    def __init__(self):
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
        self.DB_FILE = os.path.join(pasta_atual, "concessionaria.db")

    def inicializar_banco(self):
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS veiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                ano INTEGER NOT NULL,
                preco REAL NOT NULL
            )
        """)
        
        cursor.execute("SELECT COUNT(*) FROM veiculos")
        resultado = cursor.fetchone()
        
        if resultado and resultado[0] == 0:
            carros_iniciais = [
                ("carro", "Toyota", "Corolla", 2022, 120000.0),
                ("carro", "Chevrolet", "Onix", 2020, 70000.0),
                ("moto", "Honda", "CB 500X", 2023, 45000.0),
                ("moto", "Yamaha", "Fazer 250", 2021, 22000.0)
            ]
            cursor.executemany("INSERT INTO veiculos (tipo, marca, modelo, ano, preco) VALUES (?, ?, ?, ?, ?)", carros_iniciais)
            conn.commit()
            
        conn.close()

    def inserir_veiculo(self,tipo,marca, modelo, ano, preco):
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO veiculos (tipo,marca, modelo, ano, preco) VALUES (?, ?, ?, ?,?)",
            (tipo,marca, modelo, ano, preco)
        )
        conn.commit()
        novo_id = cursor.lastrowid
        conn.close()
        return novo_id
    
    def excluir_veiculo(self, veiculo_id):
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM veiculos WHERE id = ?", (veiculo_id,))
        conn.commit()
        linhas_afetadas = cursor.rowcount
        conn.close()
        return linhas_afetadas > 0

    def listar_veiculos(self):
        conn = sqlite3.connect(self.DB_FILE)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo, marca, modelo, ano, preco FROM veiculos")
        veiculos = cursor.fetchall()
        conn.close()
        return veiculos

    def buscar_veiculo_por_id(self, veiculo_id):
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo, marca, modelo, ano, preco FROM veiculos WHERE id = ?", (veiculo_id,))
        linha = cursor.fetchone()
        conn.close()
        return linha
    

    



