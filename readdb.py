import sqlite3
import pandas as pd

class DBReader:
	# Creating Connection to the sqlite database having products data
	def __init__(self, db):
		try:
			print(f"Creating connection to {db}")
			self.conn = sqlite3.connect(db)
		except:
			print(f"Cannot create connection")

	# Reading contents of the tables present in the database 
	def readTable(self, table, cols):
		try:
			SQL_Query = pd.read_sql_query(f"select * from {table}", self.conn)
			data = pd.DataFrame(SQL_Query, columns=cols)
			print(data)
		except:
			print(f"Cannot select from {table} table")

	# Closing connection to the database to avoid anomalies
	def closeConnection(self):
		try:
			print("Closing connection to db")
			self.conn.close()
		except:
			pass

def main():
	obj = DBReader('database.db')
	print("PRODUCTS TABLE CONTENT")
	obj.readTable('PRODUCTS', cols=["name", "sku", "description"])
	print("\n\nAAGR_TABLE TABLE CONTENT")
	obj.readTable('AAGR_TABLE', cols=["name", "no_of_products"])
	obj.closeConnection()

if __name__ == '__main__':
	main()