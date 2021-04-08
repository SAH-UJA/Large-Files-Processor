# Large-Files-Processor
### Problem Statement :
Aim is to build a system which is able to handle long running processes in a distributed fashion. We need to be able to import products from a CSV file and into a database. There are half a million product details to be imported into the database. You can find the CSV file here in a compressed format Large File processing - Assignment.  After the import, we will run an aggregate query to give us no. of products with the same name.

### Introduction :
This repo provides a basic framework for aggregating CSV files with the same schema in a distributed fashion with a partial parallelism using threads and event loop. A data source is defined which hosts its data and staus. If there is a change in data at a given data source, the status changes. The Master Server continuously monitors this status via a HTTP call to the /sense endpoint hosted by each data source. Once, one pass of scanning is complete the fetching of data happens. The data once fetched is stored into a dataframe. Merging of data from all the data sources happens with a separate thread. After merging a groupby operation also takes place to club data on the basis of "name" and then everything is stored in the local sqlite database. User can also use the UI for updating the db.

### Steps to run your code :

Step 1 : Download the repository and cd to the downloaded repo folder. Create a virtualenv and activate it. Install packages using requirements.txt as shown in the figure below.

![1 - Setup](https://user-images.githubusercontent.com/53290539/113976502-dd2d1880-985e-11eb-9e29-0c76c1f06c52.JPG)

Step 2 : Run `python starter.py` to setup the database locally.

![2 - Setup](https://user-images.githubusercontent.com/53290539/113976518-e0c09f80-985e-11eb-9af8-46654a80b806.JPG)

Step 3 : cd to data_source_1 folder and run `python file_server.py` to activate the data source. Use a new terminal.

![3 - Data Source 1](https://user-images.githubusercontent.com/53290539/113976525-e3bb9000-985e-11eb-9406-e8346f41a59b.JPG)

Step 4 : cd to data_source_2 folder and run `python file_server.py` to activate the data source. This server listens to the data/ folder and senses modifications and exposes 2 endpoints `/sense` and `/read`. If there is some change, the /sense api will send status of 1 otherwise 0. If status is 1 the master puts it in queue and reads the data using /read api. Use a new terminal for this as well.

![4 - Data Source 2](https://user-images.githubusercontent.com/53290539/113976539-e74f1700-985e-11eb-968a-9a5c17847e7b.JPG)

Step 5 : Open a new terminal and cd to the repo folder and run `python master.py` as shown in the figure below. What master does is it senses all the data sources using the `/sense` api and aggregates the data after fetching the data using `/read` using a kind-of event loop. Simultaneously it updates the local db which has 2 tables : `PRODUCTS` and `AAGR_TABLE`. Parallely, it serves a form which acts as a UI for updating the local DB.

![5 - Master Listener and Aggregator](https://user-images.githubusercontent.com/53290539/113976549-eae29e00-985e-11eb-8f1b-8b4708e388c7.JPG)

Step 6 : We can read the `database.db` file partially by running `python readdb.py` in a different terminal.

![6 - Reading DB](https://user-images.githubusercontent.com/53290539/113976565-ef0ebb80-985e-11eb-97f3-5e8620806c23.JPG)

Step 7 : Goto the browser after running master.py and type http://localhost:5000/ and this form will appear. Make sure you enter a `sku` value which exists in the db already to see changes in the db. Refer the image given below.

![7 - Updation Form](https://user-images.githubusercontent.com/53290539/113976576-f209ac00-985e-11eb-87ea-a58fa915aa09.JPG)

![8 - Updation Form](https://user-images.githubusercontent.com/53290539/113976579-f5049c80-985e-11eb-9c6d-2bacc1eaab22.JPG)

Step 8 : To see the changes in the DB you can run `python readdb.py`. Here, you can spot changes reflected wrt `sku="lay-raise-best-end"`

![9 - Read DB after updation](https://user-images.githubusercontent.com/53290539/113981559-6e9f8900-9865-11eb-8bac-1062e0c40f23.JPG)


### Details of all the tables and their schema :
DATABASE : database.db

TYPE : `SQLITE`

NO. OF TABLES : `2`

TABLE : `PRODUCTS (name text, sku text primary key, description text)`

TABLE : `AAGR_TABLE (name text, no_of_products text)`

### What is done from “Points to achieve” and number of entries in all your tables :
1) Your code should follow concept of OOPS
2) Support for regular non-blocking parallel ingestion of the given file into a table. Consider thinking about the scale of what should happen if the file is to be processed in 2 mins.
3) Support for updating existing products in the table based on `sku` as the primary key. (Yes, we know about the kind of data in the file. You need to find a workaround for it)
4) All product details are to be ingested into a single table
5) An aggregated table on above rows with `name` and `no. of products` as the columns

### What is not done from “Points to achieve” :
1) Partial Parallel ingestion was achieved.
2) It is assumed that MERGING is required and not CONCAT.

### What would you improve if given more days :
Unfortunately, due to lack of compute resources and time, the following remains in the backlog:
1) Use of Dask Framework for Parallel Processing at every level. We can use dask in place of pandas dataframes to boost up performance as dask loads data partially onto the RAM. Also, it has partitioning features which helps to process large datasets. Dask achieves parallelism through Mutliprocessing by utilizing all the cores of the CPU.
2) Numba is a library which uses jit wrappers to drastically optimize pyhton code performance.
3) Even PySpark would be a great framework for this project. It is used in the industry for Big Data tasks like this and has internal support of its own sql as well.
4) A Design optimization was essential here. There was a need of a data structure to find differences in the incoming data and existing local db to optimize updates by just doing processing on the difference and not on the entire db. Also, Triggers could be handly here to reflect changes in the `AAGR_TABLE` when there is some change in the `PRODUCTS` table.
5) Instead of pandas dataframes, I could have used Vaex which is another awesome framework that can handle a billion records in seconds. Due to lack of compute, I couldn't try it out. 
6) Async calls can be made to the data source end points using `asynio` and `aiohttp` to achieve parallel ingestion in a better way.
7) A better DB like Alteryx could have been used for achieving parallel ingestion.
