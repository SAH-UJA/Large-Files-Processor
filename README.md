# Large-Files-Processor
### Problem Statement :
Aim is to build a system which is able to handle long running processes in a distributed fashion. We need to be able to import products from a CSV file and into a database. There are half a million product details to be imported into the database. You can find the CSV file here in a compressed format Large File processing - Assignment.  After the import, we will run an aggregate query to give us no. of products with the same name.

### Introduction :
This repo provides a basic framework for aggregating CSV files with the same schema in a distributed fashion with a partial parallelism using threads and event loop. A data source is defined which hosts its data and staus. If there is a change in data at a given data source, the status changes. The Master Server continuously monitors this status via a HTTP call to the /sense endpoint hosted by each data source. Once, one pass of scanning is complete the fetching of data happens. The data once fetched is stored into a dataframe. Merging of data from all the data sources happens with a separate thread. After merging a groupby operation also takes place to club data on the basis of "name" and then everything is stored in the local sqlite database. User can also use the UI for updating the db.

### Steps to run your code :

Step 1 : Download the repository and cd to the downloaded repo folder. Create a virtualenv and activate it. Install packages using requirements.txt as shown in the figure below.

![1 - Setup](https://user-images.githubusercontent.com/53290539/113976502-dd2d1880-985e-11eb-9e29-0c76c1f06c52.JPG)

Step 2 : Run "python starter.py" to setup the database locally.

![2 - Setup](https://user-images.githubusercontent.com/53290539/113976518-e0c09f80-985e-11eb-9af8-46654a80b806.JPG)

Step 3 : cd to data_source_1 folder and run "python file_server.py" to activate the data source. Use a new terminal.
![3 - Data Source 1](https://user-images.githubusercontent.com/53290539/113976525-e3bb9000-985e-11eb-9406-e8346f41a59b.JPG)

Step 4 : cd to data_source_2 folder and run "python file_server.py" to activate the data source. This server listens to the data/ folder and senses modifications and exposes 2 endpoints /sense and /read. If there is some change, the /sense api will send status of 1 otherwise 0. If status is 1 the master puts it in queue and reads the data using /read api. Use a new terminal for this as well.

![4 - Data Source 2](https://user-images.githubusercontent.com/53290539/113976539-e74f1700-985e-11eb-968a-9a5c17847e7b.JPG)

Step 5 : Open a new terminal and cd to the repo folder and run "python master.py" as shown in the figure below. What master does is it senses all the data sources using the /sense api and aggregates the data after fetching the data using /read using a kind-of event loop. Simultaneously it updates the local db which has 2 tables : PRODUCTS and AAGR_TABLE. Parallely, it serves a form which acts as a UI for updating the local DB.

![5 - Master Listener and Aggregator](https://user-images.githubusercontent.com/53290539/113976549-eae29e00-985e-11eb-8f1b-8b4708e388c7.JPG)

Step 6 : We can read the database.db partially by running "python readdb.py" in a different terminal.
![6 - Reading DB](https://user-images.githubusercontent.com/53290539/113976565-ef0ebb80-985e-11eb-97f3-5e8620806c23.JPG)

Step 7 : Goto the browser after running master.py and type http://localhost:5000/ and this form will appear. Make sure you enter a "sku" value which exists in the db already to see changes in the db. Refer the image given below.

![7 - Updation Form](https://user-images.githubusercontent.com/53290539/113976576-f209ac00-985e-11eb-87ea-a58fa915aa09.JPG)

![8 - Updation Form](https://user-images.githubusercontent.com/53290539/113976579-f5049c80-985e-11eb-9c6d-2bacc1eaab22.JPG)

Step 8 : To see the changes in the DB you can run "python readdb.py". Here, you can spot changes reflected wrt sku="lay-raise-best-end"

![9 - Read DB after updation](https://user-images.githubusercontent.com/53290539/113981559-6e9f8900-9865-11eb-8bac-1062e0c40f23.JPG)


Details of all the tables and their schema
What is done from “Points to achieve” and number of entries in all your tables
What is not done from “Points to achieve”.
What would you improve if given more days
