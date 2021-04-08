import threading
import pandas as pd
import requests
import sqlite3
from flask import *
app = Flask(__name__)

# Fetching existing data from the local db into dataframe
conn = sqlite3.connect('database.db')
SQL_Query = pd.read_sql_query("select * from PRODUCTS", conn)
data = pd.DataFrame(SQL_Query, columns=["name", "sku", "description"])
print("Loaded data from sqlite db")
print(data.head())
print(f"Row Count: {len(data)}")
conn.close()

# Endpoint support to update the database using "sku" as primary_key and new "name" and "description" as API args
@app.route('/update')
def update():
	global data
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	try:
		if request.args.get('name'):
			if request.args.get('description'):

				# Both "name" and "description" is provided for updation
				c.execute(f"UPDATE PRODUCTS SET name='{request.args.get('name')}' , description='{request.args.get('description')}' where sku='{request.args.get('sku')}'")
				data = pd.DataFrame(SQL_Query, columns=["name", "sku", "description"])
				data.groupby(["name"]).count().drop(columns=["description"]).rename(columns={"sku":"no_of_products"}).reset_index().to_sql('AAGR_TABLE', conn, if_exists='replace', index = False)
			else:

				# Only "name" is provided for updation
				c.execute(f"UPDATE PRODUCTS SET name='{request.args.get('name')}' where sku='{request.args.get('sku')}'")
				data = pd.DataFrame(SQL_Query, columns=["name", "sku", "description"])
				data.groupby(["name"]).count().drop(columns=["description"]).rename(columns={"sku":"no_of_products"}).reset_index().to_sql('AAGR_TABLE', conn, if_exists='replace', index = False)
		
		elif request.args.get('description'):

			# Only description is provided for updation
			c.execute(f"UPDATE PRODUCTS SET description='{request.args.get('description')}' where sku='{request.args.get('sku')}'")
			data = pd.DataFrame(SQL_Query, columns=["name", "sku", "description"])
			data.groupby(["name"]).count().drop(columns=["description"]).rename(columns={"sku":"no_of_products"}).reset_index().to_sql('AAGR_TABLE', conn, if_exists='replace', index = False)
		
		else:

			# No new "name" or "description" is provided
			return "Insufficient args in query"
		conn.commit()
		conn.close()

	except:

		# Sku is not provided or some exception occurred
		conn.close()
		return "Some error occurred"

	return "Successfully updated db"

@app.route('/')
def home():
	return render_template('index.html')

# Class to accumulate data from all distributed data_sources/hosts
class DataLoader(threading.Thread):
	def __init__(self, hosts):
		threading.Thread.__init__(self)
		self.name = "DataLoader"
		self.hosts = hosts

	def run(self):
		global data

		# Continuously monitor all the hosts
		while True:
			updates = False
			for url in self.hosts:
				try:
					# Read the sense API if some changes have occurred
					resp = requests.get(url+"/sense")

					# If some change has taken place merge changes to the dataframe
					if resp.json()['status'] == 1:
						print(f"Sensed update on {url}")
						updates = True
						data = pd.concat([data, pd.read_csv(url+"/read")], axis=0).drop_duplicates()
				except:
					continue
			
			# If some modification has been sensed in any host, update the local db with the refined dataframe
			if updates:
				conn = sqlite3.connect('database.db')
				print(f"Dumping updates to db")
				data.to_sql('PRODUCTS', conn, if_exists='replace', index = False)
				data.groupby(["name"]).count().drop(columns=["description"]).rename(columns={"sku":"no_of_products"}).reset_index().to_sql('AAGR_TABLE', conn, if_exists='replace', index = False)
				print(f"Updated row count: {len(data)}")
				conn.commit()
				conn.close()

# Class to handle the update API
class App(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.name = "API"
	def run(self):
		app.run()

if __name__ == '__main__':
	thread1 = DataLoader(['http://localhost:5001', 'http://localhost:5002'])
	thread2 = App()
	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()
	print("Exitting")