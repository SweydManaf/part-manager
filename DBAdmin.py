import os
import sqlite3


class BancoDeDados:
    def __init__(self):
        self.conexao = sqlite3.connect('dataBase.db')
        self.stateDB = os.path.isfile('dataBase.db')

        if not self.stateDB:
            with sqlite3.connect('dataBase.db') as conexao:
                conexao.execute("""
                                    CREATE TABLE pecas(
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        partName text,
                                        customer text,
                                        retailer text,
                                        price integer
                                    )"""
                                )

    def insert_new_part(self, partName, customer, retailer, price):
        with self.conexao as conexao:
            if self.verify_if_part_exists(partName, customer, retailer, price):
                conexao.execute("INSERT INTO pecas(partName, customer, retailer, price) VALUES(?, ?, ?, ?)",
                                (partName, customer, retailer, price))
                return True
            else:
                return False

    def verify_if_part_exists(self, partName, customer, retailer, price):
        repeat = 1
        with self.conexao as conexao:
            for registro in conexao.execute('SELECT * FROM pecas'):
                if partName == registro[1] and customer == registro[2] and retailer == registro[3] and price == str(
                        registro[4]):
                    repeat = 0
                else:
                    pass

        return repeat

    def list_parts(self):
        with self.conexao as conexao:
            for registro in conexao.execute('SELECT * FROM pecas'):
                yield registro

    def delete_part(self, id):
        with self.conexao as conexao:
            conexao.execute('DELETE FROM pecas WHERE id=?', id)

    def update_part(self, id, partname, customer, retailer, price):
        with self.conexao as conexao:
            conexao.execute('UPDATE pecas SET partName=?, customer=?, retailer=?, price=? WHERE id=?',
                            (partname, customer, retailer, price, id))
