import sqlite3

class DBReader:
	# Creating Connection to the sqlite database having products data
	def __init__(self, db):
		try:
			print(f"Creating connection to {db}")
			f = open(db,'w')
			f.close()
			self.conn = sqlite3.connect(db)
			self.cur = self.conn.cursor()
		except:
			print(f"Cannot create database or connection")

	# Reading contents of the tables present in the database 
	def createTable(self, table, schema):
		try:
			self.cur.execute(f"create table {table} ({schema})")
			self.conn.commit()
		except:
			print(f"Cannot create {table} table")

	# Closing connection to the database to avoid anomalies
	def closeConnection(self):
		try:
			print("Closing connection to db")
			self.conn.close()
		except:
			pass
def main():
	obj = DBReader('database.db')
	print("PRODUCTS TABLE CREATION IN PROGRESS")
	obj.createTable(table = 'PRODUCTS', schema="name text, sku text primary key, description text")
	print("AAGR_TABLE CREATION IN PROGRESS")
	obj.createTable(table = 'AAGR_TABLE', schema="name text, no_of_products text")
	obj.closeConnection()

if __name__ == '__main__':
	main()