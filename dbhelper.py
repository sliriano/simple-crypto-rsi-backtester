import sqlite3

class DBHelper:

    def __init__(self, dbname="Trades.db"):
        # sets database name and establishes a connection to it
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        # creates a table within our databse
        drop_table = "DROP TABLE IF EXISTS trades"
        self.conn.execute(drop_table) 
        create_table = "CREATE TABLE trades (date, ordertype, price, CryptoBalance, USDbalance)"
        self.conn.execute(create_table)
        self.conn.commit()
    
    def add_trade(self, trade_tuple):
        # inserts an item into the table
        insert = "INSERT INTO trades VALUES (?,?,?,?,?)"
        self.conn.execute(insert, trade_tuple)
        self.conn.commit()
    
    def remove_trade(self, date):
        remove = "DELETE FROM trades WHERE date = (?)"
        id_tuple = (date,)
        self.conn.execute(remove,id_tuple)
        self.conn.commit()

    def get_table(self):
        table = []
        for row in self.conn.execute('SELECT * FROM trades'):
            table.append(row)
        return table