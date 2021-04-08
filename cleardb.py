import sqlite3

class DBTruncation:
	# Creating Connection to the sqlite database having products data
	def __init__(self, db):
		try:
			print(f"Creating connection to {db}")
			self.conn = sqlite3.connect(db)
			self.cur = self.conn.cursor()
		except:
			print(f"Cannot create connection")

	# Clearing contents of the database already present
	def truncateTable(self, table):
		try:
			self.cur.execute(f"DELETE FROM {table}")
			print(f"Truncated {table} table")
			self.conn.commit()
		except:
			print(f"Cannot truncate {table} table")

	# Closing connection to the database to avoid anomalies
	def closeConnection(self):
		try:
			print("Closing connection to db")
			self.conn.close()
		except:
			pass
def main():
	obj = DBTruncation('database.db')
	obj.truncateTable('PRODUCTS')
	obj.truncateTable('AAGR_TABLE')
	obj.closeConnection()
if __name__ == '__main__':
	main()