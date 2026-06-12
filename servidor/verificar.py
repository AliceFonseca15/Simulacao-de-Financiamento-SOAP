import sqlite3
import os

pasta_atual = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(pasta_atual, "concessionaria.db")

print(f"Lendo o banco em: {db_file}")

conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute("SELECT * FROM veiculos")
dados = cursor.fetchall()

print(f"Total de registros encontrados: {len(dados)}")
for linha in dados:
    print(linha)

conn.close()
