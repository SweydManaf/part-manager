import os
import sqlite3


class BancoDeDados:
    def __init__(self):
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

        self.conexao = sqlite3.connect('dataBase.db')

    def insert_new_part(self, partname, customer, retailer, price):
        with self.conexao as conexao:
            if self.verify_if_part_exists(partname, customer, retailer, price):
                conexao.execute("INSERT INTO pecas(partName, customer, retailer, price) VALUES(?, ?, ?, ?)",
                                (partname, customer, retailer, price))
                return True
            else:
                return False

    def verify_if_part_exists(self, partname, customer, retailer, price):
        repeat = 1
        with self.conexao as conexao:
            for registro in conexao.execute('SELECT * FROM pecas'):
                if partname == registro[1] and customer == registro[2] and retailer == registro[3] and price == str(
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


    def list_parts_by_id(self, order):
        with self.conexao:
            if order:
                for registro in self.conexao.execute('SELECT * FROM pecas ORDER BY id'):
                    yield registro
            else:
                for registro in self.conexao.execute('SELECT * FROM pecas ORDER BY id DESC'):
                    yield registro

    def list_parts_by_partname(self, order):
        with self.conexao:
            if order:
                for registro in self.conexao.execute('SELECT * FROM pecas ORDER BY partName'):
                    yield registro
            else:
                for registro in self.conexao.execute('SELECT * FROM pecas ORDER BY partName DESC'):
                    yield registro

    def list_parts_by_customer(self, order):
        with self.conexao:
            if order:
                for registro in self.conexao.execute('SELECT * FROM pecas ORDER BY customer'):
                    yield registro
            else:
                for registro in self.conexao.execute('SELECT * FROM pecas ORDER BY customer DESC'):
                    yield registro

    def list_parts_by_retailer(self, order):
        with self.conexao:
            if order:
                for registro in self.conexao.execute('SELECT * FROM pecas ORDER BY retailer'):
                    yield registro
            else:
                for registro in self.conexao.execute('SELECT * FROM pecas ORDER BY retailer DESC'):
                    yield registro

    def list_parts_by_price(self, order):
        with self.conexao:
            if order:
                for registro in self.conexao.execute('SELECT * FROM pecas ORDER BY price'):
                    yield registro
            else:
                for registro in self.conexao.execute('SELECT * FROM pecas ORDER BY price DESC'):
                    yield registro