import cleardb
import readdb
import createdb

if __name__ == '__main__':
	print("Creating new DB")
	createdb.main()
	print("\n\nReading DB")
	readdb.main()